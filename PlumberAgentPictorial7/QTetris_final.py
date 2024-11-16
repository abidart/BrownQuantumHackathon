import pygame
import random
from typing import List, Tuple
from qiskit import QuantumCircuit, QuantumRegister
import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import Statevector, Operator, SparsePauliOp
from qiskit.primitives import StatevectorSampler, PrimitiveJob
from qiskit.circuit.library import TwoLocal
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit.visualization import plot_histogram
from qiskit_ibm_runtime.fake_provider import FakeSherbrooke
from qiskit_ibm_runtime import Session, EstimatorV2 as Estimator
from qiskit_aer import AerSimulator

# Initialize Pygame
pygame.init()

# Constants
BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
SCREEN_WIDTH = BLOCK_SIZE * (GRID_WIDTH + 6)  # Extra space for next piece
SCREEN_HEIGHT = BLOCK_SIZE * GRID_HEIGHT

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)

# Tetrimino shapes
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]],  # J
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]]   # Z
]

COLORS = [CYAN, YELLOW, MAGENTA, ORANGE, BLUE, GREEN, RED]



class Tetris:

    def __init__(self):
        self.qbit_state = [2,2,2]
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Tetris')
        self.clock = pygame.time.Clock()
        
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = self.new_piece()
        self.next_piece = self.new_piece()
        self.game_over = False
        self.score = 0
        
        # Position of the current piece
        self.current_x = GRID_WIDTH // 2 - len(self.current_piece[0]) // 2
        self.current_y = 0
        
        # Game speed
        self.fall_time = 0
        self.fall_speed = 0.5  # Time in seconds between automatic falls
        
    def new_piece(self) -> Tuple[List[List[int]], int]:
        #idx = random.randint(0, len(SHAPES) - 1)
    
        qc=QuantumCircuit(3)
        

        for bit in self.qbit_state:
            if bit == 0: 
                qc.reset(bit) # r -> reset
            elif bit == 1: # x -> x
                qc.reset(bit)
                qc.x(bit)
            elif bit == 2: # h -> h
                qc.reset(bit)
                qc.h(bit)
        
        
        qc.measure_all()
        
        sampler = StatevectorSampler(default_shots=1) 
        pub = qc
        job_sampler = sampler.run([qc])
        result_sampler = job_sampler.result()
        counts_sampler = result_sampler[0].data.meas.get_counts()

        item = list(counts_sampler.keys())[0]
        
        mydict = {'000': 0, '001': 1, '010': 2, '011': 3, '100': 4, '101': 5, '110': 6}

        if item == '111': 
            idx = 6
        else: 
            idx = mydict[item]
        
        return SHAPES[idx], idx

    
    def valid_move(self, piece: List[List[int]], x: int, y: int) -> bool:
        for i in range(len(piece)):
            for j in range(len(piece[0])):
                if piece[i][j]:
                    if (y + i >= GRID_HEIGHT or 
                        x + j < 0 or 
                        x + j >= GRID_WIDTH or 
                        (y + i >= 0 and self.grid[y + i][x + j])):
                        return False
        return True
    
    def place_piece(self):
        for i in range(len(self.current_piece[0])):
            for j in range(len(self.current_piece[0][0])):
                if self.current_piece[0][i][j]:
                    if self.current_y + i < 0:
                        self.game_over = True
                        return
                    self.grid[self.current_y + i][self.current_x + j] = self.current_piece[1] + 1
        
        self.clear_lines()
        self.current_piece = self.next_piece
        self.next_piece = self.new_piece()
        self.current_x = GRID_WIDTH // 2 - len(self.current_piece[0][0]) // 2
        self.current_y = 0
    
    def rotate_piece(self):
        rotated = list(zip(*self.current_piece[0][::-1]))
        if self.valid_move(rotated, self.current_x, self.current_y):
            self.current_piece = (rotated, self.current_piece[1])
    
    def clear_lines(self):
        lines_cleared = 0
        for i in range(GRID_HEIGHT):
            if all(self.grid[i]):
                del self.grid[i]
                self.grid.insert(0, [0 for _ in range(GRID_WIDTH)])
                lines_cleared += 1
        
        self.score += lines_cleared * 100
    
    def draw(self):
        self.screen.fill(BLACK)
        
        # Draw grid
        for i in range(GRID_HEIGHT):
            for j in range(GRID_WIDTH):
                if self.grid[i][j]:
                    pygame.draw.rect(self.screen, 
                                   COLORS[self.grid[i][j] - 1],
                                   (j * BLOCK_SIZE, i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(self.screen, 
                               WHITE, 
                               (j * BLOCK_SIZE, i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 
                               1)
        
        # Draw current piece
        if self.current_piece:
            for i in range(len(self.current_piece[0])):
                for j in range(len(self.current_piece[0][0])):
                    if self.current_piece[0][i][j]:
                        pygame.draw.rect(self.screen,
                                       COLORS[self.current_piece[1]],
                                       ((self.current_x + j) * BLOCK_SIZE,
                                        (self.current_y + i) * BLOCK_SIZE,
                                        BLOCK_SIZE, BLOCK_SIZE))
        
        # Draw next piece preview
        next_x = GRID_WIDTH * BLOCK_SIZE + BLOCK_SIZE
        next_y = BLOCK_SIZE
        for i in range(len(self.next_piece[0])):
            for j in range(len(self.next_piece[0][0])):
                if self.next_piece[0][i][j]:
                    pygame.draw.rect(self.screen,
                                   COLORS[self.next_piece[1]],
                                   (next_x + j * BLOCK_SIZE,
                                    next_y + i * BLOCK_SIZE,
                                    BLOCK_SIZE, BLOCK_SIZE))
        
        # Draw score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(score_text, (GRID_WIDTH * BLOCK_SIZE + 10, BLOCK_SIZE * 6))
        
        pygame.display.flip()
    
    def run(self):
        last_time = pygame.time.get_ticks()

        key_map = {
        pygame.K_1: (0, 'x'),   # "1x"
        pygame.K_h: (0, 'h'),   # "1h"
        pygame.K_l: (0, 'r'),   # "1r"
        pygame.K_2: (1, 'x'),   # "2x"
        pygame.K_j: (1, 'h'),   # "2h"
        pygame.K_m: (0, 'r'),   # "2r"
        pygame.K_3: (2, 'x'),   # "3x"
        pygame.K_k: (2, 'h'),    # "3h"
        pygame.K_n: (0, 'r'),   # "3r"
        }

        
        while not self.game_over:
            current_time = pygame.time.get_ticks()
            delta_time = (current_time - last_time) / 1000.0
            last_time = current_time
            
            self.fall_time += delta_time
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        if self.valid_move(self.current_piece[0], self.current_x - 1, self.current_y):
                            self.current_x -= 1
                    elif event.key == pygame.K_RIGHT:
                        if self.valid_move(self.current_piece[0], self.current_x + 1, self.current_y):
                            self.current_x += 1
                    elif event.key == pygame.K_DOWN:
                        if self.valid_move(self.current_piece[0], self.current_x, self.current_y + 1):
                            self.current_y += 1
                    elif event.key == pygame.K_UP:
                        self.rotate_piece()
                    elif event.key == pygame.K_SPACE:
                        while self.valid_move(self.current_piece[0], self.current_x, self.current_y + 1):
                            self.current_y += 1
                        self.place_piece()
                        self.fall_time = 0
                    elif event.key in key_map: 
                        qubit, gate = key_map[event.key]
                        if gate == 'x':
                            self.qbit_state[qubit]= 1  # Apply X gate to the specified qubit
                        elif gate == 'h':
                            self.qbit_state[qubit]=2
                        elif gate == 'r':
                            self.qbit_state[qubit]=0
            
            if self.fall_time >= self.fall_speed:
                if self.valid_move(self.current_piece[0], self.current_x, self.current_y + 1):
                    self.current_y += 1
                else:
                    self.place_piece()
                self.fall_time = 0
            
            self.draw()
            self.clock.tick(60)
        
        # Game over screen
        gameover_text = "Game Over"
        text = self.font.gameover_font.render(gameover_text, 1, WHITE)
        text_pos = text.get_rect(center=(WINDOW_WIDTH / 2, WIDTH_UNIT * 10))
        screen.blit(text, text_pos)
        
        # Wait for a moment before quitting
        pygame.time.wait(2000)
        pygame.quit()

if __name__ == '__main__':
    game = Tetris()
    game.run()