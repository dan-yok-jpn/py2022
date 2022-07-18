'''
河川定期横断数値データ（guideline.html 参照）を読み込んで
低水路幅の縦断図を描画するためのデータを抽出する

py width.py sample.csv | clip を実行して、excel のワークシートにペースト
'''
import os
import sys
import csv

def main(csvFile):

    typeSelect = 12 # 水際杭の測点属性値
    distance = 0
    with open(csvFile) as f:
        csvReader = csv.reader(f)
        while True:
            try:
                basic = next(csvReader)
                kp = basic[0]
                count = int(basic[6])
                distance += float(basic[1])

                types = []; xs = [] # 空の配列
                for _ in range(count):
                    point = next(csvReader)     # 測点データ
                    types.append(int(point[0])) # 測点属性
                    xs.append(float(point[1]))  # 横距

                # >>> arr = [1, 2, 3]
                # >>> arr.append(4)
                # >>> arr
                # [1, 2, 3, 4]

                if types.count(typeSelect) == 2: # 測点属性の配列中に指定したものがあるか

                # >>> arr = [1, 2, 2, 3, 4]
                # >>> arr.count(2)
                # 2

                    il = types.index(typeSelect) # 左岸低水路肩の測点番号
                    ir = -list(reversed(types)).index(typeSelect) - 1 # 右岸低水路肩の測点番号（負）

                    # >>> arr.index(2)
                    # 1
                    # >>> list(reversed(arr))
                    # [4, 3, 2, 2, 1]
                    # >>> list(reversed(arr)).index(2)
                    # 2
                    # >>> arr[-3]
                    # 2

                    width = xs[ir] - xs[il]

                else: # 2 点指定されていない
                    width = ""

                print(f'{kp}\t{distance}\t{width}') # 低水路幅の出力

                if basic[11] != "0":
                    f.readline()

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