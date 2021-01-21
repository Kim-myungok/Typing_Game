from datetime import datetime
from random import *
import pygame
import sys
import os
import time
import sqlite3
import winsound
import datetime
from time import sleep
import tkinter
from tkinter.ttk import Button


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
    def move_y(self,speed):
        # global TEXT_SPEED
        self.y+=speed
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
        self.img = pygame.image.load("./image/life.png")
        self.img = pygame.transform.scale(self.img, (40, 40)) #이미지 사이즈 조절
        self.rect = self.img.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
    def draw(self):
        SCREEN.blit(self.img, [self.rect.x, self.rect.y])

# pygame 초기화
pygame.init()

# 스크린 전체 크기 지정
SCREEN_WIDTH = 400
SCREEN_HEIGHT  = 500

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
GRAY = (150, 150, 150)
WHITE = (255, 255, 255) #색상상수
RED = (255,0,0)#색상상수

#게임 속성관련
LIFE_CNT=3 #목숨 개수
global TEXT_SPEED # = 5 #글자 낙하속도, 속도 조절위한 global선언
global GAME_LEVEL #게임 레벨
FPS = 20 #1초당 프레임 수
#단어파일 -> 리스트로 넘어온 개수
END_OF_WORDS=0 

# 사운드 재생
def sound(sound_f, vol, playtime):      #파일명, 소리크기, 재생시킬시간
    pygame.mixer.music.load(sound_f)
    pygame.mixer.music.set_volume(vol) # 1 ~ 0.1
    pygame.mixer.music.play(playtime)

#################################################
#                  game_title():                #
#################################################
def game_Title():
    sound('./sound/openning.mid', 0.1, -1)  # 배경 사운드
    pygame.mouse.set_visible(1)
    background = pygame.Surface(SCREEN.get_size())
    background = background.convert()
    background.fill((250,250,250))
    SCREEN.blit(background, (0,0))
    pygame.display.flip()

    # background = pygame.image.load("C:/OSS_python/midTerm_typingGame/image/wall.jpg")
    image_title = pygame.image.load('./image/title.png')
    SCREEN.blit(image_title,(0,SCREEN_HEIGHT/4))

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
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                ## if mouse is pressed get position of cursor ##
                pos = pygame.mouse.get_pos()
                ## check if cursor is on button ##
                if start_button.collidepoint(pos):
                    #game_Start()
                    start_image = pygame.image.load('./image/Start_button2.png').convert_alpha()
                    start_button = SCREEN.blit(start_image,(SCREEN_WIDTH/3,250))
                    pygame.display.flip()
                    winsound.PlaySound('./sound/button.wav', winsound.SND_FILENAME)
                    game_Level()
                    # pygame.display.flip()
                elif data_button.collidepoint(pos):
                    ## data ##
                    data_image = pygame.image.load('./image/Data_button2.png').convert_alpha()
                    data_button = SCREEN.blit(data_image,(SCREEN_WIDTH/3+5,300))
                    pygame.display.flip()
                    winsound.PlaySound('./sound/button.wav', winsound.SND_FILENAME)
                    game_Data()
                elif exit_button.collidepoint(pos):
                    ## exit ##
                    exit_image = pygame.image.load('./image/exit_button2.png').convert_alpha()
                    exit_button = SCREEN.blit(exit_image,(SCREEN_WIDTH/3+10,350))
                    pygame.display.flip()
                    winsound.PlaySound('./sound/button.wav', winsound.SND_FILENAME)
                    pygame.quit()

#################################################
#                  game_Level():                 #
#################################################
def game_Level():
    pygame.mouse.set_visible(1)
    background = pygame.Surface(SCREEN.get_size())
    background = background.convert()
    background.fill((250,250,250))
    SCREEN.blit(background, (0,0))

    level1 = pygame.image.load('./image/level1.png')
    level2 = pygame.image.load('./image/level2.png')
    level3 = pygame.image.load('./image/level3.png')

    button1 = SCREEN.blit(level1,(SCREEN_WIDTH/3-10, 100))
    button2 = SCREEN.blit(level2,(SCREEN_WIDTH/3-10, 200))
    button3 = SCREEN.blit(level3,(SCREEN_WIDTH/3-10, 300))
    pygame.display.flip()

    global TEXT_SPEED
    global GAME_LEVEL
    
    playing = True
    while playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                winsound.PlaySound('./sound/button.wav', winsound.SND_FILENAME)
                playing = False
                game_Title()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                winsound.PlaySound('./sound/button.wav', winsound.SND_FILENAME)
                ## if mouse is pressed get position of cursor ##
                pos = pygame.mouse.get_pos()
                ## check if cursor is on button ##
                try:
                    if button1.collidepoint(pos):
                        ## level1 ##
                        GAME_LEVEL=1
                        TEXT_SPEED = 10
                        game_Start()
                        playing = False
                        # pygame.display.flip()
                    elif button2.collidepoint(pos):
                        ## level2 ##
                        GAME_LEVEL=2
                        TEXT_SPEED = 30
                        game_Start()
                        playing = False
                    elif button3.collidepoint(pos):
                        ## level3 ##
                        GAME_LEVEL=3
                        TEXT_SPEED = 50
                        game_Start()
                        playing = False
                except IndexError:
                    pass
        
                    
