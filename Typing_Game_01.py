from datetime import datetime
from random import *
import pygame
import sys
import os
import time
import sqlite3
import winsound


class Word:
    def __init__(self, word,x,y):
        self.word=word
        self.x=x
        self.y=y
        # Font 객체 생성
        myFont = pygame.font.SysFont("arial", 30, True, False)
        # Text를 surface에 그리기, 안티알리어싱, 검은색
        self.text_Title=myFont.render(self.word, True, BLACK)
    # y축 (위에서 아래로) 이동
    def move_y(self):
        self.y+=TEXT_SPEED
    # 스크린에 그리기
    def draw_word(self):
        SCREEN.blit(self.text_Title, [self.x, self.y])
    # y축이 화면 밖으로 나갔는지 확인(text창위까지), True:화면 밖, False:화면 안
    def is_screen_out(self):
        if self.y > (SCREEN_HEIGHT-70):
            return True

class Life:
    def __init__(self, x, y):
        self.img=""
        self.rect=""
        self.x=x
        self.y=y
    def load(self):
        self.img = pygame.image.load("./finalExam/life.png")
        self.img = pygame.transform.scale(self.img, (40, 40)) #이미지 사이즈 조절
        self.rect = self.img.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
    def draw(self):
        SCREEN.blit(self.img, [self.rect.x, self.rect.y])

#DB 생성
conn = sqlite3.connect('./resource/records.db', isolation_level=None)

#cursor 연결
cursor = conn.cursor()

#테이블 생성
cursor.execute("CREATE TABLE IF NOT EXISTS records(Nickname tex,\
    Score INTEGER, Regdate tex)")



# pygame 초기화
pygame.init()


# 스크린 전체 크기 지정
SCREEN_WIDTH = 480
SCREEN_HEIGHT  = 480

# 스크린 객체 저장
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("타이핑 게임")

# FPS를 위한 Clock 생성
clock = pygame.time.Clock()

# 입력창 위치 지정
INPUT_BOX_X = 0
INPUT_BOX_Y = 460
# 정답글자 위치
RANDOM_WEIGHT=200 #랜덤 보정값
ANS_TEXT_X=SCREEN_WIDTH-RANDOM_WEIGHT
ANS_TEXT_Y=-30
# 라이프 위치
LIFE_X_WEIGHT=25 #x값 가중치 (각 라이프들은 해당 값만큼 X축으로 떨어져있다.)
LIFE_X_FIX=300 #base 값
LIFE_Y_FIX=0

# 상수
BLACK = (0, 0, 0) #색상상수
RED = (255,0,0)#색상상수

#게임 속성관련
LIFE_CNT=3 #목숨 개수
TEXT_SPEED = 15 #글자 낙하속도
FPS = 24 #1초당 프레임 수
#단어파일 -> 리스트로 넘어온 개수
END_OF_WORDS=0 

# 사운드 재생
def sound(sound_f, vol, playtime):
    pygame.mixer.music.load(sound_f)
    pygame.mixer.music.set_volume(vol) # 1 ~ 0.1
    pygame.mixer.music.play(playtime)


#################################################
#                  game_title():                #
#################################################
def game_Title():
    # 배경 사운드
    sound('./sound/openning.mid', 0.1, -1)
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
                    game_Start()
                    pygame.display.flip()
                elif data_button.collidepoint(pos):
                    ## data ##
                    game_Data()
                elif exit_button.collidepoint(pos):
                    ## exit ##
                    playing = False
                    
