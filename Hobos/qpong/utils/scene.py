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
import random

from qpong.utils.parameters import (
    WIDTH_UNIT,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    QUANTUM_COMPUTER,
    CLASSICAL_COMPUTER,
    EASY,
    NORMAL,
    EXPERT,
    ANSWER_WIDTH,
    ANSWER_HEIGHT,
    ANSWER_MARGIN_LEFT,
    ANSWER_MARGIN_TOP,
    ANSWER_SPACING_X,
    ANSWER_SPACING_Y,
    QUESTION_HEIGHT,
    QUESTION_MARGIN_LEFT,
    QUESTION_MARGIN_TOP,
    QUESTION_WIDTH,
    Q_AND_A
)
from qpong.utils.colors import WHITE, BLACK, GRAY
from qpong.utils import gamepad
from qpong.utils.font import Font


class Scene:
    """
    Display Game Over screen and handle play again
    """

    def __init__(self):
        super().__init__()

        # get ball screen dimensions
        self.screenheight = round(WINDOW_HEIGHT * 0.7)
        self.screenwidth = WINDOW_WIDTH
        self.width_unit = WIDTH_UNIT

        self.begin = False
        self.restart = False
        self.qubit_num = 3
        self.font = Font()
        self.question_number = 0
        self.answered_correct = 0

    def start(self, screen):
        # pylint: disable=too-many-branches disable=too-many-return-statements
        """
        Show start screen
        """

        screen.fill(BLACK)

        gameover_text = "QPong"
        text = self.font.gameover_font.render(gameover_text, 1, WHITE)
        text_pos = text.get_rect(center=(WINDOW_WIDTH / 2, WIDTH_UNIT * 15))
        screen.blit(text, text_pos)

        gameover_text = "Select difficulty level"
        text = self.font.replay_font.render(gameover_text, 5, WHITE)
        text_pos = text.get_rect(center=(WINDOW_WIDTH / 2, WIDTH_UNIT * 30))
        screen.blit(text, text_pos)

        gameover_text = "[A] Easy  "
        text = self.font.replay_font.render(gameover_text, 5, WHITE)
        text_pos = text.get_rect(center=(WINDOW_WIDTH / 2, WIDTH_UNIT * 35))
        screen.blit(text, text_pos)

        gameover_text = "[B] Normal"
        text = self.font.replay_font.render(gameover_text, 5, WHITE)
        text_pos = text.get_rect(center=(WINDOW_WIDTH / 2, WIDTH_UNIT * 40))
        screen.blit(text, text_pos)

        gameover_text = "[X] Expert"
        text = self.font.replay_font.render(gameover_text, 5, WHITE)
        text_pos = text.get_rect(center=(WINDOW_WIDTH / 2, WIDTH_UNIT * 45))
        screen.blit(text, text_pos)

        self.credits(screen)

        while not self.begin:

            for event in pygame.event.get():
                pygame.event.pump()

                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.JOYBUTTONDOWN:
                    return True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return False
                    return True

            if self.begin:
                # reset all parameters to restart the game
                screen.fill(BLACK)

            pygame.display.flip()

        # reset restart flag when self.restart = True and the while ends
        self.begin = False

    def gameover(self, screen, player):
        """
        Display Game Over screen
        """
        if player == CLASSICAL_COMPUTER:

            screen.fill(BLACK)

            gameover_text = "Game Over"
            text = self.font.gameover_font.render(gameover_text, 1, WHITE)
            text_pos = text.get_rect(center=(WINDOW_WIDTH / 2, WIDTH_UNIT * 10))
            screen.blit(text, text_pos)

            gameover_text = "Classical computer"
            text = self.font.replay_font.render(gameover_text, 5, WHITE)
            text_pos = text.get_rect(center=(WINDOW_WIDTH / 2, WIDTH_UNIT * 22))
            screen.blit(text, text_pos)

            gameover_text = "still rules the world"
            text = self.font.replay_font.render(gameover_text, 5, WHITE)
            text_pos = text.get_rect(center=(WINDOW_WIDTH / 2, WIDTH_UNIT * 27))
            screen.blit(text, text_pos)

            self.credits(screen)

        if player == QUANTUM_COMPUTER:

            screen.fill(BLACK)

            gameover_text = "Congratulations!"
            text = self.font.gameover_font.render(gameover_text, 5, WHITE)
            text_pos = text.get_rect(center=(WINDOW_WIDTH / 2, WIDTH_UNIT * 10))
            screen.blit(text, text_pos)

            gameover_text = "You demonstrated quantum supremacy"
            text = self.font.replay_font.render(gameover_text, 5, WHITE)
            text_pos = text.get_rect(center=(WINDOW_WIDTH / 2, WIDTH_UNIT * 22))
            screen.blit(text, text_pos)

            gameover_text = "for the first time in human history!"
            text = self.font.replay_font.render(gameover_text, 5, WHITE)
            text_pos = text.get_rect(center=(WINDOW_WIDTH / 2, WIDTH_UNIT * 27))
            screen.blit(text, text_pos)

            self.credits(screen)

    @staticmethod
    def dashed_line(screen):
        """
        Show dashed line diving the playing field
        """
        for i in range(10, 0, 2 * WIDTH_UNIT):  # draw dashed line
            pygame.draw.rect(
                screen,
                GRAY,
                (WINDOW_WIDTH // 2 - 5, i, 0.5 * WIDTH_UNIT, WIDTH_UNIT),
                0,
            )


    def questions(self, screen):
        """
        Show question box
        """
        pygame.draw.rect(screen, GRAY, (QUESTION_MARGIN_LEFT, QUESTION_MARGIN_TOP, QUESTION_WIDTH, QUESTION_HEIGHT), width=10)

        text = self.font.player_font.render(Q_AND_A[self.question_number]['Q'], 1, WHITE)
        text_pos = text.get_rect(
            center=(QUESTION_MARGIN_LEFT + QUESTION_WIDTH * 0.5, QUESTION_MARGIN_TOP + QUESTION_HEIGHT * 0.5)
        )
        screen.blit(text, text_pos)


        text = self.font.player_font.render("|0,0>", 1, WHITE)
        text_pos = text.get_rect(
            center=(ANSWER_MARGIN_LEFT * 0.8, ANSWER_MARGIN_TOP + ANSWER_HEIGHT * 0.5)
        )
        screen.blit(text, text_pos)

        text = self.font.player_font.render("|0,1>", 1, WHITE)
        text_pos = text.get_rect(
            center=(ANSWER_MARGIN_LEFT + ANSWER_WIDTH * 2.25 + ANSWER_SPACING_X, ANSWER_MARGIN_TOP + ANSWER_HEIGHT * 0.5)
        )
        screen.blit(text, text_pos)

        text = self.font.player_font.render("|1,0>", 1, WHITE)
        text_pos = text.get_rect(
            center=(ANSWER_MARGIN_LEFT * 0.8, ANSWER_MARGIN_TOP + ANSWER_HEIGHT * 1.5 + ANSWER_SPACING_Y)
        )
        screen.blit(text, text_pos)

        text = self.font.player_font.render("|1,1>", 1, WHITE)
        text_pos = text.get_rect(
            center=(ANSWER_MARGIN_LEFT + ANSWER_WIDTH * 2.25 + ANSWER_SPACING_X, ANSWER_MARGIN_TOP + ANSWER_HEIGHT * 1.5 + ANSWER_SPACING_Y)
        )
        screen.blit(text, text_pos)


    def score(self, screen):
        """
        Show score for both player
        """
        # Print the score
        text = self.font.player_font.render(f"Score: {self.answered_correct}/{self.question_number}", 1, GRAY)
        text_pos = text.get_rect(
            center=(round(WINDOW_WIDTH * 0.25) + WIDTH_UNIT * 4.5, WIDTH_UNIT * 1.5)
        )
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
            "Made by Huang Junye, James Weaver, Jarrod Reilly and Anastasia Jeffery"
        )
        text = self.font.credit_font.render(credit_text, 1, WHITE)
        text_pos = text.get_rect(
            center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT - WIDTH_UNIT * 5)
        )
        screen.blit(text, text_pos)

        credit_text = "Initiated at IBM Qiskit Camp 2019"
        text = self.font.credit_font.render(credit_text, 1, WHITE)
        text_pos = text.get_rect(
            center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT - WIDTH_UNIT * 3)
        )
        screen.blit(text, text_pos)

        credit_text = "Powered by JavaFXpert/quantum-circuit-game"
        text = self.font.credit_font.render(credit_text, 1, WHITE)
        text_pos = text.get_rect(
            center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT - WIDTH_UNIT * 1)
        )
        screen.blit(text, text_pos)

    def replay(self, screen, score, circuit_grid_model, circuit_grid):
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
                score.reset_score()
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
                    BLACK,
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
