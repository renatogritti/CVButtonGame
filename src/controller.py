"""
--------------------------------------------------------------------------------
Jogo: CV Button Game
Arquivo: controller.py
Autor: Renato Gritti
Data: 2026-03-12
Descrição: Controlador de entrada (CV) e lógica de interação com botões.
--------------------------------------------------------------------------------
--------------------------------------------------------------------------------
"""

import pygame
from config import *

class CVController:
    def __init__(self):
        self.pinch_start = None
        self.selected_player = None

    def handle_input(self, finger_pos, is_pinching, current_team, sound_manager):
        action_triggered = False
        
        if is_pinching:
            if not self.pinch_start:
                # Try to select a player from current team
                for p in current_team:
                    if pygame.Vector2(finger_pos).distance_to(p.pos) < p.radius * SELECTION_RADIUS_MULT:
                        if p.vel.length() < STATIONARY_THRESHOLD:
                            self.pinch_start = pygame.Vector2(p.pos)
                            self.selected_player = p
                            p.selected = True
                            break
        else:
            if self.pinch_start and self.selected_player:
                direction = self.pinch_start - pygame.Vector2(finger_pos)
                force = min(direction.length() * FORCE_MULTIPLIER, MAX_FORCE)
                if force > 2:
                    self.selected_player.vel = direction.normalize() * force
                    sound_manager.play('kick')
                    action_triggered = True
                
                self.pinch_start = None
                self.selected_player.selected = False
                self.selected_player = None
                
        return action_triggered

    def get_aim_data(self, finger_pos):
        if self.pinch_start and self.selected_player:
            pull_vec = self.pinch_start - pygame.Vector2(finger_pos)
            pull_mag = min(pull_vec.length() * FORCE_MULTIPLIER, MAX_FORCE)
            return tuple(self.selected_player.pos), finger_pos, pull_mag
        return None
