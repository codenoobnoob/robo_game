from gamemodules import robo
import pygame
import math

# first working copy...

# objective is to collect all coins and get to the finnish "door". Avoid collition with monsters and falling of the obsticles. Default map is very simple. Arrow keys to move and space to kick(Kick action doesn't do anything to the monsters at the moment, you still die if you collide).


# Default map = default: Maps can be created using the following:
# rect = (rect (startpos: int) (surface height from lower end of screen: int) (length: int) (height: int))
# line = (line )
# money = (money kolikko (startpos: int) (surface height from lower end of screen: int))
# monster = (monster hirvio (startpos:int) (surface height from lower end of screen: int))
# monster = (finnish ovi (startpos:int) (surface height from lower end of screen: int))
default = """rect 100 10 500 10
rect 570 80 200 10
rect 800 120 100 10
rect 900 240 300 10
rect 1000 10 200 10
rect 1300 250 200 10
rect 1600 200 20 10
rect 1800 50 700 10
rect 2000 150 200 10
rect 2300 250 200 10
rect 2870 50 20 10
rect 3100 10 600 10
line 200 200 400 60
money kolikko 300 150
money kolikko 350 150
money kolikko 400 150
money kolikko 1100 60
money kolikko 1200 60
money kolikko 1100 350
money kolikko 2000 200
money kolikko 2050 200
money kolikko 2100 200
money kolikko 3500 150
money kolikko 3600 150
monster hirvio 950 240
monster hirvio 2000 50
finnish ovi 3650 10"""


class Obsticles:
    def __init__(self, position):
        self.x_min = position[0]
        self.x_max = position[2]
        self.y_min = position[1]
        self.y_max = position[3]

    def is_at_robo(self, robo: object, steps_x: int):
        if robo.x_min > self.x_max - steps_x or robo.x_max < self.x_min - steps_x:
            return False
        return True

    def is_colition(self, robo: object, steps_x: int, steps_y: int):
        if self.x_min - steps_x <= robo.x_max and self.x_min - steps_x >= robo.x_min or self.x_max - steps_x >= robo.x_min and self.x_max - steps_x <= robo.x_max:
            if robo.y_min + steps_y < self.y_max and robo.y_max + steps_y > self.y_max or robo.y_min + steps_y <= self.y_min and robo.y_max + steps_y > self.y_min:
                if not robo.y_min >= self.y_max:
                    return True
        return False

    def move(self, steps):
        self.x_min -= steps
        self.x_max -= steps

    def is_item_in_view(self, screen_width):
        if self.x_min < screen_width and self.x_max > 0:
            return True
        return False

    def dying(self):
        pass

    def move_y(self):
        pass


class Rectangle(Obsticles):
    def __init__(self, obj_type: str, position=[400, 400, 100, 10], color=(8, 161, 39)):
        super().__init__([
            position[0], position[1]+position[3], position[0]+position[2], position[1]])
        self.type = obj_type
        self.color = color
        self.length = position[2]
        self.height = position[3]


# This class is for creating angled surfaces, NOT READY FOR USE
class Line(Obsticles):
    def __init__(self, obj_type: str, position=[400, 400, 100, 10], color=(8, 161, 39), thickness=3):
        super().__init__(position)
        self.type = obj_type
        self.color = color
        self.angle = self.calc_angle()
        self.thickness = thickness

    def calc_angle(self):
        return math.atan((self.y_max-self.y_min)/(self.x_max-self.x_min))

    def y_at_robo(self, robo, steps_x):
        robo_center = robo.x_max-((robo.x_max-robo.x_min)/2)
        pos_x = robo_center-(self.x_min + steps_x)
        pos_y = round(pos_x*math.tan(self.angle), 1)
        return self.y_min + pos_y

    def is_colition(self, robo: object, steps_x: int, steps_y: int):
        if robo.on_slope:
            return False
        if self.x_min - steps_x <= robo.x_max and self.x_min - steps_x >= robo.x_min and robo.y_min + steps_y < self.y_min and robo.y_max + steps_y > self.y_min and steps_x > 0:
            return True
        if self.x_max - steps_x >= robo.x_min and self.x_max - steps_x <= robo.x_max and robo.y_min + steps_y < self.y_max and robo.y_max + steps_y > self.y_max and steps_x < 0:
            return True
        return False


