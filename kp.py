'''
河川定期横断数値データ（myClasses.html 参照）を読み込んで距離標の一覧を出力

py kp.py | more で確認
'''
# sample.csv はガイドライン準拠の csv ファイルを結合したファイル

f = open("sample.csv") # = open("sample.csv", "r") "r" は省略可

while True: # 無条件に以下を繰り返す

    row = f.readline()  # 行の読込

    if row == "":
        break # 空行（ファイルの終端）の場合 While ループを抜ける

    cols = row.split(",") # カンマ区切りで文字列の配列に展開

    # コマンドプロンプトから python を対話モードで起動
    # C:\Users\....\foo> py
    # Python 3.10.2 (tags/v3.10.2:a58ebcc, Jan 17 2022, 14:12:15) [MSC v.1929 64 bit (AMD64)] on win32
    # Type "help", "copyright", "credits" or "license" for more information.
    # >>> s = "a,b,c"
    # >>> # '>>>' 以降はユーザーの入力
    # >>> arr = s.split(",")
    # >>> arr
    # ['a', 'b', 'c']
    # >>> arr[0]
    # 'a'
    # >>> # python の配列の要素番号は 0 始まり
    # >>> exit()
    # C:\Users\....\foo>

    # 基礎データ
    kp = cols[0]         # 距離標（1 カラム目）
    count = int(cols[6]) # 測点数（7 カラム目）
    flag = cols[11]      # 構造物フラグ（12 カラム目）

    # >>> s = "2"
    # >>> i = int(s)
    # >>> i
    # 2
    # >>> f = float(s)
    # >>> f
    # 2.0

    for _ in range(count):  # 測点数回読み飛ばす
        f.readline()

    # >>> r = range(4)
    # >>> r
    # range(0, 4)
    # >>> # r は配列ではなく連番を生成する関数
    # >>> # 第一引数が 0 の場合は省略可能
    # >>> for i in r:
    # ...     print(i)
    # ...
    # 0
    # 1
    # 2
    # 3
    # >>> # for ループを抜ける時は '...' に対してリターンキーをヒット

    if flag != "0": # 構造物データが含まれていたら読み飛ばす
        f.readline()

    print(kp)

f.close() # ファイルを閉じる
