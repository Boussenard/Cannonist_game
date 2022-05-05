import pygame
import sys
import random


class Cannon(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.angle = 0
        self.rotate = 0
        self.end = 0
        self.pressed = 'w'
        self.can_shoot = True

        self.image = pygame.image.load('data/Cannon.png').convert_alpha()
        self.rect = self.image.get_rect(center=(400, 350))
        self.img_copy = self.image

        self.bullet_pos = (400, 295)

    def change_rotate(self, key_input):
        # W
        if key_input[pygame.K_w]:
            if self.pressed == 'a':
                self.rotate = -15
            else:
                self.rotate = 15
            self.end = 0
            self.pressed = 'w'
            self.bullet_pos = (400, 295)
            self.can_shoot = False
        # A
        elif key_input[pygame.K_a]:
            if self.pressed == 's':
                self.rotate = -15
            else:
                self.rotate = 15
            self.end = 90
            self.pressed = 'a'
            self.bullet_pos = (345, 350)
            self.can_shoot = False
        # S
        elif key_input[pygame.K_s]:
            if self.pressed == 'd':
                self.rotate = -15
            else:
                self.rotate = 15
            self.end = 180
            self.pressed = 's'
            self.bullet_pos = (400, 405)
            self.can_shoot = False
        # D
        elif key_input[pygame.K_d]:
            if self.pressed == 'w':
                self.rotate = -15
            else:
                self.rotate = 15
            self.end = 270
            self.pressed = 'd'
            self.bullet_pos = (455, 350)
            self.can_shoot = False

    def update(self):
        # Continuing rotation or stopping it
        if self.angle != self.end:
            self.angle += self.rotate
        else:
            self.rotate = 0
            self.can_shoot = True

        # If cords are getting too big or too low cutting them down
        if self.angle == 360:
            self.angle = 0
        if self.angle < 0:
            self.angle += 360

        # Drawing up and rotating our stuff
        self.img_copy = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.img_copy.get_rect(center=(400, 350))

    def death(self):
        if pygame.sprite.spritecollide(cannon, enemy_group, False):
            return True

    def create_bullet(self):
        return Bullet(self.bullet_pos[0], self.bullet_pos[1])


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = pygame.image.load('data/Bullet.png').convert_alpha()
        self.rect = self.image.get_rect(center=(pos_x, pos_y))

    def update(self):
        # W
        if self.rect.centery <= 295:
            self.rect.y -= 8
        # S
        elif self.rect.centery >= 405:
            self.rect.y += 8
        # A
        elif self.rect.centerx <= 345:
            self.rect.x -= 8
        # D
        elif self.rect.centerx >= 455:
            self.rect.x += 8

        if self.rect.y < 0 or self.rect.y > 700 or self.rect.x < 0 or self.rect.x > 800:
            self.kill()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill('Red')
        self.rect = self.image.get_rect(center=(x_pos, y_pos))

    def update(self):
        # goes up
        if self.rect.centery >= 350:
            self.rect.y -= 5
        # goes down
        if self.rect.centery <= 350:
            self.rect.y += 5
        # goes left
        if self.rect.centerx >= 400:
            self.rect.x -= 5
        # goes right
        if self.rect.centerx <= 400:
            self.rect.x += 5


def messages():
    game_name = font_big.render('Cannonist', False, (20, 20, 20))
    game_name_rect = game_name.get_rect(center=(400, 50))

    game_message_11 = font.render('Use WASD to', False, (20, 20, 20))
    game_message_12 = font.render('spin the cannon', False, (20, 20, 20))

    game_message_21 = font.render('Press "SPACEBAR" to', False, (20, 20, 20))
    game_message_22 = font.render('shoot and start the game', False, (20, 20, 20))

    screen.blit(game_name, game_name_rect)
    screen.blit(game_message_11, (50, 400))
    screen.blit(game_message_12, (50, 450))

    screen.blit(game_message_21, (50, 550))
    screen.blit(game_message_22, (50, 600))

    screen.blit(score_message, (420, 450))
    screen.blit(highest_score_message, (420, 400))


pygame.init()
size = 800, 700
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Cannonist')
clock = pygame.time.Clock()
t = 0
score = 0
highest_score = 0

# Font
font_big = pygame.font.Font('data/upheavtt.ttf', 50)
font = pygame.font.Font('data/upheavtt.ttf', 32)

game_menu = True
menu_icon = pygame.image.load('data/Menu_icon.png')

cannon = Cannon()

bullet_group = pygame.sprite.Group()

enemy_group = pygame.sprite.Group()

while 1:
    # Menu screen
    if game_menu:
        highest_score = max(highest_score, score)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_menu = False
                    score = 0

        score_message = font.render('Your score: ' + str(score), False, (20, 20, 20))
        highest_score_message = font.render('Your highest score: ' + str(highest_score), False, (20, 20, 20))

        screen.fill((139, 155, 180))
        screen.blit(menu_icon, (0, 0))
        messages()
        cannon.angle = 0
        cannon.rotate = 0
        enemy_group.empty()
        bullet_group.empty()
        cannon.pressed = 'w'
        cannon.bullet_pos = (400, 295)
        pygame.display.update()

        clock.tick(60)
    # Game screen
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                key = pygame.key.get_pressed()
                cannon.change_rotate(key)
                if event.key == pygame.K_SPACE and cannon.can_shoot and len(bullet_group) < 1:
                    bullet_group.add(cannon.create_bullet())

        screen.fill('Black')

        cannon.update()
        screen.blit(cannon.img_copy, cannon.rect)

        bullet_group.update()
        bullet_group.draw(screen)

        t += 1
        if t % 60 == 0:
            cord = random.choice(((400, -200), (400, 900), (1000, 350), (-200, 350)))
            enemy_group.add(Enemy(cord[0], cord[1]))
            t = 0

        for bullet in bullet_group:
            if pygame.sprite.spritecollide(bullet, enemy_group, True):
                pygame.sprite.spritecollide(bullet, enemy_group, True)
                bullet.kill()
                score += 1

        score_message = font.render('Score: ' + str(score), False, 'White')
        screen.blit(score_message, (0, 0))
        enemy_group.update()
        enemy_group.draw(screen)
        game_menu = cannon.death()
        pygame.display.update()
        clock.tick(60)
