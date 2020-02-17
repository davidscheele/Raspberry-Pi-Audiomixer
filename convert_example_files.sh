#!/bin/sh

for i in ./sound/calm/bgm/*.mp3; do avconv -i "$i" "${i%.*}.wav"; rm -rf "$i"; done
for i in ./sound/action/bgm/*.mp3; do avconv -i "$i" "${i%.*}.wav"; rm -rf "$i"; done