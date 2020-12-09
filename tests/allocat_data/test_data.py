from models.project import Project
from models.employee import Employee
from models.assignment import Assignment


projects = [
    Project({
        'id': 297,
        'name': 'Prj 297',
        'full_name': 'Prj Full Name 297',
        'frum': '1901',
        'thru': '1912',
        'investigator_id': 76,
        'investigator': 'EMP 76',
        'manager_id': 56,
        'manager': 'EMP 56',
        'notes': 'Note 297',
        'active': 1,
        'non_va': 1,
        'asns': [
            Assignment({
                'id': 2271,
                'employee_id': 282,
                'employee': 'EMP 282',
                'project_id': 297,
                'project': 'Prj 297',
                'frum': '1910',
                'thru': '1912',
                'effort': 45,
                'notes': 'Asn 2271 note',
                'active': 1
            }),
            Assignment({
                'id': 2272,
                'employee_id': 52,
                'employee': 'EMP 52',
                'project_id': 297,
                'project': 'Prj 297',
                'frum': '1910',
                'thru': '1912',
                'effort': 10,
                'notes': None,
                'active': 1
            })
        ]
    }),
    Project({
        'id': 298,
        'name': 'Prj 298',
        'full_name': 'Prj Full Name 298',
        'frum': '1907',
        'thru': '2406',
        'investigator_id': None,
        'investigator': None,
        'manager_id': 56,
        'manager': 'EMP 56',
        'active': 1,
        'notes': 'Note 298',
        'non_va': 0,
        'asns': [
            Assignment({
                'id': 2280,
                'employee_id': 107,
                'employee': 'EMP 107',
                'project_id': 298,
                'project': 'Prj 298',
                'frum': '1907',
                'thru': '2009',
                'effort': 50,
                'notes': None,
                'active': 1
            }),
            Assignment({
                'id': 2281,
                'employee_id': 264,
                'employee': 'EMP 264',
                'project_id': 298,
                'project': 'Prj 298',
                'frum': '1907',
                'thru': '2009',
                'effort': 10,
                'notes': None,
                'active': 1
            }),
        ]
    }),
    Project({
        'id': 299,
        'name': 'Prj 299',
        'full_name': 'Prj Full Name 299',
        'frum': '1907',
        'thru': '2106',
        'investigator_id': 76,
        'investigator': 'EMP 76',
        'manager_id': None,
        'manager': None,
        'active': 1,
        'notes': None,
        'non_va': 1,
        'asns': [
            Assignment({
                'id': 2275,
                'employee_id': 56,
                'employee': 'EMP 56',
                'project_id': 299,
                'project': 'Prj 299',
                'frum': '2002',
                'thru': '2003',
                'effort': 45,
                'notes': None,
                'active': 1
            }),
            Assignment({
                'id': 2282,
                'employee_id': 61,
                'employee': 'EMP 61',
                'project_id': 299,
                'project': 'Prj 299',
                'frum': '1907',
                'thru': '2106',
                'effort': 10,
                'notes': 'Asn 2282 note',
                'active': 1
            })
        ]
    }),
    Project({
        'id': 301,
        'name': 'Prj 301',
        'full_name': 'Prj Full Name 301',
        'frum': '1904',
        'thru': '1909',
        'investigator_id': None,
        'investigator': None,
        'manager_id': None,
        'manager': None,
        'active': 1,
        'notes': None,
        'non_va': 0,
        'asns': [
            Assignment({
                'id': 2310,
                'employee_id': 76,
                'employee': 'EMP 76',
                'project_id': 301,
                'project': 'Prj 301',
                'frum': '1907',
                'thru': '2009',
                'effort': 25,
                'notes': None,
                'active': 1
            }),
            Assignment({
                'id': 2366,
                'employee_id': 73,
                'employee': 'EMP 73',
                'project_id': 301,
                'project': 'Prj 301',
                'frum': '1910',
                'thru': '2009',
                'effort': 5,
                'notes': None,
                'active': 1
            }),
            Assignment({
                'id': 2367,
                'employee_id': 211,
                'employee': 'EMP 211',
                'project_id': 301,
                'project': 'Prj 301',
                'frum': '1910',
                'thru': '2009',
                'effort': 40,
                'notes': None,
                'active': 1
            }),
            Assignment({
                'id': 2368,
                'employee_id': 62,
                'employee': 'EMP 62',
                'project_id': 301,
                'project': 'Prj 301',
                'frum': '1910',
                'thru': '2009',
                'effort': 40,
                'notes': None,
                'active': 1
            }),
        ]
    }),
    Project({
        'id': 309,
        'name': 'Prj 309',
        'full_name': 'Prj Full Name 309',
        'frum': '1908',
        'thru': '2009',
        'investigator_id': 73,
        'investigator': 'EMP 73',
        'manager_id': 211,
        'manager': 'EMP 211',
        'active': 1,
        'notes': 'Note 309',
        'non_va': 1,
        'asns': [
            Assignment({
                'id': 2365,
                'employee_id': 106,
                'employee': 'EMP 106',
                'project_id': 309,
                'project': 'Prj 309',
                'frum': '1910',
                'thru': '2009',
                'effort': 5,
                'notes': None,
                'active': 1
            }),
            Assignment({
                'id': 2375,
                'employee_id': 107,
                'employee': 'EMP 107',
                'project_id': 309,
                'project': 'Prj 309',
                'frum': '2002',
                'thru': '2009',
                'effort': 15,
                'notes': None,
                'active': 1
            }),
            Assignment({
                'id': 2382,
                'employee_id': 76,
                'employee': 'EMP 76',
                'project_id': 309,
                'project': 'Prj 309',
                'frum': '2002',
                'thru': '2002',
                'effort': 10,
                'notes': 'Yawn',
                'active': 1
            })
        ]
    }),
    Project({
        'id': 311,
        'name': 'Prj 311',
        'full_name': 'Prj Full Name 311',
        'frum': '1910',
        'thru': '2009',
        'investigator_id': None,
        'investigator': None,
        'manager_id': 211,
        'manager': 'EMP 211',
        'active': 1,
        'notes': None,
        'non_va': 0,
        'asns': [
            Assignment({
                'id': 2378,
                'employee_id': 20,
                'employee': 'EMP 20',
                'project_id': 311,
                'project': 'Prj 311',
                'frum': '1910',
                'thru': '2009',
                'effort': 2,
                'notes': None,
                'active': 1
            }),
            Assignment({
                'id': 2379,
                'employee_id': 56,
                'employee': 'EMP 56',
                'project_id': 311,
                'project': 'Prj 311',
                'frum': '1910',
                'thru': '2009',
                'effort': 3,
                'notes': None,
                'active': 1
            }),
        ]
    }),
    Project({
        'id': 312,
        'name': 'Prj 312',
        'full_name': 'Prj Full Name 312',
        'frum': '1909',
        'thru': '2109',
        'investigator_id': 73,
        'investigator': 'EMP 73',
        'manager_id': None,
        'manager': None,
        'active': 1,
        'notes': 'Note 312',
        'non_va': 0,
        'asns': [
            Assignment({
                'id': 2380,
                'employee_id': 15,
                'employee': 'EMP 15',
                'project_id': 312,
                'project': 'Prj 312',
                'frum': '1910',
                'thru': '2009',
                'effort': 1,
                'notes': None,
                'active': 1
            }),
        ]
    }),
    Project({
        'id': 315,
        'name': 'Prj 315',
        'full_name': 'Prj Full Name 315',
        'frum': '1807',
        'thru': '2106',
        'investigator_id': None,
        'investigator': None,
        'manager_id': None,
        'manager': None,
        'active': 1,
        'notes': None,
        'non_va': 1,
        'asns': [
            Assignment({
                'id': 2283,
                'employee_id': 73,
                'employee': 'EMP 73',
                'project_id': 315,
                'project': 'Prj 315',
                'frum': '1912',
                'thru': '2002',
                'effort': 10,
                'notes': None,
                'active': 1
            }),
            Assignment({
                'id': 2396,
                'employee_id': 282,
                'employee': 'EMP 282',
                'project_id': 315,
                'project': 'Prj 315',
                'frum': '1910',
                'thru': '2009',
                'effort': 20,
                'notes': 'Burp',
                'active': 1
            })
        ]
    })
]

