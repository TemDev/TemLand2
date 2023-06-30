import noise
import csv


def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list


def generate_chunk(x, y, seed=100, chunk_size=8, biome='mountains'):
    chunk_data = []
    height_cons = 100
    for y_pos in range(chunk_size):
        for x_pos in range(chunk_size):
            cord_x = x * chunk_size + x_pos
            cord_y = y * chunk_size + y_pos
            if biome == 'plains':
                grass_height = int(noise.pnoise1(seed + cord_x * 0.1, repeat=9999999) * 10)
                grass_type = 2
            elif biome == 'mountains':
                grass_height = int(noise.pnoise1(seed + cord_x * 0.025, repeat=9999999) * 20)
                grass_type = 2
            elif biome == 'winter':
                grass_height = int(noise.pnoise1(seed + cord_x * 0.1, repeat=9999999) * 10)
                grass_type = 5
            stone_height = int(noise.pnoise1(2 * seed + cord_x * 0.1, repeat=9999999) * 5)
            cave_chance = noise.pnoise2(cord_x * 0.05, cord_y * 0.10, repeatx=9999999999, repeaty=9999999999, octaves=1)
            cloud_chance = noise.pnoise2(cord_x * 0.05, cord_y * 0.15, repeatx=9999999999, repeaty=9999999999, octaves=1)

            if cord_y > height_cons - grass_height and (cave_chance > -0.14):
                tile_type = 1
                if cord_y > height_cons + 5 - stone_height:
                    tile_type = 3
                chunk_data.append([[cord_x, cord_y], tile_type])
            elif cord_y == height_cons - grass_height and (cave_chance > -0.14):
                tile_type = grass_type
                chunk_data.append([[cord_x, cord_y], tile_type])
            elif cord_y < 80 and cloud_chance > 0.49:
                tile_type = 4
                chunk_data.append([[cord_x, cord_y], tile_type])
    return chunk_data


def image_loader(file):
    with open(file) as csv_file:
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
