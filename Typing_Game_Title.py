import pygame

pygame.init()

# WHITE= (255,255,255)
# BLACK = (0,0,0)
# black2 = (30,30,30)

# 화면 크기, 타이틀 설정
WIDTH = 480
HEIGHT = 480
screen= pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()

pygame.display.set_caption("타이핑 게임")
pygame.mouse.set_visible(1)
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((250,250,250))
screen.blit(background, (0,0))
pygame.display.flip()


# 타이틀
# background = pygame.image.load("C:/OSS_python/midTerm_typingGame/image/wall.jpg")
image_title = pygame.image.load('C:/OSS_python/midTerm_typingGame/image/title.png')
screen.blit(image_title,(15,HEIGHT/4))

# 사운드 재생
# pygame.mixer.music.load( "background.mp3" )
# play(loops=0, start=0.0)

# 버튼
start_image = pygame.image.load('C:/OSS_python/midTerm_typingGame/image/Start_button.png').convert_alpha()
start_button = screen.blit(start_image,(WIDTH/3,250))
data_image = pygame.image.load('C:/OSS_python/midTerm_typingGame/image/Data_button.png').convert_alpha()
data_button = screen.blit(data_image,(WIDTH/3+5,300))
exit_image = pygame.image.load('C:/OSS_python/midTerm_typingGame/image/exit_button.png').convert_alpha()
exit_button = screen.blit(exit_image,(WIDTH/3+10,350))
pygame.display.flip()

def game_start():
    pass

def game_data():
    pass

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            ## if mouse is pressed get position of cursor ##
            pos = pygame.mouse.get_pos()
            ## check if cursor is on button ##
            if start_button.collidepoint(pos):
                ## start ##
                game_start()
                pygame.display.flip()
            elif data_button.collidepoint(pos):
                ## data ##
                game_data()
            elif exit_button.collidepoint(pos):
                ## exit ##
                run = False
pygame.quit()