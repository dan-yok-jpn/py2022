'''
河川定期横断数値データ（guideline.html 参照）を読み込んで
低水路平均河床位の縦断図を描画するためのデータを抽出する

py zave.py sample.csv | clip を実行して、excel のワークシートにペースト
'''
import os
import sys
import csv

def Zave(xs, zs, il, ir, H = None):
    '''
    Parameters:
        xs (list of float): 横距の配列
        zs (list of float): 河床高の配列
        il (int): 平均河床位を求める範囲の左端の測点
        ir (int): 平均河床位を求める範囲の右端の測点
        H (float, optional): 基準水位
    Rerurns:
        float or None : 2 測点間の平均河床位 (基準水位が最深河床位以下の時は None)
    '''

    if H is None:
        H = min([zs[il], zs[ir]])
    elif H < min(zs):
        return None

    b = il + 1
    e = ir + 1
    x1 = xs[il]
    h1 = H - zs[il] # 水深
    t1 = h1 > 0 # 水面下か否か

    area = 0
    for x2, z2 in zip(xs[b:e], zs[b:e]): # 測点 b から (e-1) までの座標

        # >>> arr1 = [1, 2, 3, 4, 5]
        # >>> arr2 = [6, 7, 8, 9, 10]
        # >>> arr1[1:4] 
        # [2, 3, 4]
        # >>> arr2[1:4]
        # [7, 8, 9]
        # >>> for v1, v2 in zip(arr1[1:4], arr2[1:4])
        # ...      print(v1, v2)
        # ...
        # 2 7
        # 3 8
        # 4 9

        h2 = H - z2
        t2 = h2 > 0

        if x2 > x1: # オーバーハング無視

            if t1 & t2: # 両測点とも水面下
                area += (x2 - x1) * (h1 + h2) / 2

            # >>> T = True
            # >>> F = False
            # >>> T & T
            # True
            # >>> T & F
            # False
            # >>> F & F
            # False

            elif t1: # 左岸側の測点のみ水面下
                dx = (x2 - x1) * h1 / (h1 - h2)
                area += h1 * dx / 2

            elif t2: # 右岸側の測点のみ水面下
                dx = (x2 - x1) * h2 / (h2 - h1)
                area += h2 * dx / 2

        x1, h1, t1 = x2, h2, t2

    return H - area / (xs[ir] - xs[il])

def main(csvFile):

    typeSelect = 12
    distance = 0
    with open(csvFile) as f:
        csvReader = csv.reader(f)
        while True:
            try:
                basic = next(csvReader)
                kp = basic[0]
                count = int(basic[6])
                distance += float(basic[1])

                types = []; xs = []; zs = []
                for _ in range(count):
                    point = next(csvReader)
                    types.append(  int(point[0]))
                    xs.append(float(point[1]))
                    zs.append(float(point[2])) # 河床位

                if types.count(typeSelect) == 2:

                    il = types.index(typeSelect)
                    ir = -list(reversed(types)).index(typeSelect) - 1
                    zave = Zave(xs, zs, il, ir) # Zave 関数で平均河床高を計算

                else:
                    zave = ""

                print(f'{kp}\t{distance}\t{zave}')

                if basic[11] != "0":
                    next(csvReader)

            except StopIteration:
                break

            except Exception as e: # StopIteration 以外
                exit(e)

if __name__ == "__main__":

    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        msg = '''
使用方法
  py {} ファイル名'''.format(os.path.basename(__file__))
        sys.exit(msg)