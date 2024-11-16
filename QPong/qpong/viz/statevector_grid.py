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
Statevector grid for quantum player
"""

import pygame

from qiskit.quantum_info import Statevector

from qpong.utils.colors import WHITE, BLACK, GRAY
from qpong.utils.parameters import (
    WIDTH_UNIT,
    ANSWER_MARGIN_LEFT,
    ANSWER_MARGIN_TOP,
    ANSWER_WIDTH,
    ANSWER_HEIGHT,
    ANSWER_SPACING_X,
    ANSWER_SPACING_Y,
    QUESTION_MARGIN_LEFT,
    QUESTION_MARGIN_TOP,
    QUESTION_WIDTH,
    QUESTION_HEIGHT,
    Q_AND_A
)
from qpong.utils.states import comp_basis_states
from qpong.utils.ball import Ball
from qpong.utils.font import Font


class StatevectorGrid(pygame.sprite.Sprite):
    """
    Displays a statevector grid
    """

    def __init__(self, circuit, qubit_num):
        pygame.sprite.Sprite.__init__(self)
        self.image = None
        self.rect = None
        self.ball = Ball()
        self.font = Font()
        self.block_size = int(round(self.ball.screenheight / 2**qubit_num))
        self.basis_states = comp_basis_states(circuit.width())
        self.circuit = circuit
        self.question_number = 0

        self.selection = pygame.Surface([ANSWER_WIDTH, ANSWER_HEIGHT])
        pygame.draw.rect(self.selection, WHITE, (0, 0, ANSWER_WIDTH, ANSWER_HEIGHT), width=10)
        self.selection.convert()

        self.selection_before_measurement(circuit, qubit_num)

    def display_statevector(self, qubit_num):
        """
        Draw computational basis for a statevector of a specified
        number of qubits
        """
        for qb_idx in range(2**qubit_num):
            text = self.font.vector_font.render(
                "|" + self.basis_states[qb_idx] + ">", 1, WHITE
            )
            text_height = text.get_height()
            y_offset = self.block_size * 0.5 - text_height * 0.5
            self.image.blit(text, (2 * WIDTH_UNIT, qb_idx * self.block_size + y_offset))

    def display_questions(self, screen):
        """
        Show question box
        """
        # pygame.draw.rect(screen, GRAY, (0, 0, QUESTION_WIDTH, QUESTION_HEIGHT), width=10)

        # text = self.font.player_font.render(Q_AND_A[6]['Q'], 1, WHITE)
        # text_pos = text.get_rect(
        #     center=(QUESTION_WIDTH * 0.5, QUESTION_MARGIN_TOP + QUESTION_HEIGHT * 0.5)
        # )
        # screen.blit(text, text_pos)

        """
        Show option boxes
        """
        pygame.draw.rect(screen, GRAY, (0, 0, ANSWER_WIDTH, ANSWER_HEIGHT))
        pygame.draw.rect(screen, GRAY, (ANSWER_SPACING_X + ANSWER_WIDTH, 0, ANSWER_WIDTH, ANSWER_HEIGHT))
        pygame.draw.rect(screen, GRAY, (0,  ANSWER_SPACING_Y + ANSWER_HEIGHT, ANSWER_WIDTH, ANSWER_HEIGHT))
        pygame.draw.rect(screen, GRAY, (ANSWER_SPACING_X + ANSWER_WIDTH, ANSWER_SPACING_Y + ANSWER_HEIGHT, ANSWER_WIDTH, ANSWER_HEIGHT))
        """
        Show option text
        """
        for i in range(4):
            text = self.font.player_font.render(Q_AND_A[self.question_number]['A'][i], 1, WHITE)
            x_pos = i % 2
            y_pos = i // 2
            text_pos = text.get_rect(
                center=(ANSWER_WIDTH * 0.5 + (ANSWER_WIDTH + ANSWER_SPACING_X) * x_pos,
                        ANSWER_HEIGHT * 0.5 + (ANSWER_HEIGHT + ANSWER_SPACING_Y) * y_pos)
            )
            screen.blit(text, text_pos)

    def selection_before_measurement(self, circuit, qubit_num):
        """
        Get statevector from circuit, and set the
    .   selection(s) alpha values according to basis
        state(s) probabilitie(s)
        """
        self.update()
        self.display_statevector(qubit_num)
        quantum_state = Statevector(circuit)

        self.image.blit(self.selection, (0, 0))

        self.display_questions(self.image)


        for basis_state, ampl in enumerate(quantum_state):
            self.selection.set_alpha(int(round(abs(ampl) ** 2 * 255)))


            x_coord = basis_state // 2
            y_coord = basis_state % 2

            x_pos = (ANSWER_SPACING_X + ANSWER_WIDTH) * x_coord
            y_pos = (ANSWER_SPACING_Y + ANSWER_HEIGHT) * y_coord

            self.image.blit(self.selection, (x_pos, y_pos))

    def measure_state(self, circuit):
        """
        Measure all qubits on circuit
        """
        measurement_bitstring = Statevector(circuit).sample_memory(1)[0]
        print(measurement_bitstring)
        measurement_int = int(measurement_bitstring, 2)

        return measurement_int

    def update(self):
        """
        Update statevector grid
        """
        self.image = pygame.Surface(
            [ANSWER_WIDTH*2 + ANSWER_SPACING_X, ANSWER_HEIGHT*2 + ANSWER_SPACING_Y]
        )
        self.image.convert()
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
