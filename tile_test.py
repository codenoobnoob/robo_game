import pygame
from gamemodules import objects, loader, controls, dino_test
from gamemodules.settings import *


class Game:
    def __init__(self):
        pygame.init()
        self.speed = 5
        self.scale = 32
        self.display = pygame.display.set_mode(
            (int(MAGNIFICATION*WIDTH), int(MAGNIFICATION*HEIGHT)))
        self.clock = pygame.time.Clock()
        self.image_database = loader.load_images(__file__)
        self.objects = pygame.sprite.LayeredUpdates()
        self.position = 0
        self.change_image = 0
        self.font = pygame.font.SysFont("Arial", 16, True)
        self.controls = controls.Controls(5, 0.3)
        self.player = dino_test.Dino(
            (WIDTH/2, HEIGHT-100), "dino", self.image_database["dino"], (100, 100))
        self.objects.add(self.player, layer=1)
        self.map = loader.load_map(__file__, "level1", self.image_database)
        self.load_object()
        print(self.image_database["Candy_tiles"].keys())

    def load_object(self):
        for index_y, y in enumerate(self.map):
            for index_x, x in enumerate(y):
                if x in self.image_database["Candy_tiles"].keys():
                    self.objects.add(objects.Static_Object(
                        self.image_database["Candy_tiles"][x], (index_x, index_y), 1, self.scale))
        # print(self.objects.sprites())

    def play(self):
        while True:
            self.controls.update(pygame.event.get())

            self.objects.update(self.controls.vec*SPEED)

            self.draw_game()

    def draw_game(self):
        self.display.fill((155, 253, 255))
        draw_screen = pygame.Surface((WIDTH, HEIGHT))
        draw_screen.fill((155, 253, 255))
        self.objects.draw((draw_screen))

        self.display.blit(pygame.transform.scale(
            draw_screen, (int(MAGNIFICATION*WIDTH), int(MAGNIFICATION*HEIGHT))), (0, 0))
        fps = self.font.render(
            f"FPS = {self.clock.get_fps()}", True, (0, 40, 172))
        self.display.blit(fps, (10, 10))
        pygame.display.flip()
        self.clock.tick(60)


if __name__ == "__main__":
    game = Game()
    game.play()
