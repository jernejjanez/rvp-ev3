#/bin/bash
IP=192.168.0.60

sshpass -p "maker" scp -r robot@$IP:/home/robot/rvp-ev3/debug_rotation.log .debug_rotation.log;  tac .debug_rotation.log| sed -n -e '1,/---start-rotation---/p ; /---start-rotation---/q' | sed  -e '/---start-rotation---/d' | sed -e '/...end-rotation.../d' |tac | sed '1s/^/abs_degrees,deg_current,err,reg,true_reg\n /' | sed '$s/$/\nabs_degrees,deg_current,err,reg,true_reg /' | column -s, -t | less

