import pandas

df = pandas.read_csv('input.csv', encoding="utf-8",
        index_col="日付", parse_dates=True)

# 前 1 時間雨量
# resample メソッドの label 属性 "right" は指定時刻を期末とする
# 例えば、2022/4/26 8PM の値は 2022/4/26 7PM - 8PM の累積
R1 = df[['A雨量','B雨量','C雨量']].resample("H", label="right").sum()

# 毎正時の流量
# 正時以降の雨は正時の流出に寄与しないから瞬間値の方が合理的
# 観測値のノイズが気になるなら別途の前処理
Q = df[['流入量','流入量2']].asfreq("H")

# csv に出力するのではなくクリップボードに出力して
# ワークシートに貼り付けた方が直で可視化できる
# もしくは df.plot() でプレビュー
pandas.merge(Q, R1, on="日付").to_clipboard() 