#################################################
#                  game_start():                #
#################################################
def game_Start():
    words = [] # 영어 단어 리스트(1000개 로드)
    try:
        word_f = open('./finalExam/word.txt','r',encoding='utf-8')
        i=0 #1000 이 되면 종료
        while True:
            line=word_f.readline()
            if not line or i==1000:
                END_OF_WORDS = i
                break
            words.append(Word(line.strip(),randint(0,ANS_TEXT_X),ANS_TEXT_Y))
            i+=1
    except IOError:
        print("파일이 없습니다!! 게임을 진행할 수 없습니다!!")

    if words==[]:
        sys.exit()

    # Text Editing (user input)
    user_input_text = ''
    user_input_text_font = pygame.font.SysFont("arial", 30, True, False)
    user_input = user_input_text_font.render(user_input_text,True,BLACK)
    user_input_box = user_input.get_rect()
    user_input_box.topleft = (INPUT_BOX_X,INPUT_BOX_Y)
    cursor1 = pygame.Rect(user_input_box.topright,(3,user_input_box.height))

    # Life
    lifes = []
    for i in range(LIFE_CNT):
        life = Life(LIFE_X_FIX+i*LIFE_X_WEIGHT,LIFE_Y_FIX)
        life.load()
        lifes.append(life)
    #score
    score = 0

    # TIME & TEXT
    current_time = 0
    interval_time=2 #2초 주기
    words_index=0 #0~words 끝까지 interval_time 시간마다 1씩 증가하면서 screen_in_texts에 words를 넣는다.
    screen_in_texts=[] #화면 안에 있는 텍스트

    playing = True
    while playing:
        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
                pygame.quit()
            #사용자 입력 처리(텍스트 입력)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE: #백스페이스
                    if len(user_input_text)> 0:
                        user_input_text = user_input_text[:-1]
                elif event.key == pygame.K_RETURN: #엔터
                    for text in screen_in_texts:
                        if user_input_text == text.word:
                            score += len(text.word)
                            screen_in_texts.remove(text) 
                    user_input_text=""
                else: #글자
                    user_input_text += event.unicode
                user_input = user_input_text_font.render(user_input_text,True,BLACK)
                user_input_box.size = user_input.get_size()
                cursor1.topleft = user_input_box.topright

        # 스크린 배경색 칠하기
        SCREEN.fill((255, 255, 255))
        #점수판 생성
        score_font = pygame.font.SysFont("arial",20, True, False)
        score_board = score_font.render(str(score),True,BLACK)
        score_rect = score_board.get_rect()
        score_rect.x=LIFE_X_FIX+LIFE_X_WEIGHT+25
        score_rect.y=round(SCREEN_HEIGHT/2)
        SCREEN.blit(score_board,score_rect)

        # 텍스트 위에서 아래로
        mt = clock.tick(FPS) / 1000
        current_time += mt 
        if current_time > interval_time and END_OF_WORDS > words_index: #2초 주기
            screen_in_texts.append(words[words_index]) # interval_time 시간마다 1씩 증가하면서 screen_in_texts에 words를 넣는다.
            words_index+=1 #0~words 끝까지
            current_time = 0
        #실제로 텍스트 위에서 아래로 내리는 코드
        for text in screen_in_texts: 
            text.draw_word()
            text.move_y() 
            if text.is_screen_out(): #텍스트가 내려가다가 설정한 밑바닥에 닿으면 목숨 - 1
                screen_in_texts.remove(text) 
                lifes.pop()
                if len(lifes) == 0:
                    print("Game Over")
                    #pygame.quit() 게임 오버 업데이트하기 이렇게 하지말고 playing=False로 만들어서 루프 탈출 후 거기서 SCREEN그리기
        SCREEN.blit(user_input,user_input_box) #입력창 화면에 그리기

        if time.time() % 1 > 0.5: #커서 깜빡임
            pygame.draw.rect(SCREEN, RED, cursor1)

        #목숨(하트) 화면에 그리기
        for life in lifes:
            life.draw()
        
        # 작업한 스크린의 내용을 갱신하기
        pygame.display.flip()

        # FPS:24
        clock.tick(FPS)

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
def game_Data():
    # db = open("./resource/", 'r')
    pass

#### MAIN #####
game_Title()
pygame.quit()