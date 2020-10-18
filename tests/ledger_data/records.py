from models.project import Project
from models.assignment import Assignment
from models.employee import Employee
from models.department import Department


projects = [
    Project({
        'id': 297,
        'name': 'Name 297',
        'full_name': 'Full Name 297',
        'frum': '1901',
        'thru': '1912',
        'active': 1,
        'non_va': 1
    }),
    Project({
        'id': 298,
        'name': 'Name 298',
        'full_name': 'Full Name 298',
        'frum': '1907',
        'thru': '2406',
        'active': 1,
        'non_va': 0
    }),
    Project({
        'id': 299,
        'name': 'Name 299',
        'full_name': 'Full Name 299',
        'frum': '1907',
        'thru': '2106',
        'active': 1,
        'non_va': 1
    }),
    Project({
        'id': 301,
        'name': 'Name 301',
        'full_name': 'Full Name 301',
        'frum': '1904',
        'thru': '1909',
        'active': 1,
        'non_va': 0
    }),
    Project({
        'id': 309,
        'name': 'Name 309',
        'full_name': 'Full Name 309',
        'frum': '1908',
        'thru': '2009',
        'active': 1,
        'non_va': 1
    }),
    Project({
        'id': 311,
        'name': 'Name 311',
        'full_name': 'Full Name 311',
        'frum': '1910',
        'thru': '2009',
        'active': 1,
        'non_va': 0
    }),
    Project({
        'id': 312,
        'name': 'Name 312',
        'full_name': 'Full Name 312',
        'frum': '1909',
        'thru': '2109',
        'active': 1,
        'non_va': 0
    }),
    Project({
        'id': 315,
        'name': 'Name 315',
        'full_name': 'Full Name 315',
        'frum': '1807',
        'thru': '2106',
        'active': 1,
        'non_va': 1
    })
]

assignments = [
    Assignment({
        'id': 2271,
        'employee_id': 282,
        'project_id': 297,
        'frum': '1910',
        'thru': '1912',
        'effort': 45,
        'active': 1
    }),
    Assignment({
        'id': 2272,
        'employee_id': 52,
        'project_id': 297,
        'frum': '1910',
        'thru': '1912',
        'effort': 10,
        'active': 1
    }),
    Assignment({
        'id': 2280,
        'employee_id': 107,
        'project_id': 298,
        'frum': '1907',
        'thru': '2009',
        'effort': 50,
        'active': 1
    }),
    Assignment({
        'id': 2281,
        'employee_id': 264,
        'project_id': 298,
        'frum': '1907',
        'thru': '2009',
        'effort': 10,
        'active': 1
    }),
    Assignment({
        'id': 2282,
        'employee_id': 61,
        'project_id': 299,
        'frum': '1907',
        'thru': '2106',
        'effort': 10,
        'active': 1
    }),
    Assignment({
        'id': 2310,
        'employee_id': 76,
        'project_id': 301,
        'frum': '1907',
        'thru': '2009',
        'effort': 25,
        'active': 1
    }),
    Assignment({
        'id': 2366,
        'employee_id': 73,
        'project_id': 301,
        'frum': '1910',
        'thru': '2009',
        'effort': 5,
        'active': 1
    }),
    Assignment({
        'id': 2367,
        'employee_id': 211,
        'project_id': 301,
        'frum': '1910',
        'thru': '2009',
        'effort': 40,
        'active': 1
    }),
    Assignment({
        'id': 2368,
        'employee_id': 62,
        'project_id': 301,
        'frum': '1910',
        'thru': '2009',
        'effort': 40,
        'active': 1
    }),
    Assignment({
        'id': 2365,
        'employee_id': 106,
        'project_id': 309,
        'frum': '1910',
        'thru': '2009',
        'effort': 5,
        'active': 1
    }),
    Assignment({
        'id': 2378,
        'employee_id': 20,
        'project_id': 311,
        'frum': '1910',
        'thru': '2009',
        'effort': 2,
        'active': 1
    }),
    Assignment({
        'id': 2379,
        'employee_id': 56,
        'project_id': 311,
        'frum': '1910',
        'thru': '2009',
        'effort': 3,
        'active': 1
    }),
    Assignment({
        'id': 2380,
        'employee_id': 15,
        'project_id': 312,
        'frum': '1910',
        'thru': '2009',
        'effort': 1,
        'active': 1
    }),
    Assignment({
        'id': 2396,
        'employee_id': 282,
        'project_id': 315,
        'frum': '1910',
        'thru': '2009',
        'effort': 20,
        'active': 1
    })
]