employees = [
    Employee({
        'id': 106,
        'name': 'EMP 106',
        'fte': 100,
        'investigator': 0,
        'intern': 0,
        'pm': 0,
        'org': 'CCMR',
        'va_email': 'emp106@va.gov',
        'nonva_email': 'emp106@gmail.com',
        'salary': None,
        'fringe': None,
        'notes': 'Emp 106 note',
        'active': 1,
        'asns': [
            Assignment({
                'id': 2365,
                'employee_id': 106,
                'employee': 'EMP 106',
                'project_id': 309,
                'project': 'Prj 309',
                'frum': '1910',
                'thru': '2009',
                'effort': 5,
                'notes': None,
                'active': 1
            })
        ]
    }),
    Employee({
        'id': 107,
        'name': 'EMP 107',
        'fte': 100,
        'investigator': 0,
        'intern': 0,
        'pm': 0,
        'org': 'CCMR',
        'va_email': 'emp107@va.gov',
        'nonva_email': 'emp107@gmail.com',
        'salary': 74971,
        'fringe': 46,
        'notes': 'Emp 107 note',
        'active': 1,
        'asns': [
            Assignment({
                'id': 2280,
                'employee_id': 107,
                'employee': 'EMP 107',
                'project_id': 298,
                'project': 'Prj 298',
                'frum': '1907',
                'thru': '2009',
                'effort': 50,
                'notes': None,
                'active': 1
            }),
            Assignment({
                'id': 2375,
                'employee_id': 107,
                'employee': 'EMP 107',
                'project_id': 309,
                'project': 'Prj 309',
                'frum': '2002',
                'thru': '2009',
                'effort': 15,
                'notes': None,
                'active': 1
            }),
        ]
    }),
    Employee({
        'id': 15,
        'name': 'EMP 15',
        'fte': 100,
        'investigator': 0,
        'intern': 1,
        'pm': 0,
        'org': 'CCMR',
        'va_email': 'emp15@va.gov',
        'nonva_email': None,
        'salary': 52239,
        'fringe': 38.8,
        'notes': 'Intern',
        'active': 1,
        'asns': [
            Assignment({
                'id': 2380,
                'employee_id': 15,
                'employee': 'EMP 15',
                'project_id': 312,
                'project': 'Prj 312',
                'frum': '1910',
                'thru': '2009',
                'effort': 1,
                'notes': None,
                'active': 1
            }),
        ]
    }),
    Employee({
        'id': 20,
        'name': 'EMP 20',
        'fte': 100,
        'investigator': 0,
        'intern': 0,
        'org': 'CCMR',
        'pm': 1,
        'va_email': None,
        'nonva_email': None,
        'salary': 61965,
        'fringe': 35.7,
        'notes': None,
        'active': 1,
        'asns': [
            Assignment({
                'id': 2378,
                'employee_id': 20,
                'employee': 'EMP 20',
                'project_id': 311,
                'project': 'Prj 311',
                'frum': '1910',
                'thru': '2009',
                'effort': 2,
                'notes': None,
                'active': 1
            }),
        ]
    }),
    Employee({
        'id': 211,
        'name': 'EMP 211',
        'fte': 100,
        'investigator': 0,
        'intern': 0,
        'pm': 0,
        'org': 'CCMR',
        'va_email': 'emp211@va.gov',
        'nonva_email': 'emp211@yahoo.com',
        'salary': 50657,
        'fringe': 22.9,
        'notes': None,
        'active': 1,
        'asns': [
            Assignment({
                'id': 2367,
                'employee_id': 211,
                'employee': 'EMP 211',
                'project_id': 301,
                'project': 'Prj 301',
                'frum': '1910',
                'thru': '2009',
                'effort': 40,
                'notes': None,
                'active': 1
            }),
        ]
    }),
    Employee({
        'id': 264,
        'name': 'EMP 264',
        'fte': 100,
        'investigator': 0,
        'intern': 0,
        'pm': 1,
        'org': 'CCMR',
        'va_email': 'emp264@va.gov',
        'nonva_email': None,
        'salary': 70286,
        'fringe': 26.1,
        'notes': None,
        'active': 1,
        'asns': [
            Assignment({
                'id': 2281,
                'employee_id': 264,
                'employee': 'EMP 264',
                'project_id': 298,
                'project': 'Prj 298',
                'frum': '1907',
                'thru': '2009',
                'effort': 10,
                'notes': None,
                'active': 1
            }),
        ]
    }),
    Employee({
        'id': 282,
        'name': 'EMP 282',
        'fte': 100,
        'investigator': 0,
        'intern': 0,
        'pm': 0,
        'org': 'CCMR',
        'va_email': None,
        'nonva_email': None,
        'salary': 44444,
        'fringe': 4.4,
        'notes': None,
        'active': 1,
        'asns': [
            Assignment({
                'id': 2271,
                'employee_id': 282,
                'employee': 'EMP 282',
                'project_id': 297,
                'project': 'Prj 297',
                'frum': '1910',
                'thru': '1912',
                'effort': 45,
                'notes': 'Asn 2271 note',
                'active': 1
            }),
            Assignment({
                'id': 2396,
                'employee_id': 282,
                'employee': 'EMP 282',
                'project_id': 315,
                'project': 'Prj 315',
                'frum': '1910',
                'thru': '2009',
                'effort': 20,
                'notes': 'Burp',
                'active': 1
            })
        ]
    }),
    Employee({
        'id': 52,
        'name': 'EMP 52',
        'fte': 50,
        'investigator': 1,
        'intern': 0,
        'pm': 0,
        'org': 'SMITREC',
        'va_email': None,
        'nonva_email': 'emp52@umich.edu',
        'salary': 104971,
        'fringe': 33.5,
        'notes': 'Emp 52 note',
        'active': 1,
        'asns': [
            Assignment({
                'id': 2272,
                'employee_id': 52,
                'employee': 'EMP 52',
                'project_id': 297,
                'project': 'Prj 297',
                'frum': '1910',
                'thru': '1912',
                'effort': 10,
                'notes': None,
                'active': 1
            }),
        ]
    }),
    Employee({
        'id': 56,
        'name': 'EMP 56',
        'fte': 100,
        'investigator': 0,
        'intern': 0,
        'pm': 0,
        'org': 'CCMR',
        'va_email': 'emp56@va.gov',
        'nonva_email': 'emp56@umich.edu',
        'salary': 74971,
        'fringe': 43.9,
        'notes': None,
        'active': 1,
        'asns': [
            Assignment({
                'id': 2275,
                'employee_id': 56,
                'employee': 'EMP 56',
                'project_id': 299,
                'project': 'Prj 299',
                'frum': '2002',
                'thru': '2003',
                'effort': 45,
                'notes': None,
                'active': 1
            }),
            Assignment({
                'id': 2379,
                'employee_id': 56,
                'employee': 'EMP 56',
                'project_id': 311,
                'project': 'Prj 311',
                'frum': '1910',
                'thru': '2009',
                'effort': 3,
                'notes': None,
                'active': 1
            }),
        ]
    }),
    Employee({
        'id': 61,
        'name': 'EMP 61',
        'fte': 0,
        'investigator': 1,
        'intern': 0,
        'pm': 0,
        'org': 'CCMR',
        'va_email': 'emp61@va.gov',
        'nonva_email': None,
        'salary': None,
        'fringe': None,
        'notes': None,
        'active': 0,
        'asns': [
            Assignment({
                'id': 2282,
                'employee_id': 61,
                'employee': 'EMP 61',
                'project_id': 299,
                'project': 'Prj 299',
                'frum': '1907',
                'thru': '2106',
                'effort': 10,
                'notes': 'Asn 2282 note',
                'active': 0
            }),
        ]
    }),
    Employee({
        'id': 62,
        'name': 'EMP 62',
        'fte': 80,
        'investigator': 0,
        'intern': 0,
        'pm': 1,
        'org': 'CCMR',
        'va_email': None,
        'nonva_email': None,
        'salary': 53822,
        'fringe': 7.7,
        'notes': None,
        'active': 1,
        'asns': [
            Assignment({
                'id': 2368,
                'employee_id': 62,
                'employee': 'EMP 62',
                'project_id': 301,
                'project': 'Prj 301',
                'frum': '1910',
                'thru': '2009',
                'effort': 40,
                'notes': None,
                'active': 1
            }),
        ]
    }),
    Employee({
        'id': 73,
        'name': 'EMP 73',
        'fte': 62,
        'investigator': 1,
        'intern': 0,
        'pm': 0,
        'org': 'RCA',
        'va_email': None,
        'nonva_email': 'emp73@umich.edu',
        'salary': 114786,
        'fringe': 35.2,
        'notes': None,
        'active': 1,
        'asns': [
            Assignment({
                'id': 2283,
                'employee_id': 73,
                'employee': 'EMP 73',
                'project_id': 315,
                'project': 'Prj 315',
                'frum': '1912',
                'thru': '2002',
                'effort': 10,
                'notes': None,
                'active': 1
            }),
            Assignment({
                'id': 2366,
                'employee_id': 73,
                'employee': 'EMP 73',
                'project_id': 301,
                'project': 'Prj 301',
                'frum': '1910',
                'thru': '2009',
                'effort': 5,
                'notes': None,
                'active': 1
            }),
        ]
    }),
    Employee({
        'id': 76,
        'name': 'EMP 76',
        'fte': 63,
        'investigator': 1,
        'intern': 0,
        'pm': 0,
        'org': 'CCMR',
        'va_email': None,
        'nonva_email': None,
        'salary': 142052,
        'fringe': 31.7,
        'notes': None,
        'active': 1,
        'asns': [
            Assignment({
                'id': 2310,
                'employee_id': 76,
                'employee': 'EMP 76',
                'project_id': 301,
                'project': 'Prj 301',
                'frum': '1907',
                'thru': '2009',
                'effort': 25,
                'notes': None,
                'active': 1
            }),
            Assignment({
                'id': 2382,
                'employee_id': 76,
                'employee': 'EMP 76',
                'project_id': 309,
                'project': 'Prj 309',
                'frum': '2002',
                'thru': '2002',
                'effort': 10,
                'notes': 'Yawn',
                'active': 1
            }),
        ]
    }),
]

