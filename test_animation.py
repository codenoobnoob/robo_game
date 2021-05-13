import pygame
import math
import os


class Game:
    def __init__(self):
        pygame.init()
        self.width = 640
        self.height = 480
        self.display = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.animation_database = {}
        self.animation_images = {}
        self.animation_frame = 0
        self.action = "base"
        self.animation_database["base"] = self.load_animation(
            f"images/base", [4, 4, 4, 3, 3, 3, 2, 2, 2, 2, 2, 3, 3, 4, 4, 4, 3, 3])
        print(self.animation_images)
        # self.set_roll_speed(0)
        self.pressed_keys = []
        self.x_dir = 0
        self.last_image = self.animation_images['base_0']
        self.position = 0
        self.change_image = 0

    def play(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    self.pressed_keys.append(event.key)
                if event.type == pygame.KEYUP:
                    if event.key in self.pressed_keys:
                        self.pressed_keys.remove(event.key)
                if event.type == pygame.QUIT:
                    exit()

        # Check pressed keys and update x- direction
            for key in self.pressed_keys:
                if key == 1073741903:
                    self.x_dir += 1
                    if self.x_dir < 0:
                        self.change_image = 0
                elif key == 1073741904:
                    self.x_dir -= 1
                    if self.x_dir > 0:
                        self.change_image = 0

            self.x_dir = min(self.x_dir, 4)
            self.x_dir = max(self.x_dir, -4)

            # x_actual = math.ceil(abs(self.x_dir))
            # print(x_actual)
            # if self.x_dir == 0:
            #     self.action = None
            #     # self.animation_frame = 0
            # else:
            #     self.action = "base"
            self.position += self.x_dir*2
            # speed = 3 - x_actual
            self.change_image += self.x_dir
            # self.set_roll_speed(speed)
            self.draw_game()

    # def set_roll_speed(self, speed):
    #     frame_list = [speed for i in range(18)]
    #     self.animation_database["base"] = self.update_animation(
    #         f"images/base", frame_list)

    # def update_animation(self, path, frames):
    #     animation_frames = []
    #     animation_name = path.split("/")[-1]
    #     self.loaded_animation = animation_name
    #     for n, frame in enumerate(frames):
    #         image_id = f"{animation_name}_{str(n)}"
    #         for i in range(frame):
    #             animation_frames.append(image_id)
    #     return animation_frames

    def load_animation(self, path, frames):
        # animation_frames = []
        animation_name = path.split("/")[-1]
        # self.loaded_animation = animation_name
        for n, frame in enumerate(frames):
            image_id = f"{animation_name}_{str(n)}"
            image_path = f"{path}/{image_id}.png"
            animation_image = pygame.image.load(image_path).convert_alpha()
            self.animation_images[image_id] = animation_image.copy()
        #     for i in range(frame):
        #         animation_frames.append(image_id)
        # return animation_frames

    def draw_game(self):
        self.display.fill((155, 253, 255))

        # if self.action == None:
        #     self.display.blit(self.last_image, (
        #         self.width / 2 + self.position, self.height-76))
        if self.action == "base":
            # frame_list = self.animation_database[self.action]
            if self.change_image >= 4:
                self.animation_frame += 1
                self.change_image = 0
            if self.change_image <= -4:
                self.animation_frame -= 1
                self.change_image = 0
            if self.animation_frame == 18:
                self.animation_frame = 0
            if self.animation_frame == -1:
                self.animation_frame = 17

            # if self.x_dir < 0:
            #     self.display.blit(self.animation_images[f"base_{anime}"], (
            #         self.width / 2 + self.position, self.height-76))
            # else:
            self.display.blit(self.animation_images[f"base_{self.animation_frame}"], (
                self.width / 2 + self.position, self.height-76))
            # self.last_image = self.animation_images[f"base_{self.animation_frame}"]
            # self.animation_frame += 1
            # if self.animation_frame == 18:
            #     self.animation_frame = 0
            # print(self.animation_images[frame_list[self.animation_frame]])
        pygame.display.flip()
        self.clock.tick(60)


if __name__ == "__main__":
    game = Game()
    game.play()
