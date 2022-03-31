# パッケージ読み込み
import datetime as mdates
import datetime
import matplotlib as plt
import pandas as pd
import numpy as np
import csv
import os

# csv作成
file = os.path.dirname(__file__)
print(file)
url = 'https://www.pref.tottori.lg.jp/item/1248786.htm#itemid1248786'
data = pd.read_html(url, header=1)
data1 = data[0].head(1)
tottori = data1['鳥取市保健所'].iloc[-1]
kurayosi = data1['倉吉保健所'].iloc[-1]
yonago = data1['米子保健所'].iloc[-1]
sum = data1['当日計'].iloc[-1]
# 日付
dt = datetime.datetime.today()
t_now = dt.date().strftime('%Y/%m/%d')
add = np.array([[t_now,tottori,kurayosi,yonago,sum]]).reshape(1, 5)
df_add = pd.DataFrame(add, columns=['Date','鳥取市保健所','倉吉保健所','米子保健所','Sum'])
#csvを生成
body = [
        [t_now,tottori,kurayosi,yonago,sum], 
       ]
with open(os.path.dirname(__file__)/covid-19-tottori.csv, 'a',encoding='utf-8_sig',newline="") as f:
    writer = csv.writer(f, lineterminator='\n')
    for ary in df_add.values:
        writer.writerow(ary)
f.close()

# グラフを作成
