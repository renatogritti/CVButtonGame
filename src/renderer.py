"""
--------------------------------------------------------------------------------
Jogo: CV Button Game
Arquivo: renderer.py
Autor: Renato Gritti
Data: 2026-03-12
Descrição: Renderização do jogo.
--------------------------------------------------------------------------------
--------------------------------------------------------------------------------
"""

import pygame
import cv2
import math
from config import *

class Renderer:
    def __init__(self, screen):
        self.screen = screen

    def draw_field(self):
        # 0. Clear screen root (Fix ghosting bug)
        self.screen.fill(BLACK)
        
        # 1. Background Grass (Stripes)
        stripe_width = (FIELD_RIGHT - FIELD_LEFT) // STRIPE_COUNT
        for i in range(STRIPE_COUNT):
            color = GREEN_DARK if i % 2 == 0 else GREEN_LIGHT
            pygame.draw.rect(self.screen, color, (FIELD_LEFT + i * stripe_width, FIELD_TOP, stripe_width, FIELD_BOTTOM - FIELD_TOP))
        
        # 2. Outer boundary
        pygame.draw.rect(self.screen, WHITE, (FIELD_LEFT, FIELD_TOP, FIELD_RIGHT - FIELD_LEFT, FIELD_BOTTOM - FIELD_TOP), 4)
        
        # 3. Markings
        mid_x = (FIELD_LEFT + FIELD_RIGHT) // 2
        pygame.draw.line(self.screen, WHITE, (mid_x, FIELD_TOP), (mid_x, FIELD_BOTTOM), 2)
        pygame.draw.circle(self.screen, WHITE, (mid_x, HEIGHT // 2), 75, 2)
        pygame.draw.circle(self.screen, WHITE, (mid_x, HEIGHT // 2), 5)
        
        # Penalty Areas
        penalty_h = 240
        penalty_w = 100
        pygame.draw.rect(self.screen, WHITE, (FIELD_LEFT, (HEIGHT - penalty_h)//2, penalty_w, penalty_h), 2)
        pygame.draw.rect(self.screen, WHITE, (FIELD_RIGHT - penalty_w, (HEIGHT - penalty_h)//2, penalty_w, penalty_h), 2)

        # 4. Goals and Detailed Nets
        goal_y = (HEIGHT - GOAL_HEIGHT) // 2
        self._draw_goal_premium(FIELD_LEFT - GOAL_WIDTH, goal_y, GOAL_WIDTH, GOAL_HEIGHT, is_left=True)
        self._draw_goal_premium(FIELD_RIGHT, goal_y, GOAL_WIDTH, GOAL_HEIGHT, is_left=False)

    def _draw_goal_premium(self, x, y, w, h, is_left):
        # Goal Frame
        pygame.draw.rect(self.screen, WHITE, (x, y, w, h), 4)
        
        # Detailed Net (Grid)
        net_color = (200, 200, 200, 100)
        grid_size = 10
        net_surf = pygame.Surface((w, h), pygame.SRCALPHA)
        for i in range(0, w, grid_size):
            pygame.draw.line(net_surf, net_color, (i, 0), (i, h), 1)
        for j in range(0, h, grid_size):
            pygame.draw.line(net_surf, net_color, (0, j), (w, j), 1)
        self.screen.blit(net_surf, (x, y))

    def draw_entities(self, entities):
        for entity in entities:
            entity.draw(self.screen)
            
    def draw_pip(self, frame):
        if frame is not None:
            frame_small = cv2.resize(frame, PIP_SIZE)
            frame_rgb = cv2.cvtColor(frame_small, cv2.COLOR_BGR2RGB)
            surf = pygame.surfarray.make_surface(frame_rgb.swapaxes(0, 1))
            
            x = WIDTH - PIP_SIZE[0] - PIP_MARGIN
            y = HEIGHT - PIP_SIZE[1] - PIP_MARGIN
            
            pygame.draw.rect(self.screen, WHITE, (x-3, y-3, PIP_SIZE[0]+6, PIP_SIZE[1]+6), 3)
            self.screen.blit(surf, (x, y))

    def draw_aim_line(self, start_pos, end_pos, force):
        if force > 1.5:
            # 1. Color Calculation (Blue -> Yellow -> Red)
            # Max force is around 25
            ratio = min(force / MAX_FORCE, 1.0)
            if ratio < 0.5:
                # Interpolate Blue to Yellow
                r = int(40 + (255 - 40) * (ratio * 2))
                g = int(150 + (255 - 150) * (ratio * 2))
                b = int(255 - 155 * (ratio * 2))
            else:
                # Interpolate Yellow to Red
                r = 255
                g = int(255 - 225 * ((ratio - 0.5) * 2))
                b = int(100 - 100 * ((ratio - 0.5) * 2))
            
            color = (r, g, b)
            
            # 2. Draw Glow (Outer Line)
            glow_color = (r, g, b, 80)
            glow_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            pygame.draw.line(glow_surf, glow_color, start_pos, end_pos, 8)
            self.screen.blit(glow_surf, (0, 0))
            
            # 3. Draw Core Line
            pygame.draw.line(self.screen, color, start_pos, end_pos, 3)
            
            # 4. Animated Dashes/Circles
            start_vec = pygame.Vector2(start_pos)
            end_vec = pygame.Vector2(end_pos)
            dist = start_vec.distance_to(end_vec)
            if dist > 10:
                dir_vec = (end_vec - start_vec).normalize()
                time_offset = (pygame.time.get_ticks() % 1000) / 1000.0 # 0.0 to 1.0
                
                step = 25
                for d in range(int(step * time_offset), int(dist), step):
                    p = start_vec + dir_vec * d
                    # Shadow for dashes
                    pygame.draw.circle(self.screen, (0, 0, 0, 100), (int(p.x)+1, int(p.y)+1), 4)
                    # Dash core
                    pygame.draw.circle(self.screen, WHITE, (int(p.x), int(p.y)), 3)
                    pygame.draw.circle(self.screen, color, (int(p.x), int(p.y)), 4, 1)

            # 5. End Target Effect
            pulse = 2 + math.sin(pygame.time.get_ticks() * 0.01) * 2
            pygame.draw.circle(self.screen, color, (int(end_pos[0]), int(end_pos[1])), 8 + pulse, 2)
            pygame.draw.circle(self.screen, WHITE, (int(end_pos[0]), int(end_pos[1])), 4)

    def draw_score(self, scores, team_a_name, team_b_name):
        font = pygame.font.SysFont('Arial', 44, bold=True)
        # Main score text
        score_val = f"{scores[0]}   :   {scores[1]}"
        
        # Render names and score separately for layout
        surf_a = font.render(team_a_name, True, BLUE)
        surf_score = font.render(score_val, True, WHITE)
        surf_b = font.render(team_b_name, True, RED)
        
        # Shadows
        shadow_a = font.render(team_a_name, True, BLACK)
        shadow_score = font.render(score_val, True, BLACK)
        shadow_b = font.render(team_b_name, True, BLACK)
        
        spacing = 30
        total_width = surf_a.get_width() + spacing + surf_score.get_width() + spacing + surf_b.get_width()
        
        curr_x = WIDTH // 2 - total_width // 2
        pos_y = 12
        
        # Draw Team A
        self.screen.blit(shadow_a, (curr_x + 2, pos_y + 2))
        self.screen.blit(surf_a, (curr_x, pos_y))
        
        curr_x += surf_a.get_width() + spacing
        
        # Draw Score
        self.screen.blit(shadow_score, (curr_x + 2, pos_y + 2))
        self.screen.blit(surf_score, (curr_x, pos_y))
        
        curr_x += surf_score.get_width() + spacing
        
        # Draw Team B
        self.screen.blit(shadow_b, (curr_x + 2, pos_y + 2))
        self.screen.blit(surf_b, (curr_x, pos_y))

    def draw_goal_celebration(self, opacity):
        # Big GOL text in the center
        font = pygame.font.SysFont('Arial', 120, bold=True)
        text = "GOL!!!!"
        
        # Flashy effect using opacity/time
        color = (255, 255, 255) if (pygame.time.get_ticks() // 200) % 2 == 0 else (255, 255, 0)
        
        surf = font.render(text, True, color)
        # Glow/Shadow
        shadow = font.render(text, True, (0, 0, 0))
        
        center_x = WIDTH // 2 - surf.get_width() // 2
        center_y = HEIGHT // 2 - surf.get_height() // 2
        
        self.screen.blit(shadow, (center_x + 5, center_y + 5))
        self.screen.blit(surf, (center_x, center_y))

    def draw_winner_screen(self, winner):
        font = pygame.font.SysFont('Arial', 120, bold=True)
        surf_name = font.render(winner, True, WHITE)
        surf_venceu = font.render("VENCEU!", True, WHITE)
        
        shadow_name = font.render(winner, True, BLACK)
        shadow_venceu = font.render("VENCEU!", True, BLACK)
        
        line_spacing = 10
        total_height = surf_name.get_height() + surf_venceu.get_height() + line_spacing
        start_y = HEIGHT // 2 - total_height // 2
        
        # Line 1: Team Name
        pos_x1 = WIDTH // 2 - surf_name.get_width() // 2
        self.screen.blit(shadow_name, (pos_x1 + 5, start_y + 5))
        self.screen.blit(surf_name, (pos_x1, start_y))
        
        # Line 2: VENCEU!
        pos_x2 = WIDTH // 2 - surf_venceu.get_width() // 2
        pos_y2 = start_y + surf_name.get_height() + line_spacing
        self.screen.blit(shadow_venceu, (pos_x2 + 5, pos_y2 + 5))
        self.screen.blit(surf_venceu, (pos_x2, pos_y2))

    def draw_turn_indicator(self, current_turn):
        turn_color = BLUE if current_turn == 'A' else RED
        font_turn = pygame.font.SysFont('Arial', 24, bold=True)
        display_name = TEAM_A_NAME if current_turn == 'A' else TEAM_B_NAME
        turn_text = font_turn.render(f"TURNO: {display_name}", True, turn_color)
        self.screen.blit(turn_text, (WIDTH//2 - turn_text.get_width()//2, HEIGHT - 45))

    def draw_ui_cursor(self, finger_pos, is_pinching, can_play, is_aiming):
        cursor_color = RED if is_pinching else (255, 255, 0)
        if not can_play and not is_aiming:
            cursor_color = (100, 100, 100)
            
        pygame.draw.circle(self.screen, cursor_color, finger_pos, 8, 2)
        if is_pinching and (can_play or is_aiming):
             pygame.draw.circle(self.screen, cursor_color, finger_pos, 4)

    def draw_splash(self):
        import os
        image_path = os.path.join('assets', 'images', SPLASH_IMAGE)
        try:
            splash_img = pygame.image.load(image_path).convert()
            splash_img = pygame.transform.smoothscale(splash_img, (WIDTH, HEIGHT))
            self.screen.blit(splash_img, (0, 0))
            
            # Add Title
            font = pygame.font.SysFont('Arial', 80, bold=True)
            text = font.render("Button Game", True, WHITE)
            shadow = font.render("Button Game", True, BLACK)
            
            pos_x = WIDTH // 2 - text.get_width() // 2
            pos_y = HEIGHT // 2 - text.get_height() // 2
            
            self.screen.blit(shadow, (pos_x + 4, pos_y + 4))
            self.screen.blit(text, (pos_x, pos_y))
            
            pygame.display.flip()
        except Exception as e:
            print(f"Error loading splash image: {e}")
            self.screen.fill(BLACK)
            font = pygame.font.SysFont('Arial', 40, bold=True)
            text = font.render("CV BOTÃO", True, WHITE)
            self.screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
            pygame.display.flip()
