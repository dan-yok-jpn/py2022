# class を用いてファイル様式を変換する

今回作ったのは **csExchange.py** と **myClass.py**

## csExchange.py

実行は

```sh
 Exchange the series of cross-section datas

  python csExchange.py [-h] [-from type path [sheet=name] -to type path [sheet=name]]

  type : NK or CTI or IDEA or MLIT or JSON
  path : filename or directory*  *directory allow case in type=MLIT only
  sheet=name : if use Excel workbook

 for example

  python csExchange.py -frrom CTI cti.xlsx sheet=cti -to NK nk.csv

 CAUTION !!!  'openpyxl' must be installed.
```

といった感じでファイル様式が異なる河道横断データの相互変換をひとつのプログラムで可能にする。

ファイル様式を指す **MLIT** は[河川定期縦横断データ](guideline.md)、**JSON** は後述。他は社名の略号

コマンドはいちいちタイプしなくても、 **.vscode/launch.json** にいくつか登録してあるので何れかを選べば **F5** でテストできる。


## myClass.py

**csExchange.py** の肝だけ取り出すと以下のように至ってシンプル。

```Python
from myClass import CrossSections

obj = CrossSections(args[0]) # args[0] は入力ファイルのパス他
obj.export(args[1])          # args[1] は出力ファイルのパス他
```

ここで使っている **CrossSections** クラスが **myClass.py** 内で実装されている
（ただし、現状では **CTI**、**MLIT** と **JSON** しか扱えない...）。

<span style="color: red;"> 腰をすえてコードを読解して頂くしかないが (笑)</span>、
**CrossSections** オブジェクトは **CrossSection** オブジェクトのリスト
**csObjs** を属性にもち、
**CrossSection** オブジェクトは次の辞書を **cs** 属性にもつ
（区間距離は他の測線、つまり他の **CrossSection** オブジェクトに依存するので固有の属性として不適切）。 

```
{
    "name":         距離標 (文字列)
    "distance":     追加距離 (実数)
    "lowerChannel": 低水路肩の左右岸の測点番号の配列
    "levee":        堤防肩の左右岸の測点番号の配列
    "cordinates":   測点座標で二次元の配列
}
```

実際の処理はそれぞれのオブジェクトの子クラス（例えば、
**CTI**、**CTI_**）が担っている。

## JSON

元来、**JSON** は **Javascript** のオブジェクト型変数の記法であるが、
これをファイルにしてデータ交換に用いるのが**世間では標準**になっている
(**csv** のように文字・数字が何を意味するかが分からないのは不便。
**xml** のように冗長なのは辛い)。

実例は [**dst/txt_2.json**](dst/txt_2.json) をご覧頂きたい。

**Python** は標準で **JSON** ファイルの入出力をサポートしている。

以下は **JSON** クラスの定義を抜粋したものである。
このように、ファイルを読込んで初期化する **\_\_init\_\_** 関数、
**JSON** でファイル出力する **export** 関数が僅かこれだけで済む（
他のファイル様式ではあり得ない）。
また誰が書いてもこうなるので非常に分かりやすい。

建設コンサルタントも近代化しないと、なのだが・・・。
せめて当社内だけでも・・・。

```Python
import json

class JSON(CrossSections):

    def import_from(self, src):

        with open(src["file"]) as f:
            js = json.load(f)
        for j in js:
            obj = JSON_()
            obj.cs = j
            self.csObjs.append(obj)

    def export_to(self, dst):

        objs = []
        for obj in self.csObjs:
            objs.append(obj.cs)
        with open(dst["file"], "w") as  f:
            json.dump(objs, f)
```
