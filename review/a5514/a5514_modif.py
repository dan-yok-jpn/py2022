import sys
import pandas

def main(csvFile):

    cols = [1] + [i + 2 for i in [1,2]] # 時刻、変動量1 と 変動量2 を抽出
    # 時刻をインデックスとし、datetime 型に変換
    df = pandas.read_csv(csvFile, encoding="shift-jis",
            usecols=cols, index_col="時刻", parse_dates=True)
    df.asfreq("D").to_clipboard() # 0AM のデータを抽出
    # df.asfreq("12H").to_clipboard() # 0AM と 0PM のデータを抽出

if __name__ == "__main__":

    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print('csvファイルが読み込まれていません')
