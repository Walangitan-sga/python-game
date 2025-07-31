import pygame
import sys
import random

# Konstanta
WIDTH, HEIGHT = 900, 600
FPS = 60
PLAYER_SPEED = 6
BULLET_SPEED = 14

# Warna
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,60,60)  
GREEN = (60,255,60)
BLUE = (60,120,255)
YELLOW = (255,255,60)
GRAY = (40,40,40)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooter 2D Simple")
clock = pygame.time.Clock()
font = pygame.font.SysFont('arial', 32)

# Player
player_img = pygame.Surface((50, 50), pygame.SRCALPHA)
pygame.draw.rect(player_img, BLUE, (0, 0, 50, 50), border_radius=12)
player_rect = player_img.get_rect(center=(100, HEIGHT//2))

# Tombol virtual (untuk mobile/touch)
BTN_SIZE = 60
BTN_MARGIN = 18
btns = {
    "up": pygame.Rect(BTN_MARGIN+BTN_SIZE, HEIGHT-BTN_MARGIN-3*BTN_SIZE, BTN_SIZE, BTN_SIZE),
    "down": pygame.Rect(BTN_MARGIN+BTN_SIZE, HEIGHT-BTN_MARGIN-BTN_SIZE, BTN_SIZE, BTN_SIZE),
    "left": pygame.Rect(BTN_MARGIN, HEIGHT-BTN_MARGIN-2*BTN_SIZE, BTN_SIZE, BTN_SIZE),
    "right": pygame.Rect(BTN_MARGIN+2*BTN_SIZE, HEIGHT-BTN_MARGIN-2*BTN_SIZE, BTN_SIZE, BTN_SIZE),
    "shoot": pygame.Rect(WIDTH-BTN_MARGIN-BTN_SIZE, HEIGHT-BTN_MARGIN-2*BTN_SIZE, BTN_SIZE, BTN_SIZE),
    "pause": pygame.Rect(WIDTH-BTN_MARGIN-BTN_SIZE, BTN_MARGIN, BTN_SIZE, BTN_SIZE)
}
btn_colors = {
    "up": (120,120,255),
    "down": (120,120,255),
    "left": (120,120,255),
    "right": (120,120,255),
    "shoot": (255,200,60),
    "pause": (200,200,200)
}
btn_labels = {
    "up": "▲",
    "down": "▼",
    "left": "◀",
    "right": "▶",
    "shoot": "●",
    "pause": "II"
}

# Enemy types
ENEMY_TYPES = [
    {"color": RED, "hp": 1, "speed": 2, "size": 50},
    {"color": (255,180,60), "hp": 3, "speed": 1, "size": 60}, # Tank
    {"color": (120,255,255), "hp": 1, "speed": 4, "size": 35}, # Fast
]

def spawn_enemy():
    t = random.choice(ENEMY_TYPES)
    y = random.randint(60, HEIGHT-60)
    surf = pygame.Surface((t["size"], t["size"]), pygame.SRCALPHA)
    pygame.draw.rect(surf, t["color"], (0,0,t["size"],t["size"]), border_radius=12)
    rect = surf.get_rect(midleft=(WIDTH+30, y))
    return {"rect": rect, "surf": surf, "hp": t["hp"], "maxhp": t["hp"], "speed": t["speed"]}


def reset_player_and_enemies():
    player_rect.center = (100, HEIGHT//2)
    return [spawn_enemy()]

def game_loop():
    enemies = [spawn_enemy()]
    bullets = []
    score = 0
    lives = 3
    running = True
    move_touch = {"up": False, "down": False, "left": False, "right": False, "shoot": False, "pause": False}
    game_over = False
    paused = False

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if not game_over:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_SPACE:
                        bullet = pygame.Rect(player_rect.right, player_rect.centery-5, 18, 10)
                        bullets.append(bullet)
                    if event.key == pygame.K_l:
                        if not paused:
                            paused = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = event.pos
                    on_btn = False
                    for k, rect in btns.items():
                        if rect.collidepoint(mx, my):
                            move_touch[k] = True
                            on_btn = True
                            if k == "shoot":
                                bullet = pygame.Rect(player_rect.right, player_rect.centery-5, 18, 10)
                                bullets.append(bullet)
                            if k == "pause" and not paused:
                                paused = True
                    if event.button == 1 and not on_btn:
                        bullet = pygame.Rect(player_rect.right, player_rect.centery-5, 18, 10)
                        bullets.append(bullet)
                if event.type == pygame.MOUSEBUTTONUP:
                    for k in move_touch:
                        move_touch[k] = False
            else:
                # Game over: klik/tap/tekan tombol apapun untuk restart
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    enemies = [spawn_enemy()]
                    bullets = []
                    score = 0
                    lives = 3
                    game_over = False
                    player_rect.center = (100, HEIGHT//2)
        # PAUSE HANDLING
        if paused:
            unpause = False
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_l:
                    unpause = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = event.pos
                    if btns["pause"].collidepoint(mx, my):
                        unpause = True
            if unpause:
                paused = False
            # Draw pause overlay
            screen.fill(GRAY)
            pause_text = font.render("PAUSED", True, YELLOW)
            screen.blit(pause_text, (WIDTH//2 - pause_text.get_width()//2, HEIGHT//2-40))
            instr = font.render("Tekan L / tombol II untuk lanjut", True, WHITE)
            screen.blit(instr, (WIDTH//2 - instr.get_width()//2, HEIGHT//2+10))
            pygame.draw.rect(screen, btn_colors["pause"], btns["pause"], border_radius=16)
            label = font.render(btn_labels["pause"], True, BLACK)
            lx = btns["pause"].centerx - label.get_width()//2
            ly = btns["pause"].centery - label.get_height()//2
            screen.blit(label, (lx, ly))
            pygame.display.flip()
            continue

        if not game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w] or keys[pygame.K_UP] or move_touch["up"]:
                player_rect.y -= PLAYER_SPEED
            if keys[pygame.K_s] or keys[pygame.K_DOWN] or move_touch["down"]:
                player_rect.y += PLAYER_SPEED
            if keys[pygame.K_a] or keys[pygame.K_LEFT] or move_touch["left"]:
                player_rect.x -= PLAYER_SPEED
            if keys[pygame.K_d] or keys[pygame.K_RIGHT] or move_touch["right"]:
                player_rect.x += PLAYER_SPEED
            player_rect.clamp_ip(screen.get_rect())

            # Update bullet
            for bullet in bullets:
                bullet.x += BULLET_SPEED
            bullets = [b for b in bullets if b.x < WIDTH]

            # Update enemy
            for enemy in enemies:
                enemy["rect"].x -= enemy["speed"]
            enemies = [e for e in enemies if e["rect"].right > 0]
            if len(enemies) < 3 and random.random() < 0.02:
                enemies.append(spawn_enemy())

            # Collision
            for bullet in bullets[:]:
                for enemy in enemies[:]:
                    if bullet.colliderect(enemy["rect"]):
                        bullets.remove(bullet)
                        enemy["hp"] -= 1
                        if enemy["hp"] <= 0:
                            enemies.remove(enemy)
                            score += 1
                        break
            for enemy in enemies:
                if player_rect.colliderect(enemy["rect"]):
                    lives -= 1
                    if lives > 0:
                        player_rect.center = (100, HEIGHT//2)
                        enemies = [spawn_enemy()]
                        bullets = []
                        break
                    else:
                        game_over = True

        # Draw
        screen.fill(GRAY)
        screen.blit(player_img, player_rect)
        for bullet in bullets:
            pygame.draw.rect(screen, YELLOW, bullet, border_radius=4)
        for enemy in enemies:
            screen.blit(enemy["surf"], enemy["rect"])
            # HP bar
            if enemy["maxhp"] > 1:
                bar_w = enemy["rect"].width
                hp_w = int(bar_w * enemy["hp"] / enemy["maxhp"])
                pygame.draw.rect(screen, RED, (enemy["rect"].x, enemy["rect"].y-10, bar_w, 6), border_radius=3)
                pygame.draw.rect(screen, GREEN, (enemy["rect"].x, enemy["rect"].y-10, hp_w, 6), border_radius=3)
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (20, 20))
        lives_text = font.render(f"Lives: {lives}", True, WHITE)
        screen.blit(lives_text, (20, 60))
        instr = font.render("WASD/Arrow: Gerak | SPACE: Tembak | ESC: Keluar / Tombol layar HP", True, WHITE)
        screen.blit(instr, (20, HEIGHT-40))

        # Draw virtual buttons
        for k, rect in btns.items():
            pygame.draw.rect(screen, btn_colors[k], rect, border_radius=16)
            label = font.render(btn_labels[k], True, BLACK)
            lx = rect.centerx - label.get_width()//2
            ly = rect.centery - label.get_height()//2
            screen.blit(label, (lx, ly))

        # Game over overlay
        if game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0,0,0,180))
            screen.blit(overlay, (0,0))
            go_text = font.render("GAME OVER", True, RED)
            screen.blit(go_text, (WIDTH//2 - go_text.get_width()//2, HEIGHT//2-60))
            score_text2 = font.render(f"Score: {score}", True, WHITE)
            screen.blit(score_text2, (WIDTH//2 - score_text2.get_width()//2, HEIGHT//2))
            restart_text = font.render("Tap/tekan tombol apapun untuk restart", True, YELLOW)
            screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2+60))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    game_loop()
