# CAPSTONE ANSWER KEY (Instructor Only)

This file enumerates the known problems planted in the dataset.
Distribute to participants AFTER they complete the capstone, or use to verify solutions.

## Patient Data Quality
- **39** numeric first_names (invalid):
  PID 96: name='12345'
  PID 167: name='12345'
  PID 206: name='12345'
  PID 271: name='12345'
  PID 392: name='12345'
  PID 659: name='12345'
  PID 771: name='12345'
  PID 1032: name='12345'
  PID 1040: name='12345'
  PID 1248: name='12345'
  PID 1409: name='12345'
  PID 1519: name='12345'
  PID 1671: name='12345'
  PID 2010: name='12345'
  PID 2181: name='12345'
  PID 2198: name='12345'
  PID 2264: name='12345'
  PID 2269: name='12345'
  PID 2499: name='12345'
  PID 2741: name='12345'
  PID 2822: name='12345'
  PID 2868: name='12345'
  PID 2993: name='12345'
  PID 3135: name='12345'
  PID 3170: name='12345'
  PID 3394: name='12345'
  PID 3408: name='12345'
  PID 3636: name='12345'
  PID 3662: name='12345'
  PID 3797: name='12345'
  PID 3820: name='12345'
  PID 3995: name='12345'
  PID 4113: name='12345'
  PID 4140: name='12345'
  PID 4390: name='12345'
  PID 4436: name='12345'
  PID 4771: name='12345'
  PID 4852: name='12345'
  PID 4937: name='12345'
- **131** invalid emails:
  PID 7: email='user@.com'
  PID 53: email='not-an-email'
  PID 122: email='not-an-email'
  PID 184: email='not-an-email'
  PID 251: email='not-an-email'
  PID 315: email='user@.com'
  PID 316: email='not-an-email'
  PID 320: email='not-an-email'
  PID 388: email='not-an-email'
  PID 410: email='user@.com'
  PID 435: email='not-an-email'
  PID 454: email='user@.com'
  PID 473: email='not-an-email'
  PID 487: email='user@.com'
  PID 517: email='not-an-email'
  PID 525: email='user@.com'
  PID 559: email='user@.com'
  PID 596: email='user@.com'
  PID 626: email='user@.com'
  PID 642: email='user@.com'
  PID 702: email='not-an-email'
  PID 706: email='not-an-email'
  PID 718: email='user@.com'
  PID 777: email='user@.com'
  PID 913: email='not-an-email'
  PID 929: email='user@.com'
  PID 946: email='not-an-email'
  PID 947: email='user@.com'
  PID 985: email='not-an-email'
  PID 998: email='user@.com'
  PID 1028: email='not-an-email'
  PID 1047: email='user@.com'
  PID 1061: email='not-an-email'
  PID 1096: email='not-an-email'
  PID 1118: email='not-an-email'
  PID 1169: email='user@.com'
  PID 1180: email='user@.com'
  PID 1182: email='user@.com'
  PID 1216: email='not-an-email'
  PID 1232: email='user@.com'
  PID 1245: email='user@.com'
  PID 1295: email='user@.com'
  PID 1426: email='not-an-email'
  PID 1481: email='not-an-email'
  PID 1519: email='user@.com'
  PID 1604: email='user@.com'
  PID 1622: email='not-an-email'
  PID 1696: email='user@.com'
  PID 1700: email='not-an-email'
  PID 1725: email='user@.com'
  PID 1734: email='user@.com'
  PID 1794: email='not-an-email'
  PID 1815: email='not-an-email'
  PID 1832: email='not-an-email'
  PID 1887: email='not-an-email'
  PID 1948: email='not-an-email'
  PID 1989: email='user@.com'
  PID 2005: email='not-an-email'
  PID 2011: email='not-an-email'
  PID 2020: email='user@.com'
  PID 2023: email='not-an-email'
  PID 2042: email='user@.com'
  PID 2106: email='not-an-email'
  PID 2171: email='user@.com'
  PID 2282: email='user@.com'
  PID 2291: email='user@.com'
  PID 2296: email='user@.com'
  PID 2324: email='user@.com'
  PID 2337: email='user@.com'
  PID 2348: email='not-an-email'
  PID 2363: email='user@.com'
  PID 2375: email='not-an-email'
  PID 2396: email='not-an-email'
  PID 2594: email='user@.com'
  PID 2670: email='user@.com'
  PID 2778: email='user@.com'
  PID 2855: email='not-an-email'
  PID 2857: email='not-an-email'
  PID 2872: email='user@.com'
  PID 2877: email='user@.com'
  PID 2902: email='user@.com'
  PID 3033: email='user@.com'
  PID 3046: email='user@.com'
  PID 3083: email='not-an-email'
  PID 3096: email='not-an-email'
  PID 3181: email='user@.com'
  PID 3235: email='user@.com'
  PID 3316: email='not-an-email'
  PID 3355: email='not-an-email'
  PID None: email='not-an-email'
  PID 3400: email='not-an-email'
  PID 3523: email='not-an-email'
  PID 3579: email='not-an-email'
  PID 3614: email='not-an-email'
  PID 3647: email='not-an-email'
  PID 3657: email='not-an-email'
  PID 3751: email='user@.com'
  PID 3798: email='user@.com'
  PID 3864: email='not-an-email'
  PID 3878: email='user@.com'
  PID 3903: email='user@.com'
  PID 3931: email='user@.com'
  PID 3937: email='not-an-email'
  PID 3938: email='not-an-email'
  PID 3945: email='not-an-email'
  PID 3961: email='user@.com'
  PID 3972: email='user@.com'
  PID 4033: email='not-an-email'
  PID 4063: email='not-an-email'
  PID 4065: email='not-an-email'
  PID 4148: email='not-an-email'
  PID 4159: email='user@.com'
  PID 4165: email='not-an-email'
  PID 4285: email='not-an-email'
  PID None: email='user@.com'
  PID 4377: email='not-an-email'
  PID 4420: email='not-an-email'
  PID 4444: email='not-an-email'
  PID 4505: email='user@.com'
  PID 4605: email='user@.com'
  PID 4634: email='not-an-email'
  PID 4698: email='not-an-email'
  PID 4708: email='user@.com'
  PID 4808: email='user@.com'
  PID 4846: email='user@.com'
  PID 4944: email='user@.com'
  PID 4972: email='not-an-email'
  PID 4980: email='user@.com'
  PID SWP-951: email='(555) 123-4567'
  PID SWP-896: email='5551234567'
  PID SWP-175: email='not-an-email'
