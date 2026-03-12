"""
--------------------------------------------------------------------------------
Jogo: CV Button Game
Arquivo: main.py
Autor: Renato Gritti
Data: 2026-03-12
Descrição: Ponto de entrada e orquestração do loop principal.
--------------------------------------------------------------------------------
--------------------------------------------------------------------------------
"""

import pygame
import sys
from config import *
from src.entities import Ball, Player
from src.renderer import Renderer
from src.cv_handler import CVHandler
from src.physics import check_all_collisions
from src.particles import FireworkSystem
from src.audio import SoundManager
from src.game_logic import GameManager
from src.controller import CVController

def setup_teams():
    team_a = [Player(pos[0], pos[1], 'A') for pos in FORMATION_A]
    team_b = [Player(pos[0], pos[1], 'B') for pos in FORMATION_B]
    return team_a, team_b

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("CV Botão - Retro Soccer v1.2")
    clock = pygame.time.Clock()
    
    # Components
    renderer = Renderer(screen)
    cv_handler = CVHandler()
    fireworks = FireworkSystem()
    sound_manager = SoundManager()
    game_manager = GameManager()
    controller = CVController()
    
    # Initial State
    renderer.draw_splash()
    pygame.time.delay(SPLASH_DURATION * 1000)
    pygame.event.clear()
    
    sound_manager.play('start')
    sound_manager.play_bgm()
    
    team_a, team_b = setup_teams()
    ball = Ball(WIDTH // 2, HEIGHT // 2)
    all_players = team_a + team_b

    while True:
        frame = cv_handler.get_frame()
        if frame is None: break
            
        finger_pos = cv_handler.finger_pos
        is_pinching = cv_handler.is_pinching
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cv_handler.close()
                pygame.quit()
                sys.exit()

        # 1. Logic & Input
        all_stopped = all(p.vel.length() < STATIONARY_THRESHOLD for p in all_players) and ball.vel.length() < STATIONARY_THRESHOLD
        
        # 1. Logic & Input
        all_stopped = all(p.vel.length() < STATIONARY_THRESHOLD for p in all_players) and ball.vel.length() < STATIONARY_THRESHOLD
        
        is_celebrating = game_manager.update_timers(fireworks)
        
        if not is_celebrating:
            if not game_manager.winner:
                # Active turn logic
                active_team = team_a if game_manager.current_turn == 'A' else team_b
                if controller.handle_input(finger_pos, is_pinching, active_team, sound_manager):
                    game_manager.waiting_for_stop = True
                
                if game_manager.waiting_for_stop and all_stopped:
                    game_manager.toggle_turn()
        else:
            # Check for match reset after celebration
            if game_manager.goal_timer == 0 and not game_manager.winner:
                game_manager.reset_match(team_a, team_b, ball)

        # 2. Physics Updates
        for p in all_players: p.update(sound_manager)
        ball.update(sound_manager)
        check_all_collisions(all_players, ball, sound_manager)
        fireworks.update()

        # 3. Goal Detection
        game_manager.check_goals(ball, fireworks, sound_manager)

        # 4. Rendering
        renderer.draw_field()
        for p in all_players: p.draw(screen)
        ball.draw(screen)
        renderer.draw_score(game_manager.scores, TEAM_A_NAME, TEAM_B_NAME)
        fireworks.draw(screen)

        if game_manager.goal_timer > 0:
            renderer.draw_goal_celebration(game_manager.goal_timer)
        
        if game_manager.winner and game_manager.goal_timer == 0:
            renderer.draw_winner_screen(game_manager.winner)

        renderer.draw_turn_indicator(game_manager.current_turn)
        
        # UI overlays
        aim_data = controller.get_aim_data(finger_pos)
        if aim_data:
            renderer.draw_aim_line(*aim_data)
            
        can_play = all_stopped and not game_manager.waiting_for_stop and game_manager.goal_timer == 0 and not game_manager.winner
        renderer.draw_ui_cursor(finger_pos, is_pinching, can_play, aim_data is not None)

        renderer.draw_pip(frame)
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()

