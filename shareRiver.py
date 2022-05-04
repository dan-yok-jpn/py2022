
__version__ = "1.0.0"
__date__    = "May 2022"

import csv
import json

class crossSection:
    '''河道横断情報を扱うクラス

    Args:
        kiloPost (str) : 距離標
        interval (float) : 区間距離
        cordinates (list of [float, float]) : 測点の座標の配列
    '''

    def __init__(self, kiloPost, interval, cordinates):

        self._kiloPost = kiloPost
        self._interval = interval
        self._cordinates = cordinates
        self._Zmin = min([p[1] for p in cordinates])

    @property
    def kiloPost(self):
        '''str : 距離標'''
        return self._kiloPost

    @property
    def interval(self):
        '''float : 区間距離'''
        return self._interval

    @property
    def Zmin(self):
        '''float  : 最深河床位'''
        return self._Zmin

    def Width(self, il, ir):
        '''
        Args:
            il (int) : 左岸端の測点番号
            ir (int) : 右岸端の測点番号
        Returns:
            float or None : 指定した測点間の横距
        Notes:
            測点番号、基準水位が不適当な場合は None を返す
        '''
        if il is None or ir is None:
            return None
        else: 
            return self._cordinates[ir][0] - self._cordinates[il][0]

    def Zave(self, il, ir, H = None):
        '''
        Args:
            il (int) : 左岸端の測点番号
            ir (int) : 右岸端の測点番号
            H (float, optional) : 基準水位
        Returns:
            float or None : 指定した測点間の平均河床高
        Notes:
            1. 基準水位を省略した場合の基準水位は両端の標高の何れか低いもの
            2. 測点番号、基準水位が不適当な場合は None を返す
        '''
        if il is None or ir is None:
            return None

        if H is None:
            H = min([self._cordinates[il][1], self._cordinates[ir][1]])
        elif H < self.Zmin:
            return None

        b, e = il + 1, ir + 1
        x1 = self._cordinates[il][0]
        h1 = H - self._cordinates[ir][1]
        t1 = h1 > 0
        area = 0
        for (x2, z2) in self._cordinates[b:e]:
            h2 = H - z2
            t2 = h2 > 0
            if x2 > x1:
                if t1 and t2:
                    area += (x2 - x1) * (h1 + h2) / 2
                elif t1:
                    dx = (x2 - x1) * h1 / (h1 - h2)
                    area += h1 * dx / 2
                elif t2:
                    dx = (x2 - x1) * h2 / (h2 - h1)
                    area += h2 * dx / 2
            x1, h1, t1 = x2, h2, t2
        width = self._cordinates[ir][0] - self._cordinates[il][0]
        return H - area / width

class guidline(crossSection):
    '''河川定期縦横断データ作成ガイドライン準拠の河道横断情報を扱うクラス

    Args:
        csvFile (str) : csv ファイルのファイル名
    '''
    def __init__(self, csvFile):

        self.f = open(csvFile)
        self.reader = csv.reader(self.f)

    def readCrossSection(self):
        '''ガイドライン準拠の横断情報を読み込む

        Returns:
            bool : 断面データ取得の時 True、読込済みの時 False
        '''
        try:
            basic = next(self.reader)
            kiloPost = basic[0]
            interval = float(basic[1])
            count = int(basic[6])

            self.types = []; cordinates = []
            for _ in range(count):
                point = next(self.reader)
                self.types.append(int(point[0]))
                cordinates.append([float(point[1]), float(point[2])])

            if basic[11] != "0":
                self.f.readline()

            # types 以外は親クラス（crossSection）の属性として初期化
            super().__init__(kiloPost, interval, cordinates)

            return True

        except StopIteration:

            self.f.close()
            return False

    def hasBothEnd(self, typeSelect = 12):
        '''指定した測点属性を有する測点は左右岸に存在するか

        Args:
            typeSelect (int, optional) : 測点属性の指定値。guideline.html 参照。既定値の 12 は「水際杭」
        Returns:
            bool : 左右岸に存在する時 True、しない時 False
        Notes:
            True の場合は該当する測点のインデックスが記憶される
        '''
        if self.types.count(typeSelect) == 2:
            self.il = self.types.index(typeSelect)
            self.ir = -list(reversed(self.types)).index(typeSelect) - 1
            return True
        else:
            self.il = None
            self.ir = None
            return False

    def Width(self):
        '''
        Returns:
            float or None : 既定の測点属性を有する測点間の横距
        Notes:
            測点は hasBothEnd() で指定したものを使用する
        '''
        return super().Width(self.il, self.ir)

    def Zave(self, H = None):
        '''
        Args:
            H (float, optional) : 基準水位
        Returns:
            float or None : 既定の測点属性を有する測点間の平均河床位
        Notes:
            1. 測点は hasBothEnd() で指定したものを使用する
            2. 基準水位を省略した場合は上記の測点の標高の何れか低い方
        '''
        return super().Zave(self.il, self.ir, H)

class csJson(crossSection):
    '''JSON から入力した河道横断情報を扱うクラス

    Args:
        jsonFile (str) : json ファイルのファイル名
    '''

    def __init__(self, jsonFile):

        f = open(jsonFile)
        self.CSs = json.load(f)
        self.index = 0
        self.count = len(self.CSs)

    @property
    def evalPointLeft(self):
        '''int : 左岸端の測点番号'''
        pass
    @evalPointLeft.setter
    def evalPointLeft(self, il):
        self._il = il

    @property
    def evalPointRight(self):
        '''int : 右岸端の測点番号'''
        pass
    @evalPointRight.setter
    def evalPointRight(self, ir):
        self._ir = ir

    def readCrossSection(self):
        '''json ファイルから横断情報を読み込む

        Returns:
            bool : 断面データ取得の時 True、読込済みの時 False
        '''
        if self.index == self.count:
            return False
        else:
            cs = self.CSs[self.index]
            kiloPost = cs["kiloPost"]
            interval = cs["interval"]
            cordinates = cs["cordinates"]
            if "evalPoints" in cs:
                evalPoints = cs["evalPoints"]
                self._il = evalPoints[0]
                self._ir = evalPoints[1]
            super().__init__(kiloPost, interval, cordinates)
            self.index += 1
            return True

    def hasBothEnd(self):
        '''
        Returns:
            bool : 左岸端・右岸端の測点が指定されている True、指定されていない False
        '''
        return not(self._ir is None or self._ir is None) 

    def Width(self):
        '''
        Returns:
            float or None : 既定の測点属性を有する測点間の横距
        '''
        return super().Width(self._il, self._ir)

    def Zave(self, H = None):
        '''
        Args:
            H (float, optional) : 基準水位
        Returns:
            float or None : 既定の測点属性を有する測点間の平均河床位
        Notes:
            基準水位を省略した場合は上記の測点の標高の何れか低い方
        '''
        return super().Zave(self._il, self._ir, H)
