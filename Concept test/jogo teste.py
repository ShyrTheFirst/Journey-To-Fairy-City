import pygame
import random

# Inicializa o Pygame
pygame.init()

# Define as dimensões da janela
screen_width = 800
screen_height = 600

# Cria a janela do jogo
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Jogo')

# Define as cores utilizadas no jogo
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)

# Define as fontes utilizadas na HUD
font = pygame.font.SysFont(None, 30)

score = 0
#Cria os ataques
attack_group = pygame.sprite.Group()

#Cria todos os sprites
all_sprites = pygame.sprite.Group()


# Classe do jogador
class Player(pygame.sprite.Sprite):
    def __init__(self):
            super().__init__()
            self.image = pygame.Surface((50, 50))
            self.image.fill(green)
            self.rect = self.image.get_rect()
            self.rect.x = screen_width / 2
            self.rect.y = screen_height / 2
            self.health = 50
            self.direction = 'right'
     

    def update(self, dx, dy):
            self.rect.x += dx
            self.rect.y += dy

        # Mantém o jogador dentro da tela
            if self.rect.x < 0:
                self.rect.x = 0
            elif self.rect.x > screen_width - 50:
                self.rect.x = screen_width - 50
            if self.rect.y < 0:
                self.rect.y = 0
            elif self.rect.y > screen_height - 50:
                self.rect.y = screen_height - 50

    def attack(self):
            ax = self.rect.x +25
            ay = self.rect.y +25
            adir = self.direction
            attack = Attack(ax,ay,adir)
            attack_group.add(attack)
            all_sprites.add(attack_group)
########################################################################################################################################
# Classe do inimigo
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
            super().__init__()
            self.image = pygame.Surface((40, 40))
            self.image.fill(red)
            self.rect = self.image.get_rect()
            self.rect.x = random.randint(0, screen_width - 40)
            self.rect.y = random.randint(0, screen_height - 40)
            self.health = 50
            self.speed = 0.7
            self.dx = 0
            self.dy = 0

    def update(self,x,y):
        # Movimenta o inimigo em direção ao jogador
            player_pos = player.rect.center
            enemy_pos = self.rect.center
            dx, dy = player_pos[0] - enemy_pos[0], player_pos[1] - enemy_pos[1]
            dist = (dx ** 2 + dy ** 2) ** 0.5
            if dist != 0:
                    dx, dy = dx / dist, dy / dist
            self.dx, self.dy = dx * self.speed, dy * self.speed
            self.rect.x += self.dx
            self.rect.y += self.dy

        # Verifica colisão com o jogador
            if pygame.sprite.collide_rect(self, player):
                self.image.fill(black)
                player.health -= 1
         
    def draw_health(self, x, y):
    # Desenha a barra de vida do inimigo acima dele
            pygame.draw.rect(screen, red, (x, y, self.health, 5))

#Classe do ataque do jogador
class Attack(pygame.sprite.Sprite):
        def __init__(self, x, y, direction):
            super().__init__()
            self.image = pygame.Surface((5, 5))
            self.image.fill(green)
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.speed = 5
            self.direction = direction
        def update(self,x,y):
    # Movimenta o ataque na direção em que o jogador está se movendo
            if self.direction == 'left':
                    self.rect.x -= self.speed
            elif self.direction == 'right':
                    self.rect.x += self.speed
            elif self.direction == 'up':
                    self.rect.y -= self.speed
            elif self.direction == 'down':
                    self.rect.y += self.speed

    # Verifica colisão com os inimigos
            hit_enemies = pygame.sprite.spritecollide(self, enemies, True)
            for enemy in hit_enemies:
                    global score
                    score += 1

    # Remove o ataque da tela quando atinge as bordas
            if self.rect.x < 0 or self.rect.x > screen_width or self.rect.y < 0 or self.rect.y > screen_height:
                    self.kill()

#Classe da HUD
class HUD:
    def draw(self):
# Desenha as informações na tela
            health_text = font.render('Health: ' + str(player.health), True, black)
            score_text = font.render('Score: ' + str(score), True, black)
            screen.blit(health_text, (10, 10))
            screen.blit(score_text, (screen_width - score_text.get_width() - 10, 10))
            for i, enemy in enumerate(enemies.sprites()):
                    enemy.draw_health(enemy.rect.x, enemy.rect.y - 10)

#Cria o jogador
player = Player()
#Cria os inimigos
enemies = pygame.sprite.Group()
for i in range(5):
    enemies.add(Enemy())


all_sprites.add(player)
all_sprites.add(enemies)

#Cria a HUD
hud = HUD()

#Define a velocidade de atualização da tela
clock = pygame.time.Clock()

#Define a variável para controlar o jogo
game_running = True

lx = 0
rx = 0


while game_running:
# Processa eventos do Pygame
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    game_running = False
            elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        
                        lx -= 5
                        player.update(lx, 0)
                        player.direction = 'left'
                    elif event.key == pygame.K_RIGHT:
                        player.update(5, 0)
                        player.direction = 'right'
                    elif event.key == pygame.K_UP:
                        player.update(0, -5)
                        player.direction = 'up'
                    elif event.key == pygame.K_DOWN:
                        player.update(0, 5)
                        player.direction = 'down'
                    elif event.key == pygame.K_e:
                        player.attack()
                    elif event.type == pygame.KEYUP:
                        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                                player.update(0, 0)
                        elif event.key == pygame== pygame.K_DOWN:
                                player.update(0, 0)

    # Cria um novo inimigo após 30 segundos
    if pygame.time.get_ticks() % 30000 == 0:
            enemies.add(Enemy())
            all_sprites.add(enemies.sprites()[-1])

# Atualiza todos os sprites
    all_sprites.update(0,0)
    attack_group.update(0,0)

# Desenha todos os sprites na tela
    screen.fill(white)
    all_sprites.draw(screen)

# Desenha a HUD
    hud.draw()

# Atualiza a tela
    pygame.display.flip()

# Limita a velocidade de atualização da tela
    clock.tick(60)

# Verifica se o jogador morreu
    if player.health <= 0:
        # Tela de fim de jogo
            end_game = True
            while end_game:
                    # Desenha a tela de fim de jogo
                    screen.fill(black)
                    
                    end_text = font.render('Game Over', True, white)
                    score_text = font.render('Score: ' + str(score), True, white)
                    press_enter_text = font.render('Press ENTER to play again', True, white)
                    screen.blit(end_text, (screen_width//2 - end_text.get_width()//2, screen_height//2 - end_text.get_height()//2 - 30))
                    screen.blit(score_text, (screen_width//2 - score_text.get_width()//2, screen_height//2 - score_text.get_height()//2 + 10))
                    screen.blit(press_enter_text, (screen_width//2 - press_enter_text.get_width()//2, screen_height//2 - press_enter_text.get_height()//2 + 50))
                    pygame.display.update()

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            end_game = False
                            game_running = False
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_RETURN:
                            # Reinicia o jogo
                                player.health = 50
                                score = 0
                            for enemy in enemies.sprites():
                                    enemy.kill()
                            for Attacks in attack_group.sprites():
                                    Attacks.kill()
                            enemies.add(Enemy())
                            all_sprites.add(enemies.sprites()[-1])
                            end_game = False

pygame.quit()
