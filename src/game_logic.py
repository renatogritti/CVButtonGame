"""
--------------------------------------------------------------------------------
Jogo: CV Button Game
Arquivo: game_logic.py
Autor: Renato Gritti
Data: 2026-03-12
Descrição: Gerenciamento das regras do jogo, placar e turnos.
--------------------------------------------------------------------------------
--------------------------------------------------------------------------------
"""

import pygame
import random
from config import *

class GameManager:
    def __init__(self):
        self.scores = [0, 0]  # Team A (Left), Team B (Right)
        self.current_turn = 'A'
        self.goal_timer = 0
        self.winner = None
        self.conceding_team = 'A'
        self.waiting_for_stop = False

    def check_goals(self, ball, fireworks, sound_manager):
        goal_y_start = (HEIGHT - GOAL_HEIGHT) // 2
        goal_y_end = goal_y_start + GOAL_HEIGHT
        
        scored = False
        if self.goal_timer == 0 and not self.winner:
            if ball.pos.x < FIELD_LEFT and goal_y_start < ball.pos.y < goal_y_end:
                self.scores[1] += 1
                scored = True
                self.conceding_team = 'A'
                fireworks.explode(FIELD_LEFT, ball.pos.y)
                if self.scores[1] >= MAX_GOALS:
                    self.winner = TEAM_B_NAME
            elif ball.pos.x > FIELD_RIGHT and goal_y_start < ball.pos.y < goal_y_end:
                self.scores[0] += 1
                scored = True
                self.conceding_team = 'B'
                fireworks.explode(FIELD_RIGHT, ball.pos.y)
                if self.scores[0] >= MAX_GOALS:
                    self.winner = TEAM_A_NAME
            
            if scored:
                sound_manager.play('goal')
                self.goal_timer = GOAL_MESSAGE_DURATION
                self.waiting_for_stop = False
        
        return scored

    def update_timers(self, fireworks):
        if self.goal_timer > 0:
            self.goal_timer -= 1
            if self.goal_timer % 30 == 0:
                fireworks.explode(WIDTH//2 + random.randint(-200, 200), HEIGHT//2 + random.randint(-150, 150))
            return True
        return False

    def reset_match(self, team_a, team_b, ball):
        from src.entities import Player # Local import to avoid circular dependency if any
        for i, pos in enumerate(FORMATION_A):
            team_a[i].pos = pygame.Vector2(pos)
            team_a[i].vel = pygame.Vector2(0, 0)
        for i, pos in enumerate(FORMATION_B):
            team_b[i].pos = pygame.Vector2(pos)
            team_b[i].vel = pygame.Vector2(0, 0)
        ball.pos = pygame.Vector2(WIDTH // 2, HEIGHT // 2)
        ball.vel = pygame.Vector2(0, 0)
        self.current_turn = self.conceding_team
        self.waiting_for_stop = False

    def toggle_turn(self):
        self.current_turn = 'B' if self.current_turn == 'A' else 'A'
        self.waiting_for_stop = False
