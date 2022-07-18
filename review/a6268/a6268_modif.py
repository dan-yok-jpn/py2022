import os
import sys
import csv
import glob
import traceback

def usage():

    msg = '''
基準水位における川幅と基準位以下の河積から求める平均河床位の縦断分布を出力

  python {} [-h] [file_datum dir_survey]

    file_datum : 各測線の基準水位の csv ファイル (ex. HWL.csv)
    dir_survey : 河川定期横断数値データのフォルダ (ex. oudan)
    -h         : ヘルプ'''.format(os.path.basename(__file__))
    sys.exit(msg)

def Zave(xs, zs, il, ir, H):

    b = il + 1
    e = ir + 1
    x1 = xs[il]
    h1 = H - zs[il] # 水深
    t1 = h1 > 0 # 水面下か否か
    area = 0; width = 0
    for x2, z2 in zip(xs[b:e], zs[b:e]):
        h2 = H - z2
        t2 = h2 > 0
        dx = x2 - x1
        if dx > 0: # オーバーハング無視
            if t1 & t2: # 両測点とも水面下
                width += dx
                area  += dx * (h1 + h2) / 2
            elif t1: # 左岸側の測点のみ水面下
                dx *= h1 / (h1 - h2)
                width += dx
                area  += h1 * dx / 2
            elif t2: # 右岸側の測点のみ水面下
                dx *= h2 / (h2 - h1)
                width += dx
                area  += h2 * dx / 2
        x1, h1, t1 = x2, h2, t2

    return H - area / width, width

def main(file_datum, data_dir):

    with open(file_datum) as f:
        f.readline() # ヘッダ読み飛ばし
        datums = {}
        for row in csv.reader(f):
            datums[row[0]] = float(row[1]) # datums["36.8"] = 42.326

    print("kp", "datum", "zave", "width", "xl", "xr", sep="\t")

    for file in glob.glob(data_dir + "/WZAA4*.CSV"):

        with open(file) as ff:

            csvreader = csv.reader(ff) # ヘッダー
            cols = next(csvreader) 
            kp  = float(cols[0])
            count = int(cols[6])

            try:
                key = str(int(kp)) if kp == int(kp) else str(kp)
                datum = datums[key] # 基準位
                types = []; xs = []; zs = [] # 測点タイプ、座標
                for _ in range(count):
                    point = next(csvreader)
                    types.append(int(point[0]))
                    xs.append(float( point[1]))
                    zs.append(float( point[2]))
                try:
                    il = types.index( 1) # 左岸距離杭高
                    ir = types.index(18) # 右岸距離杭高
                except ValueError:
                    print(f"\n!!! {file} の左右岸距離標の位置が不明",
                        file=sys.stderr)
                    continue

                if datum > min(zs):
                    zave, width = Zave(xs, zs, il, ir, datum)
                    print(kp, datum, zave, width, xs[il], xs[ir], sep="\t")
                else:
                    print(kp, datum, "", "", xs[il], xs[ir], sep="\t")

            except KeyError:
                print(f"!!! {key} の基準位が不明", file=sys.stderr)

if __name__ == "__main__":

    if "-h" in sys.argv:
        usage()
    if len(sys.argv) == 3:
        try:
            main(sys.argv[1], sys.argv[2])
        except Exception as e:
            print("\n", traceback.format_exception_only(type(e), e)[0])
    else:
        usage()
