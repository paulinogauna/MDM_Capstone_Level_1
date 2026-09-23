from __future__ import annotations

import json
import re
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_SOURCE_DIR = BASE_DIR / "Data_Source"
SOURCE_DIR = DATA_SOURCE_DIR / "1_Sources"
OUTPUT_DIR = BASE_DIR / "outputs" / "reports"

EMAIL_REGEX = re.compile(r"^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$", re.IGNORECASE)
PHONE_PLACEHOLDER_VALUES = {"000-000-0000", "(000) 000-0000", "", "N/A", "NA", "NONE"}
NAME_INVALID_REGEX = re.compile(r"[^A-Za-z\-\s']")


def load_sources() -> list[tuple[str, pd.DataFrame]]:
    sources: list[tuple[str, pd.DataFrame]] = []
    for csv_path in sorted(SOURCE_DIR.glob("*.csv")):
        dataframe = pd.read_csv(csv_path, dtype=str, keep_default_na=False)
        dataframe.columns = [column.strip() for column in dataframe.columns]
        sources.append((csv_path.name, dataframe))
    return sources


def load_all_catalog_files() -> list[tuple[str, str, Path, pd.DataFrame]]:
    catalog_files: list[tuple[str, str, Path, pd.DataFrame]] = []
    for folder_path in sorted(DATA_SOURCE_DIR.iterdir()):
        if not folder_path.is_dir():
            continue

        for file_path in sorted(folder_path.iterdir()):
            if file_path.suffix.lower() == ".csv":
                dataframe = pd.read_csv(file_path, dtype=str, keep_default_na=False)
                dataframe.columns = [column.strip() for column in dataframe.columns]
                catalog_files.append((folder_path.name, file_path.name, file_path, dataframe))
            elif file_path.suffix.lower() in {".xlsx", ".xls"}:
                try:
                    excel_file = pd.ExcelFile(file_path)
                    for sheet_name in excel_file.sheet_names:
                        dataframe = pd.read_excel(excel_file, sheet_name=sheet_name, dtype=str, keep_default_na=False)
                        dataframe.columns = [str(column).strip() for column in dataframe.columns]
                        catalog_files.append((folder_path.name, f"{file_path.name}::{sheet_name}", file_path, dataframe))
                except ImportError:
                    dataframe = pd.DataFrame(
                        {
                            "catalog_warning": ["Excel support unavailable: install openpyxl to inspect this workbook"]
                        }
                    )
                    catalog_files.append((folder_path.name, f"{file_path.name}::unreadable", file_path, dataframe))

    return catalog_files


def normalize_text(value: str) -> str:
    return value.strip()


def is_invalid_email(value: str) -> bool:
    value = normalize_text(value)
    if not value:
        return True
    return EMAIL_REGEX.fullmatch(value) is None


def is_invalid_name(value: str) -> bool:
    value = normalize_text(value)
    if not value:
        return True
    if value.upper() in {"N/A", "NA", "UNKNOWN", "###"}:
        return True
    return NAME_INVALID_REGEX.search(value) is not None


def is_placeholder_phone(value: str) -> bool:
    value = normalize_text(value).upper()
    return value in PHONE_PLACEHOLDER_VALUES


def parse_date(series: pd.Series) -> pd.Series:
    return pd.to_datetime(series, errors="coerce")


def build_summary_rows(file_name: str, dataframe: pd.DataFrame) -> list[dict[str, object]]:
    row_count = len(dataframe)
    duplicate_patient_ids = dataframe["patient_id"].astype(str).str.strip().duplicated(keep=False).sum() if "patient_id" in dataframe.columns else 0
    summary_rows: list[dict[str, object]] = []

    for column in dataframe.columns:
        series = dataframe[column].astype(str)
        null_mask = series.str.strip().eq("")
        summary_rows.append(
            {
                "file_name": file_name,
                "column_name": column,
                "row_count": row_count,
                "null_count": int(null_mask.sum()),
                "null_pct": round(float(null_mask.mean() * 100), 2),
                "distinct_count": int(series[~null_mask].nunique(dropna=True)),
                "sample_values": " | ".join(series[~null_mask].head(3).tolist()),
                "duplicate_patient_id_rows": int(duplicate_patient_ids),
            }
        )

    return summary_rows


