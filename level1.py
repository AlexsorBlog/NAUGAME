# level1.py
import pygame
import random

# Налаштування вікна
WIDTH, HEIGHT = 400, 700
FPS = 60

# Колір
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE_BLUE = (111, 136, 204)
DARK_BLUE = (86, 83, 131)
LIGHT_BLUE = (197, 216, 235)
GREEN = (0, 255, 0)

# Ініціалізація Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Знайти Луцького")
pygame.display.set_icon(pygame.image.load("./graphics/icon.bmp"))
clock = pygame.time.Clock()

# Завантаження зображень
player_img = pygame.image.load("graphics/player.png")
enemy_img = pygame.image.load("graphics/enemy.png")
bullet_img = pygame.image.load("graphics/bullet.png")
background = pygame.image.load("graphics/background.jpg")
full_heart = pygame.transform.scale(pygame.image.load("graphics/full_heart.png"), (40, 40))
empty_heart = pygame.transform.scale(pygame.image.load("graphics/empty_heart.png"), (40, 40))
upgrade_double_img = pygame.transform.scale(pygame.image.load("graphics/upgrade_double.png"), (30, 30))
upgrade_diagonal_img = pygame.transform.scale(pygame.image.load("graphics/upgrade_diagonal.png"), (30, 30))

background = pygame.transform.scale(background, (WIDTH + 300, HEIGHT))

# ======= Класи ======= #
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(player_img, (80, 80))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 60)
        self.speed = 5
        self.mask = pygame.mask.from_surface(self.image)
        self.shoot_delay = 650
        self.last_shot = pygame.time.get_ticks()
        self.double_shot = False
        self.diagonal_shot = False

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.shoot()
            self.last_shot = now

    def shoot(self):
        if self.double_shot and self.diagonal_shot:
            bullet1 = Bullet(self.rect.centerx - 10, self.rect.top, 0, -20)
            bullet2 = Bullet(self.rect.centerx + 10, self.rect.top, 0, -20)
            bullet3 = Bullet(self.rect.centerx, self.rect.top, -5, -20)
            bullet4 = Bullet(self.rect.centerx, self.rect.top, 5, -20)
            all_sprites.add(bullet1, bullet2, bullet3, bullet4)
            player_bullets.add(bullet1, bullet2, bullet3, bullet4)
        elif self.double_shot:
            bullet1 = Bullet(self.rect.centerx - 10, self.rect.top, 0, -20)
            bullet2 = Bullet(self.rect.centerx + 10, self.rect.top, 0, -20)
            all_sprites.add(bullet1, bullet2)
            player_bullets.add(bullet1, bullet2)
        elif self.diagonal_shot:
            bullet1 = Bullet(self.rect.centerx, self.rect.top, -5, -20)
            bullet2 = Bullet(self.rect.centerx, self.rect.top, 5, -20)
            bullet3 = Bullet(self.rect.centerx, self.rect.top, 0, -20)
            all_sprites.add(bullet1, bullet2, bullet3)
            player_bullets.add(bullet1, bullet2, bullet3)
        else:
            bullet = Bullet(self.rect.centerx, self.rect.top, 0, -20)
            all_sprites.add(bullet)
            player_bullets.add(bullet)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speed_x, speed_y):
        super().__init__()
        self.image = pygame.transform.scale(bullet_img, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.top > HEIGHT or self.rect.bottom < 0 or self.rect.left > WIDTH or self.rect.right < 0:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, level):
        super().__init__()
        self.image = pygame.transform.scale(enemy_img, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(50, WIDTH - 50), -40)
        self.shoot_delay = 900
        self.speed_x = 3
        self.speed_y = 1
        self.direction = -1
        self.last_shot = pygame.time.get_ticks()
        self.mask = pygame.mask.from_surface(self.image)
        self.level = level
        self.hp = 2 if level >= 3 else 1

    def update(self):
        now = pygame.time.get_ticks()
        self.rect.x += self.speed_x * self.direction
        self.rect.y += self.speed_y
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.direction *= -1
        if self.rect.bottom >= HEIGHT:
            print("Гру завершено! Ворог досяг землі!")
            pygame.quit()
            exit()
        if pygame.sprite.spritecollide(self, player_group, False, pygame.sprite.collide_mask):
            print("Гру завершено! Ворог зіткнувся з гравцем!")
            pygame.quit()
            exit()
        if now - self.last_shot > self.shoot_delay:
            self.shoot()
            self.last_shot = now

    def shoot(self):
        if self.level < 4:
            bullet = Bullet(self.rect.centerx, self.rect.bottom, 0, 6)
            all_sprites.add(bullet)
            bullets.add(bullet)
        else:
            bullet_center = Bullet(self.rect.centerx, self.rect.bottom, 0, 3)
            bullet_left = Bullet(self.rect.centerx, self.rect.bottom, -3, 3)
            bullet_right = Bullet(self.rect.centerx, self.rect.bottom, 3, 3)
            all_sprites.add(bullet_center, bullet_left, bullet_right)
            bullets.add(bullet_center, bullet_left, bullet_right)

    def hit(self):
        self.hp -= 1
        if self.hp <= 0:
            self.kill()
            explosion = Explosion(self.rect.centerx, self.rect.centery)
            all_sprites.add(explosion)
            if random.random() < 0.3:
                upgrade_type = random.choice(["double", "diagonal"])
                if upgrade_type == "double":
                    upgrade = UpgradeDouble(self.rect.centerx, self.rect.centery)
                else:
                    upgrade = UpgradeDiagonal(self.rect.centerx, self.rect.centery)
                all_sprites.add(upgrade)
                upgrades.add(upgrade)

