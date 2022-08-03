### [JSON](https://cloudapi.kddi-web.com/magazine/json-javascript-object-notation) 仕様

|  key  |  型  | 必須 | 繰返 | 値の説明 |
| :-- | :-: | :-: | :-: | :-- |
| title |  文字列  | | | タイトル |
| crossSections | 配列 | 〇 | 〇 | 要素数 : 測線数 |
| &nbsp;&nbsp;name | 文字列 | 〇 | | 距離標 |
| &nbsp;&nbsp;distance | 実数 | 〇 | | 累加距離 (m) |
| &nbsp;&nbsp;cordinates | 配列 | 〇 | 〇 | 要素数 : 節点数 |
| &nbsp;&nbsp;&nbsp;&nbsp;cordinates[i] | 配列 | 〇 | | 要素数 : 2 |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;cordinates[i][0] | 実数 | 〇 | | 水平座標 (m) |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;cordinates[i][1] | 実数 | 〇 | | 鉛直座標 (m) |
| &nbsp;&nbsp;trimAt | 配列 | | | 要素数 : 2 |
| &nbsp;&nbsp;&nbsp;&nbsp;trimAt[0] | 整数 | 〇 | | 左岸堤防肩の節点番号 |
| &nbsp;&nbsp;&nbsp;&nbsp;trimAt[1] | 整数 | 〇 | | 右岸堤防肩の節点番号 |
| &nbsp;&nbsp;lowerChannel | 配列 | | | 要素数 : 2 |
| &nbsp;&nbsp;&nbsp;&nbsp;lowerChannel[0] | 整数 | 〇 | | 低水路左岸肩の節点番号 |
| &nbsp;&nbsp;&nbsp;&nbsp;lowerChannel[1] | 整数 | 〇 | | 低水路右岸肩の節点番号 |
| &nbsp;&nbsp;roughness または | 実数 | | | Manning の粗度係数 |
| &nbsp;&nbsp;roughness | 辞書 | | | |
| &nbsp;&nbsp;&nbsp;&nbsp;changeAt | 配列 | 〇 | 〇 | 要素数 : 変化点数 |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;changeAt[i] | 整数  | 〇 |  | 変化点の節点番号 |
| &nbsp;&nbsp;&nbsp;&nbsp;values | 配列 | 〇 | 〇 | 要素数 : 変化点数 + 1 |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;values[i] | 実数  | 〇 |  | Manning の粗度係数 |
| &nbsp;&nbsp;structure | 辞書 | | | |
| &nbsp;&nbsp;&nbsp;&nbsp;bridge | 辞書 | | | |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;name | 文字列 | 〇 | | 橋梁名 |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;piers | 配列 | 〇 | 〇 | 要素数 : 橋脚数 |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;piers[i] | 辞書 | 〇 | | |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;pos | 実数 | 〇 | | 水平距離 (m)<sup>＃</sup> |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;w | 実数 | 〇 | | 投影幅 (m) |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Cd | 実数 | 〇 | | 抵抗係数<sup>＃</sup> |
| &nbsp;&nbsp;&nbsp;&nbsp;weir | 辞書 | | | 堰<sup>＄</sup> |
| &nbsp;&nbsp;&nbsp;&nbsp;dropwork | 辞書 | | | 落差工<sup>＄</sup>|
| &nbsp;&nbsp;&nbsp;&nbsp;submergedBridge | 辞書 | | | 潜水橋<sup>＄</sup> |

※ 節点番号は 0 始まり</br>
＃ 水位計算用の仮定値なので実態に合わせて確定する必要がある</br>
＄ 説明略

### 例

```json
{
  "title": "sample-data",
  "crossSections": [
    {
      "name": "66.50k",
      "distance": 141.64,
      "cordinates": [
        [-17.63, 88.42],
        [-15.63, 88.42],
          略
        [120.27, 85.94],
        [121.27, 85.94]
      ],
      "roughness": 0.035
    },
    {
      "name": "66.51k",
      "distance": 149.171,
      "lowerChannel": [20, 30],
      "trimAt": [5, 55],
      "cordinates": [
        [-15.75, 86.72],
        [-14.75, 86.72],
          略
        [122.62, 86.08],
        [123.62, 86.08]
      ],
      "roughness": {
        "changeAt": [20, 30],
        "values": [0.035, 0.028, 0.035]
      }
    },
    {
      "name": "66.52k",
        略
    },
      略
    {
      "name": "66.58k",
        略
    }
  ]
}
```