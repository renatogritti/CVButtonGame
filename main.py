import pygame
import cv2
import sys
import random
from config import *
from src.entities import Player, Ball
from src.renderer import Renderer
from src.cv_handler import CVHandler
from src.physics import check_all_collisions
from src.particles import FireworkSystem
from src.audio import SoundManager

def setup_teams():
    team_a = [Player(pos[0], pos[1], 'A') for pos in FORMATION_A]
    team_b = [Player(pos[0], pos[1], 'B') for pos in FORMATION_B]
    return team_a, team_b

def reset_match(team_a, team_b, ball):
    for i, pos in enumerate(FORMATION_A):
        team_a[i].pos = pygame.Vector2(pos)
        team_a[i].vel = pygame.Vector2(0, 0)
    for i, pos in enumerate(FORMATION_B):
        team_b[i].pos = pygame.Vector2(pos)
        team_b[i].vel = pygame.Vector2(0, 0)
    ball.pos = pygame.Vector2(WIDTH // 2, HEIGHT // 2)
    ball.vel = pygame.Vector2(0, 0)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("CV Botão - Retro Soccer v1.2")
    clock = pygame.time.Clock()
    
    renderer = Renderer(screen)
    cv_handler = CVHandler()
    fireworks = FireworkSystem()
    sound_manager = SoundManager()
    
    sound_manager.play('start')
    sound_manager.play_bgm()
    
    team_a, team_b = setup_teams()
    ball = Ball(WIDTH // 2, HEIGHT // 2)
    all_players = team_a + team_b
    
    scores = [0, 0] # Team A (Left), Team B (Right)
    current_turn = 'A'
    pinch_start = None
    selected_player = None
    goal_timer = 0
    waiting_for_stop = False
    winner = None

    while True:
        frame = cv_handler.get_frame()
        if frame is None:
            break
            
        finger_pos = cv_handler.finger_pos
        is_pinching = cv_handler.is_pinching
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cv_handler.close()
                pygame.quit()
                sys.exit()

        # 1. Turn and Action Logic
        all_stopped = all(p.vel.length() < STATIONARY_THRESHOLD for p in all_players) and ball.vel.length() < STATIONARY_THRESHOLD
        
        if winner:
            # Game Over state logic could go here
            pass
        elif goal_timer == 0:
            if waiting_for_stop:
                if all_stopped:
                    # Movement finished, switch turn
                    current_turn = 'B' if current_turn == 'A' else 'A'
                    waiting_for_stop = False
            else:
                # Active turn
                if is_pinching:
                    if not pinch_start:
                        # Try to select a player from current team
                        active_team = team_a if current_turn == 'A' else team_b
                        for p in active_team:
                            if pygame.Vector2(finger_pos).distance_to(p.pos) < p.radius * SELECTION_RADIUS_MULT:
                                if p.vel.length() < STATIONARY_THRESHOLD:
                                    pinch_start = pygame.Vector2(p.pos)
                                    selected_player = p
                                    p.selected = True
                                    break
                else:
                    if pinch_start and selected_player:
                        direction = pinch_start - pygame.Vector2(finger_pos)
                        force = min(direction.length() * FORCE_MULTIPLIER, MAX_FORCE)
                        if force > 2:
                            selected_player.vel = direction.normalize() * force
                            sound_manager.play('kick')
                            waiting_for_stop = True # Movement started, wait for it to end
                        
                        pinch_start = None
                        selected_player.selected = False
                        selected_player = None

        # 2. Physics Updates
        for p in all_players:
            p.update(sound_manager)
        ball.update(sound_manager)
        
        check_all_collisions(all_players, ball, sound_manager)
        fireworks.update()

        # 3. Goal Detection
        goal_y_start = (HEIGHT - GOAL_HEIGHT) // 2
        goal_y_end = goal_y_start + GOAL_HEIGHT
        
        if goal_timer == 0 and not winner:
            scored = False
            if ball.pos.x < FIELD_LEFT and goal_y_start < ball.pos.y < goal_y_end:
                scores[1] += 1
                scored = True
                fireworks.explode(FIELD_LEFT, ball.pos.y)
                if scores[1] >= MAX_GOALS: winner = TEAM_B_NAME
            elif ball.pos.x > FIELD_RIGHT and goal_y_start < ball.pos.y < goal_y_end:
                scores[0] += 1
                scored = True
                fireworks.explode(FIELD_RIGHT, ball.pos.y)
                if scores[0] >= MAX_GOALS: winner = TEAM_A_NAME
            
            if scored:
                sound_manager.play('goal')
                goal_timer = GOAL_MESSAGE_DURATION
                waiting_for_stop = False
        elif goal_timer > 0:
            goal_timer -= 1
            if goal_timer % 30 == 0:
                fireworks.explode(WIDTH//2 + random.randint(-200, 200), HEIGHT//2 + random.randint(-150, 150))
            if goal_timer == 0:
                if not winner:
                    reset_match(team_a, team_b, ball)
                    current_turn = 'A' if scores[0] == scores[1] else ('B' if scored else 'A') # simplified

        # 4. Rendering
        renderer.draw_field()
        for p in all_players:
            p.draw(screen)
        ball.draw(screen)
        renderer.draw_score(scores, TEAM_A_NAME, TEAM_B_NAME)
        fireworks.draw(screen)

        if goal_timer > 0:
            renderer.draw_goal_celebration(goal_timer)
        
        if winner:
            font = pygame.font.SysFont('Arial', 60, bold=True)
            text = font.render(f"{winner} VENCEU!", True, WHITE)
            screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2))

        # Turn Indicator
        turn_color = BLUE if current_turn == 'A' else RED
        font_turn = pygame.font.SysFont('Arial', 24, bold=True)
        display_name = TEAM_A_NAME if current_turn == 'A' else TEAM_B_NAME
        turn_text = font_turn.render(f"TURNO: {display_name}", True, turn_color)
        screen.blit(turn_text, (WIDTH//2 - turn_text.get_width()//2, HEIGHT - 45))

        # Aiming Feedback
        if pinch_start and selected_player:
            pull_vec = pinch_start - pygame.Vector2(finger_pos)
            pull_mag = min(pull_vec.length() * FORCE_MULTIPLIER, MAX_FORCE)
            renderer.draw_aim_line(tuple(selected_player.pos), finger_pos, pull_mag)
            
        # Draw CV Cursor
        cursor_color = RED if is_pinching else (255, 255, 0)
        # Check if can play
        can_play = all_stopped and not waiting_for_stop and goal_timer == 0 and not winner
        if not can_play and not pinch_start:
            cursor_color = (100, 100, 100)
            
        pygame.draw.circle(screen, cursor_color, finger_pos, 8, 2)
        if is_pinching and (can_play or pinch_start):
             pygame.draw.circle(screen, cursor_color, finger_pos, 4)

        renderer.draw_pip(frame)
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
