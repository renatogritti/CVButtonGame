import pygame

# Screen Configuration
WIDTH = 800
HEIGHT = 600
FPS = 60

# Colors
GREEN_DARK = (15, 80, 15)
GREEN_LIGHT = (25, 110, 25)
WHITE = (245, 245, 245)
BLACK = (5, 5, 5)
SHADOW_COLOR = (0, 0, 0, 80)
RED = (230, 30, 60)
BLUE = (40, 150, 255)
HIGHLIGHT_COLOR = (255, 255, 255, 120)

# Field and Goals
FIELD_MARGIN_X = 75
FIELD_MARGIN_Y = 70
GOAL_WIDTH = 60
GOAL_HEIGHT = 160
STRIPE_COUNT = 10

# Internal Field Rect
FIELD_LEFT = FIELD_MARGIN_X
FIELD_RIGHT = WIDTH - FIELD_MARGIN_X
FIELD_TOP = FIELD_MARGIN_Y
FIELD_BOTTOM = HEIGHT - FIELD_MARGIN_Y

# Physics
FIELD_FRICTION = 0.972 # User tuned
BOUNCE = 0.75
MIN_VELOCITY = 0.15
STATIONARY_THRESHOLD = 0.1 # User tuned

# Celebration
GOAL_MESSAGE_DURATION = 120 # Frames
FIREWORK_PARTICLE_COUNT = 50
SPLASH_IMAGE = 'Splash.jpg'
SPLASH_DURATION = 3 # Seconds

# Match Rules
MAX_GOALS = 1
TEAM_A_IMAGE = 'Botao1.png'
TEAM_B_IMAGE = 'Botao2.png'
TEAM_A_NAME = 'Time A'
TEAM_B_NAME = 'Time B'

# Formations (2-1-2 Strategic)
FORMATION_A = [
    (FIELD_LEFT + 35, HEIGHT // 2 - 0),          # Defender Top
    (FIELD_LEFT + 210, HEIGHT // 2 - 40),          # Defender Bottom
    (FIELD_LEFT + 210, HEIGHT // 2 + 40),              # Center Mid
    (WIDTH // 2 - 60, HEIGHT // 2 - 180),       # Attacker Top
    (WIDTH // 2 - 60, HEIGHT // 2 + 180)        # Attacker Bottom
]

FORMATION_B = [
    (FIELD_RIGHT - 35, HEIGHT // 2 - 0),         # Defender Top
    (FIELD_RIGHT - 210, HEIGHT // 2 + 40),         # Defender Bottom
    (FIELD_RIGHT - 210, HEIGHT // 2 - 40),             # Center Mid
    (WIDTH // 2 + 60, HEIGHT // 2 - 180),       # Attacker Top
    (WIDTH // 2 + 60, HEIGHT // 2 + 180)        # Attacker Bottom
]

# Entities
PLAYER_RADIUS = 26
BALL_RADIUS = 9
SHADOW_OFFSET = 5

# CV Tuning
PINCH_THRESHOLD = 0.045
PINCH_RELEASE_THRESHOLD = 0.075
PINCH_STABILIZATION_FRAMES = 2
SELECTION_RADIUS_MULT = 3.5 # Increased for easier selection at edges
CV_SMOOTH_FACTOR = 0.35 
CV_SAFE_ZONE = 0.15 # Margin (0-0.5) to reach full field bounds

PIP_SIZE = (150, 112)
PIP_MARGIN = 15

FORCE_MULTIPLIER = 0.22
MAX_FORCE = 25

# Sound Assets
SOUND_START = 'begining.mp3'
SOUND_BGM = 'cheer.mp3'
SOUND_KICK = 'kick.mp3'
SOUND_GOAL = 'goal.mp3'
SOUND_HIT_PLAYER = 'hit_player.wav'
SOUND_HIT_WALL = 'hit_wall.wav'
