#/bin/sh
cd /home/pi/src/faac-1.28/
./configure --host=arm-unknown-linux-gnueabi
make
sudo make install
sudo ldconfig
sudo reboot
