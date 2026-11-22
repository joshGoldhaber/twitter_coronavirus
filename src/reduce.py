import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input_paths', nargs='+', required=True)
parser.add_argument('--output_path', required=True)
args = parser.parse_args()

import json
from collections import Counter, defaultdict

total = defaultdict(Counter)

for path in args.input_paths:
    with open(path) as f:
        counts = json.load(f)
    for hashtag, inner in counts.items():
        total[hashtag].update(inner)

with open(args.output_path, 'w') as f:
    json.dump(total, f)
