#!/bin/sh
# Run map.py on every day of 2020 in parallel; each job survives logout via nohup.
mkdir -p outputs logs
for file in '/data/Twitter dataset/'geoTwitter20-*.zip; do
    name=$(basename "$file")
    nohup python3 ./src/map.py "$file" --output_folder outputs > "logs/$name.log" 2>&1 &
done
