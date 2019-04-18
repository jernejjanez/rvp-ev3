#!/usr/bin/env python3
from ev3dev2.sensor.lego import ColorSensor, GyroSensor
from time import sleep
from ev3dev2.sound import Sound
from ev3dev2.motor import Motor, LargeMotor, OUTPUT_B, OUTPUT_C, MoveTank, MoveSteering
from ev3dev2.motor import SpeedDPS, SpeedRPM, SpeedRPS, SpeedDPM, SpeedPercent
import json
import os
import sys
import urllib.request
from move_straight import MoveStraight


ORIENTATION = ['right', 'down', 'left', 'up']
ORIENTATION_COUNTER = 0

def debug_print(*args, **kwargs):
    '''Print debug messages to stderr.
    This shows up in the output panel in VS Code. 
    '''
    print(*args, **kwargs, file=sys.stderr)

def beep(number_of_beeps=1, seconds=1, frequency=1000):
    for i in range(number_of_beeps):
        sound.play_tone(frequency, seconds*1)
        sleep(0.5)

def get_locations_url(url):
    res = urllib.request.urlopen(url)
    data = res.read()
    txt = data.decode("utf-8")
    return json.load(txt)

def get_locations(file='zemljevid.json'):
    # read file
    with open(file, 'r') as data:
        return json.load(data)

def turn_left_by_degrees(degrees):
    motor_pair.on(steering=-100, speed=5)
    gyro.wait_until_angle_changed_by(degrees)
    motor_pair.off()

def turn_right_by_degrees(degrees):
    motor_pair.on(steering=100, speed=5)
    gyro.wait_until_angle_changed_by(degrees)
    motor_pair.off()

def move_straight(centimeters):
    # 20cm == motor_pair.on_for_seconds(steering=0, speed=40, seconds=1)
    baseline = 20
    time = centimeters / baseline
    motor_pair.on_for_seconds(steering=0, speed=40, seconds=1*time)

def rotate(current_orientation, goal_orientation):
    pass

def move(current_location, next_location):
    x1, y1 = current_location
    x2, y2 = next_location
    global ORIENTATION_COUNTER

    if x2 > x1:
        while ORIENTATION[ORIENTATION_COUNTER%4] != 'right':
            turn_left_by_degrees(90)
            ORIENTATION_COUNTER -= 1
        move_straight(x2-x1)
    elif x1 > x2:
        while ORIENTATION[ORIENTATION_COUNTER%4] != 'left':
            turn_left_by_degrees(90)
            ORIENTATION_COUNTER -= 1
        move_straight(x1-x2)
        while ORIENTATION[ORIENTATION_COUNTER%4] != 'right':
            turn_left_by_degrees(90)
            ORIENTATION_COUNTER -= 1

    if y2 > y1:
        while ORIENTATION[ORIENTATION_COUNTER%4] != 'down':
            turn_left_by_degrees(90)
            ORIENTATION_COUNTER -= 1
        move_straight(y2-y1)
        while ORIENTATION[ORIENTATION_COUNTER%4] != 'right':
            turn_left_by_degrees(90)
            ORIENTATION_COUNTER -= 1
    elif y1 > y2:
        while ORIENTATION[ORIENTATION_COUNTER%4] != 'up':
            turn_left_by_degrees(90)
            ORIENTATION_COUNTER -= 1
        move_straight(y1-y2)
        while ORIENTATION[ORIENTATION_COUNTER%4] != 'right':
            turn_left_by_degrees(90)
            ORIENTATION_COUNTER -= 1





if __name__ == "__main__":
    os.system('setfont Lat15-TerminusBold14')

    # cl = ColorSensor()
    gyro = GyroSensor()
    gyro.mode = GyroSensor.MODE_GYRO_RATE
    gyro.mode = GyroSensor.MODE_GYRO_ANG
    sound = Sound()
    # lm = LargeMotor()
    tank_drive = MoveTank(OUTPUT_B, OUTPUT_C)
    # motor_pair = MoveSteering(OUTPUT_B, OUTPUT_C)
    l,r = Motor(OUTPUT_B), Motor(OUTPUT_C)
    move_straight = MoveStraight(l,r, gyro)
    beep(seconds=0.5)
    sleep(5)
    move_straight(150)

    # # color values
    # black = 1
    # blue = 2
    # yellow = 4
    # red = 5

    # locations = get_locations()
    # start = locations.pop('start')
    # debug_print(locations)
    # debug_print(start)
    # for person, location in sorted(locations.items()):
    #     debug_print(person)
    #     debug_print(location)

    # debug_print(locations['oseba1'])

    # debug_print('Angle:', gyro.angle)

    # move(start, locations['oseba1'])
    # move(locations['oseba1'], start)
    # move(start, locations['oseba2'])

    # motor_pair.on_for_seconds(steering=0, speed=40, seconds=3.5)
    # move_straight(70)
    # motor_pair.on(steering=-100, speed=5)
    # gyro.wait_until_angle_changed_by(45)
    # motor_pair.off()
    # debug_print('Angle:', gyro.angle)

    # while True:
    #     # tank_drive.on_for_rotations(50, 75, 10)
    #     # sleep(1)
    #     # Move robot forward for 3 seconds
    #     debug_print()
    #     motor_pair.on_for_seconds(steering=0, speed=50, seconds=3)


    #     # # Spin robot to the left
    #     # motor_pair.on(steering=-100, speed=5)

    #     # # Wait until angle changed by 90 degrees
    #     # gyro.wait_until_angle_changed_by(90)

    #     # # Stop motors
    #     # motor_pair.off()
    #     if cl.color == black:
    #         text = ColorSensor.COLORS[cl.color]
    #         sound.speak(text)

    #         # beep(seconds=2)
    #         sleep(2)
    #     elif cl.color == blue:
    #         text = ColorSensor.COLORS[cl.color]
    #         sound.speak(text)

    #         # beep()
    #         sleep(2)
    #     elif cl.color == yellow:
    #         text = ColorSensor.COLORS[cl.color]
    #         sound.speak(text)

    #         # beep(number_of_beeps=2)
    #         sleep(2)
    #     elif cl.color == red:
    #         text = ColorSensor.COLORS[cl.color]
    #         sound.speak(text)

    #         # beep(number_of_beeps=3)
    #         sleep(2)
    #     else:
    #         text = ColorSensor.COLORS[cl.color]
    #         sound.speak(text)
    #         sleep(2)
