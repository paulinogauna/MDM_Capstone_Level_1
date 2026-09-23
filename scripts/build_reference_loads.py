from __future__ import annotations

from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
REFERENCE_DIR = BASE_DIR / "Data_Source" / "3_Reference"
CURATED_DIR = BASE_DIR / "outputs" / "curated"
REPORTS_DIR = BASE_DIR / "outputs" / "reports"

PLACEHOLDER_VALUES = {"", "N/A", "NA", "NONE", "UNKNOWN", "NULL"}
DEPARTMENT_CANONICAL_MAP = {
    "Internal Med": "Internal Medicine",
    "Family Med": "Family Medicine",
    "Emergency Med": "Emergency Medicine",
    "ENT": "Ear, Nose, and Throat",
    "Gastro": "Gastroenterology",
}


def load_csv(file_name: str) -> pd.DataFrame:
    dataframe = pd.read_csv(REFERENCE_DIR / file_name, dtype=str, keep_default_na=False)
    dataframe.columns = [column.strip() for column in dataframe.columns]
    return dataframe.apply(lambda column: column.map(lambda value: value.strip() if isinstance(value, str) else value))


def normalize_flag(value: str) -> str:
    return "Approved" if str(value).strip().lower() == "true" else "Retired"


def build_hospitals(hospitals_df: pd.DataFrame) -> tuple[pd.DataFrame, list[dict[str, str]]]:
    issues: list[dict[str, str]] = []
    curated = hospitals_df.copy()
    curated["status"] = curated["emergency_avail"].apply(lambda _: "Approved")
    curated["canonical_name"] = curated["hospital_name"]

    for _, row in curated.iterrows():
        if row["accreditation"].strip().upper() in PLACEHOLDER_VALUES:
            issues.append(
                {
                    "domain": "HOSPITAL",
                    "record_id": row["hospital_id"],
                    "issue_type": "placeholder_value",
                    "field_name": "accreditation",
                    "issue_value": row["accreditation"],
                    "recommended_action": "Review accreditation and replace placeholder before governed load",
                }
            )
        try:
            year = int(row["established_year"])
            if year < 1850 or year > 2026:
                issues.append(
                    {
                        "domain": "HOSPITAL",
                        "record_id": row["hospital_id"],
                        "issue_type": "suspicious_year",
                        "field_name": "established_year",
                        "issue_value": row["established_year"],
                        "recommended_action": "Validate hospital established year",
                    }
                )
        except ValueError:
            issues.append(
                {
                    "domain": "HOSPITAL",
                    "record_id": row["hospital_id"],
                    "issue_type": "invalid_numeric",
                    "field_name": "established_year",
                    "issue_value": row["established_year"],
                    "recommended_action": "Provide numeric established year",
                }
            )

    curated = curated[
        [
            "hospital_id",
            "hospital_name",
            "canonical_name",
            "hospital_type",
            "city",
            "state",
            "zip_code",
            "accreditation",
            "established_year",
            "emergency_avail",
            "status",
        ]
    ]
    return curated, issues


def build_departments(departments_df: pd.DataFrame) -> tuple[pd.DataFrame, list[dict[str, str]]]:
    issues: list[dict[str, str]] = []
    curated = departments_df.copy()
    curated["canonical_name"] = curated["department_name"].replace(DEPARTMENT_CANONICAL_MAP)
    curated["status"] = "Approved"

    for _, row in curated.iterrows():
        for field_name in ["head_doctor_id", "subhead_doctor_id"]:
            value = row[field_name]
            if value in {"-1", "999", "888", "9999"}:
                issues.append(
                    {
                        "domain": "DEPARTMENT",
                        "record_id": row["department_id"],
                        "issue_type": "invalid_reference",
                        "field_name": field_name,
                        "issue_value": value,
                        "recommended_action": "Validate doctor reference before production load",
                    }
                )

    curated = curated[
        [
            "department_id",
            "department_name",
            "canonical_name",
            "floor_location",
            "wing",
            "operating_hours",
            "has_icu",
            "status",
        ]
    ]
    return curated, issues


