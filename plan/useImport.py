'''
csv 形式の河川定期横断数値データ（guideline.html 参照）を読み込んで
距離標、追加距離、低水路幅、最深河床位、低水路平均河床位の一覧を取得する

py useImport.py sample.csv | clip を実行して、excel のワークシートにペースト
'''
import os
import sys
from shareRiver import guidline
# shareRiver.py で定義されている guideline クラスを使用
# こうすると...
#   他のプログラムでも流用できる。必要があれば機能を付加する
#   他のユーザーはガイドラインの詳細を知らなくてもクラスの使い方（shareRiver.html）さえ分かれば良い

# from shareRiver import csJson
# JSON から入力する時は csJson クラスを使用すれば良い

def main(fileName):

    g = guidline(fileName)
    # g = csJson(fileName)

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