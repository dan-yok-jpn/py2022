import os
import sys
import csv
from datetime import datetime, timedelta
import pandas as pd
# import matplotlib.pyplot as plt

def exceed(ts, Hs, limit):
    if max(Hs) < limit:
        return None, None
    tb = None
    for t, H in zip(ts, Hs):
        if H >= limit:
            if tb is None: tb = t
            te = t
    return tb, te

def prn(ttl, tb, te, limit):

    print(f"\n{ttl}")
    if tb:
        print('\n exceed {:.3f}m {:.1f} hrs  ({} - {})'.format(
            limit, (te - tb).seconds / 3600, tb, te))
    else:
        print(f'\n not exceed {limit:.3f}m')

def main(csvFile, limit):
    with open(csvFile, encoding="utf-8") as f:
        for _ in range(9):
            f.readline()
        reader = csv.reader(f)
        ts, Hs = [], []
        while True:
            try:
                data = next(reader)
                tm = datetime.strptime(data[0], "%Y/%m/%d")
                tm += timedelta(hours = float(data[1].split(":")[0]))
                # tm = datetime.strptime(data[0] + " " + data[1], "%Y/%m/%d %H:%M")
                # data[1]="24:00" の時に ValueError が発生
                # time data '2019/10/12 24:00' does not match format '%Y/%m/%d %H:%M'
                ts.append(tm)
                Hs.append(float(data[2]))
            except StopIteration:
                break
            except Exception as e:
                print(e)
                print(type(e))
                exit()

        tb, te = exceed(ts, Hs, limit)
        prn("exceed()", tb, te, limit)

        df = pd.DataFrame({"ts": ts, "Hs": Hs})
        # df.plot(x = "ts", y = "Hs")
        # plt.savefig("fig3.png")
        rows = df.query("Hs >=" + str(limit))
        if len(rows): 
            tb = rows.iloc[ 0, 0]
            te = rows.iloc[-1, 0]
        prn("pandas", tb, te, limit)

if __name__ == "__main__":
    if len(sys.argv) == 3:
        main(sys.argv[1], float(sys.argv[2]))
    else:
        msg = '''
使用方法
    py {} ファイル名 検査水位'''.format(os.path.basename(__file__))
        sys.exit(msg)