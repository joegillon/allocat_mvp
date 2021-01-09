def import_spreadsheet():
    import lib.excel_lib as xl
    from dal.dao import Dao
    from models.deposit import Deposit

    file = 'c:/bench/allocat/data/test_deposits.xls'
    wb = xl.open_wb(file)
    sheets = wb.sheet_names()

    rex = []
    dao = Dao(stateful=True)
    for idx in range(0, len(sheets)):
        sh = wb.sheet_by_index(idx)
        print('Sheet ' + sh.name)

        nrows = sum(1 for _ in sh.get_rows())
        for rownum in range(0, nrows):
            if sh.cell_value(rownum, 1).startswith('506'):
                ss_rec = Deposit(sh.row_values(rownum))
                # if ss_rec.invoice_num == 'K8H1025':
                #     print('boo')
                if ss_rec.invoice_num[0:2] not in ('K0', 'K9'):
                    continue
                try:
                    db_rec = Deposit.get_by_invoice_num(dao, ss_rec.invoice_num)
                except Exception as ex:
                    print(str(ex))
                if not db_rec:
                    ss_rec.add(dao)
                    rex.append(ss_rec)
    dao.close()
    return rex

if __name__ == '__main__':
    import_spreadsheet()

