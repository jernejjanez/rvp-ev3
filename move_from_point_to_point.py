from calc_distances import Coordinates
import sys
def debug_print(*args, **kwargs):
    '''Print debug messages to stderr.
    This shows up in the output panel in VS Code. 
    '''
    print(*args, **kwargs, file=sys.stderr)
class MoveFromPointToPoint:
    def __init__(self, move_straight, rotate, gyro, start):
        self.move_straight = move_straight
        self.rotate = rotate
        self.gyro = gyro
        self.zero_degrees = self.gyro.angle()
        self.current_position = Coordinates([start.x, start.y])
        self.current_orientation = 0

    def get_current_orientation(self):
        if self.current_orientation % 360 == 0:
            return "right"
        if self.current_orientation % 360 == 90:
            return "down"
        if self.current_orientation % 360 == 180:
            return "left"
        if self.current_orientation % 360 == 270:
            return "up"
        
    def from_relative_to_abs_deg(self, degrees):
        current_degrees = self.gyro.angle()
        remaineder = (current_degrees + degrees) % 90
        if remaineder > 45:
            return current_degrees+degrees + (90-remaineder)
        else:
            return current_degrees+degrees - remaineder

    def rotate_to(self, wanted_orientation):
        current_orientation_deg = self.current_orientation % 360
      
        orientation_to_degrees = {"up": 270, "down": 90, "right": 0, "left": 180}
        wanted_orientation_deg = orientation_to_degrees[wanted_orientation]
        rotate_for_deg = (wanted_orientation_deg - current_orientation_deg)
        if rotate_for_deg > 180:
            rotate_for_real = 180 - rotate_for_deg
        elif rotate_for_deg < -180:
            rotate_for_real = -180 - rotate_for_deg
        else:
            rotate_for_real = rotate_for_deg
        rotation_num = self.from_relative_to_abs_deg(rotate_for_real)
        #debug_print(rotation_num,self.gyro.angle(),rotate_for_real)
        self.rotate(rotation_num)
        self.current_orientation = (self.current_orientation + rotate_for_deg) % 360

        

    def __call__(self, move_to_coords):
        orientation = self.get_current_orientation()
        move_in_x = None
        move_in_y = None
        if orientation == "right":
            move_in_x = move_to_coords.x - self.current_position.x
            self.move_straight(move_in_x)
            self.current_position.x += move_in_x

            move_in_y = self.current_position.y - move_to_coords.y
            if move_in_y < 0:
                self.rotate_to("down")
                self.move_straight(abs(move_in_y))
                self.current_position.y += abs(move_in_y)
            elif move_in_y > 0:
                self.rotate_to("up")
                self.move_straight(abs(move_in_y))
                self.current_position.y -= abs(move_in_y)

        elif orientation == "left":
            move_in_x = self.current_position.x - move_to_coords.x
            self.move_straight(move_in_x)
            self.current_position.x -= move_in_x

            move_in_y = self.current_position.y - move_to_coords.y
            if move_in_y < 0:
                self.rotate_to("down")
                self.move_straight(abs(move_in_y))
                self.current_position.y += abs(move_in_y)
            elif move_in_y > 0:
                self.rotate_to("up")
                self.move_straight(abs(move_in_y))
                self.current_position.y -= abs(move_in_y)

        elif orientation == "down":
            move_in_y = move_to_coords.y - self.current_position.y
            self.move_straight(move_in_y)
            self.current_position.y += move_in_y

            move_in_x = self.current_position.x - move_to_coords.x
            if move_in_x < 0:
                self.rotate_to("right")
                self.move_straight(abs(move_in_x))
                self.current_position.x += abs(move_in_x)
            elif move_in_x > 0:
                self.rotate_to("left")
                self.move_straight(abs(move_in_x))
                self.current_position.x -= abs(move_in_x)

        elif orientation == "up":
            move_in_y = self.current_position.y - move_to_coords.y
            self.move_straight(move_in_y)
            self.current_position.y -= move_in_y

            move_in_x = self.current_position.x - move_to_coords.x

            if move_in_x < 0:
                self.rotate_to("right")
                self.move_straight(abs(move_in_x))
                self.current_position.x += abs(move_in_x)
            elif move_in_x > 0:
                self.rotate_to("left")
                self.move_straight(abs(move_in_x))
                self.current_position.x -= abs(move_in_x)
        
        self.rotate_to(self.get_current_orientation())

        return self.current_position, self.current_orientation

        
        
