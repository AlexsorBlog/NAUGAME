import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Animated Character with Obstacles")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
GREEN = (0, 255, 0)

# Load background images
normal_bg = pygame.image.load("bg.jpg").convert()
normal_bg = pygame.transform.scale(normal_bg, (WINDOW_WIDTH * 2, WINDOW_HEIGHT))
final_bg = pygame.image.load("bg2.png").convert()
final_bg = pygame.transform.scale(final_bg, (WINDOW_WIDTH, WINDOW_HEIGHT))
bg_x = 0

# Load house image and scale
house_image = pygame.image.load("house.png").convert_alpha()
house_image = pygame.transform.scale(house_image, (50, 50))

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.scale_factor = 2
        directory = "Gangsters_2/"
        self.animations = {
            "Idle": self.load_animation(f"{directory}Idle.png", 7),
            "Idle_2": self.load_animation(f"{directory}Idle_2.png", 13),
            "Walk": self.load_animation(f"{directory}Walk.png", 10),
            "Run": self.load_animation(f"{directory}Run.png", 10),
            "Jump": self.load_animation(f"{directory}Jump.png", 10),
            "Attack_1": self.load_animation(f"{directory}Attack_1.png", 6),
            "Attack_2": self.load_animation(f"{directory}Attack_2.png", 4),
            "Attack_3": self.load_animation(f"{directory}Attack_3.png", 6),
            "Hurt": self.load_animation(f"{directory}Hurt.png", 4),
            "Dead": self.load_animation(f"{directory}Dead.png", 5)
        }

        self.state = "Idle"
        self.current_frame = 0
        self.animation_speed = 10
        self.animation_timer = 0
        self.loop_animation = True
        self.facing_right = True
        self.attack_sequence = 0
        self.is_attacking = False

        self.velocity_x = 0
        self.velocity_y = 0
        self.on_ground = True
        self.moving_left = False
        self.moving_right = False

        self.hp = 3
        self.is_dead = False
        self.distance_run = 0

        self.image = self.animations[self.state][0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hitbox = pygame.Rect(0, 0, self.rect.width * 0.5, self.rect.height * 0.5)
        self.hitbox.center = self.rect.center

    def load_animation(self, filename, frame_count):
        sprite_sheet = pygame.image.load(filename).convert_alpha()
        frame_width = sprite_sheet.get_width() // frame_count
        frame_height = sprite_sheet.get_height()
        frames = []
        for i in range(frame_count):
            frame = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA).convert_alpha()
            frame.blit(sprite_sheet, (0, 0), (i * frame_width, 0, frame_width, frame_height))
            frame = pygame.transform.scale(frame, (frame_width * self.scale_factor, frame_height * self.scale_factor))
            frames.append(frame)
        return frames

    def set_state(self, new_state, loop=True):
        if new_state != self.state:
            self.state = new_state
            self.current_frame = 0
            self.animation_timer = 0
            self.loop_animation = loop
            self.is_attacking = new_state in ["Attack_1", "Attack_2"]
            if new_state == "Dead":
                self.is_dead = True
                self.velocity_x = 0

    def trigger_attack(self):
        if not self.is_attacking and not self.is_dead:
            self.attack_sequence = (self.attack_sequence % 2) + 1
            if self.attack_sequence == 1:
                self.set_state("Attack_1", False)
            elif self.attack_sequence == 2:
                self.set_state("Attack_2", False)

    def take_damage(self):
        if not self.is_dead:
            self.hp -= 1
            if self.hp > 0:
                self.set_state("Hurt", False)
            elif self.hp <= 0:
                self.set_state("Dead", False)

    def update(self, dt):
        global bg_x

        self.animation_timer += dt
        if self.animation_timer >= 1 / self.animation_speed:
            self.animation_timer = 0
            self.current_frame += 1
            if self.current_frame >= len(self.animations[self.state]):
                if self.loop_animation:
                    self.current_frame = 0
                else:
                    self.current_frame = 0
                    self.is_attacking = False
                    if self.is_dead:
                        self.current_frame = len(self.animations["Dead"]) - 1
                    elif self.moving_left or self.moving_right:
                        self.state = "Run"
                        self.loop_animation = True
                    else:
                        self.state = "Idle"
                        self.loop_animation = True
            self.image = self.animations[self.state][self.current_frame]
            if not self.facing_right:
                self.image = pygame.transform.flip(self.image, True, False)

        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y
        self.hitbox.center = self.rect.center

        if not final_fight:
            bg_x -= self.velocity_x * 0.2
            if bg_x <= -WINDOW_WIDTH:
                bg_x += WINDOW_WIDTH
            elif bg_x >= WINDOW_WIDTH:
                bg_x -= WINDOW_WIDTH

        self.distance_run += abs(self.velocity_x) * dt

        if not self.on_ground:
            self.velocity_y += 0.5
        if self.rect.y >= WINDOW_HEIGHT - self.rect.height:
            self.rect.y = WINDOW_HEIGHT - self.rect.height
            self.velocity_y = 0
            self.on_ground = True
            if self.state == "Jump":
                self.set_state("Idle", True)

        self.rect.clamp_ip(screen.get_rect())