class UpgradeDouble(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = upgrade_double_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed_y = 3
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > HEIGHT:
            self.kill()

class UpgradeDiagonal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = upgrade_diagonal_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed_y = 3
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > HEIGHT:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.frames = [
            pygame.transform.scale(pygame.image.load(f"graphics/explosion{i}.png"), (70, 70))
            for i in range(1, 4)
        ]
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=(x, y))
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 70

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame_index += 1
            if self.frame_index < len(self.frames):
                self.image = self.frames[self.frame_index]
            else:
                self.kill()

class Game:
    def __init__(self):
        self.running = True
        self.playing = False
        self.paused = False
        self.player = Player()
        self.player_group = pygame.sprite.GroupSingle(self.player)
        self.enemies = pygame.sprite.Group()
        self.bg_y = 0
        self.bg_speed = 2
        all_sprites.add(self.player)
        self.score = 0
        self.font = pygame.font.Font("style/Pixel_Font-7.ttf", 36)
        self.enemy_spawn_time = 2000
        self.hp = 3
        self.max_hp = 3
        self.last_enemy_spawn = pygame.time.get_ticks()
        self.level = 1
        self.last_level_update = pygame.time.get_ticks()
        self.spawn_enemy()

    def draw_button(self, text, x, y, inactive_color, active_color):
        button_text = self.font.render(text, True, WHITE)
        padding_x, padding_y = 20, 10
        width = button_text.get_width() + padding_x * 2
        height = button_text.get_height() + padding_y * 2
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        button_rect = pygame.Rect(x, y, width, height)
        if button_rect.collidepoint(mouse):
            pygame.draw.rect(screen, active_color, (x, y, width, height), border_radius=20)
            if click[0] == 1:
                return True
        else:
            pygame.draw.rect(screen, inactive_color, (x, y, width, height), border_radius=20)
        text_rect = button_text.get_rect(center=(x + width // 2, y + height // 2))
        screen.blit(button_text, text_rect)
        return False

    def show_start_screen(self):
        screen.blit(background, (0, self.bg_y))
        text = self.font.render("Level 1:"
                                "Знайти Луцького", True, WHITE)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 100))
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            if self.draw_button("Грати", WIDTH // 2 - (self.font.render("Грати", True, WHITE).get_width() + 40) // 2, HEIGHT // 2, DARK_BLUE, WHITE_BLUE):
                waiting = False
            pygame.display.flip()

    def show_game_over_screen(self):
        all_sprites.empty()
        self.enemies.empty()
        bullets.empty()
        player_bullets.empty()
        upgrades.empty()
        screen.blit(background, (0, 0))
        text1 = self.font.render("Ви програли!", True, RED)
        text2 = self.font.render(f"Рахунок: {self.score}", True, WHITE)
        screen.blit(text1, (WIDTH // 2 - text1.get_width() // 2, HEIGHT // 3 - 75))
        screen.blit(text2, (WIDTH // 2 - text2.get_width() // 2, HEIGHT // 2 - 100))
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            if self.draw_button("Грати знову", WIDTH // 2 - (self.font.render("Грати знову", True, WHITE).get_width() + 40) // 2, HEIGHT // 2 - 10, DARK_BLUE, WHITE_BLUE):
                waiting = False
                self.reset_game()
            pygame.display.flip()

    def show_win_screen(self):
        all_sprites.empty()
        self.enemies.empty()
        bullets.empty()
        player_bullets.empty()
        upgrades.empty()
        screen.blit(background, (0, 0))
        text1 = self.font.render("Ви перемогли!", True, GREEN)
        text2 = self.font.render(f"Рахунок: {self.score}", True, WHITE)
        screen.blit(text1, (WIDTH // 2 - text1.get_width() // 2, HEIGHT // 3 - 75))
        screen.blit(text2, (WIDTH // 2 - text2.get_width() // 2, HEIGHT // 2 - 100))
        pygame.display.flip()
        pygame.time.wait(2000)  # Show win screen for 2 seconds
        self.playing = False  # Exit game loop

    def show_pause_screen(self):
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        pause_text = self.font.render("Пауза", True, WHITE)
        continue_text = self.font.render("Натисніть ESC для продовження", True, WHITE)
        screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2 - 50))
        screen.blit(continue_text, (WIDTH // 2 - continue_text.get_width() // 2, HEIGHT // 2 + 10))
        pygame.display.flip()
        pygame.event.clear()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    waiting = False

    def reset_game(self):
        self.playing = True
        self.paused = False
        self.score = 0
        self.hp = 3
        self.level = 1
        self.last_level_update = pygame.time.get_ticks()
        self.enemy_spawn_time = 2000
        self.player = Player()
        all_sprites.empty()
        self.enemies.empty()
        bullets.empty()
        player_bullets.empty()
        upgrades.empty()
        all_sprites.add(self.player)
        self.player_group.empty()
        self.player_group.add(self.player)
        self.last_enemy_spawn = pygame.time.get_ticks()
        self.spawn_enemy()

    def spawn_enemy(self):
        positions = []
        enemy_count = 1 if self.level == 1 else random.randint(2, 3)
        for _ in range(enemy_count):
            while True:
                x = random.randint(50, WIDTH - 50)
                y = random.randint(-150, -70)
                overlap = False
                for pos in positions:
                    if abs(x - pos[0]) < 60 and abs(y - pos[1]) < 60:
                        overlap = True
                        break
                if not overlap:
                    break
            positions.append((x, y))
            enemy = Enemy(self.level)
            enemy.rect.center = (x, y)
            self.enemies.add(enemy)
            all_sprites.add(enemy)

    def run(self):
        self.show_start_screen()
        self.playing = True
        while self.playing:
            clock.tick(FPS)
            self.events()
            if not self.paused:
                self.update()
            self.draw()
        return self.score >= 12  # Return True if won, False if lost or quit

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.paused = not self.paused
                if self.paused:
                    self.show_pause_screen()

    def update(self):
        all_sprites.update()
        self.bg_y += self.bg_speed
        if self.bg_y >= HEIGHT:
            self.bg_y = 0

        now = pygame.time.get_ticks()
        if now - self.last_level_update >= 15000 and self.level < 4:
            self.level += 1
            self.last_level_update = now
            if self.level == 1:
                self.enemy_spawn_time = 6000
            elif self.level == 2:
                self.enemy_spawn_time = 5000
            elif self.level == 3:
                self.enemy_spawn_time = 4000
            elif self.level == 4:
                self.enemy_spawn_time = 3000
            print(f"Рівень підвищено до {self.level}")

        if now - self.last_enemy_spawn > self.enemy_spawn_time:
            self.spawn_enemy()
            self.last_enemy_spawn = now

        for enemy in self.enemies:
            if pygame.sprite.spritecollide(enemy, player_bullets, True, pygame.sprite.collide_mask):
                enemy.hit()
                self.score += 1
                if self.score >= 12:
                    self.show_win_screen()
                    return  # Exit update to end game loop

        for upgrade in pygame.sprite.spritecollide(self.player, upgrades, True, pygame.sprite.collide_mask):
            if isinstance(upgrade, UpgradeDouble):
                self.player.double_shot = True
            elif isinstance(upgrade, UpgradeDiagonal):
                self.player.diagonal_shot = True

        if pygame.sprite.spritecollide(self.player, bullets, True, pygame.sprite.collide_mask):
            self.hp -= 1
            if self.hp <= 0:
                print("Гравець отримав удар!")
                self.running = False
                self.show_game_over_screen()

        if pygame.sprite.spritecollide(self.player, self.enemies, False, pygame.sprite.collide_mask):
            self.hp -= 1
            if self.hp <= 0:
                print("Герой загинув через зіткнення!")
                self.playing = False
                self.show_game_over_screen()

    def draw_score(self):
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))

    def draw_hearts(self):
        for i in range(self.max_hp):
            x = WIDTH - (self.max_hp - i) * 40 - 15
            y = 10
            if i < self.hp:
                screen.blit(full_heart, (x, y))
            else:
                screen.blit(empty_heart, (x, y))

    def draw(self):
        screen.blit(background, (0, self.bg_y))
        screen.blit(background, (0, self.bg_y - HEIGHT))
        all_sprites.draw(screen)
        self.draw_score()
        self.draw_hearts()
        pygame.display.flip()

# Групи
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player_group = pygame.sprite.GroupSingle()
player_bullets = pygame.sprite.Group()
upgrades = pygame.sprite.Group()

def run_level1():
    game = Game()
    return game.run()

if __name__ == "__main__":
    run_level1()
    pygame.quit()