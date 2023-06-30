import pygame
import random
from Character import Character
import sys


class NPC(Character):
    def __init__(self, x, y, npc_name, image_path):
        Character.__init__(self, x, y, npc_name, image_path)
        self.cycle = 0
        self.direction = 3

    def random_movement(self):
        if self.direction == 0:
            self.direction = random.choice(
                [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3])  # 0 is right and 1 is left
        elif self.direction == 1:
            self.direction = random.choice([1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3])
        elif self.direction == 3:
            self.direction = random.choice([3, 3, 3, 3, 3, 3, 3, 1, 1, 1, 0, 0, 0])
        else:
            self.direction = random.randint(0, 3)

    def NPC_move(self, direction):
        # Updates position with new values
        if direction == 0:
            self.move("RIGHT")
        if direction == 1:
            self.move("LEFT")
        if direction == 2:
            self.move("JUMP")

    def update(self, screen, tiles, scroll=None):
        Character.update(self, screen, tiles)
        self.cycle += 1
        if self.cycle == 30:
            self.random_movement()
            self.cycle = 0
        self.NPC_move(self.direction)


def test():
    # Test checks functioning of Character class as well as shows how it works
    clock = pygame.time.Clock()
    pygame.init()

    pygame.display.set_caption("TemLand")
    window_size = (1200, 800)
    screen = pygame.display.set_mode(window_size, 0, 32)

    character1 = NPC(50, 50, "Monkey", "images/Mosquit")

    grass_image = pygame.image.load('images/GrassyDirt.png')
    dirt_image = pygame.image.load('images/Dirt.png')
    TILE_SIZE = grass_image.get_width()

    display = pygame.Surface((300, 200))

    game_map = [['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'],
                ['1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1'],
                ['1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1'],
                ['1', '0', '0', '0', '0', '0', '0', '2', '2', '2', '2', '2', '0', '0', '0', '0', '0', '0', '1'],
                ['1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1'],
                ['1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1'],
                ['1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1'],
                ['1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1'],
                ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'],
                ['1', '0', '0', '0', '0', '0', '0', '0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'],
                ['1', '0', '0', '0', '0', '0', '0', '0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'],
                ['1', '0', '0', '0', '0', '0', '0', '0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'],
                ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1']]

    while True:
        display.fill((100, 100, 100))
        tiles = []
        y = 0
        for row in game_map:
            x = 0
            for tile in row:
                if tile == '1':
                    display.blit(dirt_image, (x * TILE_SIZE, y * TILE_SIZE))
                    tiles.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                elif tile == '2':
                    display.blit(grass_image, (x * TILE_SIZE, y * TILE_SIZE))
                    tiles.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                x += 1
            y += 1
        character1.update(display, tiles)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        surf = pygame.transform.scale(display, window_size)
        screen.blit(surf, (0, 0))
        pygame.display.update()
        clock.tick(60)


if __name__ == '__main__':
    test()
