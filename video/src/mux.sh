#!/bin/bash
# usage: mux.sh <silent.mp4> <audio.wav> <out.mp4>
FF=${FFMPEG:-ffmpeg}
$FF -y -loglevel error -i "$1" -i "$2" -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart "$3"
