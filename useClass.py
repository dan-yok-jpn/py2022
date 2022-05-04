'''
河川定期横断数値データ（guideline.md 参照）を読み込んで
距離標、追加距離、低水路幅、最深河床位、低水路平均河床位の一覧を取得する

py useClass.py sample.csv | clip を実行して、excel のワークシートにペースト
'''
import os
import sys
import csv

class guideline:

    TYPE_SELECT = 12 # 測定点属性の既定

    def __init__(self, csvFile):

        self.f = open(csvFile)
        self.reader = csv.reader(self.f)

    def readCrossSection(self):

        try:
            basic = next(self.reader)
            self.kiloPost = basic[0]
            self.interval = float(basic[1])
            count = int(basic[6])

            self.types = []; self.xs = []; self.zs = []
            for _ in range(count):
                point = next(self.reader)
                self.types.append(int(point[0]))
                self.xs.append( float(point[1]))
                self.zs.append( float(point[2]))

            self.Zmin = min(self.zs)

            if basic[11] != "0":
                self.f.readline()

            return True

        except StopIteration:

            self.f.close()
            return False

    def hasBothEnd(self, typeSelect = TYPE_SELECT):

        if self.types.count(typeSelect) == 2:
            self.il = self.types.index(typeSelect)
            self.ir = -list(reversed(self.types)).index(typeSelect) - 1
            return True
        else:
            self.il = self.ir = None
            return False

    def Width(self):

        if self.ir is not None:
            return self.xs[self.ir] - self.xs[self.il]
        else: 
            return None

    def Zave(self, H = None):

        if self.ir is None:
            return None
        if H is None:
            H = min([self.zs[self.il], self.zs[self.ir]])
        elif H < self.Zmin:
            return None

        b, e = self.il + 1, self.ir + 1
        x1, h1 = self.xs[self.il], H - self.zs[self.ir]
        t1 = h1 > 0
        area = 0
        for x2, z2 in zip(self.xs[b:e], self.zs[b:e]):
            h2 = H - z2
            t2 = h2 > 0
            if x2 > x1:
                if t1 & t2:
                    area += (x2 - x1) * (h1 + h2) / 2
                elif t1:
                    dx = (x2 - x1) * h1 / (h1 - h2)
                    area += h1 * dx / 2
                elif t2:
                    dx = (x2 - x1) * h2 / (h2 - h1)
                    area += h2 * dx / 2
            x1, h1, t1 = x2, h2, t2

        return H - area / self.Width()

def main(csvFile):

    g = guideline(csvFile) # csvFile を処理する guideline オブジェクトを作成

    print('距離標\t追加距離\t低水路幅\t最深河床位\t低水路平均河床位')
    distance = 0
    while g.readCrossSection():
        distance += g.interval
        if g.hasBothEnd():
            print('{}\t{}\t{}\t{}\t{}'.format(
                g.kiloPost, distance, g.Width(), g.Zmin, g.Zave()))
        else:
            print(f'{g.kiloPost}\t{distance}\t\t\t')

if __name__ == "__main__":

    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        msg = '''
使用方法
  py {} ファイル名'''.format(os.path.basename(__file__))
        sys.exit(msg)