def build_hospital_department_relationships(hierarchy_df: pd.DataFrame, hospitals_df: pd.DataFrame, departments_df: pd.DataFrame) -> tuple[pd.DataFrame, list[dict[str, str]]]:
    issues: list[dict[str, str]] = []
    valid_hospital_ids = set(hospitals_df["hospital_id"])
    valid_department_ids = set(departments_df["department_id"])
    relationship_rows: list[dict[str, str]] = []

    for _, row in hierarchy_df.iterrows():
        hospital_id = row["hospital_id"]
        department_id = row["department_id"]
        if hospital_id not in valid_hospital_ids:
            issues.append(
                {
                    "domain": "HOSPITAL_DEPARTMENT_REL",
                    "record_id": row["entity_id"],
                    "issue_type": "missing_parent",
                    "field_name": "hospital_id",
                    "issue_value": hospital_id,
                    "recommended_action": "Exclude relationship or add missing hospital",
                }
            )
            continue
        if department_id not in valid_department_ids:
            issues.append(
                {
                    "domain": "HOSPITAL_DEPARTMENT_REL",
                    "record_id": row["entity_id"],
                    "issue_type": "missing_child",
                    "field_name": "department_id",
                    "issue_value": department_id,
                    "recommended_action": "Exclude relationship or add missing department",
                }
            )
            continue
        relationship_rows.append(
            {
                "relationship_id": row["entity_id"],
                "hospital_id": hospital_id,
                "department_id": department_id,
                "status": "Approved",
            }
        )

    return pd.DataFrame(relationship_rows), issues


def build_payers(
    payers_df: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, list[dict[str, str]]]:
    issues: list[dict[str, str]] = []
    valid_provider_ids = set(payers_df["provider_id"])
    provider_tier_map = payers_df.set_index("provider_id")["tier"].to_dict()
    payer_group_rows: list[dict[str, str]] = []
    payer_rows: list[dict[str, str]] = []
    payer_plan_rows: list[dict[str, str]] = []
    group_to_payer_rows: list[dict[str, str]] = []
    payer_to_plan_rows: list[dict[str, str]] = []

    for _, row in payers_df.iterrows():
        provider_id = row["provider_id"]
        parent_provider_id = row["parent_provider_id"]
        tier = row["tier"]
        status = normalize_flag(row["is_active"])

        base_row = {
            "provider_id": provider_id,
            "provider_name": row["provider_name"],
            "region": row["region"],
            "headquarters_state": row["headquarters_state"],
            "negotiation_group": row["negotiation_group"],
            "status": status,
        }

        if tier == "1":
            payer_group_rows.append(base_row)
        elif tier == "2":
            payer_rows.append(
                {
                    **base_row,
                    "plan_type": row["plan_type"],
                }
            )
        elif tier == "3":
            payer_plan_rows.append(
                {
                    **base_row,
                    "plan_type": row["plan_type"],
                }
            )
        else:
            issues.append(
                {
                    "domain": "PAYER",
                    "record_id": provider_id,
                    "issue_type": "unexpected_tier",
                    "field_name": "tier",
                    "issue_value": tier,
                    "recommended_action": "Review payer tier and map it to a supported level",
                }
            )

        if parent_provider_id:
            if parent_provider_id == provider_id:
                issues.append(
                    {
                        "domain": "PAYER",
                        "record_id": provider_id,
                        "issue_type": "self_reference",
                        "field_name": "parent_provider_id",
                        "issue_value": parent_provider_id,
                        "recommended_action": "Exclude from hierarchy and review parent assignment",
                    }
                )
            elif parent_provider_id not in valid_provider_ids:
                issues.append(
                    {
                        "domain": "PAYER",
                        "record_id": provider_id,
                        "issue_type": "missing_parent",
                        "field_name": "parent_provider_id",
                        "issue_value": parent_provider_id,
                        "recommended_action": "Exclude from hierarchy or add missing parent provider",
                    }
                )
            else:
                parent_tier = provider_tier_map.get(parent_provider_id)
                if tier == "2" and parent_tier == "1":
                    group_to_payer_rows.append(
                        {
                            "parent_provider_group_id": parent_provider_id,
                            "child_payer_id": provider_id,
                            "status": "Approved",
                        }
                    )
                elif tier == "3" and parent_tier == "2":
                    payer_to_plan_rows.append(
                        {
                            "parent_payer_id": parent_provider_id,
                            "child_payer_plan_id": provider_id,
                            "status": "Approved",
                        }
                    )
                else:
                    issues.append(
                        {
                            "domain": "PAYER",
                            "record_id": provider_id,
                            "issue_type": "invalid_tier_relationship",
                            "field_name": "parent_provider_id",
                            "issue_value": f"parent_tier={parent_tier}; child_tier={tier}",
                            "recommended_action": "Review payer hierarchy because parent-child tiers do not align",
                        }
                    )

    payer_group_df = pd.DataFrame(payer_group_rows)
    payer_df = pd.DataFrame(payer_rows)
    payer_plan_df = pd.DataFrame(payer_plan_rows)
    group_to_payer_df = pd.DataFrame(group_to_payer_rows)
    payer_to_plan_df = pd.DataFrame(payer_to_plan_rows)

    inactive_provider_ids = set()
    for dataframe in [payer_group_df, payer_df, payer_plan_df]:
        if not dataframe.empty:
            inactive_provider_ids.update(dataframe.loc[dataframe["status"] == "Retired", "provider_id"])

    for _, row in group_to_payer_df.iterrows():
        if row["parent_provider_group_id"] in inactive_provider_ids:
            issues.append(
                {
                    "domain": "PAYER",
                    "record_id": row["child_payer_id"],
                    "issue_type": "inactive_parent",
                    "field_name": "parent_provider_id",
                    "issue_value": row["parent_provider_group_id"],
                    "recommended_action": "Review hierarchy because active child points to retired parent",
                }
            )

    for _, row in payer_to_plan_df.iterrows():
        if row["parent_payer_id"] in inactive_provider_ids:
            issues.append(
                {
                    "domain": "PAYER",
                    "record_id": row["child_payer_plan_id"],
                    "issue_type": "inactive_parent",
                    "field_name": "parent_provider_id",
                    "issue_value": row["parent_payer_id"],
                    "recommended_action": "Review hierarchy because active child points to retired parent",
                }
            )

    return payer_group_df, payer_df, payer_plan_df, group_to_payer_df, payer_to_plan_df, issues