- **7** SSN/tokenization leaks:
  PII-950: SSN/PII in field (check first_name/occupation/employer/allergy/family_history)
  PII-681: SSN/PII in field (check first_name/occupation/employer/allergy/family_history)
  PII-355: SSN/PII in field (check first_name/occupation/employer/allergy/family_history)
  PII-970: SSN/PII in field (check first_name/occupation/employer/allergy/family_history)
  PII-260: SSN/PII in field (check first_name/occupation/employer/allergy/family_history)
  PII-399: SSN/PII in field (check first_name/occupation/employer/allergy/family_history)
  PII-973: SSN/PII in field (check first_name/occupation/employer/allergy/family_history)

## Hierarchy Problems

| Location | Problem |
|---|---|
| Procedure_Codes 2 | parent=3 (CIRCULAR: 2 <-> 3) |
| Procedure_Codes 44 | parent=999 (broken chain) |
| Procedure_Codes 999 | 'Mystery Procedure' parent=42 |
| Procedure_Codes 50/51/52 | disconnected subtree (root 50 not linked to main tree) |
| Insurance_Provider_Hierarchy 41 | 'Ghost Insurance Co' parent=9999 (non-existent) |
| Insurance_Provider_Hierarchy 42 | 'Fake Regional' tier=1 parent=21 (tier 3) INVERTED |
| Insurance_Provider_Hierarchy 43 | 'SelfRef Insurance' parent=ITSELF |
| Insurance_Provider_Hierarchy 44/45 | inactive parent with active child |
| Hierarchy sheet 642 | hospital 1 -> dept 999 (phantom) |
| Hierarchy sheet 643 | hospital 999 -> dept 1 |
| Hierarchy sheet 644 | hospital 2 -> dept 1 (duplicate assignment) |

## Doctors with invalid data

| doctor_id | Issue |
|---|---|
| 621 (Ghost Doctor) | hospital_id=999, years_exp=0, fee=0, rating=0.0 |
| 622 (Bad Data) | years_exp=-5, fee=-100, rating=6.0, DUPLICATE license MD-904344 |
| 125 existing | invalid hospital_id (128-133) |
| 6 doctors | rating > 5.0 (invalid) |

## Orphan Records (invalid patient IDs in child tables)
- **Appointments**: orphan patient IDs = -1, -2, -5, 0, 88888, 99992, 99993, 99994, 99995, 99996, 99997, 99998
- **Billing**: orphan patient IDs = -1, -2, -3, -4, -5, -6, 0, 99992, 99993, 99994, 99995, 99999
- **Medical_Records**: orphan patient IDs = -1, -10, -2, -3, -7, -8, -9, 0, 88888, 99992, 99993, 99995
- **Visits**: orphan patient IDs = -1, -10, -2, 0, 88888, 99991, 99992, 99993, 99999
- **Prescriptions**: orphan patient IDs = -10, -7, -8, -9
- **Admissions**: orphan patient IDs = -4, -5, -6, -7, -8, 88888
- **Referrals**: orphan patient IDs = -10, 0, 2027-07-30, 2028-07-05, 88888
- **Insurance_Claims**: orphan patient IDs = 88888, 99992, 99993, 99994, 99995, 99996, 99997, 99998
- **Prescription_Administration**: orphan patient IDs = -2, -3, -4, -5, -6, 99990, 99991, 99992, 99993, 99994
- **Patient_Procedures**: orphan patient IDs = -1, -2, -3, -4, -5, 99999

## Match/Merge Candidates

- **250 patients** share phone numbers in exact-duplicate groups
- **22 patients** share email addresses
- **69 name+DOB fuzzy pairs** (names differ slightly, same DOB)
- **PID 100** = John Smith / Jon Smith / John Smyth / J. Smith (4 source systems)
- **PID 200** = Maria Garcia / Marie Garcia / Maria Garzia (4 source systems)
- **5 crosswalk patients** (Cross Walker, Multi Domain, Split Identity, Phantom Patient, Ghost Record)
  each exist under 3 IDs: positive (Epic), negative (Registration), appended (Manual)
