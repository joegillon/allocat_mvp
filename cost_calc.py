def calculate_cost(salary, fringe, effort, ndays):
    per_hr = (salary / 2087) * (1 + fringe)
    per_day = per_hr * 8
    per_asn = per_day * ndays
    return round(per_asn * effort / 100, 2), round(per_day, 2)

if __name__ == '__main__':
    import sys

    s = int(sys.argv[1])
    f = round(int(sys.argv[2]) * .001, 3)
    e = int(sys.argv[3])
    d = int(sys.argv[4])
    print(calculate_cost(s, f, e, d))
