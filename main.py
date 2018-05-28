from os import listdir
from random import shuffle, randint

import pygame

from entities import Borg, Picard, LEFT, RIGHT, DOWN
from fonts import text_to_screen
from audio import load_song


SU = 50
COLS = 10
ROWS = 18
SCREEN_WIDTH = SU * COLS
SCREEN_HEIGHT = SU * ROWS
COLOR_A = (0, 128, 255)
COLOR_B = (255, 100, 0)
DELAY = 50
# initialize engine
pygame.init()
_icon = pygame.image.load('data/img/steampunk.png')
pygame.display.set_icon(_icon)
pygame.display.set_caption("MachineWerkz")

# set the display size
screen = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT)
)
# get the event loop clock
clock = pygame.time.Clock()
# create the board
board = Borg(cols=COLS, rows=ROWS, square_unit=SU)
# create the piece that falls
piece = Picard(screen=screen, pg=pygame, square_unit=SU,
               shape=randint(0, 6), state=True, board=board,
               colors=[COLOR_A, COLOR_B],
               text_pos=[SCREEN_WIDTH - SU*3, 0],
               text_size=int(SU/4))
PLAYLIST = ['data/audio/{}'.format(_) for _ in listdir('data/audio') if _.endswith('.mp3')]
shuffle(PLAYLIST)
INTRO = PLAYLIST.pop()
SONG_END = load_song(pygame, INTRO)


def run():
    pl = PLAYLIST
    heard = []
    for s in pl:
        pygame.mixer.music.queue(s)
    np = INTRO
    print(np)
    ctr = 0
    done = False
    while not done:
        clock.tick(60)
        if ctr == 0 and piece.game_on:
            piece.fall()
        sleepy = (DELAY - piece.level*5) if (DELAY - piece.level*5) > 10 else 10
        ctr = (ctr + 1) % sleepy
        for event in pygame.event.get():
            if event.type == SONG_END:
                heard.append(np)
                try:
                    np = pl.pop()
                except Exception as e:
                    # eol
                    pl = [str(_) for _ in heard]
                    del heard[:]
                    np = pl.pop()
                load_song(pygame, np)
                print(np)
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and piece.game_on:
                    piece.game_over()
                elif event.key == pygame.K_ESCAPE and not piece.game_on:
                    done = True
                elif event.key == pygame.K_TAB and piece.game_on:
                    piece.set_color()
                if event.key == pygame.K_SPACE and piece.game_on:
                    piece.rotate()
                if event.key == pygame.K_SPACE and not piece.game_on:
                    print("restarting game")
                    board.reset()
                    piece.shape_shift()
                    piece.reset()
                    piece.restart_game()
                if event.key == pygame.K_CAPSLOCK and piece.game_on:
                    piece.shape_shift()
                if event.key == pygame.K_LEFT and piece.game_on:
                    piece.move(LEFT)
                if event.key == pygame.K_RIGHT and piece.game_on:
                    piece.move(RIGHT)
                if event.key == pygame.K_DOWN and piece.game_on:
                    piece.move(DOWN)
                    clock.tick(60)
        screen.fill((0, 0, 0))
        x, y = piece.text_pos
        _ok, msg = piece.draw()
        for t in piece.text_score:
            text_to_screen(pygame, screen, t, x, y, piece.text_size)
            y += 50
        pygame.display.flip()
        if not _ok:
            piece.swap_grid()
            piece.shape_shift()
            piece.reset()


if __name__ == "__main__":
    run()
