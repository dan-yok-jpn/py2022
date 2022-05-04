'''
河川定期横断数値データ（guideline.html 参照）を読み込んで
最深河床高の縦断図を描画するためのデータを抽出する

py zmin.py sample.csv | clip を実行して、excel のワークシートにペースト

全ての作業を python で完結する必要はない
'''
import sys # sys パッケージの使用宣言
import os  # os パッケージの使用宣言
import csv

def main(csvFile):
   
    distance = 0 # 累加距離の初期値
    with open(csvFile) as f:
        csvReader = csv.reader(f)
        while True:
            try:
                basic = next(csvReader)
                kp = basic[0]
                count = int(basic[6])
                flag = basic[11]

                zmin = 9999 # 最深河床高の初期値
                for _ in range(count):
                    z = float(next(csvReader)[2]) # 標高（測点データの 3 カラム目）
                    if z < zmin:
                        zmin = z # 最深河床高の暫定値

                if flag != "0":
                    f.readline()

                distance += float(basic[1]) # 累加距離

                # >>> i = 1
                # >>> i += 2
                # >>> i
                # 3
                # >>> i -= 1
                # >>> i
                # 2
                # >>> i *= 5
                # >>> i
                # 10
                # >>> i /= 4
                # 2.5

                print(f'{kp}\t{distance}\t{zmin}') # 結果の出力。区切り文字はタブ

                # >>> tab = "\t"
                # >>> s = kp + tab + str(distance) + tab + str(zmin)
                # >>> print(s)

            except StopIteration:
                break

if __name__ == "__main__":

    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        msg = '''
使用方法
  py {} ファイル名'''.format(os.path.basename(__file__))
        sys.exit(msg)