def build_procedures(
    procedures_df: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, list[dict[str, str]]]:
    issues: list[dict[str, str]] = []
    valid_code_ids = set(procedures_df["code_id"])

    parent_map = procedures_df.set_index("code_id")["parent_code_id"].to_dict()
    level_map: dict[str, int] = {}

    def resolve_level(code_id: str, visited: set[str] | None = None) -> int | None:
        if code_id in level_map:
            return level_map[code_id]

        if visited is None:
            visited = set()
        if code_id in visited:
            issues.append(
                {
                    "domain": "PROCEDURE",
                    "record_id": code_id,
                    "issue_type": "circular_reference",
                    "field_name": "parent_code_id",
                    "issue_value": code_id,
                    "recommended_action": "Break circular hierarchy before governed load",
                }
            )
            return None

        visited.add(code_id)
        parent_code_id = parent_map.get(code_id, "")
        if not parent_code_id:
            level_map[code_id] = 1
            return 1
        if parent_code_id not in valid_code_ids:
            return None

        parent_level = resolve_level(parent_code_id, visited)
        if parent_level is None:
            return None

        level_map[code_id] = parent_level + 1
        return level_map[code_id]

    procedure_group_rows: list[dict[str, str]] = []
    procedure_family_rows: list[dict[str, str]] = []
    procedure_code_rows: list[dict[str, str]] = []
    group_to_family_rows: list[dict[str, str]] = []
    family_to_code_rows: list[dict[str, str]] = []

    duplicate_names = procedures_df["procedure_name"].duplicated(keep=False)
    for _, row in procedures_df[duplicate_names].iterrows():
        issues.append(
            {
                "domain": "PROCEDURE",
                "record_id": row["code_id"],
                "issue_type": "duplicate_name",
                "field_name": "procedure_name",
                "issue_value": row["procedure_name"],
                "recommended_action": "Review duplicate procedure names and decide canonical representation",
            }
        )

    for _, row in procedures_df.iterrows():
        code_id = row["code_id"]
        parent_code_id = row["parent_code_id"]
        level = resolve_level(code_id)
        base_row = {
            "code_id": code_id,
            "procedure_name": row["procedure_name"],
            "category": row["category"],
            "description": row["description"],
            "status": "Approved",
        }

        if level == 1:
            procedure_group_rows.append(base_row)
        elif level == 2:
            procedure_family_rows.append(base_row)
        elif level == 3:
            procedure_code_rows.append(base_row)
        elif level is None:
            pass
        else:
            issues.append(
                {
                    "domain": "PROCEDURE",
                    "record_id": code_id,
                    "issue_type": "unsupported_depth",
                    "field_name": "parent_code_id",
                    "issue_value": str(level),
                    "recommended_action": "Review procedure hierarchy depth before load",
                }
            )

        if parent_code_id:
            if parent_code_id not in valid_code_ids:
                issues.append(
                    {
                        "domain": "PROCEDURE",
                        "record_id": code_id,
                        "issue_type": "missing_parent",
                        "field_name": "parent_code_id",
                        "issue_value": parent_code_id,
                        "recommended_action": "Exclude from hierarchy or add missing parent code",
                    }
                )
            else:
                parent_level = level_map.get(parent_code_id) or resolve_level(parent_code_id)
                if level == 2 and parent_level == 1:
                    group_to_family_rows.append(
                        {
                            "parent_procedure_group_id": parent_code_id,
                            "child_procedure_family_id": code_id,
                            "status": "Approved",
                        }
                    )
                elif level == 3 and parent_level == 2:
                    family_to_code_rows.append(
                        {
                            "parent_procedure_family_id": parent_code_id,
                            "child_procedure_code_id": code_id,
                            "status": "Approved",
                        }
                    )
                elif level is not None:
                    issues.append(
                        {
                            "domain": "PROCEDURE",
                            "record_id": code_id,
                            "issue_type": "invalid_level_relationship",
                            "field_name": "parent_code_id",
                            "issue_value": f"parent_level={parent_level}; child_level={level}",
                            "recommended_action": "Review procedure hierarchy because parent-child levels do not align",
                        }
                    )
        if row["category"].strip().upper() == "UNKNOWN":
            issues.append(
                {
                    "domain": "PROCEDURE",
                    "record_id": code_id,
                    "issue_type": "unknown_category",
                    "field_name": "category",
                    "issue_value": row["category"],
                    "recommended_action": "Classify procedure before governed load",
                }
            )

    procedure_group_df = pd.DataFrame(procedure_group_rows)
    procedure_family_df = pd.DataFrame(procedure_family_rows)
    procedure_code_df = pd.DataFrame(procedure_code_rows)
    group_to_family_df = pd.DataFrame(group_to_family_rows)
    family_to_code_df = pd.DataFrame(family_to_code_rows)
    return procedure_group_df, procedure_family_df, procedure_code_df, group_to_family_df, family_to_code_df, issues