# House class
class House(pygame.sprite.Sprite):
    def __init__(self, final_fight=False):
        super().__init__()
        self.image = house_image
        self.rect = self.image.get_rect()
        self.final_fight = final_fight
        if final_fight:
            self.rect.x = random.randint(0, WINDOW_WIDTH - self.rect.width)
            self.rect.y = -self.rect.height
            self.velocity_x = 0
            self.velocity_y = 5
        else:
            self.rect.x = WINDOW_WIDTH
            self.rect.y = random.randint(WINDOW_HEIGHT // 2, WINDOW_HEIGHT - self.rect.height)
            self.velocity_x = -5
            self.velocity_y = 0
        self.hitbox = pygame.Rect(0, 0, self.rect.width * 0.14, self.rect.height * 0.14)
        self.hitbox.center = self.rect.center

    def update(self, dt):
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y
        self.hitbox.center = self.rect.center
        if self.final_fight and self.rect.top > WINDOW_HEIGHT:
            self.kill()
        elif not self.final_fight and self.rect.right < 0:
            self.kill()

# Construction class
class Construction(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.width = 50
        self.height = 50
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(GRAY)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = WINDOW_HEIGHT - self.height
        self.hitbox = pygame.Rect(0, 0, self.width * 0.8, self.height * 0.8)
        self.hitbox.center = self.rect.center

    def update(self, dt):
        self.hitbox.center = self.rect.center

# Create sprite groups
player = Player(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 100)
all_sprites = pygame.sprite.Group(player)
houses = pygame.sprite.Group()
constructions = pygame.sprite.Group()

# Font
font = pygame.font.SysFont(None, 74)

# Game state
distance_to_final_fight = 50
final_fight = False
final_fight_timer = 0
final_fight_duration = 10

# Progress bar settings
bar_x = 10
bar_y = 50
bar_width = 200
bar_height = 20
pixel_size = 4

# Spawn settings
house_spawn_timer = 0
house_spawn_interval = 1.5
construction_spawn_timer = 0
construction_spawn_interval = 3.0

# Game loop
clock = pygame.time.Clock()
running = True

while running:
    dt = clock.tick(60) / 1000.0  # 60 FPS

    # Check for final fight
    if not final_fight and player.distance_run >= distance_to_final_fight:
        final_fight = True
        houses.empty()
        constructions.empty()
        house_spawn_timer = 0
        house_spawn_interval = 0.5
        bg_x = 0

    # Spawn houses
    house_spawn_timer += dt
    if house_spawn_timer >= house_spawn_interval and not player.is_dead:
        house_spawn_timer = 0
        new_house = House(final_fight=final_fight)
        houses.add(new_house)
        all_sprites.add(new_house)
        print(f"House spawned at {new_house.rect.x}, {new_house.rect.y}")  # Debug

    # Spawn constructions (only in normal phase)
    construction_spawn_timer += dt
    if construction_spawn_timer >= construction_spawn_interval and not player.is_dead and not final_fight:
        construction_spawn_timer = 0
        new_construction = Construction(WINDOW_WIDTH)
        constructions.add(new_construction)
        all_sprites.add(new_construction)
        print(f"Construction spawned at {new_construction.rect.x}, {new_construction.rect.y}")  # Debug

    # Update final fight timer
    if final_fight and not player.is_dead:
        final_fight_timer += dt
        if final_fight_timer >= final_fight_duration:
            break

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and not player.is_dead:
            if event.key == pygame.K_SPACE and player.on_ground:
                player.set_state("Jump", False)
                player.velocity_y = -15
                player.on_ground = False
            elif event.key == pygame.K_a:
                player.moving_left = True
                player.velocity_x = -5
                player.facing_right = False
                if not player.is_attacking:
                    player.set_state("Run", True)
            elif event.key == pygame.K_d:
                player.moving_right = True
                player.velocity_x = 5
                player.facing_right = True
                if not player.is_attacking:
                    player.set_state("Run", True)
        elif event.type == pygame.KEYUP and not player.is_dead:
            if event.key == pygame.K_a:
                player.moving_left = False
                player.velocity_x = 0
                if not player.moving_right and not player.is_attacking:
                    player.set_state("Idle", True)
            elif event.key == pygame.K_d:
                player.moving_right = False
                player.velocity_x = 0
                if not player.moving_left and not player.is_attacking:
                    player.set_state("Idle", True)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            player.trigger_attack()

    # Update
    all_sprites.update(dt)

    # Check collisions with houses
    for house in houses:
        if player.hitbox.colliderect(house.hitbox):
            if player.is_attacking:
                house.kill()
            elif not player.is_dead:
                player.take_damage()
                house.kill()

    # Check collisions with constructions
    for construction in constructions:
        if player.hitbox.colliderect(construction.hitbox):
            # if player.is_attacking:
            #     construction.kill()
            if not player.is_dead:
                player.take_damage()
                construction.kill()

    # Draw
    if final_fight:
        screen.blit(final_bg, (0, 0))
    else:
        screen.blit(normal_bg, (bg_x, 0))
        screen.blit(normal_bg, (bg_x + WINDOW_WIDTH, 0))

    all_sprites.draw(screen)
    houses.draw(screen)
    constructions.draw(screen)

    # Display HP
    hp_text = font.render(f"HP: {player.hp}", True, WHITE)
    screen.blit(hp_text, (10, 10))

    # Draw progress bar or timer
    if not final_fight:
        progress = min(player.distance_run / distance_to_final_fight, 1)
        fill_width = int(bar_width * progress)
        for x in range(bar_x, bar_x + bar_width + pixel_size, pixel_size):
            for y in range(bar_y, bar_y + bar_height + pixel_size, pixel_size):
                if x == bar_x or x == bar_x + bar_width or y == bar_y or y == bar_y + bar_height:
                    pygame.draw.rect(screen, WHITE, (x, y, pixel_size, pixel_size))
        for x in range(bar_x + pixel_size, bar_x + fill_width, pixel_size):
            for y in range(bar_y + pixel_size, bar_y + bar_height, pixel_size):
                pygame.draw.rect(screen, GREEN, (x, y, pixel_size, pixel_size))
    else:
        timer_text = font.render(f"Survive: {int(final_fight_duration - final_fight_timer)}s", True, WHITE)
        screen.blit(timer_text, (10, 50))

    # Display "GAME OVER"
    if player.is_dead:
        game_over_text = font.render("GAME OVER", True, WHITE)
        screen.blit(game_over_text, (WINDOW_WIDTH // 2 - 150, WINDOW_HEIGHT // 2 - 37))

    pygame.display.flip()

# Display "YOU WIN" if survived
if final_fight and final_fight_timer >= final_fight_duration:
    screen.fill(BLACK)
    win_text = font.render("YOU WIN", True, WHITE)
    screen.blit(win_text, (WINDOW_WIDTH // 2 - 120, WINDOW_HEIGHT // 2 - 37))
    pygame.display.flip()
    pygame.time.wait(2000)

# Quit Pygame
pygame.quit()