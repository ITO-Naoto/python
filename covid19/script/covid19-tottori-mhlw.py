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

df = pd.read_csv("https://covid19.mhlw.go.jp/public/opendata/newly_confirmed_cases_daily.csv", usecols=[0, 32], parse_dates=['Date'])

# csvのパスを探す。
path0 = os.path.dirname(__file__)
path1 = os.path.dirname(path0)
# path2 = os.path.join('Data', 'csv', "covid19-tottori.csv")

# グラフ共通設定
t = df['Date'].values
y = df['Tottori'].values
DAY = pd.to_timedelta(1, 'day')
# t0 = pd.to_datetime('2022-02-22')
t1 = pd.to_datetime('2022-06-01')
t2 = t[-1] + DAY

locator = mdates.AutoDateLocator()
formatter = mdates.ConciseDateFormatter(locator)

# 現在時刻を取得，dt_nowに格納
dt_now = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
dt_now_str = dt_now.strftime('%Y/%m/%d %H:%M:%S')
# 総計のプロット
maxt = df['Tottori'].max()
maxt_line = df['Tottori'].idxmax()
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

ax.clear()
ax2.set_yticks([])
ax.xaxis.set_major_locator(locator)
ax.xaxis.set_major_formatter(formatter)

def rt(i, interval):
    if i - 6 - interval < 0:
        return np.nan
    mean1 = y[i-6:i+1].mean()
    mean2 = y[i-6-interval:i+1-interval].mean()
    if mean2 == 0:
        return np.nan
    return (mean1 / mean2) ** (5/interval)

for interval in range(1, 8):
    a = np.array([rt(i, interval) for i in range(len(t))])
    ax.plot(t[t >= t1], a[t >= t1], label=interval)

ax.axhline(1, color='black', linewidth=1, zorder=-1)
ax.set_xlim(t1, t2)
ax.legend()

path5 = os.path.join('Data', 'fig', 'graph', "tottori-rt.svg")
figpath3 = os.path.join(path1, path5)
fig.savefig(figpath3, bbox_inches="tight")
