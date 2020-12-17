

#Zhenia Sigayev
#ICS3UO
#Pygame
#A player must "catch" as many blocks as possible within a 30 second time limit


#Imports Libraries from python

import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Initialize Variables
timer = 0 #time tracker
score = 0 #score tracker
lost = False
end = False
soundplayed = False
userEvent =  pygame.event.Event(pygame.USEREVENT)
clock = pygame.time.Clock()

# Set the height and width of the screen
screen_width  = 600
screen_height = 400
screen = pygame.display.set_mode([screen_width, screen_height])

#background image
background_image = pygame.image.load("BG.jpg").convert()
background_image = pygame.transform.scale(background_image,(screen_width,screen_height))
 

#Loads the end screen after timer runs out
end = pygame.image.load("end.jpg")
end = pygame.transform.scale(end,(screen_width,screen_height))

#Defines some colors
BLACK     = (0, 0, 0)
WHITE     = (255, 255, 255)
GREEN     = (0, 255, 0)
RED       = (255, 0, 0)
BABY_BLUE = (84, 224, 232)
PINK      = (232, 84, 224)

#Fonts
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font('freesansbold.ttf', 32) 
    text = font.render(text, True, WHITE)
    textRect = text.get_rect()
    textRect.midtop = (x, y)
    surf.blit(text, textRect)

#Represents the blocks that fall down the screen
class Block(pygame.sprite.Sprite):

    def __init__(self, color, width, height):
        super().__init__()  # Function adapted from: https://stackoverflow.com/questions/576169/understanding-python-super-with-init-methods
 
        # Create an image of the block, and fills it with a color.
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
 
    def reset_block_position(self):
        #Reset position to the top of the screen, at a random x location.
        #Called by update() or the main program loop if there is a collision.
       
        self.rect.x = random.randrange(0, screen_width)     #spawns a rectangle randomly on the horizontal side of the screen width
        self.rect.y = random.randrange(-30, -20)            #spawns a rectangle randomly 20 to 30 pixles above the screen
 
    def update(self):
 
        self.rect.y += 3 # Move block down 3 pixels *Called every frame
 
        # If block is too far down, reset to top of screen.
        if self.rect.y > screen_height:
            self.reset_block_position()

#Represents the players block
class Player(Block):

    #moves the block with the mouse position
    def update(self):
        position = pygame.mouse.get_pos()
        self.rect.x = position[0]    #player x coordinate = mouse x coordinate
        self.rect.y = position[1]    #player y coordinate = mouse y coordinate
 

 
# This is a list of 'sprites.' Each block in the program is
# added to this list. The list is managed by a class called 'Group.'
block_list = pygame.sprite.Group()
 
# This is a list of every sprite. All blocks and the player block as well.
all_sprites_list = pygame.sprite.Group()

#50 blocks MAX can be present on the screen at any given moment.
for i in range(50): 

    # This represents a block's color, width, and height.
    block = Block(PINK, 20, 15) 
 
    # Set a random location for the block
    block.rect.x = random.randrange(screen_width)
    block.rect.y = random.randrange(screen_height)
 
    # Add the block to the list of objects
    block_list.add(block)
    all_sprites_list.add(block)
 
# Create a green player
player = Player(GREEN, 20, 15)
all_sprites_list.add(player)
 
# Loop until the user clicks the close button or time reaches 30 seconds
done = False

  
# -------- Main Program Loop -----------


while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    timer += 1 #adds 1 to a timer every millisecond

    #Plays intense gamer music
    if soundplayed == False:    #Playing sound code adapted from: #https://www.pygame.org/docs/ref/mixer.html#pygame.mixer.Sound.get_volume
        pygame.mixer.music.load("BGMusic.wav") #Music from: https://www.youtube.com/watch?v=GR47lpQoPc8
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play()

        soundplayed = True
        
    # Clear the screen
    screen.blit(background_image, [0,0])
    # Calls update() method on every sprite in the list
    all_sprites_list.update()
 
    # See if the player block has collided with anything.
    blocks_hit_list = pygame.sprite.spritecollide(player, block_list, False)
 
    # Check the list of collisions.
    for block in blocks_hit_list:
        score += 1
        print(score)
 
        # Reset block to the top of the screen to fall again.
        block.reset_block_position()
 
    # Draw all the spites to ensure 50 are always present on screen
    all_sprites_list.draw(screen)
 
    # Limit to 60 frames per second
    clock.tick(60)
    

    #Keep redrawing all the blocks and the player's current score
    draw_text(screen, ("Current Score: ") + str(score), 32, screen_width / 2, 10)
    pygame.display.flip()

    if timer in range(1050,1200):
        draw_text(screen,("20 SECONDS REMAINING "), 32, screen_width /2 , screen_height/2-20)
        pygame.display.flip()

    if timer in range(2100,2250):
        draw_text(screen,("10 SECONDS REMAINING "), 32, screen_width /2 , screen_height/2-20)
        pygame.display.flip()
        
    if timer >= 3150:   #30 second timer
    
        #Loads the game over image
        end = pygame.image.load("end.jpg") 
        screen.blit(end,(0,0))

        #Prints the player's final score and how long they have until the game closes
        draw_text(screen,("Final Score: ") + str(score), 32, screen_width /2 , screen_height -375)
        draw_text(screen,"GAME WILL EXIT IN 5 SECONDS", 32, screen_width /2 , screen_height -85)
        pygame.display.update()

        #Delays any functions for "x" seconds
        time.sleep(5) 
        event = pygame.event.wait()

        done = True
     
pygame.quit()