employees = [
    Employee({
        'id': 52,
        'name': 'Emp name 52',
        'fte': 50,
        'investigator': 0,
        'intern': 0,
        'org': 'CCMR',
        'email': 'emp52@va.gov',
        'nonva_email': 'emp52@gmail.com',
        'salary': 104971,
        'fringe': 33.5,
        'active': 1
    }),
    Employee({
        'id': 107,
        'name': 'Emp name 107',
        'fte': 100,
        'investigator': 0,
        'intern': 0,
        'org': 'CCMR',
        'email': 'emp107@va.gov',
        'nonva_email': 'emp107@gmail.com',
        'salary': 74971,
        'fringe': 46.0,
        'active': 1
    }),
    Employee({
        'id': 264,
        'name': 'Emp name 264',
        'fte': 100,
        'investigator': 0,
        'intern': 0,
        'org': 'CCMR',
        'email': 'emp264@va.gov',
        'nonva_email': 'emp264@gmail.com',
        'salary': 70286,
        'fringe': 26.1,
        'active': 1
    }),
    Employee({
        'id': 61,
        'name': 'Emp name 61',
        'fte': 0,
        'investigator': 1,
        'intern': 0,
        'org': 'CCMR',
        'email': 'emp61@va.gov',
        'nonva_email': 'emp61@gmail.com',
        'salary': 123554,
        'fringe': 42.0,
        'active': 1
    }),
    Employee({
        'id': 76,
        'name': 'Emp name 76',
        'fte': 63,
        'investigator': 1,
        'intern': 0,
        'org': 'CCMR',
        'email': 'emp76@va.gov',
        'nonva_email': 'emp76@gmail.com',
        'salary': 142052,
        'fringe': 31.7,
        'active': 1
    }),
    Employee({
        'id': 73,
        'name': 'Emp name 73',
        'fte': 62,
        'investigator': 1,
        'intern': 0,
        'org': 'CCMR',
        'email': 'emp73@va.gov',
        'nonva_email': 'emp73@gmail.com',
        'salary': 114786,
        'fringe': 35.2,
        'active': 1
    }),
    Employee({
        'id': 211,
        'name': 'Emp name 211',
        'fte': 100,
        'investigator': 0,
        'intern': 0,
        'org': 'CCMR',
        'email': 'emp211@va.gov',
        'nonva_email': 'emp211@gmail.com',
        'salary': 50657,
        'fringe': 22.9,
        'active': 1
    }),
    Employee({
        'id': 62,
        'name': 'Emp name 62',
        'fte': 100,
        'investigator': 0,
        'intern': 0,
        'org': 'CCMR',
        'email': 'emp62@va.gov',
        'nonva_email': 'emp62@gmail.com',
        'salary': 53822,
        'fringe': 7.7,
        'active': 1
    }),
    Employee({
        'id': 20,
        'name': 'Emp name 20',
        'fte': 100,
        'investigator': 0,
        'intern': 0,
        'org': 'CCMR',
        'email': 'emp20@va.gov',
        'nonva_email': 'emp20@gmail.com',
        'salary': 61965,
        'fringe': 35.7,
        'active': 1
    }),
    Employee({
        'id': 56,
        'name': 'Emp name 56',
        'fte': 100,
        'investigator': 0,
        'intern': 0,
        'org': 'CCMR',
        'email': 'emp56@va.gov',
        'nonva_email': 'emp56@gmail.com',
        'salary': 74971,
        'fringe': 43.9,
        'active': 1
    }),
    Employee({
        'id': 15,
        'name': 'Emp name 15',
        'fte': 100,
        'investigator': 0,
        'intern': 0,
        'org': 'CCMR',
        'email': 'emp15@va.gov',
        'nonva_email': 'emp15@gmail.com',
        'salary': 52239,
        'fringe': 38.8,
        'active': 1
    }),
    Employee({
        'id': 282,
        'name': 'Emp name 282',
        'fte': 100,
        'investigator': 0,
        'intern': 0,
        'org': 'CCMR',
        'email': 'emp282@va.gov',
        'nonva_email': 'emp282@gmail.com',
        'salary': 44444,
        'fringe': 4.4,
        'active': 1
    })
]

department_items = [
    '',
    'ANESTHESIOLOGY',
    'CARDIOLOGY',
    'CARDIOVASCULAR',
    'CSP',
    'EMERGENCY MEDICINE',
    'FAMILY MEDICINE',
    'GENERAL MEDICINE',
    'GI',
    'HEMATOLOGY',
    'HOSPITAL MEDICINE',
    'IHPI',
    'INFECTIOUS DISEASE',
    'INTERNAL MEDICINE',
    'NEPHROLOGY',
    'NURSING',
    'PALLIATIVE CARE',
    'PSYCHIATRY',
    'PULMONARY',
    'RADIATION ONCOLOGY',
    'SPH',
    'UROLOGY',
    'VASCULAR SURGERY',
    'VERAM'
]

grant_admin_items = [
    '',
    'CARSON,CHAD',
    'DALLAIRE,AMANDA',
    'DENSEN,BRAD',
    'DURON,MIKE',
    'GOROWSKI,TERRI',
    'KOLODICA,JEFF',
    'KRAMER-SMITH,LARA',
    'LUEVANO,LINDA'
]

ledger_rex = []
