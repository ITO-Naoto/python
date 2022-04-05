# グラフ作成
import datetime as mdates
from datetime import datetime
import datetime
import matplotlib
import pandas as pd
import numpy as np
import os
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pytz
import japanize_matplotlib
# csvのパスを探す。
path0 = os.path.dirname(__file__)
path1 = os.path.dirname(path0)
path2 = os.path.join('Data', 'csv', "covid19-tottori.csv")
csvpath = os.path.join(path1, path2)

# csv読み込み
df = pd.read_csv(csvpath, parse_dates=['Date'], header=0)
# グラフ共通設定
t = df['Date'].values
y = df['Sum'].values
DAY = pd.to_timedelta(1, 'day')
t1 = pd.to_datetime('2022-02-01')
t2 = t[-1] + DAY
# グラフをいい感じにする。
locator = mdates.AutoDateLocator()
formatter = mdates.ConciseDateFormatter(locator)
# 現在時刻を取得，dt_nowに格納
dt_now = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
dt_now_str = dt_now.strftime('%Y/%m/%d %H:%M:%S')

# グラフ作成：1/2

# 上の設定を代入
fig, ax = plt.subplots()
ax.xaxis.set_major_locator(locator)
ax.xaxis.set_major_formatter(formatter)
df2 = df.fillna(0)
data0 = df2['Sum']
data1 = df2['東部']
data2 = df2['中部']
data3 = df2['西部']
ax.bar(t, data0, label='総計', width=DAY, align="edge", edgecolor='black')
ax.bar(t, data1, label="東部", width=DAY, align='edge', edgecolor='black')
ax.bar(t, data2, bottom=data1, label="中部", width=DAY, align='edge', edgecolor='black')
ax.bar(t, data3, bottom=data1 + data2, label="西部", width=DAY, align='edge', edgecolor='black')
ax.set_xlim(t1, t2)
ax.set_title("地区ごと感染者数の推移", fontsize=15, loc='left', pad=30)
fig.text(0.9, 0.89, '更新日時: ' + dt_now_str + '(JST)', horizontalalignment='right')
# ax.xlabel("")
# ax.ylabel("感染者数")
ax.legend()
path3 = os.path.join('Data', 'fig', 'graph', "tottori-area.svg")
figpath1 = os.path.join(path1, path3)
fig.savefig(figpath1, bbox_inches="tight")

# グラフ作成:2/2
maxt = df['Sum'].max()
maxt_line = df['Sum'].idxmax()
maxt_date = df.iloc[maxt_line, 0].strftime('%Y/%m/%d')
maxt_str = '最高感染者数:' + str(maxt)+'人'+'（{}）'
maxt_date_print = maxt_str.format(maxt_date)


# グラフを書く。
fig, ax = plt.subplots()
ax.xaxis.set_major_locator(locator)
ax.xaxis.set_major_formatter(formatter)
cmap = plt.get_cmap('tab20c')
# https://github.com/okumuralab/okumuralab.github.io/blob/master/python/code/COVID-tokyo.py の45,46行目を引用。一部変更
# colにcmapをリスト
col = [cmap(0), cmap(0), cmap(0), cmap(0), cmap(0), cmap(2), cmap(2)]
# numpyの配列を作成
cols = np.array([col[pd.Timestamp(i).dayofweek] for i in t])
# ここまで
# https://github.com/okumuralab/okumuralab.github.io/blob/master/python/code/COVID-tokyo.py の51，52行目を引用
ax.bar(t[t >= t1], y[t >= t1], color=cols[t >= t1], width=DAY,
       align='edge', edgecolor="black", linewidth=0.5)
ax.set_xlim(t1, t2)
# ここまで

# グラフへ作成に日時を追加。dt_now_strを代入。(x,y)=(0.9,0.89)の右側へテキスト挿入
fig.text(0.9, 0.89, '更新日時: ' + dt_now_str +'(JST)', horizontalalignment='right')
# 凡例を追加。上部左
ax.legend(['陽性者数'], loc='upper left')
# グラフタイトルを追加。
ax.set_title('鳥取県 コロナウイルス陽性者数の推移\n___'+maxt_date_print, loc='left', pad=30)
# 右側へ今日の感染者のラベルをつける。
ax2 = ax.twinx()
# 位置をｙ軸の最大値
ax2.set_ylim(ax.get_ylim())
ax2.set_yticks([y[-1]])
path4 = os.path.join('Data', 'fig', 'graph', "tottori.svg")
figpath2 = os.path.join(path1, path4)
fig.savefig(figpath2, bbox_inches="tight")
