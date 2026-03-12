"""
--------------------------------------------------------------------------------
Jogo: CV Button Game
Arquivo: entities.py
Autor: Renato Gritti
Data: 2026-03-12
Descrição: Entidades do jogo.
--------------------------------------------------------------------------------
--------------------------------------------------------------------------------
"""

import pygame
import math
import os
from config import *

class Entity:
    def __init__(self, x, y, radius, color):
        self.pos = pygame.Vector2(x, y)
        self.vel = pygame.Vector2(0, 0)
        self.radius = radius
        self.color = color

    def update(self, sound_manager=None):
        self.pos += self.vel
        self.vel *= FIELD_FRICTION
        
        if self.vel.length() < MIN_VELOCITY:
            self.vel = pygame.Vector2(0, 0)

        # Boundary collision logic
        goal_y_start = (HEIGHT - GOAL_HEIGHT) // 2
        goal_y_end = goal_y_start + GOAL_HEIGHT

        # 1. Horizontal Collisions (including Goal areas)
        # Left side
        if self.pos.x - self.radius < FIELD_LEFT:
            if goal_y_start < self.pos.y < goal_y_end:
                if self.pos.x - self.radius < FIELD_LEFT - GOAL_WIDTH:
                    self.pos.x = (FIELD_LEFT - GOAL_WIDTH) + self.radius
                    self.vel.x *= -BOUNCE
                    if sound_manager: sound_manager.play('hit_wall')
            else:
                self.pos.x = FIELD_LEFT + self.radius
                self.vel.x *= -BOUNCE
                if sound_manager and self.vel.length() > 0.5:
                    sound_manager.play('hit_wall')

        # Right side
        elif self.pos.x + self.radius > FIELD_RIGHT:
            if goal_y_start < self.pos.y < goal_y_end:
                if self.pos.x + self.radius > FIELD_RIGHT + GOAL_WIDTH:
                    self.pos.x = (FIELD_RIGHT + GOAL_WIDTH) - self.radius
                    self.vel.x *= -BOUNCE
                    if sound_manager: sound_manager.play('hit_wall')
            else:
                self.pos.x = FIELD_RIGHT - self.radius
                self.vel.x *= -BOUNCE
                if sound_manager and self.vel.length() > 0.5:
                    sound_manager.play('hit_wall')

        # 2. Vertical Collisions
        is_in_goal_x_left = (FIELD_LEFT - GOAL_WIDTH < self.pos.x < FIELD_LEFT)
        is_in_goal_x_right = (FIELD_RIGHT < self.pos.x < FIELD_RIGHT + GOAL_WIDTH)

        if is_in_goal_x_left or is_in_goal_x_right:
            if self.pos.y - self.radius < goal_y_start:
                self.pos.y = goal_y_start + self.radius
                self.vel.y *= -BOUNCE
                if sound_manager: sound_manager.play('hit_wall')
            elif self.pos.y + self.radius > goal_y_end:
                self.pos.y = goal_y_end - self.radius
                self.vel.y *= -BOUNCE
                if sound_manager: sound_manager.play('hit_wall')
        else:
            if self.pos.y - self.radius < FIELD_TOP:
                self.pos.y = FIELD_TOP + self.radius
                self.vel.y *= -BOUNCE
                if sound_manager and self.vel.length() > 0.5:
                    sound_manager.play('hit_wall')
            elif self.pos.y + self.radius > FIELD_BOTTOM:
                self.pos.y = FIELD_BOTTOM - self.radius
                self.vel.y *= -BOUNCE
                if sound_manager and self.vel.length() > 0.5:
                    sound_manager.play('hit_wall')

    def draw_shadow(self, screen):
        shadow_surf = pygame.Surface((self.radius * 2.5, self.radius * 2.5), pygame.SRCALPHA)
        pygame.draw.circle(shadow_surf, (0, 0, 0, 60), (self.radius * 1.25, self.radius * 1.25), self.radius)
        screen.blit(shadow_surf, (int(self.pos.x - self.radius * 1.25 + SHADOW_OFFSET), int(self.pos.y - self.radius * 1.25 + SHADOW_OFFSET)))

class Player(Entity):
    def __init__(self, x, y, team):
        color = BLUE if team == 'A' else RED
        super().__init__(x, y, PLAYER_RADIUS, color)
        self.team = team
        self.selected = False
        
        # Load specific image for team
        img_filename = TEAM_A_IMAGE if team == 'A' else TEAM_B_IMAGE
        image_path = os.path.join('assets', 'images', img_filename)
        try:
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.smoothscale(self.image, (int(self.radius * 2), int(self.radius * 2)))
        except:
            print(f"Error loading {image_path}, falling back to primitive.")
            self.image = None

    def draw(self, screen):
        self.draw_shadow(screen)
        if self.image:
            screen.blit(self.image, (int(self.pos.x - self.radius), int(self.pos.y - self.radius)))
        else:
            pygame.draw.circle(screen, self.color, (int(self.pos.x), int(self.pos.y)), self.radius)
            shade_color = [max(0, c - 40) for c in self.color]
            pygame.draw.circle(screen, shade_color, (int(self.pos.x), int(self.pos.y)), self.radius, 3)

class Ball(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, BALL_RADIUS, WHITE)
    
    def draw(self, screen):
        self.draw_shadow(screen)
        pygame.draw.circle(screen, self.color, (int(self.pos.x), int(self.pos.y)), self.radius)
        highlight_pos = (int(self.pos.x - self.radius*0.3), int(self.pos.y - self.radius*0.3))
        pygame.draw.circle(screen, (255, 255, 255, 200), highlight_pos, self.radius // 2)
        pygame.draw.circle(screen, (100, 100, 100), (int(self.pos.x), int(self.pos.y)), self.radius, 2)
