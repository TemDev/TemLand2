import math
import os
import pygame
import random
import sys
from pygengine import *
import time
import csv
import pickle
import inventorySystem


class Character:
    # Character IDs, incremented at creation of each character
    character_id = 1

    def __init__(self, x, y, name, image):
        # Character name
        self.name = name
        self.char_id = self.character_id
        self.inventory = inventorySystem.Inventory()
        Character.character_id += 1

        # Character images + animation
        self.animation_walk_count = 4
        self.count = 0
        self.image = pygame.image.load('images/' + image + '.png')
        self.right_images = []
        self.right_image_monitor = 0
        self.left_images = []
        self.left_image_monitor = 0
        self.min_width = self.image.get_width()
        self.current_image = self.image
        # tries to load animation images
        try:
            self.jump_image = pygame.image.load('images/' + image + '-jump/' + image + '-jump.png')
            if self.jump_image.get_width() < self.min_width:
                self.min_width = self.jump_image.get_width()
        except (pygame.error, FileNotFoundError):
            self.jump_image = self.image
        try:
            files = []
            for filename in os.listdir('images/' + image + '-right'):
                f = os.path.join('images/' + image + '-right', filename)
                files.append(f)
            files.sort()
            for file in files:
                right_image = pygame.image.load(file)
                self.right_images.append(right_image)
                if right_image.get_width() < self.min_width:
                    self.min_width = right_image.get_width()
            files = []
            for filename in os.listdir('images/' + image + '-left'):
                f = os.path.join('images/' + image + '-left', filename)
                files.append(f)
            files.sort()
            for file in files:
                left_image = pygame.image.load(file)
                self.left_images.append(left_image)
                if left_image.get_width() < self.min_width:
                    self.min_width = left_image.get_width()
        except (pygame.error, FileNotFoundError):
            self.right_images.append(self.image)
            self.left_images.append(self.image)

        self.right_image_max = len(self.right_images) - 1
        self.left_image_max = len(self.left_images) - 1

        # Character conditions
        self.health = 100
        self.hunger = 0

        # Character Air Manipulation
        # jump_speed - is the initial speed of the jumping character, can be changed for different equipment
        # jump_state - whether character is currently in jumping motion
        # flying - whether character can fly
        # current_speed - the current speed of character when in jumping motion
        # original_y - the original y coordinate of character before jump

        self.jump_speed = -4
        self.jump_state = False
        self.flying = False
        self.current_speed = 0

        # Variables indicate whether character is currently moving to the left or right
        self.moving_right = False
        self.moving_left = False

        # Rectangle for collision detection
        self.character_rect = pygame.Rect(x, y, self.image.get_width(), self.image.get_height())
        self.speed_cons = 2
        self.fall_cons = 16
        pass

    def draw(self, screen, tiles, scroll=None, image=None):
        # Function creates rectangle around image and draws object on screen
        if image is None:
            image = self.image
        if scroll is None:
            scroll = [0, 0]
        self.character_rect = pygame.Rect(self.character_rect.x, self.character_rect.y,
                                          self.current_image.get_width(), self.current_image.get_height())

        character_rect = pygame.Rect(self.character_rect.x, self.character_rect.y,
                                     image.get_width(), image.get_height())

        if self.jump_state:
            character_rect.y += 1

        if collision_test(character_rect, tiles):
            difference_x = image.get_width() - self.character_rect.width
            difference_y = image.get_height() - self.character_rect.height
            self.character_rect = pygame.Rect(self.character_rect.x - difference_x,
                                              self.character_rect.y - difference_y,
                                              image.get_width(), image.get_height())

            if collision_test(self.character_rect, tiles):
                image = self.current_image
                self.character_rect = pygame.Rect(self.character_rect.x + difference_x,
                                                  self.character_rect.y + difference_y,
                                                  image.get_width(), image.get_height())
        screen.blit(image, (self.character_rect.x - scroll[0], self.character_rect.y - scroll[1]))
        self.current_image = image

    def move(self, key):
        # Move function enables movement of character depending on the key passed on
        # Keys available: "JUMP", "RIGHT", "LEFT"
        if key == "JUMP":
            # checks if flying is on, if it is on then jump should be disabled as jumping is only
            # allowed when jump_state is False
            if self.flying:
                self.jump_state = False

            if not self.jump_state:
                self.jump_state = True
                self.current_speed = self.jump_speed

        if key == "RIGHT":
            self.moving_right = not self.moving_right
            self.right_image_monitor = 0
            self.count = 0

        if key == "LEFT":
            self.moving_left = not self.moving_left
            self.left_image_monitor = 0
            self.count = 0

    def update(self, screen, tiles, dt, scroll=None):
        # Function updates current x and y coordinates of the character
        # collision types indicates which collisions have occurred - no real practical purpose though
        collision_types = {'top': False, 'right': False, 'bottom': False, 'left': False}
        current_image = None
        self.count += 1

        # Condition statement if moving_right is True
        if self.moving_right:
            if self.count == self.animation_walk_count:
                if self.right_image_monitor < self.right_image_max:
                    self.right_image_monitor += 1
                else:
                    self.right_image_monitor = 0
                self.count = 0
            current_image = self.right_images[self.right_image_monitor]
            self.character_rect.x += round(self.speed_cons * dt)
            hit_list = collision_test(self.character_rect, tiles)
            for tile in hit_list:
                self.character_rect.right = tile.left
                collision_types['right'] = True

        # Condition statement if moving_right is True
        if self.moving_left:
            if self.count == self.animation_walk_count:
                if self.left_image_monitor < self.left_image_max:
                    self.left_image_monitor += 1
                else:
                    self.left_image_monitor = 0
                self.count = 0
            current_image = self.left_images[self.left_image_monitor]
            self.character_rect.x -= round(self.speed_cons * dt)
            hit_list = collision_test(self.character_rect, tiles)
            for tile in hit_list:
                self.character_rect.left = tile.right
                collision_types['left'] = True

        if self.current_speed < self.fall_cons:
            self.current_speed += 0.2 * dt
        else:
            self.current_speed = self.fall_cons
        self.character_rect.y += round(self.current_speed * dt)
        if self.current_speed >= 0:
            self.character_rect.y += 1
        hit_list = collision_test(self.character_rect, tiles)
        if self.current_speed >= 0:
            self.character_rect.y -= 1
        if not hit_list:
            self.jump_state = True
        for tile in hit_list:
            if self.current_speed > 0:
                self.character_rect.bottom = tile.top
                collision_types['bottom'] = True
                self.jump_state = False
            elif self.current_speed < 0:
                self.character_rect.top = tile.bottom
                collision_types['top'] = True
            self.current_speed = 0

        if self.jump_state:
            current_image = self.jump_image

        self.draw(screen, tiles, scroll, image=current_image)

    def damage(self, weapon):
        # Damage dealt on character depends on weapon damage attribute
        self.health -= weapon.damage


