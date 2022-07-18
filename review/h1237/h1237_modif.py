'''
第 1 カラムが所定の値以下のデータを列挙
'''
import os
import sys
import csv
import datetime

def main(args):

    input    = args[0]
    limit    = float(args[1]) # 変数名として val は抽象的なので
    header_r = int(  args[2]) if len(args) == 3 else 1

    output = ".".join(input.split(".")[:-1]) + \
                f"_{limit}以下.csv" # 出力ファイル名
    fo = open(output, "w")
    # fo = sys.stderr # デバッグする時はこちらを使う

    start = datetime.datetime.now()
    lines = header_r
    with open(input) as f:
        for _ in range(header_r):
            print(next(f)[:-1], file=fo) # 画面でなく fo に出力
        for cols in csv.reader(f): # 列数が一定の場合はこのように書ける
            v = float(cols[0])
            if v <= limit:
                print(",".join(cols), file=fo) # 入力行に復元
                lines += 1
    print()
    print(f" ファイル名 {output}")
    print(f" 行数       {lines}")
    print(f" 処理時間   {datetime.datetime.now() - start}")

    fo.close()

if __name__ == "__main__":

    if len(sys.argv) < 5:
        main(sys.argv[1:])
    else:
        print('''
 使用方法

   python {} csvファイル名 上限値 [ヘッダ行数]''' \
        .format(os.path.basename(__file__)), file=sys.stderr)