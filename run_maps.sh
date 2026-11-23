#!/bin/sh
mkdir -p outputs logs
for file in '/data/Twitter dataset/'geoTwitter20-*.zip; do
    name=$(basename "$file")
    nohup python3 ./src/map.py "$file" --output_folder outputs > "logs/$name.log" 2>&1 &
done