class Monster(Obsticles):
    def __init__(self, obj_type: str, image: str, position: list, surface: Rectangle):
        self.type = obj_type
        self.image = pygame.image.load(f"images/{image}.png")
        super().__init__([position[0]+5, position[1], position[0] +
                          self.image.get_width()-5, position[1] + self.image.get_height()])
        self.type = obj_type
        self.surface = surface
        self.direction = 2

    def move(self, steps_x):
        if self.x_min < self.surface.x_min and self.direction > 0:
            self.direction = -2
        elif self.x_max > self.surface.x_max and self.direction < 0:
            self.direction = 2

        self.x_min -= (steps_x + self.direction)
        self.x_max -= (steps_x + self.direction)


class Money(Obsticles):
    def __init__(self, obj_type: str, image: str, position: list):
        self.type = obj_type
        self.image = pygame.image.load(f"images/{image}.png")
        super().__init__([position[0], position[1], position[0] +
                          self.image.get_width(), position[1] + self.image.get_height()])


class Finnish(Obsticles):
    def __init__(self, obj_type: str, image: str, position: list):
        self.type = obj_type
        self.image = pygame.image.load(f"images/{image}.png")
        super().__init__([position[0]+5, position[1], position[0] +
                          self.image.get_width()-5, position[1] + self.image.get_height()])


class Robo:
    def __init__(self, image: str, position: list):

        self.image = pygame.image.load(f"images/{image}.png")
        self.x_min = position[0]+5
        self.x_max = position[0]+self.image.get_width()-5
        self.y_max = position[1] + self.image.get_height()
        self.y_min = self.y_max - self.image.get_height()
        self.jump_height = 0
        self.rising = False
        self.falling = False
        self.rotate = False
        self.angle = 0
        self.on_slope = False

    def move_y(self, steps: int, ceiling: int, ground: int):
        self.jump_height += steps

        if self.rising and self.y_max + steps >= ceiling or self.rising and self.jump_height >= 140:

            self.rising = False
            self.falling = True
            self.jump_height -= steps
            return -1
        elif self.falling and self.y_min + steps <= ground or self.on_slope:

            self.falling = False
            self.y_max = ground + self.image.get_height()
            self.y_min = ground
            self.jump_height = 0
            return 0
        else:
            self.y_max += steps
            self.y_min += steps
            return 1

    def jumping(self, y_dir):
        if y_dir > 0:
            if self.jump_height < 80:
                return 8
            elif self.jump_height < 110:
                return 6
            elif self.jump_height < 130:
                return 4
            elif self.jump_height < 160:
                return 2
            else:
                return 0

        elif y_dir < 0:
            if self.jump_height < 80:
                return -8
            elif self.jump_height < 110:
                return -6
            elif self.jump_height < 130:
                return -4
            elif self.jump_height < 160:
                return -2
            else:
                return 0

    def calculate_angle(self, x_dir):
        if self.rotate and x_dir > 0:
            self.angle += 20
            self.angle = min(90, self.angle)
        elif self.rotate and x_dir < 0:
            self.angle -= 20
            self.angle = max(-90, self.angle)
        elif not self.rotate and self.angle > 0 or self.rotate and x_dir == 0:
            self.angle -= 20
            self.angle = max(0, self.angle)
        elif not self.rotate and self.angle < 0 or self.rotate and x_dir == 0:
            self.angle += 20
            self.angle = min(0, self.angle)