assignments = [
    Assignment({
        'id': 2271,
        'employee_id': 282,
        'project_id': 297,
        'frum': '1910',
        'thru': '1912',
        'effort': 45,
        'notes': 'Asn 2271 note',
        'active': 1
    }),
    Assignment({
        'id': 2272,
        'employee_id': 52,
        'project_id': 297,
        'frum': '1910',
        'thru': '1912',
        'effort': 10,
        'notes': None,
        'active': 1
    }),
    Assignment({
        'id': 2275,
        'employee_id': 56,
        'project_id': 299,
        'frum': '2002',
        'thru': '2003',
        'effort': 45,
        'notes': None,
        'active': 1
    }),
    Assignment({
        'id': 2280,
        'employee_id': 107,
        'project_id': 298,
        'frum': '1907',
        'thru': '2009',
        'effort': 50,
        'notes': None,
        'active': 1
    }),
    Assignment({
        'id': 2281,
        'employee_id': 264,
        'project_id': 298,
        'frum': '1907',
        'thru': '2009',
        'effort': 10,
        'notes': None,
        'active': 1
    }),
    Assignment({
        'id': 2282,
        'employee_id': 61,
        'project_id': 299,
        'frum': '1907',
        'thru': '2106',
        'effort': 10,
        'notes': 'Asn 2282 note',
        'active': 1
    }),
    Assignment({
        'id': 2283,
        'employee_id': 73,
        'project_id': 315,
        'frum': '1912',
        'thru': '2002',
        'effort': 10,
        'notes': None,
        'active': 1
    }),
    Assignment({
        'id': 2310,
        'employee_id': 76,
        'project_id': 301,
        'frum': '1907',
        'thru': '2009',
        'effort': 25,
        'notes': None,
        'active': 1
    }),
    Assignment({
        'id': 2365,
        'employee_id': 106,
        'project_id': 309,
        'frum': '1910',
        'thru': '2009',
        'effort': 5,
        'notes': None,
        'active': 1
    }),
    Assignment({
        'id': 2366,
        'employee_id': 73,
        'project_id': 301,
        'frum': '1910',
        'thru': '2009',
        'effort': 5,
        'notes': None,
        'active': 1
    }),
    Assignment({
        'id': 2367,
        'employee_id': 211,
        'project_id': 301,
        'frum': '1910',
        'thru': '2009',
        'effort': 40,
        'notes': None,
        'active': 1
    }),
    Assignment({
        'id': 2368,
        'employee_id': 62,
        'project_id': 301,
        'frum': '1910',
        'thru': '2009',
        'effort': 40,
        'notes': None,
        'active': 1
    }),
    Assignment({
        'id': 2375,
        'employee_id': 107,
        'project_id': 309,
        'frum': '2002',
        'thru': '2009',
        'effort': 15,
        'notes': None,
        'active': 1
    }),
    Assignment({
        'id': 2378,
        'employee_id': 20,
        'project_id': 311,
        'frum': '1910',
        'thru': '2009',
        'effort': 2,
        'notes': None,
        'active': 1
    }),
    Assignment({
        'id': 2379,
        'employee_id': 56,
        'project_id': 311,
        'frum': '1910',
        'thru': '2009',
        'effort': 3,
        'notes': None,
        'active': 1
    }),
    Assignment({
        'id': 2380,
        'employee_id': 15,
        'project_id': 312,
        'frum': '1910',
        'thru': '2009',
        'effort': 1,
        'notes': None,
        'active': 1
    }),
    Assignment({
        'id': 2382,
        'employee_id': 76,
        'project_id': 309,
        'frum': '2002',
        'thru': '2002',
        'effort': 10,
        'notes': 'Yawn',
        'active': 1
    }),
    Assignment({
        'id': 2396,
        'employee_id': 282,
        'project_id': 315,
        'frum': '1910',
        'thru': '2009',
        'effort': 20,
        'notes': 'Burp',
        'active': 1
    })
]

pi_list_items = ['', 'EMP 52', 'EMP 73', 'EMP 76']

pm_iist_items = [
    '', 'EMP 106', 'EMP 107', 'EMP 15', 'EMP 20',
    'EMP 211', 'EMP 264', 'EMP 282', 'EMP 56', 'EMP 62'
]