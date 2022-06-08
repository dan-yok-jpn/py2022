'''
河川定期横断数値データ（guideline.html 参照）を読み込んで距離標の一覧を出力（csv モジュールを使用する場合）

# py kp_csvReader.py | more で確認
'''

import csv # csv モジュールの使用宣言

# C:\Users\....\foo> type bar.csv
# 1,2,3,4
# 5,6,7,8
# C:\Users\....\foo> py
# >>> import csv
# >>> f = open("bar.csv")
# >>> reader = csv.reader(f)
# >>> for row in reader:
# ...   print(row)
# ...
# ['1', '2', '3', '4']
# ['5', '6', '7', '8']
# >>> # 入力する行が csv であることが宣言されているので
# >>> # 毎回 split(",") で分解しなくて済む
# >>> 
# >>> row = next(reader)
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
# StopIteration
# >>> # 読込が終了したファイルに対して更に読み込もうとすると
# >>> # 「StopIteration」という名前のエラーが発生する
# >>> f.close()
# >>> # 一旦、閉じる
# >>>
# >>> f = open("bar.csv")
# >>> reader = csv.reader(f)
# >>> row = next(reader)
# >>> row
# ['1', '2', '3', '4']
# >>> print(next(reader))
# ['5', '6', '7', '8']
# >>> exit()
# C:\Users\....\foo>

with open("sample.csv") as f: # 以下の処理が終わったら自動的にファイルを閉じる

    csvReader = csv.reader(f)

    while True:

        try:

            cols = next(csvReader)  # 次の行を読込んで文字列の配列に展開
            kp = cols[0]
            count = int(cols[6])
            flag = cols[11]

            for _ in range(count):
                f.readline() #  展開不要なので単純に読み飛ばし

            if flag != "0":
                f.readline()

            print(kp)

        except: # StopIteration:

            break # 読込済みなら While ループを抜ける
