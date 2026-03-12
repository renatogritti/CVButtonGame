"""
--------------------------------------------------------------------------------
Jogo: CV Button Game
Arquivo: particles.py
Autor: Renato Gritti
Data: 2026-03-12
Descrição: Partículas do jogo.
--------------------------------------------------------------------------------
--------------------------------------------------------------------------------
"""

import pygame
import random
import math
from config import *

class Particle:
    def __init__(self, x, y, color):
        self.pos = pygame.Vector2(x, y)
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 6)
        self.vel = pygame.Vector2(math.cos(angle) * speed, math.sin(angle) * speed)
        self.life = 1.0 # 100% to 0%
        self.decay = random.uniform(0.01, 0.03)
        self.color = color

    def update(self):
        self.pos += self.vel
        self.vel *= 0.95 # Air resistance
        self.vel.y += 0.1 # Gravity
        self.life -= self.decay

    def draw(self, screen):
        alpha = int(self.life * 255)
        # Create a tiny surface for alpha blending if needed, but circles are fine
        radius = max(1, int(self.life * 4))
        p_color = list(self.color)
        pygame.draw.circle(screen, p_color, (int(self.pos.x), int(self.pos.y)), radius)

class FireworkSystem:
    def __init__(self):
        self.particles = []

    def explode(self, x, y):
        colors = [(255, 50, 50), (50, 255, 50), (50, 50, 255), (255, 255, 50), (255, 50, 255)]
        color = random.choice(colors)
        for _ in range(FIREWORK_PARTICLE_COUNT):
            self.particles.append(Particle(x, y, color))

    def update(self):
        for p in self.particles[:]:
            p.update()
            if p.life <= 0:
                self.particles.remove(p)

    def draw(self, screen):
        for p in self.particles:
            p.draw(screen)
