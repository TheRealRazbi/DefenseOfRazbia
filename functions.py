from objects import TowerTile, BaseTile, UnitTile
import pickle
import pygame


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
                screen.blit(tile.image, (tile.position[0],
                                         tile.position[1],
                                         tile.position[0] + tile.size[0],
                                         tile.position[1] + tile.size[1]))
