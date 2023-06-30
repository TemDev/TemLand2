import os


def reset_game(files):
    for file in files:
        os.remove(file)


def main():
    files = ['game_map.json', 'main_character.json', 'variables.json']
    reset_game(files)


if __name__ == '__main__':
    main()