class NPC(Character):
    def __init__(self, x, y, npc_name, image_path):
        Character.__init__(self, x, y, npc_name, image_path)
        self.cycle = 0
        self.direction = 'STAND'
        self.update_state = True

    def random_movement(self):
        if self.direction == 'RIGHT':
            self.direction = random.choice(['RIGHT', 'RIGHT', 'RIGHT', 'RIGHT', 'RIGHT', 'RIGHT', 'LEFT', 'LEFT',
                                            'LEFT', 'LEFT', 'STAND', 'STAND', 'STAND', 'STAND', 'STAND', 'STAND',
                                            'STAND', 'STAND', 'STAND', 'STAND', 'STAND', 'STAND', 'STAND', 'STAND',
                                            'STAND'])
        elif self.direction == 'LEFT':
            self.direction = random.choice(['LEFT', 'LEFT', 'LEFT', 'LEFT', 'LEFT', 'LEFT', 'RIGHT', 'RIGHT', 'RIGHT',
                                            'RIGHT', 'STAND', 'STAND', 'STAND', 'STAND', 'STAND', 'STAND', 'STAND',
                                            'STAND', 'STAND', 'STAND', 'STAND', 'STAND', 'STAND', 'STAND', 'STAND'])
        elif self.direction == 'STAND':
            self.direction = random.choice(['STAND', 'STAND', 'STAND', 'STAND', 'STAND', 'STAND', 'STAND', 'LEFT',
                                            'LEFT', 'LEFT', 'RIGHT', 'RIGHT', 'RIGHT'])
        else:
            self.direction = random.choice(['RIGHT', 'LEFT', 'JUMP', 'STAND'])

    def update(self, screen, tiles, dt, scroll=None):
        if self.update_state:
            Character.update(self, screen, tiles, dt, scroll)
            self.cycle += 1
            if self.cycle == 30:
                self.random_movement()
                self.cycle = 0
            self.move(self.direction)
        self.update_state = True


