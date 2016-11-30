#/bin/sh
cd /home/pi/src
git clone --depth 1 https://github.com/FFmpeg/FFmpeg.git ffmpeg
cd ffmpeg
./configure --enable-cross-compile --arch=armel --target-os=linux --enable-gpl --enable-libx264 --enable-nonfree --enable-libfdk-aac --enable-libvpx --enable-libopus --enable-librtmp --enable-libmp3lame
make -j3
sudo make install
