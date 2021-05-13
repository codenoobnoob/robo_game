import pygame
import math


def robo_init(head_radius: int, body_width: int, body_height: int, dist: int, leg_radius: int, position: tuple, color=(0, 0, 0)):

    class Robo_head(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.gap = leg_radius*2 + dist*2 + body_height+head_radius+10
            self.vector_gap = leg_radius + dist*2 + body_height+head_radius
            self.gap_bottom = leg_radius
            self.y_dir = 0
            self.y_ismoving = False
            self.x = position[0]
            self.y = position[1]
            self.angle = 0
            self.image = pygame.Surface((
                200, 180))
            self.calc_vectors()
            self.draw_head()
            self.rect = self.image.get_rect()
            self.rect.center = (self.x, self.y)

        def draw_head(self):
            self.image = pygame.Surface((200, 180))
            self.image.fill((255, 255, 255))
            self.image.set_colorkey((255, 255, 255))
            pygame.draw.circle(
                self.image, color, (self.vector[1][0], self.vector[1][1]), head_radius)

        def calc_vectors(self):
            hypotenusa = self.vector_gap
            angle1 = 90 - self.angle

            vec_x1 = self.image.get_width()/2
            vec_y1 = self.image.get_height()-self.gap_bottom
            vec_x2 = vec_x1 + (hypotenusa * math.cos(math.radians(angle1)))
            vec_y2 = vec_y1 - (hypotenusa * math.sin(math.radians(angle1)))

            self.vector = [[vec_x1, vec_y1], [vec_x2, vec_y2+self.y_dir]]

        def update(self, x_dir, x: float, y: float, angle: float, rising: bool, falling: bool, jump_height: float, ceiling: float, y_dir: int):

            if y_dir > 0 and jump_height < 80 and not self.y_ismoving:
                self.y_dir -= 3

            elif y_dir > 0 and jump_height > 80 and not self.y_ismoving:
                self.y_dir += 2
            elif jump_height >= 138 and not self.y_ismoving:
                self.y_dir = 0
                self.y_ismoving = True
            # elif y_dir > 0 and jump_height < 130 and self.y_ismoving:
            #     self.y_dir += 12
            elif y_dir < 0 and self.y_dir > -60:
                self.y_dir -= 4
            elif y_dir == 0 and self.y_ismoving and self.y_dir <= 0:
                self.y_dir += 8
            elif y_dir == 0 and self.y_ismoving and self.y_dir < 20:
                self.y_dir += 2
            elif y_dir > 0 and self.y_ismoving:
                self.y_dir = 0
                self.y_ismoving = False
            elif y_dir == 0 and self.y_ismoving and self.y_dir >= 20:
                self.y_dir -= 2
                self.y_ismoving = False
            elif y_dir == 0 and not self.y_ismoving and self.y_dir < 20 and self.y_dir > 0:
                self.y_dir -= 2
                self.y_ismoving = False
            elif y_dir == 0 and not self.y_ismoving and self.y_dir < 0:
                self.y_dir = 0
            if not rising and not falling and not self.y_ismoving and self.y_dir == 0:
                self.y_dir = 0

            self.angle = angle
            self.x = x
            self.y = y
            self.rect.center = (x, y)
            self.calc_vectors()
            self.draw_head()

    class Robo_body(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)

            self.vector_gap = dist+body_height/2+leg_radius
            self.gap_bottom = leg_radius
            self.length = body_width
            self.height = body_height
            self.y_dir = 0
            self.jump_height = 0
            self.y_ismoving = False
            self.x = position[0]
            self.y = position[1]
            self.angle = 0
            self.image = pygame.Surface((
                200, 180))
            self.calc_vectors()
            self.draw_line()
            self.rect = self.image.get_rect()
            self.rect.center = (self.x, self.y)
            self.angle = 0

        def draw_line(self):
            self.image = pygame.Surface((
                200, 180))
            self.image.fill((255, 255, 255))
            self.image.set_colorkey((255, 255, 255))
            pygame.draw.line(self.image, color,
                             (self.vector1[1][0], self.vector1[1][1]), (self.vector2[1][0], self.vector2[1][1]), body_height)

        def calc_vectors(self):
            hypotenusa = math.sqrt(
                (self.length/2)**2+(self.vector_gap)**2)
            angle1 = 90 - self.angle + \
                math.degrees(math.asin((self.length/2)/hypotenusa))
            angle2 = 90 - self.angle - \
                math.degrees(math.asin((self.length/2)/hypotenusa))

            vec1_x1 = self.image.get_width()/2
            vec1_y1 = self.image.get_height()-self.gap_bottom
            vec1_x2 = vec1_x1 + (hypotenusa * math.cos(math.radians(angle1)))
            vec1_y2 = vec1_y1 - (hypotenusa * math.sin(math.radians(angle1)))
            vec2_x2 = vec1_x1 + (hypotenusa * math.cos(math.radians(angle2)))
            vec2_y2 = vec1_y1 - (hypotenusa * math.sin(math.radians(angle2)))
            self.vector1 = [[vec1_x1, vec1_y1],
                            [vec1_x2, vec1_y2 + self.y_dir]]
            self.vector2 = [[vec1_x1, vec1_y1],
                            [vec2_x2, vec2_y2 + self.y_dir]]

        def update(self, x_dir, x: float, y: float, angle: float, rising: bool, falling: bool, jump_height: float, ceiling: float, y_dir: int):
            y_max = jump_height - 140
            if y_dir == 0:
                self.jump_height = 0
            self.jump_height += y_dir
            if y_dir > 0 and not self.y_ismoving and self.jump_height < 100:
                self.y_dir -= 1

            elif y_dir > 0 and not self.y_ismoving and self.jump_height > 100:
                self.y_dir += 1
            elif jump_height >= 138:
                self.y_dir = 0
                self.y_ismoving = True
            elif y_dir < 0 and self.y_dir > -30:
                self.y_dir -= 2
            elif y_dir == 0 and self.y_ismoving and self.y_dir <= 0:
                self.y_dir += 8
            elif y_dir == 0 and self.y_ismoving and self.y_dir < 20:
                self.y_dir += 4
            elif y_dir > 0 and self.y_ismoving and self.y_dir < 100:
                self.y_dir = 0
                self.y_ismoving = False
            elif y_dir == 0 and self.y_ismoving and self.y_dir >= 20:
                self.y_dir -= 3
                self.y_ismoving = False
            elif y_dir == 0 and not self.y_ismoving and self.y_dir < 20 and self.y_dir > 0:
                self.y_dir -= 2
                self.y_ismoving = False
            elif y_dir == 0 and not self.y_ismoving and self.y_dir <= 0:
                self.y_dir = 0
            # if not rising and not falling and not self.y_ismoving and self.y_dir == 0:
            #     self.y_dir = 0

            self.angle = angle
            self.x = x
            self.y = y
            self.calc_vectors()
            self.rect.center = (x, y)
            self.draw_line()

    class Robo_leg(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.gap = (head_radius*2+dist*2+body_height+leg_radius)
            self.x = position[0]
            self.y = position[1]
            self.travel = 0
            self.animation_images = {}
            self.animation_frame = 0
            self.image = pygame.Surface((
                200, 180))
            self.load_animation("images/base")
            self.image.fill((255, 255, 255))
            self.image.set_colorkey((255, 255, 255))
            pygame.draw.circle(self.image, color, (self.image.get_width(
            )/2, self.image.get_height()-leg_radius), leg_radius)
            self.rect = self.image.get_rect()
            self.rect.center = (self.x, self.y)

        def update_image(self):
            self.image.fill((255, 255, 255))
            self.image.set_colorkey((255, 255, 255))
            self.image.blit(
                self.animation_images[f"base_{self.animation_frame}"], (50, 100))

        def update(self, x_dir, x: float, y: float, angle: float, rising: bool, falling: bool, jump_height: float, ceiling: float, y_dir: int):
            if x_dir < 0 and x_dir > self.x:
                self.change_image = 0
            if x_dir > 0 and x_dir < self.x:
                self.change_image = 0
            self.travel += x_dir

            if self.travel >= 4:
                self.animation_frame += 1
                self.travel = 0
            if self.travel <= -4:
                self.animation_frame -= 1
                self.travel = 0
            if self.animation_frame == 18:
                self.animation_frame = 0
            if self.animation_frame == -1:
                self.animation_frame = 17

            self.x = x
            self.y = y
            self.rect.center = (x, y)
            self.update_image()

        def load_animation(self, path):
            animation_name = path.split("/")[-1]
            for n in range(18):
                image_id = f"{animation_name}_{str(n)}"
                image_path = f"{path}/{image_id}.png"
                animation_image = pygame.image.load(image_path).convert_alpha()
                self.animation_images[image_id] = animation_image.copy()

    robo_head = Robo_head()
    robo_body = Robo_body()
    robo_leg = Robo_leg()

    robo_full = pygame.sprite.Group()

    robo_full.add(robo_head, robo_body, robo_leg)

    return robo_full
