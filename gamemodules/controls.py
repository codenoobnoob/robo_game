import pygame
import pygame.math

# Next steps implement movement ease or somehow use the camera class to ease the movement (controls class). Also develop the separate movement classes.


class Controls:
    def __init__(self, max_speed: int, movement_ease: float):
        """max_speed: int --> max speed of x-axis movement
        self.vec is the vector that's created by the key presses
        and can be used to move objects. Also has self.(right, left, up, down, space, W, A, S, D, ctrl) that store a boolean to denote if the key is pressed.
        """
        self.ease = movement_ease
        self.__speed = max_speed
        self.vec = pygame.math.Vector2()
        self.vec.update((1, 1))
        self.right = False
        self.left = False
        self.up = False
        self.down = False
        self.space = False
        self.W = False
        self.D = False
        self.S = False
        self.A = False
        self.ctrl = False
        self.__key_dict = {1073741904: self.left, 1073741903: self.right, 1073741906: self.up, 1073741905: self.down,
                           32: self.space, 100: self.D, 97: self.A, 115: self.S, 119: self.W, 1073742049: self.ctrl}
        self.__key_list = []

    def set_direction(self):
        x, y = 0, 0
        for key in self.__key_list:
            if key == 1073741904 or key == 97:
                x = -1
            elif key == 1073741903 or key == 100:
                x = 1
            elif key == 1073741906 or key == 119:
                y = -1
            elif key == 1073741905 or key == 115:
                y = 1

        self.vec.update(x*self.__speed, y*self.__speed)

    def set_speed(self, new_speed: int):
        self.__speed = new_speed

    def update(self, events: object):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in self.__key_dict.keys():
                    self.__key_dict[event.key] = True
                    if event.key not in self.__key_list:
                        self.__key_list.append(event.key)
            if event.type == pygame.KEYUP:
                if event.key in self.__key_dict.keys():
                    self.__key_dict[event.key] = False
                    if event.key in self.__key_list:
                        self.__key_list.remove(event.key)

            if event.type == pygame.QUIT:
                return exit()
        self.set_direction()


class Object_movement():
    def __init__(self, speed: int, movement_ease: float):
        self.speed = speed
        self.ease = movement_ease
        self.vec = Vector2((1, 1))

    def get_vector(self, other: object):
        """takes in a vector and return the vector modified 
        by the movement type"""
        result = other*self.vec
        return result

    def set_vec(self, other: object):
        pass


class Repeat_x(Object_movement):
    def __init__(self, width: int, speed: int, movement_ease: float, start_left=False, start_center=True, start_right=False, start_move_right=True):
        super().__init__(speed, movement_ease)
        self.width = width


class Repeat_y(Object_movement):
    def __init__(self, height: int, speed: int, movement_ease: float, start_high=False, start_center=True, start_low=False, start_move_up=True):
        super().__init__(speed, movement_ease)
        self.height = height


class Follow_player(Object_movement):
    def __init__(self, speed: int, movement_ease: float):
        super().__init__(speed, movement_ease)


class Ease_x(Object_movement):
    def __init__(self, speed: int, movement_ease: float, right=True, left=True):
        super().__init__(speed, movement_ease)


class Ease_y(Object_movement):
    def __init__(self, speed: int, movement_ease: float, up=True, down=True):
        super().__init__(speed, movement_ease)


class Sticky(Object_movement):
    def __init__(self, speed: int, movement_ease: float, sides=(True, False, False, False)):
        """sides = (defaults: top = True, right = False, down = False, left = False)
        """
        super().__init__(speed, movement_ease)
        self.sides = sides
