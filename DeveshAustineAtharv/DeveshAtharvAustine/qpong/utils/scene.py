#
# Copyright 2022 the original author or authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""
A container for managing game screens
"""

import pygame

from qpong.utils.parameters import (
    WIDTH_UNIT,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    QUANTUM_COMPUTER,
    CLASSICAL_COMPUTER,
    EASY,
    NORMAL,
    EXPERT,
)
from qpong.utils.colors import WHITE, BLACK, GRAY
from qpong.utils.font import Font


class Scene:
    """
    Display Game Over screen and handle play again
    """

    def __init__(self):
        super().__init__()

        self.begin = False
        self.restart = False
        self.qubit_num = 3
        self.font = Font()

    def start(self, screen):
        # pylint: disable=too-many-branches disable=too-many-return-statements
        """
        Show start screen
        """

        screen.fill(WHITE)

        gameover_text = "Quantum Composer"
        text = self.font.gameover_font.render(gameover_text, 1, WHITE)
        text_pos = text.get_rect(center=(WINDOW_WIDTH / 2, WIDTH_UNIT * 15))
        screen.blit(text, text_pos)

        gameover_text = "[A] Start"
        text = self.font.replay_font.render(gameover_text, 5, WHITE)
        text_pos = text.get_rect(center=(WINDOW_WIDTH / 2, WIDTH_UNIT * 35))
        screen.blit(text, text_pos)

        self.credits(screen)

        while not self.begin:

            for event in pygame.event.get():
                pygame.event.pump()

                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return False
                    if event.key == pygame.K_a:
                        # start
                        return True

            if self.begin:
                # reset all parameters to restart the game
                #
                # screen.fill(BLACK)
                pass

            pygame.display.flip()

        # reset restart flag when self.restart = True and the while ends
        self.begin = False

    def gameover(self, screen, player):
        """
        Display Game Over screen
        """
        if player == CLASSICAL_COMPUTER:


            gameover_text = "Game Over"
            text = self.font.gameover_font.render(gameover_text, 1, WHITE)
            text_pos = text.get_rect(center=(WINDOW_WIDTH / 2, WIDTH_UNIT * 10))
            screen.blit(text, text_pos)

    def credits(self, screen):
        """
        Show credits screen
        """
        credit_text = "Credits"
        text = self.font.credit_font.render(credit_text, 1, WHITE)
        text_pos = text.get_rect(
            center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT - WIDTH_UNIT * 8)
        )
        screen.blit(text, text_pos)

        credit_text = (
            "Made by Austine, Atharv, and Devesh"
        )
        text = self.font.credit_font.render(credit_text, 1, WHITE)
        text_pos = text.get_rect(
            center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT - WIDTH_UNIT * 5)
        )
        screen.blit(text, text_pos)

    def replay(self, screen, circuit_grid_model, circuit_grid):
        """
        Pause the game and ask if the player wants to play again
        """
        blink_time = pygame.time.get_ticks()

        while not self.restart:

            for event in pygame.event.get():
                pygame.event.pump()

                if event.type == pygame.QUIT:
                    pygame.quit()
                else:
                    self.restart = True

            if self.restart:
                # reset all parameters to restart the game
                circuit_grid_model.reset_circuit()
                circuit_grid.update()
                circuit_grid.reset_cursor()

            # Make blinking text
            if pygame.time.get_ticks() - blink_time > 1000:
                blink_time = pygame.time.get_ticks()
            if pygame.time.get_ticks() - blink_time > 500:
                replay_text = "Press Any Key to Play Again"
                text = self.font.replay_font.render(replay_text, 1, WHITE)
                text_pos = text.get_rect(center=(WINDOW_WIDTH / 2, WIDTH_UNIT * 40))
                screen.blit(text, text_pos)
                pygame.display.flip()
            else:
                # show a black box to blink the text every 0.5s
                pygame.draw.rect(
                    screen,
                    WHITE,
                    (
                        WIDTH_UNIT * 10,
                        WIDTH_UNIT * 35,
                        WIDTH_UNIT * 80,
                        WIDTH_UNIT * 10,
                    ),
                )
                pygame.display.flip()

        # reset restart flag when self.restart = True and the while ends
        self.restart = False
