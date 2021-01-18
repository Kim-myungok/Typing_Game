import pygame,time

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
background = pygame.image.load("C:/OSS_python/midTerm_typingGame/image/wall.jpg")
image_title = pygame.image.load('C:/OSS_python/midTerm_typingGame/image/title.png')
screen.blit(image_title,(15,HEIGHT/4))

# 버튼
start_button = pygame.image.load('C:/OSS_python/midTerm_typingGame/image/Start_button.png').convert_alpha()
screen.blit(start_button,(WIDTH/3,250))
data_button = pygame.image.load('C:/OSS_python/midTerm_typingGame/image/Data_button.png').convert_alpha()
screen.blit(data_button,(WIDTH/3+5,300))
exit_button = pygame.image.load('C:/OSS_python/midTerm_typingGame/image/exit_button.png').convert_alpha()
screen.blit(exit_button,(WIDTH/3+10,350))
pygame.display.flip()


start_button = start_button.get_rect()


while True:
        for event in pygame.event.get():
            if event.type == pygame.mouse.get_pressed():
                ## if mouse is pressed get position of cursor ##
                pos = pygame.mouse.get_pos()
                ## check if cursor is on button ##
                if button.collidepoint(pos):
                    ## exit ##
                    exit()