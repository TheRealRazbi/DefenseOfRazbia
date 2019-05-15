from objects import TowerTile, BaseTile, UnitTile
import pickle
import pygame


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


def create_track(list_of_coordionates, name):
    with open(f'lib/tracks/{name}.txt', 'wb') as f:
        pickle.dump(list_of_coordionates, f)


def load_track(name='default_track', also_print=False):
    with open(f'lib/tracks/{name}.txt', 'rb') as f:
        res = pickle.load(f)
    if also_print:
        print(res)
    return res


def build_base_track(size, screen):
    grid = [
        [
            BaseTile((x, y))
            for x in range(0, size[0], BaseTile.size[0])
        ]
        for y in range(0, size[1], BaseTile.size[1])
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
                UnitTile((x, y))
                for x in range(rectangle[0], rectangle[2], UnitTile.size[0])
            ]
            for y in range(rectangle[1], rectangle[3], UnitTile.size[1])
        ])

    for l1 in grid:
        for l2 in l1:
            for tile in l2:
                top_x, top_y, bottom_x, bottom_y = tile.area

                screen.blit(tile.image, (top_x,
                                         top_y,
                                         bottom_x+top_x,
                                         bottom_y+top_y))
