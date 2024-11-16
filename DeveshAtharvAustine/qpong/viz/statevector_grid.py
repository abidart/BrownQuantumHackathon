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

from qpong.utils.colors import WHITE, BLACK
from qpong.utils.parameters import WIDTH_UNIT
from qpong.utils.states import comp_basis_states
from qpong.utils.font import Font


class StatevectorGrid(pygame.sprite.Sprite):
    """
    Displays a statevector grid
    """

    def __init__(self, circuit, qubit_num):
        pygame.sprite.Sprite.__init__(self)
        self.image = None
        self.rect = None
        self.font = Font()
        self.block_size = int(round(500 / 2**qubit_num))
        self.basis_states = comp_basis_states(circuit.width())
        self.circuit = circuit

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
            
    def print_statevector(self, qubit_num):
        """
        Print computational basis for a statevector of a specified
        number of qubits
        """
        for qb_idx in range(2**qubit_num):
            text = "|" + self.basis_states[qb_idx] + ">", 1, WHITE
            print(text)

    def update(self):
        """
        Update statevector grid
        """
        self.image = pygame.Surface(
            [(self.circuit.width() + 1) * 3 * WIDTH_UNIT, 500]
        )
        self.image.convert()
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
