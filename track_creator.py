from functions import create_track, load_track, save_track
from objects import Game

if __name__ == '__main__':
    track_used = "buffer"
    size = (800, 600)

    create_track([[60, 0, 90, 190], [90, 160, 190, 190], [180, 90, 210, 190],
                  [180, 90, 620, 120], [620, 120, 590, 290], [590, 290, 500, 260],
                  [500, 260, 530, 180], [500, 180, 420, 210], [420, 210, 450, 290],
                  [420, 290, 330, 260], [330, 260, 360, 180], [330, 180, 260, 210],
                  [260, 210, 290, 340], [260, 310, 160, 340], [160, 330, 190, 240],
                  [170, 240, 60, 270], [60, 270, 90, 440], [90, 440, 380, 410],
                  [380, 410, 350, 340], [380, 370, 800, 340], [0, 0, 0, 0]],
                 f"{track_used}")

    unit_track = load_track(also_print=True, name=track_used)

    game = Game(size)
    game.run()
