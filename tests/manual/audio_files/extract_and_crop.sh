#!/usr/bin/env bash
# Scans all .mp4 files in the current folder and extracts:
#   op_{i}.wav  – first 6 minutes (mono)
#   ed_{i}.wav  – last  6 minutes (mono)

DURATION=360  # 6 minutes in seconds

i=1
for f in *.mp4; do
    [ -e "$f" ] || { echo "No .mp4 files found."; exit 1; }

    echo "Processing [$i]: $f"

    # Opening – first 6 minutes
    ffmpeg -y -i "$f" \
        -ss 0 -t $DURATION \
        -ac 1 -map 0:a:0 \
        "op_${i}.wav"

    # Ending – last 6 minutes
    total=$(ffprobe -v error -show_entries format=duration \
        -of default=noprint_wrappers=1:nokey=1 "$f")
    start=$(echo "$total $DURATION" | awk '{s=$1-$2; if(s<0)s=0; print s}')

    ffmpeg -y -i "$f" \
        -ss "$start" -t $DURATION \
        -ac 1 -map 0:a:0 \
        "ed_${i}.wav"

    i=$((i + 1))
done

echo "Done. Processed $((i - 1)) file(s)."