def write_outputs(dataframes: dict[str, pd.DataFrame], issues: list[dict[str, str]]) -> None:
    CURATED_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    for file_name, dataframe in dataframes.items():
        dataframe.to_csv(CURATED_DIR / file_name, index=False)

    issues_df = pd.DataFrame(issues)
    if issues_df.empty:
        issues_df = pd.DataFrame(
            columns=["domain", "record_id", "issue_type", "field_name", "issue_value", "recommended_action"]
        )
    issues_df.to_csv(REPORTS_DIR / "reference_data_issues.csv", index=False)


def main() -> None:
    hospitals_df = load_csv("Hospitals.csv")
    departments_df = load_csv("Departments.csv")
    hierarchy_df = load_csv("Hierarchy.csv")
    payers_df = load_csv("Insurance_Provider_Hierarchy.csv")
    procedures_df = load_csv("Procedure_Codes.csv")

    hospitals_curated, hospital_issues = build_hospitals(hospitals_df)
    departments_curated, department_issues = build_departments(departments_df)
    hospital_department_rel, hierarchy_issues = build_hospital_department_relationships(
        hierarchy_df, hospitals_df, departments_df
    )
    payer_groups_curated, payers_curated, payer_plans_curated, payer_group_rel, payer_plan_rel, payer_issues = build_payers(payers_df)
    procedure_groups_curated, procedure_families_curated, procedures_curated, procedure_group_rel, procedure_code_rel, procedure_issues = build_procedures(procedures_df)

    write_outputs(
        {
            "reference_hospital.csv": hospitals_curated,
            "reference_department.csv": departments_curated,
            "reference_relationship_hospital_department.csv": hospital_department_rel,
            "reference_payer_group.csv": payer_groups_curated,
            "reference_payer.csv": payers_curated,
            "reference_payer_plan.csv": payer_plans_curated,
            "reference_relationship_payer_group_to_payer.csv": payer_group_rel,
            "reference_relationship_payer_to_plan.csv": payer_plan_rel,
            "reference_procedure_group.csv": procedure_groups_curated,
            "reference_procedure_family.csv": procedure_families_curated,
            "reference_procedure_code.csv": procedures_curated,
            "reference_relationship_procedure_group_to_family.csv": procedure_group_rel,
            "reference_relationship_procedure_family_to_code.csv": procedure_code_rel,
        },
        hospital_issues + department_issues + hierarchy_issues + payer_issues + procedure_issues,
    )


if __name__ == "__main__":
    main()
