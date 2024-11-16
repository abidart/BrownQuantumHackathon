"""
Quantum version of the classic Pong game
"""

import random

import pygame
from pygame import DOUBLEBUF, HWSURFACE, FULLSCREEN

from qpong.utils.input import Input
from qpong.utils.level import Level
from qpong.utils.scene import Scene
from qpong.viz.statevector_grid import StatevectorGrid
from qpong.utils.parameters import (
    WINDOW_SIZE,
    CLASSICAL_COMPUTER,
    QUANTUM_COMPUTER,
    WIN_SCORE,
    WIDTH_UNIT,
    MEASURE_RIGHT,
)


def main():
    """
    Main game loop
    """

    if not pygame.get_init():
        print("Warning, fonts disabled")
        pygame.init()

    if not pygame.font.get_init():
        print("Warning, fonts disabled")
        pygame.font.init()

    if not pygame.mixer.get_init():
        print("Warning, sound disabled")
        pygame.mixer.init()

    # hardware acceleration to reduce flickering. Works only in full screen
    flags = DOUBLEBUF | HWSURFACE | FULLSCREEN
    screen = pygame.display.set_mode(WINDOW_SIZE, flags)


    # clock for timing
    clock = pygame.time.Clock()
    old_clock = pygame.time.get_ticks()

    # initialize scene, level and input Classes
    scene = Scene()
    level = Level()
    input = Input()

    # update the screen
    pygame.display.flip()

    # Main Loop
    while input.running:
        # set maximum frame rate
        clock.tick(60)
        # refill whole screen with black color at each frame
        screen.fill((0, 0, 0))
        # handle input events
        input.handle_input(level, screen, scene)

    level.statevector_grid.print_statevector(5)
    pygame.quit()


if __name__ == "__main__":
    main()
