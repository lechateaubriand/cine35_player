#!/bin/bash

if [ "$AUTO_BA" = 0 ]; then 

#sleep 3 
. /home/poky/my_envs/lecteur_ba/bin/activate 
sleep 1
nohup python /home/pi/my_envs/lecteur_ba/scripts/telecommande.py >/dev/null 2>&1 &
sleep 3
nohup python /home/pi/my_envs/lecteur_ba/scripts/launch_automatic_ba.py >/dev/null 2>&1 &
sleep 3
nohup flask run 2>&1 &

fi
