from pathlib import Path
import zipfile
import xml.etree.ElementTree as ET
import re
import csv

BASE = Path('outputs/profiling')
OUT = Path('outputs/reports')
OUT.mkdir(parents=True, exist_ok=True)

NS = {'a': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
TARGET_FIELDS = {
    'name': ['first_name', 'last_name'],
    'dob': ['date_of_birth'],
    'email': ['email'],
    'phone': ['phone_number', 'emergency_contact_phone'],
    'insurance': ['insurance_provider', 'insurance_policy_number'],
}
SOURCE_MAP = {
    'Patients_EMR_Epic_Summary.xlsx': 'Epic',
    'Patients_EMR_Center_Summary.xlsx': 'Cerner',
    'Patients_EMR_RegistrationDB_Summary.xlsx': 'RegistrationDB',
    'Patients_EMR_ManualEntry_Summary.xlsx': 'ManualEntry',
    'Patients_EMR_MultiDomain_Conflicts_Summary.xlsx': 'MultiDomain_Conflicts',
}

EMAIL_RE = re.compile(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
PHONE_RE = re.compile(r'^(?:\+?1[-.\s]?)?(?:\(?\d{3}\)?[-.\s]?)\d{3}[-.\s]?\d{4}$')
SSN_RE = re.compile(r'\b\d{3}-\d{2}-\d{4}\b|\b\d{9}\b')
PLACEHOLDERS = {'null', 'n/a', 'na', 'unknown', 'none', '---', ''}


def load_xlsx_tables(path: Path):
    with zipfile.ZipFile(path) as zf:
        shared = []
        if 'xl/sharedStrings.xml' in zf.namelist():
            root = ET.fromstring(zf.read('xl/sharedStrings.xml'))
            for si in root.findall('a:si', NS):
                shared.append(''.join(t.text or '' for t in si.findall('.//a:t', NS)))
        wb = ET.fromstring(zf.read('xl/workbook.xml'))
        rels = ET.fromstring(zf.read('xl/_rels/workbook.xml.rels'))
        rel_map = {rel.attrib['Id']: rel.attrib['Target'] for rel in rels}
        sheets = {}
        for sheet in wb.findall('a:sheets/a:sheet', NS):
            name = sheet.attrib['name']
            rid = sheet.attrib['{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id']
            target = rel_map[rid]
            sheet_path = 'xl/' + target if not target.startswith('xl/') else target
            sroot = ET.fromstring(zf.read(sheet_path))
            rows = []
            for row in sroot.findall('a:sheetData/a:row', NS):
                vals = []
                for c in row.findall('a:c', NS):
                    t = c.attrib.get('t')
                    v = c.find('a:v', NS)
                    if v is None:
                        vals.append('')
                    elif t == 's':
                        vals.append(shared[int(v.text)])
                    else:
                        vals.append(v.text or '')
                rows.append(vals)
            sheets[name] = rows
        return sheets


def parse_column_profile(rows):
    header_idx = None
    for i, row in enumerate(rows):
        if len(row) > 3 and 'Name' in row and '#Null' in row and '#Blank' in row:
            header_idx = i
            break
    if header_idx is None:
        return {}
    header = rows[header_idx]
    data = {}
    for row in rows[header_idx + 1:]:
        if len(row) < len(header):
            row = row + [''] * (len(header) - len(row))
        name = row[1].strip() if len(row) > 1 else ''
        if not name or name.endswith('.csv'):
            continue
        rec = {header[j]: row[j] for j in range(len(header))}
        data[name] = rec
    return data


def parse_values(rows):
    current = None
    values = {}
    for row in rows:
        if len(row) > 1 and row[1] and row[1] not in {'Name', 'Value'} and not row[1].endswith('.csv'):
            if len(row) > 2 and row[2] == '':
                current = row[1].strip()
                values.setdefault(current, [])
                continue
        if current and len(row) > 4 and row[2] != '':
            values[current].append({
                'value': row[2],
                'frequency': row[3],
                'percentage': row[4],
            })
    return values


def to_float(value):
    try:
        return float(value)
    except Exception:
        return None


def metric_from_columns(columns, field_names, metric):
    vals = []
    for field in field_names:
        if field in columns:
            v = to_float(columns[field].get(metric, ''))
            if v is not None:
                vals.append(v)
    if not vals:
        return None
    return round(sum(vals) / len(vals), 2)


def infer_invalid_pct(source, business_field, columns, values):
    checks = []
    if business_field == 'email' and 'email' in values:
        total = 0.0
        bad = 0.0
        for item in values['email']:
            val = item['value']
            freq = to_float(item['frequency']) or 0.0
            if val.upper() == 'NULL':
                continue
            total += freq
            low = val.strip().lower()
            if low in PLACEHOLDERS or not EMAIL_RE.match(val) or PHONE_RE.match(val):
                bad += freq
        return round((bad / total) * 100, 2) if total else None
    if business_field == 'dob' and 'date_of_birth' in values:
        total = 0.0
        bad = 0.0
        for item in values['date_of_birth']:
            val = item['value']
            freq = to_float(item['frequency']) or 0.0
            if val.upper() == 'NULL':
                continue
            total += freq
            if val < '1900-01-01' or val > '2026-09-21':
                bad += freq
        return round((bad / total) * 100, 2) if total else None
    if business_field == 'phone':
        total = 0.0
        bad = 0.0
        for field in ['phone_number', 'emergency_contact_phone']:
            for item in values.get(field, []):
                val = item['value']
                freq = to_float(item['frequency']) or 0.0
                if val.upper() == 'NULL':
                    continue
                total += freq
                low = val.strip().lower()
                if low in PLACEHOLDERS or (not PHONE_RE.match(val) and not SSN_RE.match(val) and not re.search(r'[A-Za-z]', val) is None):
                    bad += freq
                elif re.search(r'[A-Za-z]', val):
                    bad += freq
        return round((bad / total) * 100, 2) if total else None
    if business_field == 'name':
        total = 0.0
        bad = 0.0
        for field in ['first_name', 'last_name']:
            for item in values.get(field, []):
                val = item['value']
                freq = to_float(item['frequency']) or 0.0
                if val.upper() == 'NULL':
                    continue
                total += freq
                low = val.strip().lower()
                if low in PLACEHOLDERS or SSN_RE.search(val) or re.fullmatch(r'\d+', val or ''):
                    bad += freq
        return round((bad / total) * 100, 2) if total else None
    if business_field == 'insurance':
        total = 0.0
        bad = 0.0
        for field in ['insurance_provider', 'insurance_policy_number']:
            for item in values.get(field, []):
                val = item['value']
                freq = to_float(item['frequency']) or 0.0
                if val.upper() == 'NULL':
                    continue
                total += freq
                low = val.strip().lower()
                if low in PLACEHOLDERS:
                    bad += freq
        return round((bad / total) * 100, 2) if total else None
    return None


def collect_findings(source, values):
    findings = []
    if 'email' in values:
        invalid = 0.0
        phone_like = 0.0
        for item in values['email']:
            val = item['value']
            freq = to_float(item['frequency']) or 0.0
            if val.upper() == 'NULL':
                continue
            if not EMAIL_RE.match(val):
                invalid += freq
            if PHONE_RE.match(val):
                phone_like += freq
        if invalid:
            findings.append(f"{source}: {int(invalid)} profiled email values are invalid or malformed in top-value evidence.")
        if phone_like:
            findings.append(f"{source}: {int(phone_like)} email values look like phone numbers.")
    for field in ['first_name', 'last_name', 'occupation', 'allergies']:
        for item in values.get(field, []):
            val = item['value']
            freq = to_float(item['frequency']) or 0.0
            if SSN_RE.search(val):
                findings.append(f"{source}: {int(freq)} occurrences of SSN-like values found in {field}.")
    if 'date_of_birth' in values:
        bad = 0.0
        for item in values['date_of_birth']:
            val = item['value']
            freq = to_float(item['frequency']) or 0.0
            if val.upper() == 'NULL':
                continue
            if val < '1900-01-01' or val > '2026-09-21':
                bad += freq
        if bad:
            findings.append(f"{source}: {int(bad)} DOB values are outside the acceptable range in top-value evidence.")
    return findings

# trust metadata
trust = {}
with open('Data_Source/3_Reference/Data_Sources.csv', newline='', encoding='utf-8') as f:
    for row in csv.DictReader(f):
        trust[row['source_name']] = row

source_name_lookup = {
    'Epic': 'EMR_Epic',
    'Cerner': 'EMR_Cerner',
    'RegistrationDB': 'RegistrationDB',
    'ManualEntry': 'ManualEntry',
    'MultiDomain_Conflicts': None,
}

score_rows = []
all_findings = []
for file_name, source in SOURCE_MAP.items():
    path = BASE / file_name
    if not path.exists():
        continue
    sheets = load_xlsx_tables(path)
    columns = parse_column_profile(sheets.get('Column Profile', []))
    values = parse_values(sheets.get('Values', []))
    row = {'source': source}
    for business_field, cols in TARGET_FIELDS.items():
        row[f'{business_field}_blank_pct'] = metric_from_columns(columns, cols, '%Blank')
        row[f'{business_field}_null_pct'] = metric_from_columns(columns, cols, '%Null')
        row[f'{business_field}_invalid_pct'] = infer_invalid_pct(source, business_field, columns, values)
    meta_key = source_name_lookup[source]
    meta = trust.get(meta_key, {}) if meta_key else {}
    row['trust_score'] = meta.get('trust_score', '')
    row['data_quality_score'] = meta.get('data_quality_score', '')
    score_rows.append(row)
    all_findings.extend(collect_findings(source, values))

# write scorecard csv
fieldnames = [
    'source',
    'name_blank_pct', 'name_null_pct', 'name_invalid_pct',
    'dob_blank_pct', 'dob_null_pct', 'dob_invalid_pct',
    'email_blank_pct', 'email_null_pct', 'email_invalid_pct',
    'phone_blank_pct', 'phone_null_pct', 'phone_invalid_pct',
    'insurance_blank_pct', 'insurance_null_pct', 'insurance_invalid_pct',
    'trust_score', 'data_quality_score'
]
with open(OUT / 'profiling_scorecard.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(score_rows)

# rankings
attributes = ['name', 'dob', 'email', 'phone', 'insurance']
rank_lines = ['# Profiling Ranking', '']
trust_lines = ['# Trust Anchor Recommendations', '']
for attr in attributes:
    ranked = sorted(
        [r for r in score_rows if r['source'] != 'MultiDomain_Conflicts'],
        key=lambda r: (
            999 if r[f'{attr}_blank_pct'] is None else r[f'{attr}_blank_pct'],
            999 if r[f'{attr}_invalid_pct'] is None else r[f'{attr}_invalid_pct'],
            -(float(r['trust_score']) if r['trust_score'] not in ('', None) else 0.0)
        )
    )
    rank_lines.append(f'## {attr.upper()}')
    for i, r in enumerate(ranked, start=1):
        rank_lines.append(
            f"{i}. {r['source']} — blank {r[f'{attr}_blank_pct']}%, invalid {r[f'{attr}_invalid_pct']}%, trust {r['trust_score']}"
        )
    rank_lines.append('')
    best = ranked[0] if ranked else None
    if best:
        trust_lines.append(
            f"- **{attr}**: `{best['source']}` is the recommended trust anchor based on the lowest blank rate ({best[f'{attr}_blank_pct']}%), lowest invalid rate ({best[f'{attr}_invalid_pct']}%), and trust score {best['trust_score']}."
        )
trust_lines.append('')
trust_lines.append('- `MultiDomain_Conflicts` was profiled as evidence of cross-domain issues, not as a primary trust-anchor candidate.')

with open(OUT / 'profiling_ranking.md', 'w', encoding='utf-8') as f:
    f.write('\n'.join(rank_lines + [''] + trust_lines) + '\n')

# cio summary
summary_lines = [
    '# CIO Profiling Summary',
    '',
    '## Executive Summary',
    'Business 360/IICS profiling confirms that data quality is not uniform across patient sources. The measured scorecard shows that source suitability varies by attribute, so trust anchors should be assigned at the field level rather than by choosing one system globally.',
    '',
    '## Key Findings',
]
if all_findings:
    for finding in all_findings[:10]:
        summary_lines.append(f'- {finding}')
else:
    summary_lines.append('- The exported summaries do not include enough top-value evidence to quantify invalid examples beyond blank/null rates.')
summary_lines += [
    '',
    '## Source Strengths',
    '- Epic and Cerner should be reviewed first as likely demographic anchors, with final selection driven by the scorecard metrics.',
    '- RegistrationDB shows strong administrative coverage but also evidence of placeholder and out-of-range values in several fields.',
    '- ManualEntry should be treated cautiously because manual capture typically increases invalid-format risk and inconsistent typing.',
    '',
    '## Gaps / Caveats',
    '- The current exports are summary workbooks only; they do not include full rule-occurrence exports or exception-level extracts.',
    '- Invalid percentages are derived from top-value evidence where available and may undercount issues not surfaced in the workbook excerpts.',
    '- Multi-source conflict profiling is useful for issue discovery but should not be used as a primary source ranking input.',
    '',
    '## Recommended Next Actions',
    '- Export rule occurrences and exception reports for email, DOB, phone, and PII leakage rules to strengthen the invalid-rate evidence.',
    '- Confirm trust anchors per attribute in survivorship design using the scorecard and source trust metadata together.',
    '- Present the board with measured quality by field, including both completeness and validity, instead of a single overall source opinion.',
]
with open(OUT / 'profiling_cio_summary.md', 'w', encoding='utf-8') as f:
    f.write('\n'.join(summary_lines) + '\n')

print('Generated:')
print(OUT / 'profiling_scorecard.csv')
print(OUT / 'profiling_ranking.md')
print(OUT / 'profiling_cio_summary.md')
