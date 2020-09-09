def build_departments():
    create_departments_tbl()
    populate_departments_tbl()


def create_departments_tbl():
    print('Creating departments table')
    sql = ("CREATE TABLE IF NOT EXISTS departments ("
           "id INTEGER PRIMARY KEY AUTOINCREMENT, "
           "name TEXT UNIQUE NOT NULL);")
    try:
        # Need this empty tuple to avoid parameters error from sqlite
        dao.execute(sql, ())
        print('Departments table created!')
        return True
    except Exception as e:
        print('Error creating departments table: ' + str(e))
        return False


def populate_departments_tbl():
    from models.department import Department

    depts = [
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
    print('Populating departments...')
    for dept in depts:
        try:
            Department.add_rec(dao, dept)
        except Exception as e:
            print('Error adding department %s: %s' % (dept, str(e)))
            return False
    print('Departments populated!')
    return True


def build_grant_admins():
    create_grant_admins_tbl()
    populate_grant_admins_tbl()


def create_grant_admins_tbl():
    print('Creating grant_admins table')
    sql = ("CREATE TABLE IF NOT EXISTS grant_admins ("
           "id INTEGER PRIMARY KEY AUTOINCREMENT, "
           "name TEXT UNIQUE NOT NULL, "
           "email TEXT);")
    try:
        # Need this empty tuple to avoid parameters error from sqlite
        dao.execute(sql, ())
        print('Table grant_admins created!')
        return True
    except Exception as e:
        print('Error creating grant_admins table: ' + str(e))
        return False


def populate_grant_admins_tbl():
    from models.grant_admin import GrantAdmin

    admins = [
        ('LUEVANO,LINDA', 'lindal@med.umich.edu'),
        ('CARSON,CHAD', ''),
        ('GOROWSKI,TERRI', 'terrig@umich.edu'),
        ('DALLAIRE,AMANDA', 'dallaire@umich.edu'),
        ('KOLODICA,JEFF', 'jmkolod@med.umich.edu'),
        ('KRAMER-SMITH,LARA', 'lkramers@umich.edu'),
        ('DURON,M', ''),
        ('DENSEN,BRAD', 'bdensen@umich.edu')
    ]
    print('Populating grant_admins table...')
    for admin in admins:
        try:
            GrantAdmin.add_admin(dao, admin[0], admin[1])
        except Exception as e:
            print('Error adding grant admin %s: %s' % (admin[0], str(e)))
            return False
    print('Grant_admins populated!')
    return True


def build_ledger_employees():
    create_ledger_employees_tbl()
    create_update_ledger_trigger()
    populate_ledger_employees_tbl()


def create_ledger_employees_tbl():
    print('Creating ledger_employees table')
    sql = ("CREATE TABLE IF NOT EXISTS ledger_employees ("
           "id INTEGER PRIMARY KEY AUTOINCREMENT, "
           "emp_id INTEGER REFERENCES employees (id), "
           "va_email TEXT, "
           "nonva_email TEXT, "
           "salary DECIMAL, "
           "fringe DECIMAL);")
    try:
        # Need this empty tuple to avoid parameters error from sqlite
        dao.execute(sql, ())
        print('Table ledger_employees created!')
        return True
    except Exception as e:
        print('Error creating ledger_employees table: ' + str(e))
        return False


def create_update_ledger_trigger():
    print('Creating update_ledger trigger...')
    sql = ("CREATE TRIGGER update_ledger "
           "AFTER INSERT ON employees "
           "BEGIN "
           "INSERT INTO ledger_employees (emp_id) "
           "VALUES(new.id); "
           "END;")
    try:
        dao.execute(sql, ())
        print('Update_ledger trigger created!')
    except Exception as e:
        print('Error creating update_ledger trigger: ' + str(e))


def populate_ledger_employees_tbl():
    print('Populating ledger_employees table...')
    sql = ("INSERT INTO ledger_employees "
           "(emp_id) "
           "SELECT id FROM employees")
    try:
        # Need this empty tuple to avoid parameters error from sqlite
        dao.execute(sql, ())
        print('Ledger_employees table populated!')
        return True
    except Exception as e:
        print('Error populating ledger_employees: ' + str(e))
        return False


def build_ledger():
    create_ledger()
    populate_ledger()


def create_ledger():
    sql = ("CREATE TABLE IF NOT EXISTS ledger ("
           "id INTEGER PRIMARY KEY AUTOINCREMENT,"
           "quarter INTEGER NOT NULL,"
           "department TEXT,"
           "admin_approved BOOLEAN DEFAULT (0),"
           "va_approved BOOLEAN DEFAULT (0),"
           "invoice_num TEXT,"
           "project TEXT,"
           "staff TEXT,"
           "pct_effort INTEGER,"
           "salary INTEGER,"
           "fringe DECIMAL,"
           "total_day DECIMAL,"
           "days INTEGER,"
           "amount DECIMAL,"
           "frum DATE,"
           "thru DATE,"
           "paid BOOLEAN,"
           "balance DECIMAL,"
           "short_code TEXT,"
           "grant_admin TEXT,"
           "grant_admin_email TEXT);")
    print('Creating ledger table...')
    try:
        # Need this empty tuple to avoid parameters error from sqlite
        dao.execute(sql, ())
        print('Ledger table created!')
        return True
    except Exception as e:
        print('Error creating ledger table: ' + str(e))
        return False


def populate_ledger():
    pass


if __name__ == '__main__':
    from dal.dao import Dao

    dao = Dao(stateful=True)
    build_departments()
    build_grant_admins()
    build_ledger_employees()
    build_ledger()
    dao.close()

    print('Done!')