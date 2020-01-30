#!/bin/bash
for i in *.ts
do
    echo "${i%.*}"
    ffmpeg -i "$i" -acodec copy -vcodec copy -f mp4 "${i%.*}.mp4" > /dev/null 2>&1
done