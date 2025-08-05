#!/bin/sh

python3 server.py | sudo ffmpeg -i - -vf "fps=20,eq=brightness=0.1" -vcodec libx264 -movflags faststart -vprofile baseline -level 3.0 -g 150 -s 640x480 -an -flags +loop-global_header -map 0 -bsf h264_mp4toannexb -f segment -segment_format mpegts -segment_time 5 -segment_list /var/www/html/stream/playlist.m3u8 /var/www/html/stream/v%03d.ts
