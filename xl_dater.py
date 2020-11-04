import lib.excel_lib as xl

if __name__ == '__main__':
    import sys

    m = int(sys.argv[1])
    d = int(sys.argv[2])
    y = int(sys.argv[3])
    print(xl.to_xl_date(m, d, y))
