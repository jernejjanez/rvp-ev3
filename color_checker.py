#!/usr/bin/env python3
import time

def debug_print(*args, **kwargs):
    import sys
    '''Print debug messages to stderr.
    This shows up in the output panel in VS Code. 
    '''
    print(*args, **kwargs, file=sys.stderr)


class Color:
    def __init__(self, color_name, number_of_buzzes):
        self.name = color_name
        self.number_of_buzzes = number_of_buzzes


class ColorChecker:
    def __init__(self, color_sensor, sound):
        self.color_sensor = color_sensor
        self.sound = sound
        
        # TODO: black je treba dt na 0
        self.colors = {1: Color("black",4), 2:Color("blue", 1), 4: Color("yellow", 2), 5: Color("red",3), 7: Color("brown",1)}
    
    def beep(self, number_of_beeps, seconds=1, frequency=1000):
        for i in range(number_of_beeps):
            self.sound.play_tone(frequency, seconds*1)
            time.sleep(0.5)



    def __call__(self):
        sensed_color_num = self.color_sensor.color
        try:            
            current_color = self.colors[sensed_color_num]
            #debug_print(current_color.name)
            if current_color.name == "black":
                self.beep(1,seconds=2)
            else:
                self.beep(current_color.number_of_buzzes)
            return current_color.name
        except Exception as e:
            debug_print(e)
            debug_print("Unknown color index: {}".format(sensed_color_num))