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
    return pygame.image.load(f'lib/tracks/{name}/{name}.png').convert()


def load_path(name='default_map', also_print=False, scaling=(800, 600)):
    with open(f'lib/tracks/{name}/path.txt', 'rb') as f:
        res = pickle.load(f)
    ratio = (scaling[0] / 800), (scaling[1] / 600)
    new_res = []
    for paths in res:
        temp = []
        for index, value in enumerate(paths):
            if index % 2:
                value = value * ratio[1]
            else:
                value = value * ratio[0]
            temp.append(float(value))
        new_res.append(temp)

    if also_print:
        print(new_res)


    return new_res