def build_issue_rows(file_name: str, dataframe: pd.DataFrame) -> list[dict[str, object]]:
    issues: list[dict[str, object]] = []
    working_df = dataframe.copy()

    for column in ["patient_id", "first_name", "last_name", "email", "phone_number", "emergency_contact_phone", "date_of_birth", "registration_date", "last_visit_date", "height_cm", "weight_kg", "bmi", "patient_status", "blood_type"]:
        if column not in working_df.columns:
            working_df[column] = ""

    dob = parse_date(working_df["date_of_birth"])
    registration_date = parse_date(working_df["registration_date"])
    last_visit_date = parse_date(working_df["last_visit_date"])
    height = pd.to_numeric(working_df["height_cm"], errors="coerce")
    weight = pd.to_numeric(working_df["weight_kg"], errors="coerce")
    bmi = pd.to_numeric(working_df["bmi"], errors="coerce")

    duplicate_patient_ids = working_df["patient_id"].astype(str).str.strip().duplicated(keep=False)

    for index, row in working_df.iterrows():
        patient_id = normalize_text(str(row.get("patient_id", "")))
        full_name = f"{normalize_text(str(row.get('first_name', '')))} {normalize_text(str(row.get('last_name', '')))}".strip()

        def add_issue(issue_type: str, column_name: str, issue_value: object, rule_name: str) -> None:
            issues.append(
                {
                    "file_name": file_name,
                    "row_number": index + 2,
                    "patient_id": patient_id,
                    "full_name": full_name,
                    "issue_type": issue_type,
                    "column_name": column_name,
                    "issue_value": "" if pd.isna(issue_value) else str(issue_value),
                    "rule_name": rule_name,
                }
            )

        if not patient_id:
            add_issue("missing_identifier", "patient_id", row["patient_id"], "patient_id_required")
        else:
            patient_id_numeric = pd.to_numeric(pd.Series([patient_id]), errors="coerce").iloc[0]
            if pd.isna(patient_id_numeric):
                add_issue("invalid_identifier", "patient_id", row["patient_id"], "patient_id_must_be_numeric")
            elif patient_id_numeric <= 0:
                add_issue("invalid_identifier", "patient_id", row["patient_id"], "patient_id_must_be_positive")

        if duplicate_patient_ids.iloc[index]:
            add_issue("duplicate_identifier", "patient_id", row["patient_id"], "patient_id_should_be_unique_within_source")

        if is_invalid_name(str(row["first_name"])):
            add_issue("invalid_name", "first_name", row["first_name"], "first_name_must_be_present_and_alphabetic")

        if is_invalid_name(str(row["last_name"])):
            add_issue("invalid_name", "last_name", row["last_name"], "last_name_must_be_present_and_alphabetic")

        if is_invalid_email(str(row["email"])):
            add_issue("invalid_email", "email", row["email"], "email_must_match_standard_pattern")

        if is_placeholder_phone(str(row["phone_number"])):
            add_issue("placeholder_phone", "phone_number", row["phone_number"], "phone_number_should_not_be_placeholder")

        if is_placeholder_phone(str(row["emergency_contact_phone"])):
            add_issue("placeholder_phone", "emergency_contact_phone", row["emergency_contact_phone"], "emergency_contact_phone_should_not_be_placeholder")

        if pd.isna(dob.iloc[index]):
            add_issue("invalid_date", "date_of_birth", row["date_of_birth"], "date_of_birth_must_be_parseable")
        else:
            if dob.iloc[index] > pd.Timestamp.today().normalize():
                add_issue("future_date", "date_of_birth", row["date_of_birth"], "date_of_birth_cannot_be_in_future")
            if dob.iloc[index] < pd.Timestamp("1900-01-01"):
                add_issue("suspicious_date", "date_of_birth", row["date_of_birth"], "date_of_birth_should_be_after_1900")

        if normalize_text(str(row["registration_date"])) and pd.isna(registration_date.iloc[index]):
            add_issue("invalid_date", "registration_date", row["registration_date"], "registration_date_must_be_parseable")

        if normalize_text(str(row["last_visit_date"])) and pd.isna(last_visit_date.iloc[index]):
            add_issue("invalid_date", "last_visit_date", row["last_visit_date"], "last_visit_date_must_be_parseable")

        if not pd.isna(registration_date.iloc[index]) and not pd.isna(last_visit_date.iloc[index]) and last_visit_date.iloc[index] < registration_date.iloc[index]:
            add_issue("date_sequence_issue", "last_visit_date", row["last_visit_date"], "last_visit_date_should_be_on_or_after_registration_date")

        if not pd.isna(height.iloc[index]) and (height.iloc[index] < 45 or height.iloc[index] > 250):
            add_issue("out_of_range_measure", "height_cm", row["height_cm"], "height_cm_should_be_between_45_and_250")

        if not pd.isna(weight.iloc[index]) and (weight.iloc[index] < 2 or weight.iloc[index] > 400):
            add_issue("out_of_range_measure", "weight_kg", row["weight_kg"], "weight_kg_should_be_between_2_and_400")

        if normalize_text(str(row["bmi"])) and pd.isna(bmi.iloc[index]):
            add_issue("invalid_numeric", "bmi", row["bmi"], "bmi_should_be_numeric_when_present")
        elif not pd.isna(bmi.iloc[index]) and (bmi.iloc[index] <= 0 or bmi.iloc[index] > 100):
            add_issue("out_of_range_measure", "bmi", row["bmi"], "bmi_should_be_between_0_and_100")

        patient_status = normalize_text(str(row["patient_status"]))
        if patient_status and patient_status != patient_status.title():
            add_issue("standardization_needed", "patient_status", row["patient_status"], "patient_status_should_use_standard_casing")

        blood_type = normalize_text(str(row["blood_type"]))
        if blood_type and blood_type.upper() not in {"A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"}:
            add_issue("invalid_domain_value", "blood_type", row["blood_type"], "blood_type_should_match_known_domain")

        address_value = normalize_text(str(row.get("address", "")))
        if address_value:
            try:
                json.loads(address_value)
            except json.JSONDecodeError:
                add_issue("invalid_json", "address", row.get("address", ""), "address_should_be_valid_json")

    return issues


