'''
大臣管理の河川区域について管区（地方整備局名）と市町村名から都道府県名を割り出す
'''
import csv

with open("City.csv") as f:
    next(f)
    dic1 = {}
    for cols in csv.reader(f):
        pref = cols[0]
        city = cols[1]
        if city != "":
            try:
                test = dic1[city]
                dic1[city].append(pref)
            except:
                dic1[city]= [pref]

# https://ja.wikipedia.org/wiki/地方整備局#地方整備局の一覧
dic2 = {
    "東北": ["青森県","岩手県","宮城県","秋田県","山形県","福島県"],
    "関東": ["茨城県","栃木県","群馬県","埼玉県","千葉県","東京都","神奈川県",
             "山梨県","長野県"],
    "北陸": ["新潟県","富山県","石川県","長野県"],
    "中部": ["岐阜県","静岡県","愛知県","三重県","長野県"],
    "近畿": ["滋賀県","京都府","大阪府","兵庫県","奈良県","和歌山県","福井県"],
    "中国": ["鳥取県","島根県","岡山県","広島県","山口県"],
    "四国": ["香川県","徳島県","愛媛県","高知県"],
    "九州": ["福岡県","佐賀県","長崎県","熊本県","大分県","宮崎県","鹿児島県"]
}
regions = dic2.keys() # ["東北","関東","北陸","中部","近畿","中国","四国","九州"]

with open("2.H30.07.csv") as g:
    next(g)
    for cols in csv.reader(g):
        if cols[0] == "国":
            region = cols[1]
            if region == "北海道":
                pref = region
            else:
                city = cols[4]
                prefs = dic1[city]
                if len(prefs) == 1: # 該当する都府県はひとつ
                    pref = prefs[0]
                else:
                    # 府中市は東京都と広島県にある
                    pref = ""
                    for p in prefs: # 候補の都府県群
                        for r in regions:
                            if p in dic2[r]: # 候補の都府県を含む管区
                                if r == region: # cols[1] の管区と一致
                                    pref += p + " " # 念のため全て候補についてチェック
            print("\t".join(cols), "\t", pref) # タブ区切りで出力

# python b0095_modif.py | clip とすると、cntl-v でワークシートにペーストできる