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
Game level
"""

import pygame

from qpong.model.circuit_grid_model import CircuitGridModel
from qpong.containers.vbox import VBox
from qpong.viz.statevector_grid import StatevectorGrid
from qpong.controls.circuit_grid import CircuitGrid

from qpong.utils.parameters import WIDTH_UNIT, CIRCUIT_DEPTH


class Level:
    """
    Start up a level
    """

    def __init__(self):
        self.level = 3  # game level
        self.win = False  # flag for winning the game
        self.left_paddle = pygame.sprite.Sprite()
        self.right_paddle = pygame.sprite.Sprite()
        self.circuit_grid_model = CircuitGridModel(5, CIRCUIT_DEPTH)
        self.circuit = self.circuit_grid_model.construct_circuit()
        self.circuit_grid = CircuitGrid(0, 500, self.circuit_grid_model)
        self.statevector_grid = StatevectorGrid(self.circuit, 5)
        self.right_statevector = VBox(
            WIDTH_UNIT * 90, WIDTH_UNIT * 0, self.statevector_grid
        )

    def setup(self, scene):
        """
        Setup a level with a certain level number
        """
        scene.qubit_num = self.level
        self.circuit_grid_model = CircuitGridModel(scene.qubit_num, CIRCUIT_DEPTH)

        self.circuit = self.circuit_grid_model.construct_circuit()
        self.statevector_grid = StatevectorGrid(self.circuit, scene.qubit_num)
        self.right_statevector = VBox(
            WIDTH_UNIT * 90, WIDTH_UNIT * 0, self.statevector_grid
        )
        self.circuit_grid = CircuitGrid(0, 500, self.circuit_grid_model)

        # computer paddle

