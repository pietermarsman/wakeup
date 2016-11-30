#/bin/sh
cd /home/pi/src
git clone https://chromium.googlesource.com/webm/libvpx
cd libvpx
git checkout v1.6.0
./configure --target=armv6-linux-gcc
make
sudo checkinstall --pkgname=libvpx --pkgversion="1:$(date +%Y%m%d%H%M)-git" --backup=no     --deldoc=yes --fstrans=no --default
