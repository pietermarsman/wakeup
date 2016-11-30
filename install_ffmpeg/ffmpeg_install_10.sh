#/bin/sh
cd /home/pi/src
wget -O fdk-aac.tar.gz https://github.com/mstorsjo/fdk-aac/tarball/master 
tar xzvf fdk-aac.tar.gz 
cd mstorsjo-fdk-aac* 
autoreconf -fiv 
./configure --enable-shared 
make -j2 
sudo make install
