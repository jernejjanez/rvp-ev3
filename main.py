#!/usr/bin/env python3
from ev3dev2.sensor.lego import ColorSensor#, GyroSensor
from gyro_correcter import GyroSensor
from ev3dev2.sound import Sound
from ev3dev2.motor import Motor, OUTPUT_B, OUTPUT_C

import time
import json
import os
import sys
import urllib.request

from move_straight import MoveStraight
from rotation import Rotation
from calc_distances import *
from move_from_point_to_point import MoveFromPointToPoint
from color_checker import ColorChecker

def debug_print(*args, **kwargs):
    '''Print debug messages to stderr.
    This shows up in the output panel in VS Code. 
    '''
    print(*args, **kwargs, file=sys.stderr)

def beep(number_of_beeps=1, seconds=1, frequency=1000):
    for i in range(number_of_beeps):
        sound.play_tone(frequency, seconds*1)
        time.sleep(0.5)

def get_locations_url(url):
    res = urllib.request.urlopen(url)
    data = res.read()
    txt = data.decode("utf-8")
    return json.loads(txt)

def get_locations(file='zemljevid.json'):
    # read file
    with open(file, 'r') as data:
        return json.load(data)




if __name__ == "__main__":
    # FIXME!!!!!!: bug učasih pri rotaciji senzor daje da je naredu kot 90 uresnic je pa ene 190
    os.system('setfont Lat15-TerminusBold14')
    debug_print("start")
    
    points = CalcDistances(get_locations_url("http://192.168.0.200:8080/zemljevid.json"))
    #points = CalcDistances(get_locations())

    debug_print(str(points.next_person.coords))
    cl = ColorSensor()
    gyro = GyroSensor()
    sound = Sound()
    l,r = Motor(OUTPUT_B), Motor(OUTPUT_C)

    move_straight = MoveStraight(l,r, gyro)
    rotate = Rotation(l,r, gyro)
    move_to_point = MoveFromPointToPoint(move_straight, rotate, gyro, points.start)
    color_checker = ColorChecker(cl, sound)
    beep(seconds=0.5)
    time.sleep(1)

    move_straight(100)

    #move_straight(-100)
    
    sys,exit(0)

    color_checker()

    while points.next_person:
        point_to_move = points.next_person.coords
        debug_print(point_to_move)
        move_to_point(point_to_move)
        color = color_checker()
        points.check_as_visited()

        if color == "blue" or color == "yellow" or color == "brown": # FIXME: zbris brown
            move_to_point(points.start)
            color = color_checker()
            points.calculate_next(points.start)
        else:
            points.calculate_next(point_to_move)
    move_to_point(points.start)
    color_checker()

    