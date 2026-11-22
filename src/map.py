import zipfile, json, sys
import itertools
import os
from collections import Counter
from collections import defaultdict

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("filename")
parser.add_argument("--numdp", type=int)
parser.add_argument("--output_folder", default="outputs")
args = parser.parse_args()

# load from file
with open("hashtags") as hf:
    hashtags = [h.strip().lower() for h in hf if h.strip()]

# counters keyed by hashtag first: lang_counter[hashtag][lang]
lang_counter = defaultdict(lambda: Counter())
country_counter = defaultdict(lambda: Counter())

print(f"args.filename={args.filename}")

with zipfile.ZipFile(args.filename) as z:
    for name in z.namelist():
        print('name=', name)
        with z.open(name) as f:
            for i, line in itertools.islice(enumerate(f), args.numdp):
                data = json.loads(line)
                text = data['text'].lower()
                lang = data.get('lang')
                place = data.get('place') or {}
                country = place.get('country_code')
                for hashtag in hashtags:
                    if hashtag in text:
                        lang_counter[hashtag][lang] += 1
                        country_counter[hashtag][country] += 1
                lang_counter['_all'][lang] += 1
                country_counter['_all'][country] += 1


os.makedirs(args.output_folder, exist_ok=True)
output_path_base = os.path.join(args.output_folder, os.path.basename(args.filename))
with open(output_path_base + '.lang', 'w') as f:
    json.dump(lang_counter, f)
with open(output_path_base + '.country', 'w') as f:
    json.dump(country_counter, f)
print(f"wrote {output_path_base}.lang and {output_path_base}.country")
