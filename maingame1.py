import pygame 
from sys import exit 
from random import randint, choice   

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load('img/bird.png').convert_alpha()        
        self.rect = self.image.get_rect(midbottom = (80, 200))    

    def input(self):
        keys = pygame.key.get_pressed() 
        if keys[pygame.K_SPACE]:
            self.rect.y -= 3 
        else:
            self.rect.y += 3  
        if self.rect.y <= 0:
            self.rect.y = 0 
        if self.rect.y >= 260:
            self.rect.y = 260

    def update(self):
        self.input() 

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        if type == 'bottom1':
            pipe1 = pygame.image.load('img/obstacle1.png').convert_alpha()  #bottom 
            y_pos = 305 
            self.frames = pipe1 
        elif type == 'bottom2':
            pipe2 = pygame.image.load('img/obstacle3.png').convert_alpha()  #bottom 
            y_pos = 305
            self.frames = pipe2
        elif type == 'top1':
                pipe3 = pygame.image.load('img/obstacle2.png').convert_alpha()  #top  
                y_pos = 0
                self.frames = pipe3
        elif type == 'top2': 
            pipe4 = pygame.image.load('img/obstacle4.png').convert_alpha() #top 
            y_pos = 0 
            self.frames = pipe4
        self.image = self.frames
        if type == 'bottom1' or type == 'bottom2': 
            self.rect = self.image.get_rect(midbottom = (randint(900,1100), y_pos))  
        else:
            self.rect = self.image.get_rect(midtop = (randint(900, 1100), y_pos))  

    def destroy(self):
        if self.rect.x == -100:
            self.kill() 

    def update(self):
        self.destroy() 
        self.rect.x -= 4  

def collision():
    if pygame.sprite.spritecollide(bird.sprite, obstacle, False):  
        obstacle.empty()  
        return False   
    return True   

pygame.init() 
screen = pygame.display.set_mode((800, 400)) 
pygame.display.set_caption('Flappy Birds')
clock = pygame.time.Clock()

bird = pygame.sprite.GroupSingle() 
bird.add(Bird()) 

obstacle = pygame.sprite.Group() 

obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)   

#Surfaces 
sky_surface = pygame.image.load('img/bluesky.png').convert()  
sky_surface_scale = pygame.transform.scale(sky_surface, (800, 310))  
ground_surface = pygame.image.load('img/ground.JPG').convert()  
ground_surface_scale = pygame.transform.scale(ground_surface, (800, 400))  
game_over_surface = pygame.image.load('img/gameover.png').convert(); 
game_over_surface_scale = pygame.transform.scale(game_over_surface, (800,400)); 

test_font = pygame.font.Font('Pixeltype.ttf', 50) 

count = 0 
game_over = True 
score = 0;  

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit() 
        if game_over:
            if event.type == obstacle_timer:
                if count == 0:
                    obstacle.add(Obstacle('bottom1'))
                    count = 1
                elif count == 1:
                    obstacle.add(Obstacle('top1')) 
                    count = 2
                elif count == 2:
                    obstacle.add(Obstacle('bottom2'))
                    count = 3
                else:
                    obstacle.add(Obstacle('top2'))
                    count = 0  
                score += 1;  
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                score = 0
                game_over = True 

    if game_over:
        screen.blit(sky_surface_scale, (0,0))     
        screen.blit(ground_surface, (0,300))  
        bird.draw(screen)  
        bird.update() 
        obstacle.draw(screen) 
        obstacle.update() 
        game_over = collision()  
        score_message = test_font.render('Score: ' + str(score), False, ('Black'))  
        score_message_rect = score_message.get_rect(center = (400,50))
        screen.blit(score_message, score_message_rect) 
    else: 
        screen.blit(game_over_surface_scale, (0,0));    
        game_over_message = test_font.render('Press space to play again!', False, ('Black'))  
        game_over_message_rect = game_over_message.get_rect(center = (400, 300)) 
        screen.blit(game_over_message, game_over_message_rect) 
        score_over_message = test_font.render("Score: " + str(score), False, ('Black'))
        score_over_message_rect = score_over_message.get_rect(center = (400, 100));
        screen.blit(score_over_message, score_over_message_rect) 

    pygame.display.update()
    clock.tick(60) 
