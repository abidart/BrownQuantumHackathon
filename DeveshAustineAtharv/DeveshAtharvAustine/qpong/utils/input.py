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
Quantum player input events and control
"""

import numpy as np

import pygame

from qpong.utils.navigation import MOVE_UP, MOVE_DOWN, MOVE_LEFT, MOVE_RIGHT


class Input:
    """
    Handle input events
    """

    def __init__(self):
        self.running = True

    def handle_input(self, level, screen, scene):
        # pylint: disable=too-many-branches disable=too-many-statements
        """
        Handle quantum player input
        """

        circuit_grid = level.circuit_grid

        # Handle Input Events
        for event in pygame.event.get():
            pygame.event.pump()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_a:
                    circuit_grid.move_to_adjacent_node(MOVE_LEFT)
                    circuit_grid.draw(screen)
                    pygame.display.flip()
                elif event.key == pygame.K_d:
                    circuit_grid.move_to_adjacent_node(MOVE_RIGHT)
                    circuit_grid.draw(screen)
                    pygame.display.flip()
                elif event.key == pygame.K_w:
                    circuit_grid.move_to_adjacent_node(MOVE_UP)
                    circuit_grid.draw(screen)
                    pygame.display.flip()
                elif event.key == pygame.K_s:
                    circuit_grid.move_to_adjacent_node(MOVE_DOWN)
                    circuit_grid.draw(screen)
                    pygame.display.flip()
                elif event.key == pygame.K_x:
                    circuit_grid.handle_input_x()
                    circuit_grid.draw(screen)
                    pygame.display.flip()
                elif event.key == pygame.K_y:
                    circuit_grid.handle_input_y()
                    circuit_grid.draw(screen)
                    pygame.display.flip()
                elif event.key == pygame.K_z:
                    circuit_grid.handle_input_z()
                    circuit_grid.draw(screen)
                    pygame.display.flip()
                elif event.key == pygame.K_h:
                    circuit_grid.handle_input_h()
                    circuit_grid.draw(screen)
                    pygame.display.flip()
                elif event.key == pygame.K_SPACE:
                    circuit_grid.handle_input_delete()
                    circuit_grid.draw(screen)
                    pygame.display.flip()
                elif event.key == pygame.K_c:
                    # Add or remove a control
                    circuit_grid.handle_input_ctrl()
                    circuit_grid.draw(screen)
                    pygame.display.flip()
                elif event.key == pygame.K_UP:
                    # Move a control qubit up
                    circuit_grid.handle_input_move_ctrl(MOVE_UP)
                    circuit_grid.draw(screen)
                    pygame.display.flip()
                elif event.key == pygame.K_DOWN:
                    # Move a control qubit down
                    circuit_grid.handle_input_move_ctrl(MOVE_DOWN)
                    circuit_grid.draw(screen)
                    pygame.display.flip()
                elif event.key == pygame.K_LEFT:
                    # Rotate a gate
                    circuit_grid.handle_input_rotate(-np.pi / 8)
                    circuit_grid.draw(screen)
                    pygame.display.flip()
                elif event.key == pygame.K_RIGHT:
                    # Rotate a gate
                    circuit_grid.handle_input_rotate(np.pi / 8)
                    circuit_grid.draw(screen)
                    pygame.display.flip()
    @staticmethod
    def move_update_circuit_grid_display(screen, circuit_grid, direction):
        """
        Update circuit grid after move
        """
        circuit_grid.move_to_adjacent_node(direction)
        circuit_grid.draw(screen)
        pygame.display.flip()