def test():
    # Test checks functioning of Character class as well as shows how it works
    # This could be used when working on the display class
    clock = pygame.time.Clock()
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load('SC-5588.mp3')
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)

    pygame.display.set_caption("Temland")
    window_size = (1200, 800)
    screen = pygame.display.set_mode(window_size, 0, 32)
    all_npc = []
    main_character = Character(0, 400, "Joe", "Skeleton")
    character2 = NPC(0, 400, "Mosq", "Mosquit")
    all_npc.append(character2)
    try:
        with open('main_character.json', 'rb') as main_character_file:
            processed_character = pickle.load(main_character_file)
            main_character.character_rect.x = processed_character[0]
            main_character.character_rect.y = processed_character[1]
            main_character.health = processed_character[2]
    except FileNotFoundError:
        pass

    try:
        with open('game_map.json', 'rb') as game_map_file:
            game_map = pickle.load(game_map_file)
    except FileNotFoundError:
        game_map = {}

    try:
        with open('variables.json', 'rb') as variables_file:
            variables = pickle.load(variables_file)
            true_scroll = variables[0]
    except FileNotFoundError:
        true_scroll = [0, 0]
    '''
    with open('Blocks.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
            else:
                if row[5]:
                    statement = row[3] + " = pygame.image.load('images/" + row[2] + "')"
                    exec(statement, globals())
            line_count += 1
    '''
    dirt_image = pygame.image.load('images/Dirt.png')
    grass_image = pygame.image.load('images/GrassyDirt.png')
    stone_image = pygame.image.load('images/Stone.png')
    cloud_image = pygame.image.load('images/Cloud.png')
    frost_image = pygame.image.load('images/Frost.png')
    tile_index = {1: dirt_image, 2: grass_image, 3: stone_image, 4: cloud_image, 5: frost_image}

    TILE_SIZE = grass_image.get_width()
    # default value 420
    surface_width = 420
    display = pygame.Surface((surface_width, surface_width * 2 / 3))
    chunk_size = 8
    chunk_count = 8
    num_chunks = 5

    half_width = main_character.image.get_width() / 2
    half_height = main_character.image.get_height() / 2

    # generates random seed and fixes the randomness to make recoverable results
    random.seed(2)
    seed = random.randint(1, 1000000)

    frame_rate = 60
    last_time = time.time()

    mouse_down = False
    mining_stage = 0
    mining_limit = None
    mining_block = []
    block_crack = pygame.image.load('images/Block-crack/Block-crack.png')
    block_crack1 = pygame.image.load('images/Block-crack/Block-crack1.png')
    block_crack2 = pygame.image.load('images/Block-crack/Block-crack2.png')
    block_crack3 = pygame.image.load('images/Block-crack/Block-crack3.png')
    block_crack4 = pygame.image.load('images/Block-crack/Block-crack4.png')
    r_mapping = {1: 'plains', 2: 'mountains', 3: 'winter'}
    while True:
        dt = time.time() - last_time
        dt *= frame_rate
        last_time = time.time()
        surf = pygame.transform.scale(display, window_size)
        screen.blit(surf, (0, 0))
        # scroll measures the amount by which the tiles need to be moved to the opposite direction of character movement
        # reason for dividing by 20 is to make is more game-like
        # true scroll contains decimals as well
        true_scroll[0] += ((main_character.character_rect.x - true_scroll[0] - (surface_width / 2 - half_width)) / 20) * dt
        true_scroll[1] += ((main_character.character_rect.y - true_scroll[1] - (surface_width / 3 - half_height)) / 20) * dt
        scroll = [round(true_scroll[0]), round(true_scroll[1])]
        # fills display a certain colour to reset everything
        display.fill((100, 120, 100))

        # stores all tiles on screen
        tiles = []
        # calculates range of chunks that have to be loaded depending on scroll value
        cons_x = -1 + round(scroll[0] / (chunk_size * 16))
        cons_y = -1 + round(scroll[1] / (chunk_size * 16))
        minimal_x = cons_x * 128
        maximal_x = (num_chunks + cons_x) * 128
        minimal_y = cons_y * 128
        maximal_y = (num_chunks + cons_y) * 128
        for y in range(num_chunks):
            for x in range(num_chunks):
                cord_x = x + cons_x
                cord_y = y + cons_y
                target_chunk = str(cord_x) + ';' + str(cord_y)
                if chunk_count == 8:
                    r = random.randint(1, 3)
                    chunk_count = 0
                if target_chunk not in game_map:
                    game_map[target_chunk] = generate_chunk(cord_x, cord_y, seed, chunk_size, r_mapping[r])
                    chunk_count += 1
                for tile in game_map[target_chunk]:
                    x_cor = tile[0][0] * TILE_SIZE
                    y_cor = tile[0][1] * TILE_SIZE
                    # displays all tiles on screen
                    display.blit(tile_index[tile[1]], (x_cor - scroll[0], y_cor - scroll[1]))
                    # adds a rectangle for each tile for collision detection
                    tiles.append(pygame.Rect(x_cor, y_cor, TILE_SIZE, TILE_SIZE))

                    if [x_cor, y_cor] == mining_block:
                        with open('Blocks.csv') as csv_file:
                            csv_reader = csv.reader(csv_file, delimiter=',')
                            for row in csv_reader:
                                if row[0] == str(tile[1]):
                                    mining_limit = row[5]
                                    break
                        # draws correct image of animation
                        if mining_stage == int(mining_limit):
                            game_map[target_chunk].remove(tile)
                        elif mining_stage > int(mining_limit) / 5 * 4:
                            display.blit(block_crack4, (x_cor - scroll[0], y_cor - scroll[1]))
                        elif mining_stage > int(mining_limit) / 5 * 3:
                            display.blit(block_crack3, (x_cor - scroll[0], y_cor - scroll[1]))
                        elif mining_stage > int(mining_limit) / 5 * 2:
                            display.blit(block_crack2, (x_cor - scroll[0], y_cor - scroll[1]))
                        elif mining_stage > int(mining_limit) / 5:
                            display.blit(block_crack1, (x_cor - scroll[0], y_cor - scroll[1]))
                        elif mining_stage > 0:
                            display.blit(block_crack, (x_cor - scroll[0], y_cor - scroll[1]))

        # updates the two characters
        main_character.update(display, tiles, dt, scroll)
        character2.update(display, tiles, dt, scroll)

        for character in all_npc:
            if character.character_rect.x < minimal_x or character.character_rect.x > maximal_x or \
                    character.character_rect.y < minimal_y or character.character_rect.y > maximal_y:
                character.update_state = False

        # events for the main character
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                with open('game_map.json', 'wb') as game_map_file:
                    pickle.dump(game_map, game_map_file)
                with open('variables.json', 'wb') as variables_file:
                    variables = [true_scroll]
                    pickle.dump(variables, variables_file)
                with open('main_character.json', 'wb') as main_character_file:
                    variables = [main_character.character_rect.x, main_character.character_rect.y, main_character.health]
                    pickle.dump(variables, main_character_file)
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    main_character.move("RIGHT")
                if event.key == pygame.K_a:
                    main_character.move("LEFT")
                if event.key == pygame.K_w:
                    main_character.move("JUMP")
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    main_character.move("RIGHT")
                if event.key == pygame.K_a:
                    main_character.move("LEFT")
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_down = True
                elif event.button == 3:
                    mx, my = pygame.mouse.get_pos()
                    mx /= 1200 / surface_width
                    my /= 800 / (surface_width / 3 * 2)
                    mx += scroll[0]
                    my += scroll[1]
                    mouse_rect = pygame.Rect(mx, my, 1, 1)
                    mx = math.floor(mx / TILE_SIZE)
                    my = math.floor(my / TILE_SIZE)
                    block_mouse_rect = pygame.Rect(mx * 16, my * 16, TILE_SIZE, TILE_SIZE)
                    if not collision_test(mouse_rect, tiles) and not collision_test(block_mouse_rect, [main_character.character_rect]):
                        target_chunk = str(math.floor(mx / chunk_size)) + ';' + str(math.floor(my / chunk_size))
                        game_map[target_chunk].append([[mx, my], 1])
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    mining_stage = 0
                    mouse_down = False
        if mouse_down:
            mx, my = pygame.mouse.get_pos()
            # adjust mouse coordinates to screen coordinates
            mx /= 1200 / surface_width
            my /= 800 / (surface_width / 3 * 2)
            mx += scroll[0]
            my += scroll[1]
            # create rect for mouse to detect collisions
            mouse_rect = pygame.Rect(mx, my, 1, 1)
            if hit_list := collision_test(mouse_rect, tiles):
                for tile in hit_list:
                    tile_character = math.sqrt(
                        (tile.x - main_character.character_rect.x - main_character.current_image.get_width()
                         / 2 + TILE_SIZE / 2) ** 2 +
                        (tile.y - main_character.character_rect.y - main_character.current_image.get_height()
                         / 2 + TILE_SIZE / 2) ** 2)
                    if [tile.x, tile.y] != mining_block:
                        mining_block = [tile.x, tile.y]
                        mining_stage = 0
                    if tile_character > 50:
                        mining_stage = 0
            else:
                mining_stage = 0
            mining_stage += 1

        # Scales up surface called display to window size
        pygame.display.update()
        clock.tick(frame_rate)


if __name__ == '__main__':
    test()
