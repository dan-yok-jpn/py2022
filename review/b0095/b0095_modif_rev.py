'''
大臣管理の河川区域について管区（地方整備局名）と市町村名から都道府県名を割り出す
'''
import csv

def make_dictionaly():

    with open("City.csv") as f:
        next(f)
        dic = {} # 市町村が該当する都道府県
        for cols in csv.reader(f):
            pref = cols[0]
            city = cols[1]
            if city != "":
                try:
                    _ = dic[city] # 既存か否かをテスト
                    dic[city].append(pref)
                except KeyError:
                    dic[city]= [pref] # 同名の市町村があるのでリスト

    return dic

def make_other():

    # https://ja.wikipedia.org/wiki/地方整備局#地方整備局の一覧

    dic = { # 管区を構成する都府県
        "東北": ("青森県","岩手県","宮城県","秋田県","山形県","福島県"),
        "関東": ("茨城県","栃木県","群馬県","埼玉県","千葉県","東京都","神奈川県",
                "山梨県","長野県"),
        "北陸": ("新潟県","富山県","石川県","長野県"),
        "中部": ("岐阜県","静岡県","愛知県","三重県","長野県"),
        "近畿": ("滋賀県","京都府","大阪府","兵庫県","奈良県","和歌山県","福井県"),
        "中国": ("鳥取県","島根県","岡山県","広島県","山口県"),
        "四国": ("香川県","徳島県","愛媛県","高知県"),
        "九州": ("福岡県","佐賀県","長崎県","熊本県","大分県","宮崎県","鹿児島県")
    }
    dic2 = {} # 逆引き（都府県が該当する管区）
    for region in dic.keys():
        prefs = dic[region]
        for pref in prefs:
            try:
                _ =  dic2[pref] # 既存か否かをテスト
                dic2[pref].append(region) # 長野県だけ
            except KeyError:
                dic2[pref] = [region] # 複数の管区に分かれる場合があるのでリスト

    return dic2

def main(input):

    dic1 = make_dictionaly() # 市町村が該当する都道府県群
    dic2 = make_other()      # 都府県が該当する管区群

    with open(input) as f:
        next(f)
        for cols in csv.reader(f):
            if cols[0] == "国":
                theRegion = cols[1] # 特定管区
                if theRegion == "北海道":
                    pref = "北海道"
                else:
                    theCity = cols[4] # 特定市町村
                    prefs = dic1[theCity] # 特定市町村が該当する都道府県群
                    for pref in prefs:
                        regions = dic2[pref] # 候補の都府県が該当する管区群
                        match = False
                        for region in regions:
                            if region == theRegion: # 特定管区と一致
                                match = True
                                break
                        if match:
                            break
                        else:
                            pref = "不明"
                print("\t".join(cols), "\t", pref) # タブ区切りで出力

            else: # 二級水系（探索不要）
                continue

if __name__ == "__main__":

    main("2.H30.07.csv")

# python b0095_modif.py | clip とすると、cntl-v でワークシートにペーストできる