#################################################
#                  game_start():                #
#################################################
def game_Start():
    #DB 생성
    conn = sqlite3.connect('./resource/records.db', isolation_level=None)

    #cursor 연결
    cursor = conn.cursor()

    #테이블 생성
    cursor.execute("CREATE TABLE IF NOT EXISTS records(\
        Score INTEGER, Record tex, Regdate tex)")
    #table select
    cursor.execute("select * from records")
    insert_list = cursor.fetchall()
    
    words = [] # 영어 단어 리스트(1000개 로드)
    try:
        word_f = open('./resource/word.txt','r',encoding='utf-8')
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
    
    # Start Time
    start = time.time()

    playing = True
    while playing:
        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                winsound.PlaySound('./sound/button.wav', winsound.SND_FILENAME)
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
        pygame.draw.rect(SCREEN, BLACK, [0,455,400,45],2)

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
            if GAME_LEVEL==3:
                speed=randint(10,40)
            else :
                speed = TEXT_SPEED
            text.move_y(speed) 
            if text.is_screen_out(): #텍스트가 내려가다가 설정한 밑바닥에 닿으면 목숨 - 1
                screen_in_texts.remove(text) 
                lifes.pop()
                # 게임 종료되었을때 GAME_OVER 화면에 출력
                if len(lifes) == 0:
                    end = time.time()       # End Time
                    et = end - start        # 총 게임 시간
                    et = format(et, ".3f")  # 소수 셋째 자리 출력(시간)

                    SCREEN.fill(GRAY)
                    pygame.display.flip()
                    clock.tick(FPS)
                    pygame.display.update()

                    # PRINT "GAME_OVER"
                    font = pygame.font.Font(None, 40)
                    text_surface = font.render("GAME_OVER", True, WHITE)
                    text_rect = text_surface.get_rect()
                    text_rect.center = (200, 150)

                    SCREEN.blit(text_surface, text_rect)
                    pygame.display.flip()
                    clock.tick(FPS)
                    pygame.display.update()
                    
                    ## 결과 기록
                    cursor.execute("INSERT INTO records('Score', 'Record', 'Regdate')\
                        VALUES(?,?,?)", (score, et, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

                    ## 접속 해제
                    conn.close()

                    sleep(2)
                    pygame.display.update()
                    game_Title()
                    # 게임 플레이 결과 확인 후 플레이어가 엔터 누를 때 종료
                    # sleep(10)
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


#################################################
#                  game_data():                 #
#################################################
def game_Data():
    #DB 생성
    conn = sqlite3.connect('./resource/records.db', isolation_level=None)

    #cursor 연결
    cursor = conn.cursor()

    #테이블 생성
    cursor.execute("CREATE TABLE IF NOT EXISTS records(\
        Score INTEGER, Record tex, Regdate tex)")
    #table select
    cursor.execute("select * from records")
    insert_list = cursor.fetchall()

    #GUI창 생성
    root = tkinter.Tk()
    root.title("record")
    root.geometry("350x270+585+220")
    root.resizable(False, False)
    # label 생성
    lbl = tkinter.Label(root, text="RECORD")
    lbl.pack()
    #quit 버튼 생성
    #quit_button = Button(root, text="QUIT", command= game_Title())
    #quit_button.place(x=0, y=0)
    #quit_button.pack()
    #표생성
    treeview = tkinter.ttk.Treeview(root, columns=["one", "two", "three"], displaycolumns=["one", "two", "three"])
    treeview.pack()

    #각 컬럼 설정
    treeview.column("#0", width=50, anchor="center")
    treeview.heading("#0", text="ID")

    treeview.column("#1", width=50, anchor="center")
    treeview.heading("one", text="SCORE", anchor="center")

    treeview.column("#2", width=60, anchor="center")
    treeview.heading("two", text="RECORD", anchor="center")

    treeview.column("#3", width=150, anchor="center")
    treeview.heading("three", text="REGDATE", anchor="center")

    treeview.scrollable = True


    # db 데이터를 표에 삽입
    for i in range(len(insert_list)):
        treeview.insert('', 'end', text=i, values=insert_list[i], iid=str(i)+"번")

    root.mainloop()
    winsound.PlaySound('./sound/button.wav', winsound.SND_FILENAME)
    root.protocol('WM_DELETE_WINDOW', game_Title()) # 창 닫으면 game_Title 실행
    
    # DB 접속 해제
    conn.close()

#### MAIN #####
game_Title()
pygame.quit()