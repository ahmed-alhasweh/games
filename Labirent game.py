import pygame
import sys
import random

# Ekran boyutları
WIDTH = 820
HEIGHT = 725

# Renkler
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Labirent haritası
MAP = [
    "XXXXXXXXXXXXXXXXXXXX",
    "X   X    X   X     X",
    "X X X XX X XX X   XX",
    "X X     X X X  X   X",
    "X XXXXX X X X XX   X",
    "X          X       X",
    "X XXXXX X XXXX  XX X",
    "X X   X X   X      X",
    "X X X X XXX X X   XX",
    "X X X   X     X    X",
    "X X XXXXX XXXXX   XX",
    "X   X   X          X",
    "X X X X X X X X    X",
    "X X X X X X X X    X",
    "X X   X X X   X    X",
    "X XXXXX X XXXXX    X",
    "X                  X",
    "XXXXXX XXXXXXXX    C",
]

# Oyuncu hızı
PLAYER_SPEED = 3

# Pencere oluştur
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Labirent Oyunu")
clock = pygame.time.Clock()

# Font ayarları
font = pygame.font.Font(None, 74)

# Oyuncu sınıfı
class Player(pygame.sprite.Sprite):
    def __init__(self, color, start_pos):
        super().__init__()
        self.image = pygame.Surface((25, 25))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = start_pos

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

        # Duvarlarla çarpışmayı kontrol et
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dx > 0:  # Sağa gitme
                    self.rect.right = wall.rect.left
                if dx < 0:  # Sola gitme
                    self.rect.left = wall.rect.right
                if dy > 0:  # Aşağı gitme
                    self.rect.bottom = wall.rect.top
                if dy < 0:  # Yukarı gitme
                    self.rect.top = wall.rect.bottom

# Duvar sınıfı
class Wall(pygame.sprite.Sprite):
    def __init__(self, color, rect):
        super().__init__()
        self.image = pygame.Surface(rect.size)
        self.image.fill(color)
        self.rect = rect

# Labirent oluştur
all_sprites = pygame.sprite.Group()
walls = pygame.sprite.Group()
exit_pos = None  # Çıkış pozisyonunu saklamak için

for y, row in enumerate(MAP):
    for x, char in enumerate(row):
        if char == "X":
            wall = Wall(BLACK, pygame.Rect(x * 40, y * 40, 40, 40))
            all_sprites.add(wall)
            walls.add(wall)
        elif char == "C":
            exit_pos = (x * 40, y * 40)
            exit_wall = Wall(BLUE, pygame.Rect(exit_pos[0], exit_pos[1], 40, 40))  # Çıkışı göstermek için mavi bir duvar ekleyin
            all_sprites.add(exit_wall)

def get_random_start():
    available_starts = []
    for y, row in enumerate(MAP):
        for x, char in enumerate(row):
            if char == " ":
                available_starts.append((x * 40 + 25, y * 40 + 25))  # مركز الخلية
    return random.choice(available_starts) if available_starts else None

player1_start = get_random_start()
player2_start = get_random_start()

player1 = Player(RED, player1_start)
player2 = Player(GREEN, player2_start)
all_sprites.add(player1)
all_sprites.add(player2)

# Oyun döngüsü
running = True
winner = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Oyuncu hareket kontrolleri
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        player1.move(0, -PLAYER_SPEED)
    if keys[pygame.K_DOWN]:
        player1.move(0, PLAYER_SPEED)
    if keys[pygame.K_LEFT]:
        player1.move(-PLAYER_SPEED, 0)
    if keys[pygame.K_RIGHT]:
        player1.move(PLAYER_SPEED, 0)

    if keys[pygame.K_w]:
        player2.move(0, -PLAYER_SPEED)
    if keys[pygame.K_s]:
        player2.move(0, PLAYER_SPEED)
    if keys[pygame.K_a]:
        player2.move(-PLAYER_SPEED, 0)
    if keys[pygame.K_d]:
        player2.move(PLAYER_SPEED, 0)

    # Oyun alanı sınırlarını kontrol et
    player1.rect.clamp_ip(screen.get_rect())
    player2.rect.clamp_ip(screen.get_rect())

    # Oyuncuların çıkışa ulaşıp ulaşmadığını kontrol et
    if player1.rect.colliderect(pygame.Rect(exit_pos, (40, 40))):
        winner = "Kırmızı Oyuncu"
        running = False
    elif player2.rect.colliderect(pygame.Rect(exit_pos, (40, 40))):
        winner = "Yeşil Oyuncu"
        running = False

    # Ekranı temizle و güncelle
    screen.fill(WHITE)
    all_sprites.draw(screen)

    # Kazanan varsa, kazananın ismini ekrana yaz
    if winner:
        text = font.render(f"Kazanan: {winner}", True, RED)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)
        pygame.display.flip()  # Kazanan metnini ekrana çizdirmek için ekranı güncelle
        pygame.time.wait(5000)  # Kazanan metnini 5 saniye ekranda tut
        break  # Döngüyü kırarak kazanan metni ekranda kalırken diğer işlemleri durdur

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
