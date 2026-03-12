import pygame
import cv2
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
        if force > 2:
            pygame.draw.line(self.screen, (255, 255, 0), start_pos, end_pos, max(1, int(force//4)))
            pygame.draw.circle(self.screen, (255, 50, 50), end_pos, 7)

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
