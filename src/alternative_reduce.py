'''
Plot daily usage of hashtags over 2020.

Scans every per-day output of map.py in the outputs folder, builds a
{hashtag: {date: count}} dataset, then draws one line per hashtag.
'''

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('hashtags', nargs='+')
parser.add_argument('--input_folder', default='outputs')
parser.add_argument('--output_path', default='img/hashtags_over_time.png')
args = parser.parse_args()

import os
import re
import json
import datetime
from collections import defaultdict

import logging
logging.getLogger('matplotlib.font_manager').setLevel(logging.ERROR)
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
plt.rcParams['font.family'] = ['DejaVu Sans', 'WenQuanYi Zen Hei']

dataset = defaultdict(dict)
pattern = re.compile(r'geoTwitter(\d\d)-(\d\d)-(\d\d)\.zip\.lang$')
for name in sorted(os.listdir(args.input_folder)):
    m = pattern.search(name)
    if not m:
        continue
    yy, mm, dd = map(int, m.groups())
    day = datetime.date(2000 + yy, mm, dd)
    with open(os.path.join(args.input_folder, name)) as f:
        counts = json.load(f)
    for hashtag in args.hashtags:
        dataset[hashtag][day] = sum(counts.get(hashtag, {}).values())

# plot
fig, ax = plt.subplots(figsize=(12, 6))
for hashtag in args.hashtags:
    days = sorted(dataset[hashtag])
    ax.plot(days, [dataset[hashtag][d] for d in days], label=hashtag, linewidth=1.5)
ax.set_xlabel('Date (2020)')
ax.set_ylabel('Number of tweets per day')
ax.set_title('Daily tweets containing each hashtag in 2020')
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, _: f'{x:,.0f}'))
ax.grid(alpha=0.3)
ax.legend()
fig.tight_layout()
os.makedirs(os.path.dirname(args.output_path) or '.', exist_ok=True)
fig.savefig(args.output_path, dpi=150)
print(f'saved {args.output_path}')
