import pygame
import math
map1 = [
    [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1,
        0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0,
        1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1,
        0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0,
        1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1,
        0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0,
        1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1,
        0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0,
        1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
        2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1,
     0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0,
        1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]]


class Tile(pygame.sprite.Sprite):
    def __init__(self, image: object, position: tuple, scale: int):
        pygame.sprite.Sprite.__init__(self)
        self.vec = pygame.Vector2()
        self.vec.update((position[0]*16, position[1]*16))
        self.image = image
        self.rect = pygame.Surface.get_rect(self.image)
        self.rect.topleft = self.vec


class Game:
    def __init__(self):
        pygame.init()
        self.scale = 16
        self.width = 640
        self.height = 480
        self.draw_screen = pygame.Surface((self.width, self.height))
        self.display = pygame.display.set_mode(
            (2*self.width, 2*self.height))
        self.clock = pygame.time.Clock()
        self.tiles = pygame.sprite.LayeredUpdates()
        self.image_database = {}
        self.load_images(f"images/tile")
        self.pressed_keys = []
        self.x_dir = 0
        self.position = 0
        self.change_image = 0
        self.read_map(map1)

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
            self.position += self.x_dir*2
            self.change_image += self.x_dir
            self.draw_game()

    def read_map(self, map: list):
        for y_num, y in enumerate(map):
            for x_num, x in enumerate(y):
                self.tiles.add(
                    [Tile(self.image_database["tile"][x], (x_num, y_num), self.scale)], layer=1)

    def load_images(self, path):
        image_name = path.split("/")[-1]
        self.image_database[image_name] = []
        for n in range(3):
            image_id = f"{image_name}_{str(n)}"
            image_path = f"{path}/{image_id}.png"
            image = pygame.image.load(image_path).convert_alpha()
            self.image_database[image_name].append(image)

    def draw_game(self):
        self.display.fill((155, 253, 255))
        self.tiles.draw(self.draw_screen)
        self.display.blit(pygame.transform.scale(
            self.draw_screen, (self.width*2, self.height*2)), (0, 0))
        pygame.display.flip()
        self.clock.tick(60)


if __name__ == "__main__":
    game = Game()
    game.play()
