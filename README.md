# wakeup
Raspberry pi alarm clock with top40 songs

# Dependencies
 
- python3 (at least, that's what I use) 
- schedule
- Flask
- pygame
- pytube
- beautifulsoup4

```
sudo apt-get install python3-dev python3-numpy python3-pyqt4

pip install schedule Flask pytube beautifulsoup4 lxml pyOpenSSL

hg clone https://bitbucket.org/pygame/pygame 
cd pygame
python setup.py build
python setup.py install

./ffmpeg_install.sh # if you want to compile for the raspberry-pi arm
```
