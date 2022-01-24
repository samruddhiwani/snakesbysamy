#import modules
import pygame
import random
import os

pygame.mixer.init()      #for backgruond music
pygame.init()            #initialize pygame


#colors define
white = (255, 255, 255)
red = (255, 0, 0, 0)
black =(0, 0, 0)

#creating window
screen_width = 1000
screen_height = 600
gameWindow = pygame.display.set_mode((screen_width, screen_height))    #display mode->input leta hai hai aur woh i/p ek tuple hota hai(w x h) gmaewindow->used for opeing window
pygame.display.set_caption("Snakes By Samy")                           #title of the fame
pygame.display.update()

#background image
bgimg = pygame.image.load("images.jfif")
bgimg = pygame.transform.scale(bgimg, (screen_width,screen_height))           #.convert_aplha()    #image ko apne game size main laneke liye
 # convert_alpha-> bar bar game ke ander is backgruond img ko blit krenge toh apne game ke speed ko koi effect nhi hoga
intro = pygame.image.load("wellcome.png")
intro = pygame.transform.scale(intro, (screen_width,screen_height))
outro = pygame.image.load("img.jfif")
outro = pygame.transform.scale(outro, (screen_width,screen_height))

clock = pygame.time.Clock()                                     #define clock
font = pygame.font.SysFont(None, 55)



def text_screen(text, color,x, y):                               #screen pe text , colour aur kaha karna chahte ho
    screen_text = font.render(text, True, color)                 #high resolution ko low resolution main put krte hai toh antialyzing
    gameWindow.blit(screen_text, [x,y])                          #ye batata hai ki screen ko update karo

def plot_snake(gameWindow, color, snk_list, snake_size):
    for x,y in snk_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])         #rectangle draw (in gamewindow ,colur black, x,y,w,h) #creating snake head

#welcome screen
def welcome(): 
    exit_game = False
    while not exit_game:
        gameWindow.blit(intro, (0,0))
        text_screen("Welcome Press Space Bar To Play", (255,255,0), 160, 30)
                                                                #text_screen("Press Space Bar To Play", black, 237, 280)
        for event in pygame.event.get():                        #event handling for quit function
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:                #space dabavoge toh game chalu hoga
                    pygame.mixer.music.fadeout(200)
                    pygame.mixer.music.load('back.mp3')        #music load hota hai
                    pygame.mixer.music.play()                  #jab game chalu hoga tab music play hoga
                    gameloop()

        pygame.display.update()
        clock.tick(60)

#creating a game loop
def gameloop():                                             #define
                                                            #game specific variables
    exit_game = False                                       #game band krne ke liye by default false rakha hai true hoga toh band hojayega game
    game_over = False                                       # ye true tab hoga jaga player ka game over hojayega 
    snake_x = 45
    snake_y = 55
    velocity_x = 0
    velocity_y = 0
    snk_list = []
    snk_length = 1

    #check if hiscore file exists
    if(not os.path.exists("hiscore.txt")):              #file nahi exists krti toh file banadenge
        with open("hiscore.txt", "w") as f:
            f.write("0")

    with open("hiscore.txt", "r") as f:
        hiscore = f.read()

    init_velocity = 4
    food_x = random.randint(20, screen_width/2)
    food_y = random.randint(20, screen_height/2)
    score = 0
    snake_size = 15
    fps = 60                                            #frame per sec   #ek sec main kitne frame chahiye woh hota hai fps

    while not exit_game:                                #jabtak exit game false hai tabtak game chlta rahega true ho gaya toh yeh whileloop chalega mean game exit krega
        if game_over:                                   #gameover hua toh fill wdow in white
            with open("hiscore.txt", "w") as f:
                f.write(str(hiscore))

#gameOverScreen
            gameWindow.blit(outro,(0,0))
            text_screen(" Game Over!", red, 60, 300 )
            text_screen("Press Enter To Continue", red, 20, 350 )
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:   
                    if event.key == pygame.K_RETURN:     #enter press kroge toh firse game chalu hoga
                        welcome()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:            #konsi key press hui agar key press hui toh if loop ke andar jayega
                    if event.key == pygame.K_RIGHT:         #right arrow
                        velocity_x = init_velocity          #move hoga aage x ke direction main ->
                        velocity_y = 0                      #kyuki snake daigonal main na bhage
                    if event.key == pygame.K_LEFT:          #left arrow
                        velocity_x = - init_velocity        #move hoga aage x ke direction main ->
                        velocity_y = 0                      #kyuki snake daigonal main na bhage
                    if event.key == pygame.K_UP:            #up arrow
                        velocity_y =  - init_velocity       #move hoga aage y ke direction main up
                        velocity_x = 0                      #kyuki snake daigonal main na bhage
                    if event.key == pygame.K_DOWN:          #down arrow
                        velocity_y =   init_velocity        #move hoga aage y ke direction main down
                        velocity_x = 0                      #kyuki snake daigonal main na bhage
                    if event.key == pygame.K_q:             #for cheat code score badjayega when we press q
                        score +=10

            snake_x = snake_x + velocity_x                  #snake ki position chnge hogi  #giving speed to our snake
            snake_y =  snake_y +velocity_y

            if abs(snake_x - food_x )<6 and abs(snake_y - food_y) <6:
                score +=10
                print("Score: ", score * 10)
                
                food_x = random.randint(20, screen_width / 2)
                food_y = random.randint(20, screen_height / 2)
                snk_length += 4
                if score>int(hiscore):
                    hiscore = score
                

            gameWindow.fill(white)                                                              #for white screen
            gameWindow.blit(bgimg, (0, 0))
            text_screen("Score: "+ str(score) + "  Hiscore: "+str(hiscore), black, 5, 5)
            pygame.draw.rect(gameWindow, red, [food_x, food_y, snake_size, snake_size])         #for snake food

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if len(snk_list)>snk_length: 
                del snk_list[0]                                                                #delete start part of snake

            if head in snk_list[:-1]:                                                          #snake apneaap ko cross krega toh gameover hojayega
                game_over = True
                pygame.mixer.music.load('gameover.mp3')                                        #music load hota hai
                pygame.mixer.music.play()                                                      #music play hoga

            if snake_x<0 or snake_x> screen_width or snake_y<0 or snake_y> screen_height:
                game_over = True 
                pygame.mixer.music.load('gameover.mp3')                                        #music load hota hai
                pygame.mixer.music.play()                                                      #music play hoga 
            plot_snake(gameWindow, black,snk_list, snake_size)
        pygame.display.update()                                                                #to updatethechanges
        clock.tick(fps)


    pygame.quit()                                                                       #pygame ka quit ,jab ye while loop exit hoga toh yeh quit run hoga
    quit()                                                                              #python ka quit
welcome()
