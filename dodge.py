import pygame
import random

#Import locals - here for key actions
from pygame.locals import (
    K_r,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

#Initialise the pygame library
pygame.init()

#Initialise a Player class - extended from the pygame sprite class.
class Player(pygame.sprite.Sprite):
    def __init__(self):
        #Basic player information (size, color)
        super(Player, self).__init__()
        self.surf = pygame.Surface((75, 25))
        self.surf.fill((51, 255, 0))
        self.rect = self.surf.get_rect()

    #What happens when a key is pressed
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0,-5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        #Stop the player from going off the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width
        #Set to as 100 to allow space for title
        if self.rect.top < 100:
            self.rect.top = 100
        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height

#Initialise an Enemy class - extended from the pygame sprite class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, speed1=5, speed2=20, size1=20, size2=10):
        #Basic enemy information (size, colour)
        super(Enemy, self).__init__()
        self.surf = pygame.Surface((size1, size2))
        self.surf.fill((98, 255, 98))
        #Where the enemy should appear (off screen, anywhere between 20 and 100px right, and anywhere from 100px to bottom)
        self.rect = self.surf.get_rect(
            center = (
                random.randint(screen_width + 20, screen_width + 100),
                #Top starts at 100 to allow room for title
                random.randint(100, screen_height),
            )
        )
        #Set speed of the enemy between two values
        self.speed = random.randint(speed1,speed2)

    #Update where the enermy is. If enemy has passed the left hand side of the screen, enemy is removed and player score is increased by 1
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            global level_score
            level_score = level_score + 1
            global total_score
            total_score += 1
            self.kill()

#Import clock - needed to set frame rate (fps)
clock = pygame.time.Clock()

#Variables needed for the game.
screen_width = 800
screen_height = 600
level_score = 0
level = 1
total_score = 0
num_enemies = 0
max_enemies = 20
game_started = False
levels = [
    [5, 10, 20, 10, 50],
    [10, 20, 20, 10, 100],
    [5, 25, 20, 30, 200],
    [10, 30, 50, 10, 400],
    [30, 35, 50, 30, 600]
]

#Set the game title
font = pygame.font.Font('freesansbold.ttf', 32)
text = font.render('Dodge', True, (51,255,0),(0,0,0))
textRect = text.get_rect()
textRect.center = (screen_width / 2, 35)

#Set the game score area
def disp_level_score():
    font3 = pygame.font.Font('freesansbold.ttf', 15)
    score_text = font3.render('Level Score: ' + str(level_score), True, (51,255,0),(0,0,0))
    scoreRect = score_text.get_rect()
    scoreRect.center = ((screen_width/2) + 300, 35)
    screen.blit(score_text, scoreRect)

#Set the game score area
def disp_level():
    font3 = pygame.font.Font('freesansbold.ttf', 15)
    level_text = font3.render('Level: ' + str(level), True, (51,255,0),(0,0,0))
    levelRect = level_text.get_rect()
    levelRect.center = ((screen_width/2) + 300, 15)
    screen.blit(level_text, levelRect)

#Set the game score area
def disp_total():
    font3 = pygame.font.Font('freesansbold.ttf', 15)
    total_text = font3.render('Total Score: ' + str(total_score), True, (51,255,0),(0,0,0))
    totalRect = total_text.get_rect()
    totalRect.center = ((screen_width/2) + 300, 55)
    screen.blit(total_text, totalRect)

#Function to print a message onto the screen
def you_message(message):
    font2 = pygame.font.Font('freesansbold.ttf', 100)
    text_message = font2.render(str(message), True, (0,0,0), (51,255,0))
    text_messageRect = text_message.get_rect()
    text_messageRect.center = (screen_width/2, screen_height/2)
    screen.blit(text_message, text_messageRect)

#Initialise the screen
screen = pygame.display.set_mode((screen_width,screen_height))

#Create a new customer event for adding an enemy
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)

#Instantiate player, and create sprite groups. Add player to all_sprites group
player = Player()
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

#running sets the game loop going. play adds an aditional loop to hold the screen once the player loses.
running = True
play = True

#Game loop
while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            #If 'r' is pressed and the game has finished, restart game. Clear all groups and variables.
            if event.key == K_r and play == False:
                enemies.empty()
                all_sprites.empty()
                all_sprites.add(player)
                level_score = 0
                num_enemies = 0
                game_started = 0
                play = True
            #If escape or quit pressed, exit game
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False
        #If we have not exceeded the maximum number of enemies, add a new enemy to the enemies and all_sprites groups. Increment enemies counter
        elif event.type == ADDENEMY:
            if num_enemies < levels[level-1][4]:
                new_enemy = Enemy(speed1 = levels[level-1][0], speed2 = levels[level-1][1], size1 = levels[level-1][2], size2 = levels[level-1][3])
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)
                num_enemies += 1

    #Show start message at start of game
    if not game_started:
        screen.fill((0, 0, 0))
        you_message('READY')
        pygame.display.flip()
        pygame.time.wait(1000)
        screen.fill((0, 0, 0))
        you_message('STEADY')
        pygame.display.flip()
        pygame.time.wait(1000)
        screen.fill((0, 0, 0))
        you_message('DODGE!')
        pygame.display.flip()
        pygame.time.wait(500)
        game_started = True

    #As long as game has not been lost, the game continues to be played.
    if play:
        #Get the key that has been pressed
        pressed_keys = pygame.key.get_pressed()

        #Update position of player based on key pressed. Then also update enemies (i.e. positions, number)
        player.update(pressed_keys)
        enemies.update()

        #Fill the screen with black
        screen.fill((0, 0, 0))

        #Put the title onto the screen and the score and the level
        screen.blit(text, textRect)
        disp_level_score()
        disp_level()
        disp_total()

        #For each sprite on screen, update its position
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)

        #If the player has collided with any member of the enemies group, the player is killed and the 'you lose' message is displayed. Play loop is stopped.
        if pygame.sprite.spritecollideany(player, enemies):
            player.kill()
            you_message('YOU LOSE')
            play = False

        #Check if player has won level. If yes, move to next level until all levels complete.
        if level_score == levels[level-1][4]:
            if level < len(levels):
                level += 1
                enemies.empty()
                all_sprites.empty()
                all_sprites.add(player)
                level_score = 0
                num_enemies = 0
                screen.fill((0, 0, 0))
                you_message('LEVEL ' + str(level))
                pygame.display.flip()
                pygame.time.wait(1000)
            else:
                you_message('YOU WIN')
                play = False
            
        #Screen is updated.
        pygame.display.flip()

        #FPS set
        clock.tick(30)

