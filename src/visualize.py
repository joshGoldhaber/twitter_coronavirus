#!/usr/bin/env python3

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input_path',required=True)
parser.add_argument('--key',required=True)
parser.add_argument('--percent',action='store_true')
parser.add_argument('--output_path', help='png path (default: derived from input_path and key)')
args = parser.parse_args()

import os
import json
from collections import Counter,defaultdict

import logging
logging.getLogger('matplotlib.font_manager').setLevel(logging.ERROR)
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = ['DejaVu Sans', 'WenQuanYi Zen Hei']

with open(args.input_path) as f:
    counts = json.load(f)

if args.percent:
    for k in counts[args.key]:
        counts[args.key][k] /= counts['_all'][k]

items = sorted(counts[args.key].items(), key=lambda item: (item[1],item[0]), reverse=True)
for k,v in items:
    print(k,':',v)

top = sorted(items[:10], key=lambda item: item[1])
keys = ['unknown' if k == 'null' else k for k, _ in top]
values = [v for _, v in top]

kind = os.path.splitext(args.input_path)[1].lstrip('.')  # 'lang' or 'country'
xlabel = {'lang': 'Language', 'country': 'Country'}.get(kind, 'Key')

fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(keys, values, color='steelblue')
ax.set_xlabel(xlabel)
ax.set_ylabel('Fraction of tweets' if args.percent else 'Number of tweets')
ax.set_title(f'Top 10 {xlabel.lower()} codes for tweets containing {args.key} (2020)')
ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, _: f'{x:,.0f}'))
for i, v in enumerate(values):
    ax.text(i, v, f'{v:,}', ha='center', va='bottom', fontsize=9)
fig.tight_layout()

output_path = args.output_path or f'{os.path.basename(args.input_path)}_{args.key.lstrip("#")}.png'
fig.savefig(output_path, dpi=150)
print(f'saved {output_path}')
