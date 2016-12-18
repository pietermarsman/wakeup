#!/bin/bash
echo "running"
sudo xvfb-run -ae /dev/stdout ~/other/virtual_envs/py34/bin/python /home/pi/wakeup/view.py
