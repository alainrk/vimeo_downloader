#!/bin/bash

echo "Insert name (no spaces): "
read fileName

echo "Insert URL master json: "
read masterJsonURL

echo ${fileName}.mp4
echo ${masterJsonURL}

python video.py ${masterJsonURL} &&
python audio.py ${masterJsonURL} &&
ffmpeg -i video.mp4 -i audio.mp4 -c:v copy -c:a aac -strict experimental ${fileName}.mp4 &&
rm audio.mp4 &&
rm video.mp4

exit 0