import random
from pgzero.rect import Rect
from pgzero.actor import Actor

WIDTH = 800
HEIGHT = 400

game_state = "menu"
gameover_timer = 0
sound_on = True

enemy_timer = 0
enemies = []

difficulty = 3  # 1: Easy, 5: Hard
difficulty_settings = {
    1: {"enemy_interval": 200, "jump_strength": -20},
    2: {"enemy_interval": 150, "jump_strength": -17},
    3: {"enemy_interval": 100, "jump_strength": -14},
    4: {"enemy_interval": 75, "jump_strength": -12},
    5: {"enemy_interval": 50, "jump_strength": -10},
}

# --- OOP Sınıfları ---
class Player:
    def __init__(self):
        self.images_walk = ["hero/player_walk1", "hero/player_walk2"]
        self.image_jump = "hero/player_jump"
        self.index = 0
        self.timer = 0
        self.actor = Actor(self.images_walk[0], (100, HEIGHT - 70))
        self.vy = 0
        self.gravity = 0.5
        self.jump_strength = difficulty_settings[difficulty]["jump_strength"]
        self.on_ground = True

    def update(self):
        self.vy += self.gravity
        self.actor.y += self.vy

        if self.actor.y >= HEIGHT - 70:
            self.actor.y = HEIGHT - 70
            self.vy = 0
            self.on_ground = True
        else:
            self.on_ground = False

        if not self.on_ground:
            self.actor.image = self.image_jump
        else:
            self.timer += 1
            if self.timer > 10:
                self.index = (self.index + 1) % len(self.images_walk)
                self.actor.image = self.images_walk[self.index]
                self.timer = 0

    def jump(self):
        if self.on_ground:
            self.vy = self.jump_strength
            self.on_ground = False
            if sound_on:
                sounds.jump.play()

    def draw(self):
        self.actor.draw()

    def reset_position(self):
        self.actor.x, self.actor.y = 100, HEIGHT - 70

    @property
    def rect(self):
        return self.actor._rect

class Enemy:
    def __init__(self):
        self.actor = Actor("zombi/head", (WIDTH, HEIGHT - 50))  # Yüksekliği biraz küçültüldü
        self.actor.scale = 0.7  # Zombi boyutu %70'e düşürüldü

    def update(self):
        self.actor.x -= 5

    def draw(self):
        self.actor.draw()

    @property
    def rect(self):
        return self.actor._rect

# --- Butonlar ---
start_button = Rect((WIDTH // 2 - 100, 150), (200, 50))
sound_button = Rect((WIDTH // 2 - 100, 220), (200, 50))
quit_button = Rect((WIDTH // 2 - 100, 290), (200, 50))
difficulty_buttons = [
    Rect((WIDTH // 2 - 110 + i * 45, 350), (40, 40)) for i in range(5)
]

# --- Oyuncu Nesnesi ---
player = Player()

def draw():
    screen.clear()

    if game_state == "menu":
        screen.fill((30, 30, 30))
        screen.draw.text("RUNNER GAME", center=(WIDTH // 2, 80), fontsize=50, color="white")
        screen.draw.filled_rect(start_button, (0, 200, 0))
        screen.draw.text("Start Game", center=start_button.center, color="white")
        screen.draw.filled_rect(sound_button, (0, 0, 200))
        screen.draw.text(f"Sound: {'On' if sound_on else 'Off'}", center=sound_button.center, color="white")
        screen.draw.filled_rect(quit_button, (200, 0, 0))
        screen.draw.text("Quit", center=quit_button.center, color="white")

        for i, button in enumerate(difficulty_buttons):
            color = (255, 255, 0) if (i + 1) == difficulty else (100, 100, 100)
            screen.draw.filled_rect(button, color)
            screen.draw.text(str(i + 1), center=button.center, fontsize=30, color="black")

    elif game_state == "playing":
        screen.fill((0, 150, 255))
        player.draw()
        for enemy in enemies:
            enemy.draw()

    elif game_state == "gameover":
        screen.fill((0, 0, 0))
        screen.draw.text("GAME OVER", center=(WIDTH // 2, HEIGHT // 2), fontsize=70, color="red")

def update():
    global game_state, gameover_timer, enemy_timer

    if game_state == "menu":
        return

    elif game_state == "gameover":
        gameover_timer += 1
        if gameover_timer > 120:
            game_state = "menu"
            enemies.clear()
            player.reset_position()
            music.stop()
        return

    # Playing durumu
    player.update()

    enemy_timer += 1
    if enemy_timer > difficulty_settings[difficulty]["enemy_interval"]:
        enemy_timer = 0
        enemies.append(Enemy())

    for enemy in enemies:
        enemy.update()

    enemies[:] = [e for e in enemies if e.rect.x > -50]

    for enemy in enemies:
        if player.rect.colliderect(enemy.rect):
            if sound_on:
                sounds.funny_crash.play()
                sounds.gameover.play()
            game_state = "gameover"
            gameover_timer = 0
            break

def on_key_down(key):
    if game_state != "playing":
        return

    if key == keys.SPACE:
        player.jump()

def on_mouse_down(pos):
    global game_state, sound_on, difficulty, player

    if game_state == "menu":
        if start_button.collidepoint(pos):
            player = Player()
            game_state = "playing"
            if sound_on:
                music.play("background")
                music.set_volume(0.4)
        elif sound_button.collidepoint(pos):
            sound_on = not sound_on
            if not sound_on:
                music.stop()
        elif quit_button.collidepoint(pos):
            quit()
        else:
            for i, button in enumerate(difficulty_buttons):
                if button.collidepoint(pos):
                    difficulty = i + 1
                    break