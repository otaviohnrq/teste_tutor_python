# jungle_jumper.py

import pgzrun
import math
import random
from pygame import Rect

# --- CONSTANTS ---
WIDTH = 800
HEIGHT = 600
GRAVITY = 0.8
JUMP_STRENGTH = -15
PLAYER_SPEED = 5
ENEMY_SPEED = 2

# --- GAME STATE ---
game_state = 'main_menu'
sound_on = True

# --- GLOBAL OBJECTS ---
player = None
platforms = []
enemies = []  # Nova lista para os inimigos

# --- MAIN MENU BUTTONS ---
start_button = Rect(WIDTH/2 - 100, HEIGHT/2 - 25, 200, 50)
sound_button = Rect(WIDTH/2 - 100, HEIGHT/2 + 35, 200, 50)
exit_button = Rect(WIDTH/2 - 100, HEIGHT/2 + 95, 200, 50)

# --- CUSTOM CLASSES ---

class Player:
    # (A classe Player continua a mesma de antes, sem alterações)
    def __init__(self, x, y):
        self.rect = Rect(x, y, 32, 32)
        self.velocity_y = 0
        self.on_ground = False
        self.facing_right = True
        self.state = 'idle'
        self.frame_index = 0
        self.animation_timer = 0
        self.animation_speed = 0.1
        self.frames = {
            'idle': {'right': ['player_idle_1', 'player_idle_2'], 'left': ['player_idle_1_left', 'player_idle_2_left']},
            'run': {'right': ['player_run_1', 'player_run_2'], 'left': ['player_run_1_left', 'player_run_2_left']},
            'jump': {'right': ['player_jump'], 'left': ['player_jump_left']}
        }
        self.image = self.frames[self.state]['right'][self.frame_index]
    def animate(self):
        direction = 'right' if self.facing_right else 'left'
        self.animation_timer += 1 / 60
        if self.animation_timer > self.animation_speed:
            self.animation_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.frames[self.state][direction])
        self.image = self.frames[self.state][direction][self.frame_index]
    def update(self, platforms):
        dx, dy = 0, 0
        is_moving = False
        if keyboard.left:
            dx = -PLAYER_SPEED
            self.facing_right = False
            is_moving = True
        if keyboard.right:
            dx = PLAYER_SPEED
            self.facing_right = True
            is_moving = True
        new_state = 'idle'
        if not self.on_ground:
            new_state = 'jump'
        elif is_moving:
            new_state = 'run'
        if self.state != new_state:
            self.state = new_state
            self.frame_index = 0
            self.animation_timer = 0
        self.velocity_y += GRAVITY
        if self.velocity_y > 10: self.velocity_y = 10
        dy += self.velocity_y
        self.on_ground = False
        for plat in platforms:
            if plat.colliderect(self.rect.x + dx, self.rect.y, self.rect.width, self.rect.height):
                dx = 0
            if plat.colliderect(self.rect.x, self.rect.y + dy, self.rect.width, self.rect.height):
                if self.velocity_y < 0:
                    dy = plat.bottom - self.rect.top
                    self.velocity_y = 0
                else:
                    dy = plat.top - self.rect.bottom
                    self.velocity_y = 0
                    self.on_ground = True
        self.rect.x += dx
        self.rect.y += dy
        self.animate()
    def jump(self):
        if self.on_ground:
            self.velocity_y = JUMP_STRENGTH
    def draw(self):
        screen.blit(self.image, self.rect)