def build_file_level_summary(summary_df: pd.DataFrame, issues_df: pd.DataFrame) -> pd.DataFrame:
    file_summary = (
        summary_df.groupby("file_name", as_index=False)
        .agg(
            row_count=("row_count", "max"),
            column_count=("column_name", "count"),
            duplicate_patient_id_rows=("duplicate_patient_id_rows", "max"),
        )
    )

    issue_counts = issues_df.groupby("file_name", as_index=False).size().rename(columns={"size": "issue_count"}) if not issues_df.empty else pd.DataFrame(columns=["file_name", "issue_count"])
    return file_summary.merge(issue_counts, on="file_name", how="left").fillna({"issue_count": 0})


def build_catalog_rows() -> list[dict[str, object]]:
    catalog_rows: list[dict[str, object]] = []
    for folder_name, file_name, file_path, dataframe in load_all_catalog_files():
        workbook_name = file_path.name if file_path.suffix.lower() in {".xlsx", ".xls"} else ""
        sheet_name = file_name.split("::", 1)[1] if "::" in file_name else ""
        catalog_rows.append(
            {
                "folder_name": folder_name,
                "file_name": file_name,
                "workbook_name": workbook_name,
                "sheet_name": sheet_name,
                "file_path": str(file_path.relative_to(BASE_DIR)),
                "row_count": len(dataframe),
                "column_count": len(dataframe.columns),
                "columns": " | ".join(dataframe.columns.tolist()),
                "sample_columns": " | ".join(dataframe.columns[:8].tolist()),
                "is_patient_source": folder_name == "1_Sources",
                "is_transactional": folder_name == "2_Transactional",
                "is_reference": folder_name == "3_Reference",
                "is_golden_draft": folder_name == "4_Master_Golden_Draft",
            }
        )
    return catalog_rows


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    sources = load_sources()
    catalog_rows = build_catalog_rows()

    summary_rows: list[dict[str, object]] = []
    issue_rows: list[dict[str, object]] = []

    for file_name, dataframe in sources:
        summary_rows.extend(build_summary_rows(file_name, dataframe))
        issue_rows.extend(build_issue_rows(file_name, dataframe))

    summary_df = pd.DataFrame(summary_rows)
    issues_df = pd.DataFrame(issue_rows)
    file_summary_df = build_file_level_summary(summary_df, issues_df)
    catalog_df = pd.DataFrame(catalog_rows)

    summary_df.to_csv(OUTPUT_DIR / "source_profile_details.csv", index=False)
    file_summary_df.to_csv(OUTPUT_DIR / "source_profile_summary.csv", index=False)
    issues_df.to_csv(OUTPUT_DIR / "patient_quality_issues.csv", index=False)
    catalog_df.to_csv(OUTPUT_DIR / "full_data_catalog.csv", index=False)

    print("Generated:")
    print(f"- {OUTPUT_DIR / 'source_profile_details.csv'}")
    print(f"- {OUTPUT_DIR / 'source_profile_summary.csv'}")
    print(f"- {OUTPUT_DIR / 'patient_quality_issues.csv'}")
    print(f"- {OUTPUT_DIR / 'full_data_catalog.csv'}")


if __name__ == "__main__":
    main()