import json
from shareRiver import guidline

g = guidline("sample.csv")
ds = []
while g.readCrossSection():
    g.hasBothEnd()
    d = {"kiloPost": g.kiloPost, "interval": g.interval,
        "evalPoints": g.evalPoints, "cordinates": g.cordinates}
    ds.append(d)
print("[")
for i, d in enumerate(ds):
    c = "," if i else " "
    print(c, json.dumps(d, ensure_ascii=False))
print("]")
