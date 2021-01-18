import pygame
import random
import time
import sys

class Word:
    def __init__(self, word,x,y):
        self.word=word
        self.x=x
        self.y=y
        # Font 객체 생성
        myFont = pygame.font.SysFont("arial", 30, True, False)
        # Text를 surface에 그리기, 안티알리어싱, 검은색
        self.text_Title=myFont.render(self.word, True, BLACK)
    def move_y(self):
        self.y+=10
    # 스크린에 그리기
    def draw_word(self):
        SCREEN.blit(self.text_Title, [self.x, self.y])
    


# 스크린 전체 크기 지정
SCREEN_WIDTH = 400
SCREEN_HEIGHT  = 500

# 색상 상수
BLACK = (0, 0, 0)

# pygame 초기화
pygame.init()

# 스크린 객체 저장
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("타이핑 게임")

# FPS를 위한 Clock 생성
clock = pygame.time.Clock()

words = [] # 영어 단어 리스트(1000개 로드)
try:
    word_f = open('./finalExam/word.txt','r',encoding='utf-8')
    i=0 #1000 이 되면 종료
    while True:
        line=word_f.readline()
        if not line or i==1000:
            break
        words.append(Word(line.strip(),5,-50))
        i+=1
except IOError:
    print("파일이 없습니다!! 게임을 진행할 수 없습니다!!")

if words==[]:
    sys.exit()

#테스트
current_time = 0
test=0
a_time=2

playing = True
while playing:
    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
            pygame.quit()

    # 스크린 배경색 칠하기
    SCREEN.fill((255, 255, 255))

    mt = clock.tick(24) / 1000

    # 텍스트 위에서 아래로
    current_time += mt
    print(current_time)
    if current_time > a_time:
        test+=1
        current_time = 0
            
    for i in range(test):
        words[i].draw_word()
        words[i].move_y()

    # 작업한 스크린의 내용을 갱신하기
    pygame.display.flip()

    # FPS:24
    clock.tick(24)




