#/bin/sh
cd /home/pi/src
curl -#LO http://downloads.sourceforge.net/project/faac/faac-src/faac-1.28/faac-1.28.tar.gz
tar xzvf faac-1.28.tar.gz
cd faac-1.28
nano common/mp4v2/mpeg4ip.h
