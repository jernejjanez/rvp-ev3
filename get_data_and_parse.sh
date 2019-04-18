#/bin/bash
sshpass -p "maker" scp -r robot@10.6.4.105:/home/robot/rvp-ev3/debug.log .debug.log;  tac .debug.log| sed -n -e '1,/---start-straight---/p ; /---start-straight---/q' | sed  -e '/---start-straight---/d' | sed -e '/...end-straight.../d' |tac | sed '1s/^/err_path,speed,real_reg,angle_red,real_angle_red,left,right,angle,time_passed,curr_path,rotation_integrl\n /' | sed '$s/$/\nerr_path,speed,real_reg,angle_red,real_angle_red,left,right,angle,time_passed,curr_path,rotation_ingtgrl /' | column -s, -t | less

