#!/bin/bash

if [ "$AUTO_BA" = 0 ]; then 

sleep 3 
. /home/pi/my_envs/cine35_player/bin/activate 
sleep 1
nohup python /home/pi/my_envs/cine35_player/scripts/telecommande.py >/dev/null 2>&1 &
nohup flask run --host=0.0.0.0 2>&1 &

fi
