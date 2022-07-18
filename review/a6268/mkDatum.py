import os
import sys
import glob

filename = "HWL.csv"
dir      = "oudan"

if not os.path.exists(dir):
    sys.exit(f"\n データフォルダ {dir} がありません")

with open(filename, "w") as f:
    print("kp,H", file=f)
    for file in glob.glob(dir + "/WZAA4*.CSV"):
        with open(file) as f:
            kp = float(f.readline().split(",")[0])
            if kp == int(kp): kp = int(kp) # excel にあわせる
            print(f"{kp},", file=f)