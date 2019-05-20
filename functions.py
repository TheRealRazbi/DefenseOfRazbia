import objects
import pickle
import pygame


def scale_pos(size: tuple, number: tuple):
    default_size = 800, 600
    if default_size == size:
        return number
    scale = size[0] / default_size[0], size[1] / default_size[1]

    return [a/b for a, b in zip(number, scale)]


def scale_size(size, coordinates, debug=False):
    default_size = 800, 600
    if default_size == size:
        return coordinates
    size_scale = size[0] / default_size[0], size[1] / default_size[1]
    result = []
    if debug:
        print("scale size is", size_scale)
        print(coordinates)
    for _ in coordinates:
        temp = []
        for index, number in enumerate(_):
            if index % 2 == 0:
                number *= size_scale[1]
            elif index % 2 != 0:
                number *= size_scale[0]

            temp.append(int(number))

        result.append(temp)

    if debug:
        print(result)

    return result



def create_path(path, name):
    with open(f"lib/tracks/{name}/path.txt", "wb") as f:
        pickle.dump(path, f)


def load_track(name='default_map'):
    return pygame.image.load(f'lib/tracks/{name}/{name}.png')


def load_path(name='default_map', also_print=False):
    with open(f'lib/tracks/{name}/path.txt', 'rb') as f:
        res = pickle.load(f)
    if also_print:
        print(res)
    return res



def build_base_track(size, screen):
    grid = [
        [
            objects.BaseTile((x, y))
            for x in range(0, size[0], objects.BaseTile.size[0])
        ]
        for y in range(0, size[1], objects.BaseTile.size[1])
    ]

    for tile in grid:
        for actual_tile in tile:

            screen.blit(actual_tile.image, (actual_tile.position[0],
                                            actual_tile.position[1],
                                            actual_tile.position[0]+actual_tile.size[0],
                                            actual_tile.position[1]+actual_tile.size[1]))


def build_unit_track(track, screen):
    grid = []
    for rectangle in track:
        if rectangle[0] > rectangle[2]:
            rectangle[0], rectangle[2] = rectangle[2], rectangle[0]
        if rectangle[1] > rectangle[3]:
            rectangle[1], rectangle[3] = rectangle[3], rectangle[1]

        grid.append([
            [
                objects.UnitTile((x, y))
                for x in range(rectangle[0], rectangle[2], objects.UnitTile.size[0])
            ]
            for y in range(rectangle[1], rectangle[3], objects.UnitTile.size[1])
        ])

    for l1 in grid:
        for l2 in l1:
            for tile in l2:
                top_x, top_y, bottom_x, bottom_y = tile.area

                screen.blit(tile.image, (top_x,
                                         top_y,
                                         bottom_x+top_x,
                                         bottom_y+top_y))
