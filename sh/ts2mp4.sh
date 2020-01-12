#!/bin/bash
for i in *.ts;
do ffmpeg -i "$i" -acodec copy -vcodec copy -f mp4 "${i%.*}.mp4"
done