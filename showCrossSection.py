'''
特定の距離標の横断図を描画する

py showCrossSection.py sample.csv 24.8 を実行

ラフに可視化する時、matplotlib は強力
'''
import sys # sys パッケージの使用宣言
import os  # os パッケージの使用宣言
import csv
import matplotlib.pyplot as plt # matplotlib パッケージの使用宣言

def main(csvFile, theKp):

    theKp = theKp.strip("0").rstrip(".")
    with open(csvFile) as f:
        csvReader = csv.reader(f)
        while True:
            try:
                basic = next(csvReader)
                kp = basic[0]
                count = int(basic[6])
                flag = basic[11]

                if theKp == kp.strip("0").rstrip("."):
                    xs, zs = [], []
                    for _ in range(count):
                        point = next(csvReader)
                        xs.append(float(point[1])) # 後で説明
                        zs.append(float(point[2]))
                    plt.title(kp)
                    plt.plot(xs, zs)
                    plt.show() # 以上の 8 行で描画できる！
                    break

                else:
                    for _ in range(count):
                        f.readline()
                    if flag != "0":
                        f.readline()

            except StopIteration:
                sys.exit(f'`{theKp}` は {csvFile} に含まれません')

if __name__ == "__main__":

    if len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2])
    else:
        msg = '''
使用方法
  py {} ファイル名 距離標'''.format(os.path.basename(__file__))
        sys.exit(msg)