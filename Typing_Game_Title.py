from datetime import datetime
from random import *
import pygame
import sys
import os
import time
import sqlite3
import winsound

#DB 생성
conn = sqlite3.connect('./resource/records.db', isolation_level=None)

#cursor 연결
cursor = conn.cursor()

#테이블 생성
cursor.execute("CREATE TABLE IF NOT EXISTS records(Nickname tex,\
    Score INTEGER, Regdate tex)")

pygame.init()

# 스크린 전체 크기 지정
SCREEN_WIDTH = 480
SCREEN_HEIGHT  = 480

# 색상 상수
BLACK = (0, 0, 0)

# pygame 초기화
pygame.init()

# 스크린 객체 저장
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("타이핑 게임")

# FPS를 위한 Clock 생성
clock = pygame.time.Clock()

# 사운드 재생
def sound(sound_f, vol, playtime):
    pygame.mixer.music.load(sound_f)
    pygame.mixer.music.set_volume(vol) # 1 ~ 0.1
    pygame.mixer.music.play(playtime)


#################################################
#                  game_title():                #
#################################################
def game_title():
    # 배경 사운드
    sound('./sound/openning01.mid', 0.1, -1)
    pygame.mouse.set_visible(1)
    background = pygame.Surface(SCREEN.get_size())
    background = background.convert()
    background.fill((250,250,250))
    SCREEN.blit(background, (0,0))
    pygame.display.flip()

    # background = pygame.image.load("C:/OSS_python/midTerm_typingGame/image/wall.jpg")
    image_title = pygame.image.load('./image/title.png')
    SCREEN.blit(image_title,(15,SCREEN_HEIGHT/4))

    # 버튼
    global start_button, data_button, exit_button
    start_image = pygame.image.load('./image/Start_button.png').convert_alpha()
    data_image = pygame.image.load('./image/Data_button.png').convert_alpha()
    exit_image = pygame.image.load('./image/exit_button.png').convert_alpha()


    start_button = SCREEN.blit(start_image,(SCREEN_WIDTH/3,250))
    data_button = SCREEN.blit(data_image,(SCREEN_WIDTH/3+5,300))
    exit_button = SCREEN.blit(exit_image,(SCREEN_WIDTH/3+10,350))
    pygame.display.flip()

    playing = True
    while playing:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                winsound.PlaySound('./sound/button.wav', winsound.SND_FILENAME)
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
                    playing = False
                    
#################################################
#                  game_start():                #
#################################################
def game_start():
    pass

    # ## 결과 기록
    # cursor.execute("INSERT INTO records('Nickname', 'Score', 'record', 'Regdate')\
    #     VALUES(?,?,?,?)", (nickname, score, et, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

    ## 접속 해제
    conn.close()

    # ## 수행 시간 출력
    # print_screen = words.render(("\t플레이 시간 :", et, "초\n", "\t점수 : {}".format(score)), True, BLACK)
    # SCREEN.blit(print_screen, [10, SCREEN_HEIGHT-SCREEN_HEIGHT/3])

#################################################
#                  game_data():                 #
#################################################
def game_data():
    # db = open("./resource/data", 'r')
    pass

#### MAIN #####
game_title()
pygame.quit()