# --- NOVA CLASSE ENEMY ---
class Enemy:
    def __init__(self, x, y, patrol_end_x):
        self.rect = Rect(x, y, 32, 32)
        self.patrol_start_x = x
        self.patrol_end_x = patrol_end_x
        self.direction = 1  # 1 for right, -1 for left
        
        # Animation
        self.frame_index = 0
        self.animation_timer = 0
        self.animation_speed = 0.15 # Slower animation than player
        self.frames = {
            'right': ['enemy_walk_1', 'enemy_walk_2'],
            'left': ['enemy_walk_1_left', 'enemy_walk_2_left']
        }

    def animate(self):
        direction = 'right' if self.direction == 1 else 'left'
        self.animation_timer += 1 / 60
        if self.animation_timer > self.animation_speed:
            self.animation_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.frames[direction])
        self.image = self.frames[direction][self.frame_index]

    def update(self):
        # Move the enemy
        self.rect.x += ENEMY_SPEED * self.direction
        
        # Check if it reached the patrol limits
        if self.rect.right > self.patrol_end_x or self.rect.left < self.patrol_start_x:
            self.direction *= -1 # Invert direction
        
        self.animate()

    def draw(self):
        screen.blit(self.image, self.rect)

# --- GAME SETUP FUNCTION ---
def setup_game():
    global player, platforms, enemies
    player = Player(100, HEIGHT - 200)
    platforms = [
        Rect(0, HEIGHT - 40, WIDTH, 40),
        Rect(200, HEIGHT - 150, 150, 20),
        Rect(450, HEIGHT - 250, 150, 20)
    ]
    # Cria os inimigos e os adiciona à lista
    enemies = [
        Enemy(200, HEIGHT - 150 - 32, 320), # Patrulha na plataforma 1
        Enemy(450, HEIGHT - 250 - 32, 570)  # Patrulha na plataforma 2
    ]

# --- MUSIC ---
music.play('music_background')

# --- MAIN PYGAME ZERO HOOKS ---
def draw():
    screen.clear()
    if game_state == 'main_menu':
        draw_main_menu()
    elif game_state == 'playing':
        draw_playing()
    elif game_state == 'game_over':
        draw_game_over()

def update():
    if game_state == 'playing':
        update_playing()
    elif game_state == 'game_over':
        update_game_over()

def on_mouse_down(pos):
    global game_state, sound_on
    if game_state == 'main_menu':
        if start_button.collidepoint(pos):
            setup_game()
            game_state = 'playing'
        elif sound_button.collidepoint(pos):
            sound_on = not sound_on
            if sound_on: music.unpause()
            else: music.pause()
        elif exit_button.collidepoint(pos):
            quit()

# --- STATE-SPECIFIC DRAW FUNCTIONS ---
def draw_main_menu():
    # ... (código do menu sem alterações) ...
    screen.fill('darkgreen')
    screen.draw.text('Jungle Jumper', center=(WIDTH/2, HEIGHT/4), fontsize=70, color='white', owidth=1, ocolor='black')
    screen.draw.filled_rect(start_button, 'green')
    screen.draw.text('Start Game', center=start_button.center, fontsize=35, color='white')
    screen.draw.filled_rect(sound_button, 'orange')
    sound_text = f"Sound: {'ON' if sound_on else 'OFF'}"
    screen.draw.text(sound_text, center=sound_button.center, fontsize=35, color='white')
    screen.draw.filled_rect(exit_button, 'red')
    screen.draw.text('Exit', center=exit_button.center, fontsize=35, color='white')

def draw_playing():
    screen.fill((135, 206, 235))
    for plat in platforms:
        screen.draw.filled_rect(plat, 'saddlebrown')
    
    # Desenha cada inimigo na lista
    for enemy in enemies:
        enemy.draw()
        
    player.draw()

def draw_game_over():
    screen.fill('black')
    screen.draw.text('GAME OVER', center=(WIDTH/2, HEIGHT/2), fontsize=60, color='red')

# --- STATE-SPECIFIC UPDATE FUNCTIONS ---
def update_playing():
    player.update(platforms)
    if keyboard.space or keyboard.up:
        player.jump()
    
    # Atualiza cada inimigo e verifica colisões
    for enemy in enemies:
        enemy.update()
        if player.rect.colliderect(enemy.rect):
            # Inimigo é perigoso! Reinicia o jogo.
            print("Player hit by enemy! Resetting level.")
            setup_game()

def update_game_over():
    pass

# --- START THE GAME ---
pgzrun.go()