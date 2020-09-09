import sqlite3
import globals as gbl


class Dao(object):
    def __init__(self, stateful=None, db_path=None):
        if db_path:
            self.__db = sqlite3.connect(db_path)
        else:
            self.__db = sqlite3.connect(gbl.DB_PATH)

        self.__db.execute('PRAGMA FOREIGN_KEYS = ON')

        self.__cursor = self.__db.cursor()
        self.__stateful = stateful

    def execute(self, sql, params=None):
        self.op = sql.split(' ', 1)[0].upper()
        if self.op == 'SELECT':
            result = self.__read(sql, params)
        else:
            result = self.__write(sql, params)
        if not self.__stateful:
            self.__db.close()
        return result

    def __read(self, sql, params=None):
        # Seems you can't pass a None type to the execute func.
        if params:
            n = self.__cursor.execute(sql, params)
        else:
            n = self.__cursor.execute(sql)
        if not n:
            return []
        rex = self.__cursor.fetchall()
        flds = [f[0] for f in self.__cursor.description]
        return [dict(zip(flds, rec)) for rec in rex] if rex else []

    def __write(self, sql, params=None):
        self.__cursor.execute(sql, params)
        self.__db.commit()
        if self.op == 'INSERT':
            return self.__cursor.lastrowid
        else:
            return self.__cursor.rowcount

    def close(self):
        self.__db.close()

    def get_param_str(self, lst):
        return ('?,' * len(lst))[0:-1]

    def txn_write(self, sql, params=None):
        self.__cursor.execute(sql, params)

    def rollback(self):
        self.__db.rollback()

    def commit(self):
        self.__db.commit()