class Roborunner:
    def __init__(self):
        pygame.init()
        self.width = 640
        self.height = 480
        self.display = pygame.display.set_mode((self.width, self.height))
        self.font = pygame.font.SysFont("Arial", 16, True)
        self.font_large = pygame.font.SysFont("Arial", 24, True)
        self.clock = pygame.time.Clock()

    def init_game(self):
        self.money_collected = 0
        self.monsters = []
        self.money = []
        self.pressed_keys = []
        self.obsticles = []
        self.read_map(self.choose_level())
        self.robo = Robo("robo", [(self.width/2)-50, 30])
        self.y_dir = 0
        self.x = 0
        self.gameover = False
        self.gamewin = False

    def choose_level(self):
        # here we choose the map to use. If not "default" then must return a .txt file ex: "map1.txt"
        return "default"

    def read_map(self, file: str):
        if file == "default":
            data = default
        else:
            with open(file) as f:
                data = f.read()

        data = data.split("\n")
        data = [i.split(" ") for i in data]
        for line in data:
            if line[0] == "rect":
                self.obsticles.append(Rectangle(line[0], [int(line[1]), int(line[2]), int(
                    line[3]), int(line[4])]))
            elif line[0] == "line":
                self.obsticles.append(Line(line[0], [int(line[1]), int(line[2]), int(
                    line[3]), int(line[4])]))
            elif line[0] == "money":
                self.obsticles.append(Money(line[0], line[1], [int(line[2]), int(
                    line[3])]))
            elif line[0] == "monster":
                for surface in self.obsticles:
                    if surface.x_min < int(line[2]) and surface.x_max > int(line[2]) and surface.y_max == int(line[3]):
                        self.obsticles.append(Monster(line[0], line[1], [int(line[2]), int(
                            line[3])], surface))
            elif line[0] == "finnish":
                self.obsticles.append(Finnish(line[0], line[1], [int(line[2]), int(
                    line[3])]))

    def play(self):
        self.init_game()
        while True:
            if self.game_over() or self.win_game():
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.init_game()
            else:
                self.handle_event()
            self.draw_game()

    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                self.pressed_keys.append(event.key)
                if event.key == pygame.K_SPACE:
                    self.robo.rotate = True
                if event.key == pygame.K_UP:
                    if not self.robo.rising and not self.robo.falling:
                        self.robo.rising = True
                        self.y_dir = 8
            if event.type == pygame.KEYUP:
                if event.key in self.pressed_keys:
                    self.pressed_keys.remove(event.key)
                if event.key == pygame.K_SPACE:
                    self.robo.rotate = False
            if event.type == pygame.QUIT:
                exit()

        # Check pressed keys and update x- direction
        for key in self.pressed_keys:
            if key == 1073741903:
                self.x += 0.1
            elif key == 1073741904:
                self.x -= 0.1
            self.x = min(self.x, 5)
            self.x = max(self.x, -5)

        if self.x > 0 and 1073741903 not in self.pressed_keys:
            self.x -= 0.1
        if self.x < 0 and 1073741904 not in self.pressed_keys:
            self.x += 0.1

        self.ceiling = self.height
        self.ground = -110

        # calc ground and ceiling and check if collition
        for i in self.obsticles:
            if not i.is_item_in_view(self.width):
                next
            if i.type == "rect":
                if i.is_at_robo(self.robo, self.x):
                    if self.robo.y_min >= i.y_max and i.y_max > self.ground:
                        self.ground = i.y_max
                    if self.robo.y_max <= i.y_min and i.y_min < self.ceiling:
                        self.ceiling = i.y_min
            if i.type == "line":
                if i.is_at_robo(self.robo, self.x):
                    y_at_robo = i.y_at_robo(self.robo, self.x)
                    if self.robo.y_min + self.x * math.tan(i.angle) + 2 >= y_at_robo and y_at_robo > self.ground:
                        self.ground = y_at_robo
                    if self.robo.y_max <= y_at_robo and y_at_robo < self.ceiling:
                        self.ceiling = y_at_robo

                    if round(self.robo.y_min + self.x * math.tan(i.angle), 0) + 1 >= round(y_at_robo, 0) and self.x != 0:
                        self.robo.on_slope = True

            if i.is_colition(self.robo, self.x, self.y_dir):
                if i.type == "monster":
                    self.gameover = True
                elif i.type == "money":
                    self.money_collected += 1
                    self.obsticles.remove(i)
                elif i.type == "finnish":
                    self.gamewin = True
                elif i.type == "line":
                    self.x = 0

                else:
                    self.x = 0

        if self.robo.rising or self.robo.falling:
            self.robo.on_slope = False
            self.y_dir = self.robo.jumping(self.y_dir)

        if not self.robo.rising and not self.robo.falling and self.robo.y_min > self.ground:
            self.robo.falling = True
            self.y_dir = -8
            self.robo.on_slope = False

        self.move_all()

    def move_all(self):
        for i in self.obsticles:
            i.move(self.x)

        self.y_dir *= self.robo.move_y(self.y_dir,
                                       self.ceiling, self.ground)

        # Calculate robo "ninja tilt" (space while jumping)
        if self.robo.falling or self.robo.rising:
            if self.robo.rotate or self.robo.angle != 0:
                self.robo.calculate_angle(self.x)
        else:
            self.robo.angle = 0

    def game_over(self):
        if self.robo.y_min < -100:
            self.pressed_keys = []
            return True
        if self.gameover:
            return True
        return False

    def win_game(self):
        if self.gamewin:
            return True
        return False

    def draw_game(self):
        self.display.fill((155, 253, 255))

        # draw obsticles that are in view
        for i in self.obsticles:
            if i.is_item_in_view(self.width):
                if i.type == "rect":
                    pygame.draw.rect(self.display, i.color,
                                     (i.x_min, self.height - i.y_max, i.length, i.height))
                if i.type == "line":
                    pygame.draw.line(self.display, i.color,
                                     (i.x_min, self.height-i.y_min), (i.x_max, self.height-i.y_max), i.thickness)
                if i.type == "money":
                    self.display.blit(
                        i.image, (i.x_min, self.height - i.y_max))
                if i.type == "monster":
                    self.display.blit(
                        i.image, (i.x_min, self.height - i.y_max))
                if i.type == "finnish":
                    self.display.blit(
                        i.image, (i.x_min, self.height - i.y_max))

        # draw roboninja
        self.display.blit(pygame.transform.rotate(
            self.robo.image, self.robo.angle), (self.robo.x_min, self.height-self.robo.y_max))

        # Update points
        text_points = self.font.render(
            f"Bank = {self.money_collected}", True, (0, 40, 172))
        self.display.blit(text_points, (10, 10))

        if self.game_over():
            text_gameover1 = self.font_large.render(
                "Game Over", True, (174, 0, 0))
            self.display.blit(text_gameover1, (self.width/2-text_gameover1.get_width() /
                                               2, self.height/2-text_gameover1.get_height()/2))

            text_gameover2 = self.font.render(
                "Press esc to start over", True, (0, 0, 0))
            self.display.blit(text_gameover2, (self.width/2-text_gameover2.get_width() /
                                               2, self.height/2-text_gameover2.get_height()/2+20))

        if self.win_game():
            text_gameover1 = self.font_large.render(
                "Level Complete", True, (174, 0, 0))
            self.display.blit(text_gameover1, (self.width/2-text_gameover1.get_width() /
                                               2, self.height/2-text_gameover1.get_height()/2))

            text_gameover2 = self.font.render(
                "Press esc to start over", True, (0, 0, 0))
            self.display.blit(text_gameover2, (self.width/2-text_gameover2.get_width() /
                                               2, self.height/2-text_gameover2.get_height()/2+20))

        pygame.display.flip()

        self.clock.tick(60)


if __name__ == "__main__":

    game = Roborunner()
    game.play()
