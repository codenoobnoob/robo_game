import pygame
from gamemodules import objects, imageloader, controls, dino_test


class Game:
    def __init__(self):
        pygame.init()
        self.speed = 5
        self.scale = 16
        self.width = 640
        self.height = 480
        # self.draw_screen = pygame.Surface((self.width, self.height))
        self.display = pygame.display.set_mode(
            (2*self.width, 2*self.height))
        self.clock = pygame.time.Clock()
        self.image_database = imageloader.load(__file__)
        self.tile = objects.Static_Object(
            self.image_database["normal"]["tile_2"], (10, 10), self.scale)
        self.objects = pygame.sprite.LayeredUpdates()
        self.objects.add(self.tile, layer=1)
        self.position = 0
        self.change_image = 0
        self.font = pygame.font.SysFont("Arial", 16, True)
        self.controls = controls.Controls(5, 0.3)
        self.player = dino_test.Dino(
            (self.width/2, self.height-100), "dino", self.image_database["dino"], (100, 100))
        self.objects.add(self.player, layer=1)

    def play(self):
        while True:
            self.controls.update(pygame.event.get())

            self.objects.update(self.controls.vec)

            self.draw_game()

    def draw_game(self):
        self.display.fill((155, 253, 255))
        draw_screen = pygame.Surface((self.width, self.height))
        draw_screen.fill((155, 253, 255))
        self.objects.draw((draw_screen))

        self.display.blit(pygame.transform.scale(
            draw_screen, (self.width*2, self.height*2)), (0, 0))
        fps = self.font.render(
            f"FPS = {self.clock.get_fps()}", True, (0, 40, 172))
        self.display.blit(fps, (10, 10))
        pygame.display.flip()
        self.clock.tick(60)


if __name__ == "__main__":
    game = Game()
    game.play()
