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
                value = (value * ratio[0])
            temp.append(float(value))
        new_res.append(temp)

    if also_print:
        print(new_res)

    return new_res


def clicked_in_a_box(hit_box: tuple, click: tuple):
    if hit_box[0] <= click[0] <= hit_box[2] and \
            hit_box[1] <= click[1] <= hit_box[3]:
            return True
    return False


def load_tower_placements(map_name, also_print=False):
    with open(f'lib/tracks/{map_name}/placements.txt', 'rb') as f:
        res = pickle.load(f)

    for group in res:
        if group[0] > group[2]:
            group[2], group[0] = group[0], group[2]
        if group[1] > group[3]:
            group[1], group[3] = group[3], group[1]

        group[2], group[3] = abs(group[2]-group[0]), abs(group[3]-group[1])

    if also_print:
        print(res)
    return res


def create_tower_placement(placements, map_name):
    with open(f"lib/tracks/{map_name}/placements.txt", "wb") as f:
        pickle.dump(placements, f)


def create_wave(wave_number, enemies):
    with open(f"lib/waves/{wave_number}.txt", "wb") as f:
        pickle.dump(enemies, f)


def load_wave(wave_number, also_print=False):
    with open(f"lib/waves/{wave_number}.txt", "rb") as f:
        res = pickle.load(f)

    if also_print:
        print(res)
    return res


def move_towards_an_area(current_pos, destination, speed, move_x=True, move_y=True):
    if move_x:
        for new_pos in range(speed):
            for new_destination in range(speed):
                if current_pos[0]+new_pos == destination[0]+new_destination:
                    return 0, 0

            if current_pos[0] < destination[0]:
                return speed, 0
            else:
                return -speed, 0

    if move_y:
        for new_pos in range(speed):
            for new_destination in range(speed):
                if current_pos[1]+new_pos == destination[1]+new_destination:
                    return 0, 0

        if current_pos[1] < destination[1]:
            return 0, speed
        else:
            return 0, -speed

    return 0, 0





