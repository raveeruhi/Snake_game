import pygame
import random
import os
#for audio and pictures to be inserted
pygame.mixer.init()
#for norml pygame function
pygame.init()
# Colors
white = (0, 0, 0)
red = (255, 0, 0)
black = (255, 255, 255)

# Creating window
screen_width = 900
screen_height = 600
#to set display of game screen
gameWindow = pygame.display.set_mode((screen_width, screen_height))
#Background Image
bgimg = pygame.image.load("snake.jpg")#to load the image from the folder
bgimg = pygame.transform.scale(bgimg, (screen_width, screen_height)).convert_alpha()#to fit pic to screen
intro = pygame.image.load("welcome1.jpg")
intro = pygame.transform.scale(intro, (screen_width, screen_height)).convert_alpha()
o1= pygame.image.load("poor.jpg")
o1 = pygame.transform.scale(o1, (screen_width, screen_height)).convert_alpha()
o2 = pygame.image.load("mid.jpg")
o2 = pygame.transform.scale(o2, (screen_width, screen_height)).convert_alpha()
o3 = pygame.image.load("highscore.jpg")
o3 = pygame.transform.scale(o3, (screen_width, screen_height)).convert_alpha()
# Game Title
pygame.display.set_caption("Snake Game")
pygame.display.update()#arfer any change to screen we have to update the screen
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 55)#to set the font style


def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x,y])#to apply on screen


def plot_snake(gameWindow, color, snk_list, snake_size):
    for x,y in snk_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])#to draw a rect on the screen

def welcome():
    exit_game = False
    while not exit_game:
        gameWindow.blit(intro,(0,0))
        for event in pygame.event.get():#for any event in pygame
            if event.type == pygame.QUIT:#for close button
                exit_game = True
            if event.type == pygame.KEYDOWN:#for any key pressed
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.load('back.mp3.mpeg')
                    pygame.mixer.music.play()
                    gameloop()

        pygame.display.update()
        clock.tick(60)#updation time for window


# Game Loop
def gameloop():
    # Game specific variables
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    velocity_x = 0
    velocity_y = 0
    snk_list = []
    snk_length = 1
    mili=0
    time=0
    # Check if hiscore file exists
    if(not os.path.exists("highscore.txt")):
        with open("highscore.txt", "w") as f:
            f.write("0")

    with open("highscore.txt", "r") as f:
        hiscore = f.read()

    food_x = random.randint(20, screen_width / 2)#for creating a random integer
    food_y = random.randint(20, screen_height / 2)
    power_y = random.randint(20, screen_height / 2)
    power_x = random.randint(20, screen_width / 2)


    score = 0
    init_velocity = 3
    snake_size = 20
    fps = 60
    while not exit_game:
        if game_over:
            with open("highscore.txt", "w") as f:
                f.write(str(hiscore))

            if score>=int(hiscore)-50 and score< int(hiscore):
                gameWindow.blit(o2,(0,0))#for applying the o2 pic on the screen
            elif score>=int(hiscore):
                gameWindow.blit(o3,(0,0))
            else:
                gameWindow.blit(o1,(0,0))

            text_screen("Your Score:"+ str(score)+" "+"High Score:"+ str(hiscore), red, 160, 300)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()

        else:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_LEFT:
                        velocity_x = - init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_UP:
                        velocity_y = - init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_q:
                        score +=10

            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y

            if abs(snake_x - food_x)<20 and abs(snake_y - food_y)<20:
                score +=5
                food_x = random.randint(20, screen_width / 2)
                food_y = random.randint(20, screen_height / 2)
                snk_length +=5
            if time>=1 and time<=1.3:
                if abs(power_x-snake_x)<20 and abs(power_y-snake_y)<20:
                    score+=10
                    power_x = random.randint(20, screen_width / 2)
                    power_y = random.randint(20, screen_height / 2)
                    snk_length+=8
                    time=0

            if score>int(hiscore):
                hiscore = str(score)

            gameWindow.blit(bgimg, (0, 0))
            text_screen("Score: " + str(score), (230,200,0), 5, 5)
            pygame.draw.rect(gameWindow, red, [food_x, food_y, snake_size, snake_size])
            mili=clock.tick() #for counting the time in mili sec
            time+=mili/1000
            if time>=1 and time<=1.3 :
                pygame.draw.circle(gameWindow, (0,255,0), [power_x,power_y], snake_size)#for drawing the circle
            if time>1.4:time=0


            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if len(snk_list)>snk_length:
                del snk_list[0]

            if head in snk_list[:-2]:
                game_over = True
                pygame.mixer.music.load('gameover..mpeg')
                pygame.mixer.music.play(100)
                pygame.mixer.music.set_volume(.9)

            if snake_x<0 or snake_x>screen_width or snake_y<0 or snake_y>screen_height:
                game_over = True
                pygame.mixer.music.load('gameover..mpeg')
                pygame.mixer.music.play(100)
                pygame.mixer.music.set_volume(.9)
            plot_snake(gameWindow, black, snk_list, snake_size)
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()
welcome()