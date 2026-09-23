from pathlib import Path
import zipfile
import xml.etree.ElementTree as ET

base = Path('outputs/profiling')
ns = {'a': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
for path in sorted(base.glob('*.xlsx')):
    print(f'FILE: {path.name}')
    with zipfile.ZipFile(path) as zf:
        shared = []
        if 'xl/sharedStrings.xml' in zf.namelist():
            root = ET.fromstring(zf.read('xl/sharedStrings.xml'))
            for si in root.findall('a:si', ns):
                text = ''.join(t.text or '' for t in si.findall('.//a:t', ns))
                shared.append(text)
        wb = ET.fromstring(zf.read('xl/workbook.xml'))
        rels = ET.fromstring(zf.read('xl/_rels/workbook.xml.rels'))
        rel_map = {rel.attrib['Id']: rel.attrib['Target'] for rel in rels}
        for sheet in wb.findall('a:sheets/a:sheet', ns):
            name = sheet.attrib['name']
            rid = sheet.attrib['{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id']
            target = rel_map[rid]
            sheet_path = 'xl/' + target if not target.startswith('xl/') else target
            sroot = ET.fromstring(zf.read(sheet_path))
            rows = []
            for row in sroot.findall('a:sheetData/a:row', ns):
                vals = []
                for c in row.findall('a:c', ns):
                    t = c.attrib.get('t')
                    v = c.find('a:v', ns)
                    if v is None:
                        vals.append('')
                    elif t == 's':
                        vals.append(shared[int(v.text)])
                    else:
                        vals.append(v.text or '')
                if any(val != '' for val in vals):
                    rows.append(vals)
                if len(rows) >= 15:
                    break
            print(f'  SHEET: {name}')
            for r in rows:
                print('   ', r)
    print()
