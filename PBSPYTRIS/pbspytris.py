# -*-coding:utf-8-*-
# PYTRIS Copyright (c) 2017 Jason Kim All Rights Reserved.

import pygame
import operator
import wave
import os
from mino import *
from random import *
from pygame.locals import *
from var import *
from DB import *

# Unchanged values Define 변하지 않는 변수 선언

block_size = 17  # Height, width of single block
width = 10
height = 20

board_x = 10
board_y = 20
board_width = 800 # Board width
board_height = 450 # Board height
board_rate = 0.5625 #가로세로비율
block_size = int(board_height * 0.045)
mino_matrix_x = 4 #mino는 4*4 배열이어서 이를 for문에 사용
mino_matrix_y = 4 #mino는 4*4 배열이어서 이를 for문에 사용

speed_change = 40 # 레벨별 블록 하강 속도 상승 정도

framerate = 30  # Bigger -> Slower

min_width = 400
min_height = 225
mid_width = 1200

total_time = 60 # 타임 어택 시간
attack_time = 30 # 어택모드 제한시간

# 기본 볼륨
music_volume = 5
effect_volume = 5

initalize = True

pygame.init()


# Class 설정
# Inputbox 초기 설정
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
FONT = pygame.font.Font(None, 32)

clock = pygame.time.Clock() #창, 화면을 초당 몇번 출력하는가(FPS) clock.tick 높을수록 cpu많이 사용
screen = pygame.display.set_mode((board_width, board_height), pygame.RESIZABLE) #GUI창 설정하는 변수
pygame.display.set_caption("PBSPYTRIS") #GUI 창의 이름

class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)

# input box 설정
#signup할때 box
input_box1 = InputBox(int(board_width*322/800), int(board_height*195.5/450), 156, 32)
input_box2 = InputBox(int(board_width*322/800), int(board_height*242.5/450), 156, 32)
input_boxes_signup = [input_box1, input_box2]
#signin할때 box
input_box3 = InputBox(int(board_width*322/800), int(board_height*195.5/450), 156, 32)
input_box4 = InputBox(int(board_width*322/800), int(board_height*242.5/450), 156, 32)
input_boxes_signin = [input_box3, input_box4]

class ui_variables:
    font_path = "./assets/fonts/OpenSans-Light.ttf"
    font_path_b = "./assets/fonts/OpenSans-Bold.ttf"
    font_path_i = "./assets/fonts/Inconsolata/Inconsolata.otf"

    # Font(글씨체, 글자크기)
    h1 = pygame.font.Font(font_path_b, 80)
    h2 = pygame.font.Font(font_path_b, 30)
    h3 = pygame.font.Font(font_path_b, 25)
    h4 = pygame.font.Font(font_path_b, 20)
    h5 = pygame.font.Font(font_path_b, 13)
    h6 = pygame.font.Font(font_path_b, 10)

    h1_b = pygame.font.Font(font_path_b, 30)
    h2_b = pygame.font.Font(font_path_b, 30)

    h2_i = pygame.font.Font(font_path_i, 30)
    h5_i = pygame.font.Font(font_path_i, 13)

    # Sounds
    pygame.mixer.music.load("assets/sounds/SFX_BattleMusic.wav") #음악 불러옴
    pygame.mixer.music.set_volume(0.5) # 이 부분도 필요 없음, set_volume에 추가해야 함
    intro_sound = pygame.mixer.Sound("assets/sounds/SFX_Intro.wav")
    fall_sound = pygame.mixer.Sound("assets/sounds/SFX_Fall.wav")
    break_sound = pygame.mixer.Sound("assets/sounds/SFX_Break.wav")
    click_sound = pygame.mixer.Sound("assets/sounds/SFX_ButtonUp.wav") #여기부터
    move_sound = pygame.mixer.Sound("assets/sounds/SFX_PieceMoveLR.wav")
    drop_sound = pygame.mixer.Sound("assets/sounds/SFX_PieceHardDrop.wav")
    single_sound = pygame.mixer.Sound("assets/sounds/SFX_SpecialLineClearSingle.wav")
    double_sound = pygame.mixer.Sound("assets/sounds/SFX_SpecialLineClearDouble.wav")
    triple_sound = pygame.mixer.Sound("assets/sounds/SFX_SpecialLineClearTriple.wav") #여기까지는 기존코드
    tetris_sound = pygame.mixer.Sound("assets/sounds/SFX_SpecialTetris.wav")
    LevelUp_sound = pygame.mixer.Sound("assets/sounds/SFX_LevelUp.wav")
    GameOver_sound = pygame.mixer.Sound("assets/sounds/SFX_GameOver.wav")

    # Combo graphic
    combos = []
    large_combos = []
    combo_ring = pygame.image.load("assets/Combo/4combo ring.png")  # 4블록 동시제거 그래픽
    combo_4ring = pygame.transform.smoothscale(combo_ring,
                     (int(board_width*0.25), int(board_height*0.222)))
    #이미지를 특정 크기로 불러옴, 200=가로크기, 100=세로크기
    for i in range(1, 11): #10가지의 콤보 이미지 존재. 각 숫자에 해당하는 이미지 불러옴
        combos.append(pygame.image.load("assets/Combo/" + str(i) + "combo.png"))
        large_combos.append(pygame.transform.smoothscale(combos[i - 1],
         (int(board_width*0.1875), int(board_height*0.4444)))) #콤보이미지를 특정 크기로 불러옴, 150=가로크기, 200=세로크기#

    combos_sound = []
    for i in range(1, 10): #1-9까지 콤보사운드 존재. 각 숫자에 해당하는 음악 불러옴
        combos_sound.append(pygame.mixer.Sound("assets/sounds/SFX_" + str(i + 2) + "Combo.wav"))

    #rainbow 보너스점수 graphic
    rainbow_vector = pygame.image.load('assets/vector/rainbow.png')

    # Background colors. RGB 값에 해당함
    black = (10, 10, 10)  # rgb(10, 10, 10)
    black_pause = (0, 0, 0, 127)
    white = (0, 153, 153)  # rgb(255, 255, 255) # 청록색으로 변경
    real_white = (255, 255, 255)  # rgb(255, 255, 255)
    skyblue = (173,211,210) #rgb(250, 165, 255) 핑크+보라#

    grey_1 = (70, 130, 180)  # rgb(26, 26, 26) 테두리 파랑색
    grey_2 = (221, 221, 221)  # rgb(35, 35, 35)
    grey_3 = (000, 000, 139)  # rgb(55, 55, 55) #남색
    bright_yellow = (255, 217, 102)  # 밝은 노랑

    # Tetrimino colors. RGB 값에 해당함
    cyan = (10, 255, 226)  # rgb(69, 206, 204) # I
    blue = (64, 105, 255)  # rgb(64, 111, 249) # J
    orange = (245, 144, 12)  # rgb(253, 189, 53) # L
    yellow = (225, 242, 41)  # rgb(246, 227, 90) # O
    green = (22, 181, 64)  # rgb(98, 190, 68) # S
    pink = (242, 41, 195)  # rgb(242, 64, 235) # T
    red = (204, 22, 22)  # rgb(225, 13, 27) # Z

    t_color = [grey_2, cyan, blue, orange, yellow, green, pink, red, grey_3]
    cyan_image = 'assets/block_images/cyan.png'
    blue_image = 'assets/block_images/blue.png'
    orange_image = 'assets/block_images/orange.png'
    yellow_image = 'assets/block_images/yellow.png'
    green_image = 'assets/block_images/green.png'
    pink_image = 'assets/block_images/purple.png'
    red_image = 'assets/block_images/red.png'
    ghost_image = 'assets/block_images/ghost.png'
    table_image = 'assets/block_images/background.png'
    linessent_image = 'assets/block_images/linessent.png'
    light_image = 'assets/block_images/lightblock.png' # lightblock image
    tnt_image = 'assets/block_images/tntblock.png' # tntblock image
    # item_image 2개 넣기
    t_block = [table_image, cyan_image, blue_image, orange_image, yellow_image, green_image, pink_image, red_image,
               ghost_image, linessent_image, light_image, tnt_image]

class button(): #버튼객체
    def __init__(self, board_width, board_height, x_rate, y_rate, width_rate, height_rate, img=''): #버튼생성
        self.x = board_width * x_rate #버튼 x좌표
        self.y = board_height * y_rate #버튼 y좌표
        self.width = int(board_width * width_rate) #버튼 너비
        self.height = int(board_height * height_rate) #버튼 높이
        self.x_rate = x_rate # x좌표를 만드는 비율
        self.y_rate = y_rate # y좌표를 만드는 비율
        self.width_rate = width_rate #board_width * width_rate = 버튼 너비
        self.height_rate = height_rate #board_height * height_rate = 버튼 높이
        self.image = img #불러올 버튼 이미지

    def change(self, board_width, board_height): #버튼 위치, 크기 바꾸기
        self.x = board_width * self.x_rate #x좌표
        self.y = board_height * self.y_rate #y좌표
        self.width = int(board_width * self.width_rate) #너비
        self.height = int(board_height * self.height_rate) #높이

    def draw(self, win, outline=None): #버튼 보이게 만들기
        if outline:
            draw_image(screen, self.image, self.x, self.y,
                 self.width, self.height)

    def isOver(self, pos): #마우스의 위치에 따라 버튼 누르기 pos[0]은 마우스 x좌표, pos[1]은 마우스 y좌표
        if pos[0] > self.x - (self.width / 2) and pos[0] < self.x + (self.width / 2):
            if pos[1] > self.y - (self.height / 2) and pos[1] < self.y + (self.height / 2):
                return True
        return False

    def isOver_2(self, pos):
        #start 화면에서 single,pvp,help,setting을 위해서 y좌표 좁게 인식하도록
        if pos[0] > self.x - (self.width / 2) and pos[0] < self.x + (self.width / 2):
            if pos[1] > self.y - (self.height / 4) and pos[1] < self.y + (self.height / 4):#243줄에서의 2을 4로 바꿔주면서 좁게 인식할수 있도록함. 더 좁게 인식하고 싶으면 숫자 늘려주기#
                return True
        return False

#버튼객체 생성 class Button에서 확인
#def __init__(self, board_width, board_height, x_rate, y_rate, width_rate, height_rate, img='')
#(현재 보드너비, 현재보드높이, 버튼의 x좌표 위치비율, 버튼의 y좌표 위치비율, 버튼의 너비 길이비율, 버튼의 높이 길이비율)
#  - 전체화면 크기에 대한 비율
# (800, 450, 800*x좌표, 450*y좌표, 너비 비율, 높이 비율)

# login page 1) main
sign_up_button1 = button(board_width, board_height, 0.415, 0.5, 12/80, 4/45, button_sign_up)
sign_in_button1 = button(board_width, board_height, 0.585, 0.5, 12/80, 4/45, button_sign_in)
log_quit = button(board_width, board_height, 0.5, 0.9, 0.16, 0.084, button_quit)
# login page 2) sign up / sign in
sign_up_button2 = button(board_width, board_height, 0.415, 0.7, 12/80, 4/45, button_sign_up)
sign_in_button2 = button(board_width, board_height, 0.415, 0.7, 12/80, 4/45, button_sign_in)
log_back = button(board_width, board_height, 0.585, 0.7, 12/80, 4/45, button_log_back)

# main page 1) nothing
game_button = button(board_width, board_height, 0.375, 0.8, 0.16, 0.084, button_game)
help_button = button(board_width, board_height, 0.375, 0.9, 0.16, 0.084, button_help)
shop_button = button(board_width, board_height, 0.625, 0.8, 0.16, 0.084, button_shop)
quit_button = button(board_width, board_height, 0.625, 0.9, 0.16, 0.084, button_quit)

challenge_vector = button(board_width, board_height, 0.05, 0.9,0.0625, 0.1111, vector_challenge)
leader_vector = button(board_width, board_height, 0.15, 0.9,0.0625, 0.1111, vector_leader)
setting_vector = button(board_width, board_height, 0.95, 0.9,0.0625, 0.1111, vector_setting)

# main page 2) start board
single_button = button(board_width, board_height, 0.3, 0.38, 0.16, 0.084, button_single)
timeattack_button = button(board_width, board_height, 0.3, 0.58, 0.16, 0.084, button_timeattack)
sandbox_button = button(board_width, board_height, 0.7, 0.58, 0.16, 0.084, button_sandbox)
difficulty_button = button(board_width, board_height, 0.7, 0.38, 0.16, 0.084, button_difficulty)
back_button = button(board_width, board_height, 0.5, 0.725, 0.16, 0.084, button_back)
# same in start,leader, help
# setting, volume, screen board

# main page 3) sandbox board
attack_button = button(board_width, board_height, 0.3, 0.35, 0.16, 0.084, button_attack)
gravity_button = button(board_width, board_height, 0.3, 0.51, 0.16, 0.084, button_gravity)
back_right_button = button(board_width, board_height, 0.65, 0.66, 0.16, 0.084, button_back)
start_left_button = button(board_width, board_height, 0.35, 0.66, 0.16, 0.084, button_start)
# back and start is same
# sandbox, difficulty board


level_minus_vector = button(board_width, board_height,
         0.7275, 0.43, 0.04, 0.0711, vector_minus)

level_plus_vector = button(board_width, board_height,
         0.8475, 0.43, 0.04, 0.0711, vector_plus)

# level_icon 0.6125, 0.67, 0.16, 0.084
# combo_icon 0.6125, 0.77, 0.16, 0.084
# speed_icon 0.6125, 0.87, 0.16, 0.084

# main page 4) difficulty board
easy_button     = button(board_width, board_height, 0.3, 0.37, 0.16, 0.084, button_easy)
normal_button   = button(board_width, board_height, 0.5, 0.37, 0.16, 0.084, button_normal)
hard_button     = button(board_width, board_height, 0.7, 0.37, 0.16, 0.084, button_hard)

# main page 5) help board
# help board
# help image

# main page 6) leader board
rank_single = button(board_width, board_height, 0.2, 0.3, 0.1, 0.0527, button_single)
rank_easy = button(board_width, board_height, 0.35, 0.3, 0.1, 0.0527, button_easy)
rank_normal = button(board_width, board_height, 0.5, 0.3, 0.1, 0.0527, button_normal)
rank_hard = button(board_width, board_height, 0.65, 0.3, 0.1, 0.0527, button_hard)
rank_ta = button(board_width, board_height, 0.8, 0.3, 0.1, 0.0527, button_timeattack)


# main page 7) setting board
volume_vector = button(board_width, board_height, 0.4, 0.4, 0.125, 0.2222, vector_volume)
screen_vector = button(board_width, board_height, 0.6, 0.4, 0.125, 0.2222, vector_screen)

# main page 8) volume board
allmute_button = button(board_width, board_height, 0.5, 0.24, 0.16, 0.084, button_allmute)

# music_number_board 0.46, 0.38, 0.04, 0.53
music_plus_vector = button(board_width, board_height,
 0.38, 0.38, 0.04, 0.0711, vector_plus)
music_minus_vector = button(board_width, board_height,
 0.54, 0.38, 0.04, 0.0711, vector_minus)
music_on_button = button(board_width, board_height,
 0.62, 0.38, 0.0625, 0.1111, vector_sound_on)


# effect_number_board 0.46, 0.52, 0.04, 0.53
effect_plus_vector = button(board_width, board_height,
 0.38, 0.52, 0.04, 0.0711, vector_plus)
effect_minus_vector = button(board_width, board_height,
 0.54, 0.52, 0.04, 0.0711, vector_minus)
effect_on_button = button(board_width, board_height,
 0.62, 0.52, 0.0625, 0.1111, vector_sound_on)


# main page 9) screen board
smallsize_button = button(board_width, board_height, 0.5, 0.24, 0.2, 0.08, size_s)
midiumsize_button = button(board_width, board_height, 0.5, 0.38, 0.2, 0.08, size_m)
bigsize_button = button(board_width, board_height, 0.5, 0.52, 0.2, 0.08, size_b)

# main page 10) shop board
tnt_buy_button = button(board_width, board_height, 0.72, 0.3, 0.0925, 0.04, button_buy)
light_buy_button = button(board_width, board_height, 0.72, 0.45, 0.0925, 0.04, button_buy)
earth_buy_button = button(board_width, board_height, 0.72, 0.6, 0.0925, 0.04, button_buy)

# main page 11) challenge board
off1_button = button(board_width, board_height, 0.8, 0.28, 105/800, 40/450, off)
off2_button = button(board_width, board_height, 0.8, 0.44, 105/800, 40/450, off)
off3_button = button(board_width, board_height, 0.8, 0.60, 105/800, 40/450, off)


# game page 1) pause board
resume_button = button(board_width, board_height, 0.5, 0.33, 0.16, 0.084, button_resume)
restart_button = button(board_width, board_height, 0.5, 0.51, 0.16, 0.084, button_restart)
setting_button = button(board_width, board_height, 0.5, 0.69, 0.16, 0.084, button_setting)
quit_game_button = button(board_width, board_height, 0.5, 0.87, 0.16, 0.084, button_quit)

# gmae page 2) setting board
# 위와 동일

# game page 3) volume board
# 위와 동일

# game page 4) screen board
# 위와 동일

# game page 5) game over board
menu_button = button(board_width, board_height, 0.5, 0.33, 0.16, 0.084, button_menu)
# restart
ok_button = button(board_width, board_height, 0.5, 0.87, 0.16, 0.084, button_ok)

# sandbox
level_plus_button = button(board_width, board_height, 0.63, 0.7719, 0.0375, 0.0666, vector_plus)
level_minus_button = button(board_width, board_height, 0.56, 0.7719, 0.0375, 0.0666, vector_minus)


#게임 중 버튼 생성하기위한 버튼객체 리스트 (버튼 전체)
button_list = [
    game_button, help_button, shop_button, quit_button, challenge_vector,
    leader_vector, setting_vector, single_button, timeattack_button, sandbox_button,
    difficulty_button, back_button, attack_button, gravity_button,
    back_right_button, start_left_button, level_minus_vector, level_plus_vector,
    easy_button, normal_button, hard_button, volume_vector, screen_vector,
    allmute_button, music_plus_vector, music_minus_vector, music_on_button,
    effect_plus_vector, effect_minus_vector, effect_on_button,
    smallsize_button, midiumsize_button, bigsize_button, light_buy_button,
    tnt_buy_button, earth_buy_button, resume_button,
    restart_button, setting_button, quit_game_button, menu_button, ok_button,
    level_plus_button, level_minus_button, off1_button, off2_button, off3_button,
    sign_up_button1, sign_up_button2, sign_in_button1, sign_in_button2,
    log_back, log_quit, rank_single, rank_easy, rank_normal, rank_hard, rank_ta
]

def set_volume():
    ui_variables.fall_sound.set_volume(effect_volume / 10) #set_volume의 argument는 0.0~1.0으로 이루어져야하기 때문에 소수로 만들어주기 위해 10으로 나눔#
    ui_variables.click_sound.set_volume(effect_volume / 10)
    ui_variables.break_sound.set_volume(effect_volume / 10)
    ui_variables.move_sound.set_volume(effect_volume / 10)
    ui_variables.drop_sound.set_volume(effect_volume / 10)
    ui_variables.single_sound.set_volume(effect_volume / 10)
    ui_variables.double_sound.set_volume(effect_volume / 10)
    ui_variables.triple_sound.set_volume(effect_volume / 10)
    ui_variables.tetris_sound.set_volume(effect_volume / 10)
    ui_variables.LevelUp_sound.set_volume(effect_volume / 10)
    ui_variables.GameOver_sound.set_volume(music_volume / 10)
    ui_variables.intro_sound.set_volume(music_volume / 10)
    pygame.mixer.music.set_volume(music_volume / 10)
    for i in range(1, 10): #10가지의 combo 사운드를 한번에 조절함
        ui_variables.combos_sound[i - 1].set_volume(effect_volume / 10)


def draw_image(window, img_path, x, y, width, height):
    x = x - (width / 2) #해당 이미지의 가운데 x좌표, 가운데 좌표이기 때문에 2로 나눔
    y = y - (height / 2) #해당 이미지의 가운데 y좌표, 가운데 좌표이기 때문에 2로 나눔
    image = pygame.image.load(img_path)
    image = pygame.transform.smoothscale(image, (width, height))
    window.blit(image, (x, y))


# Draw block
def draw_block(x, y, color):
    pygame.draw.rect(
        screen,
        color,
        Rect(x, y, block_size, block_size)
    )
    pygame.draw.rect(
        screen,
        ui_variables.grey_1,
        Rect(x, y, block_size, block_size),
        1
    )


def draw_block_image(x, y, image):
    draw_image(screen, image, x, y, block_size, block_size) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)


# grid[i][j] = 0 / matrix[tx + j][ty + i] = 0에서
# 0은 빈 칸 / 1-7은 테트리스 블록 종류 / 8은 ghost / 9은 장애물(벽돌)/ 10은 light item, 11는 tnt item 에 해당함 = t_block 참고

# Draw game screen
def draw_board(next1, next2, hold, score, level, goal):
    sidebar_width = int(board_width * 0.5312)
    #크기 비율 고정, 전체 board 가로길이에서 원하는 비율을 곱해줌#

    # Draw sidebar
    pygame.draw.rect(
        screen,
        ui_variables.skyblue,
        Rect(sidebar_width, 0, int(board_width * 0.2375), board_height) #크기 비율 고정
    )

    # Draw item
    dx3 = int(board_width*0.715)
    dy3_1 = int(board_height*0.578)
    dy3_2 = int(board_height*0.711)
    dy3_3 = int(board_height*0.844)
    i_size_x = int(board_width*0.05)
    i_size_y = int(board_height*0.089)
    if difficulty_mode:
        draw_image(screen, item_light, dx3, dy3_1, i_size_x, i_size_y)
        draw_image(screen, item_tnt, dx3, dy3_2, i_size_x, i_size_y)
        draw_image(screen, item_earth, dx3, dy3_3, i_size_x, i_size_y)
    
        


    # Draw next mino 다음 블록
    grid_n1 = tetrimino.mino_map[next1 - mino_x][mino_y] #(배열이라-1) 다음 블록의 원래 모양
    grid_n2 = tetrimino.mino_map[next2 - mino_x][mino_y] #(배열이라-1) 다음 블록의 원래 모양

    for i in range(mino_matrix_y): #다음 블록
        for j in range(mino_matrix_x):
            dx1 = int(board_width * 0.025) + sidebar_width + block_size * j #위치 비율 고정, 전체 board 가로길이에서 원하는 비율을 곱해줌#
            dy1 = int(board_height * 0.3743) + block_size * i #위치 비율 고정, 전체 board 세로길이에서 원하는 비율을 곱해줌#
            if grid_n1[i][j] != mino_zero: #해당 부분에 블록 존재하면
                draw_block_image(dx1, dy1, ui_variables.t_block[grid_n1[i][j]]) #블록 이미지 출력

    for i in range(mino_matrix_y): #다다음블록
        for j in range(mino_matrix_x):
            dx2 = int(board_width * 0.145) + sidebar_width + block_size * j #위치 비율 고정, 전체 board 가로길이에서 원하는 비율을 곱해줌#
            dy2 = int(board_height * 0.3743) + block_size * i #위치 비율 고정, 전체 board 세로길이에서 원하는 비율을 곱해줌#
            if grid_n2[i][j] != mino_zero: #해당 부분에 블록 존재하면
                draw_block_image(dx2, dy2, ui_variables.t_block[grid_n2[i][j]]) #블록 이미지 출력

    # Draw hold mino
    grid_h = tetrimino.mino_map[hold - mino_x][mino_y]  #(배열이라-1) 기본 모양

    if hold_mino != h_mino: #hold 존재X
        for i in range(mino_matrix_y):
            for j in range(mino_matrix_x):
                dx = int(board_width * 0.045) + sidebar_width + block_size * j #위치 비율 고정
                dy = int(board_height * 0.1336) + block_size * i #위치 비율 고정
                if grid_h[i][j] != mino_zero: #해당 부분에 블록이 존재하면
                    draw_block_image(dx, dy, ui_variables.t_block[grid_h[i][j]]) #hold 블록 출력

    # Set max score
    if score > max_score:
        score = max_score #최대 점수가 999999를 넘기지 못하도록 설정#

    # Draw texts
    #render("텍스트이름", 안티에일리어싱 적용, 색깔), 즉 아래의 코드에서 숫자 1=안티에일리어싱 적용에 관한 코드
    if textsize==False:
        text_hold = ui_variables.h5.render("HOLD", 1, ui_variables.real_white)
        text_next = ui_variables.h5.render("NEXT", 1, ui_variables.real_white)
        text_score = ui_variables.h5.render("SCORE", 1, ui_variables.real_white)
        score_value = ui_variables.h4.render(str(score), 1, ui_variables.real_white)
        text_level = ui_variables.h5.render("LEVEL", 1, ui_variables.real_white)
        level_value = ui_variables.h4.render(str(level), 1, ui_variables.real_white)
        text_combo = ui_variables.h5.render("COMBO", 1, ui_variables.real_white)
        combo_value = ui_variables.h4.render(str(combo_count), 1, ui_variables.real_white)
        light_value = ui_variables.h4.render(str(num_light), 1, ui_variables.real_white)
        earth_value = ui_variables.h4.render(str(num_earthquake), 1, ui_variables.real_white)
        tnt_value = ui_variables.h4.render(str(num_tnt), 1, ui_variables.real_white)
        if time_attack:
            time = total_time - elapsed_time
            value = ui_variables.h5.render("TIME : "+str(int(time)), 1, ui_variables.real_white)
            screen.blit(value, (int(board_width * -0.445) + sidebar_width, int(board_height * 0.015))) #각각 전체 board 가로길이, 세로길이에 대한 원하는 비율을 곱해줌#
        if attack_mode:
            time = attack_time - elapsed_attack_time
            value = ui_variables.h5.render("TIME : "+str(int(time)), 1, ui_variables.real_white)
            screen.blit(value, (int(board_width * -0.445) + sidebar_width, int(board_height * 0.015))) #각각 전체 board 가로길이, 세로길이에 대한 원하는 비율을 곱해줌#

    if textsize==True: #render("텍스트이름", 안티에일리어싱 적용, 색깔), 즉 아래의 코드에서 숫자 1=안티에일리어싱 적용에 관한 코드
        text_hold = ui_variables.h3.render("HOLD", 1, ui_variables.real_white)
        text_next = ui_variables.h3.render("NEXT", 1, ui_variables.real_white)
        text_score = ui_variables.h3.render("SCORE", 1, ui_variables.real_white)
        score_value = ui_variables.h2.render(str(score), 1, ui_variables.real_white)
        text_level = ui_variables.h3.render("LEVEL", 1, ui_variables.real_white)
        level_value = ui_variables.h2.render(str(level), 1, ui_variables.real_white)
        text_combo = ui_variables.h3.render("COMBO", 1, ui_variables.real_white)
        combo_value = ui_variables.h2.render(str(combo_count), 1, ui_variables.real_white)
        light_value = ui_variables.h4.render(str(num_light), 1, ui_variables.real_white)
        earth_value = ui_variables.h4.render(str(num_earthquake), 1, ui_variables.real_white)
        tnt_value = ui_variables.h4.render(str(num_tnt), 1, ui_variables.real_white)
        if time_attack:
            time = total_time - elapsed_time
            value = ui_variables.h2.render("TIME : "+str(int(time)), 1, ui_variables.real_white)
            screen.blit(value, (int(board_width * -0.445) + sidebar_width, int(board_height * 0.015)))
        if attack_mode:
            time = attack_time - elapsed_attack_time
            value = ui_variables.h5.render("TIME : "+str(int(time)), 1, ui_variables.real_white)
            screen.blit(value, (int(board_width * -0.445) + sidebar_width, int(board_height * 0.015))) #각각 전체 board 가로길이, 세로길이에 대한 원하는 비율을 곱해줌#

    #if time_attack:
    #    time = total_time - elapsed_time
    #    value = ui_variables.h5.render("TIME : "+str(int(time)), 1, ui_variables.real_white)
    #    screen.blit(value, (int(board_width * -0.445) + sidebar_width, int(board_height * 0.015)))
    # Place texts. 위치 비율 고정, 각각 전체 board 가로길이, 세로길이에 대한 원하는 비율을 곱해줌#
    screen.blit(text_hold, (int(board_width * 0.045) + sidebar_width, int(board_height * 0.0374)))
    screen.blit(text_next, (int(board_width * 0.045) + sidebar_width, int(board_height * 0.2780)))
    screen.blit(text_score, (int(board_width * 0.045) + sidebar_width, int(board_height * 0.5187)))
    screen.blit(score_value, (int(board_width * 0.055) + sidebar_width, int(board_height * 0.5614)))
    screen.blit(text_level, (int(board_width * 0.045) + sidebar_width, int(board_height * 0.6791)))
    screen.blit(level_value, (int(board_width * 0.055) + sidebar_width, int(board_height * 0.7219)))
    screen.blit(text_combo, (int(board_width * 0.045) + sidebar_width, int(board_height * 0.8395)))
    screen.blit(combo_value, (int(board_width * 0.055) + sidebar_width, int(board_height * 0.8823)))

    if difficulty_mode:
        screen.blit(light_value, (int(board_width*0.715), int(board_height*0.62)))
        screen.blit(tnt_value, (int(board_width*0.715), int(board_height * 0.78)))
        screen.blit(earth_value, (int(board_width*0.715), int(board_height * 0.90)))

    # Draw board
    for x in range(width):
        for y in range(height):
            dx = int(board_width * 0.25) + block_size * x  #위치비율 고정, board 가로길이에 원하는 비율을 곱해줌#
            dy = int(board_height * 0.055) + block_size * y #위치비율 고정, board 세로길이에 원하는 비율을 곱해줌#
            draw_block_image(dx, dy, ui_variables.t_block[matrix[x][y + mino_x]])


# Draw a tetrimino
def draw_mino(x, y, mino, r, matrix): #mino는 모양, r은 회전된 모양 중 하나
    grid = tetrimino.mino_map[mino - mino_x][r] #grid : 출력할 테트리스

    tx, ty = x, y
    while not is_bottom(tx, ty, mino, r, matrix): #테트리스가 바닥에 존재하면 true -> not이니까 바닥에 없는 상태
        ty += mino_x #한칸 밑으로 하강

    # Draw ghost
    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            if grid[i][j] != mino_zero: #테트리스 블록에서 해당 행렬위치에 블록 존재하면
                matrix[tx + j][ty + i] = g_mino #테트리스가 쌓일 위치에 8 이라는 ghost 만듦

    # Draw mino
    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            if grid[i][j] != mino_zero:  #테트리스 블록에서 해당 행렬위치에 블록 존재하면
                matrix[x + j][y + i] = grid[i][j] #해당 위치에 블록 만듦

# Erase a tetrimino
def erase_mino(x, y, mino, r, matrix):
    grid = tetrimino.mino_map[mino - mino_x][r]

    # Erase ghost
    for j in range(board_y+1):
        for i in range(board_x):
            if matrix[i][j] == g_mino: #테트리스 블록에서 해당 행렬위치에 ghost블록 존재하면
                matrix[i][j] = mino_zero  #없애서 빈 곳으로 만들기

    # Erase mino
    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            if grid[i][j] != mino_zero:  #테트리스 블록에서 해당 행렬위치에 블록 존재하면
                matrix[x + j][y + i] = mino_zero #해당 위치에 블록 없애서 빈 곳으로 만들기

    # light item
    for j in range(board_y+1):
        for i in range(board_x):
            if matrix[i][j] == light_mino: #테트리스 블록에서 해당 행렬위치에 lightning 블록 존재하면
                m = i-1
                n = j-1
                for k in range(l_range):
                    for q in range(l_range):
                        if m+k >= mino_zero and n+q >= mino_zero :
                            matrix[m+k][n+q] = mino_zero
                 

    # tnt item
    for j in range(board_y+1):
        for i in range(board_x):
            if matrix[i][j] == tnt_mino: #테트리스 블록에서 해당 행렬위치에 TNT 블록 존재하면
                m = i-2
                n = j-2
                for k in range(t_range):
                    for q in range(t_range):
                        if m+k >= mino_zero and n+q >= mino_zero :
                            matrix[m+k][n+q] = mino_zero

# Returns true if mino is at bottom
def is_bottom(x, y, mino, r, matrix):
    grid = tetrimino.mino_map[mino - mino_x][r] #grid : 출력할 테트리스

    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            if grid[i][j] != mino_zero: #테트리스 블록에서 해당 행렬위치에 블록 존재하면
                if (y + i + mino_x) > board_y :   #바닥의 y좌표에 있음(바닥에 닿음)
                    return True
                elif matrix[x + j][y + i + mino_x] != mino_zero and matrix[x + j][y + i + mino_x] != g_mino: #그 블록위치에 0, 8 아님(즉 블록 존재 함)
                    return True

    return False

def earthquake(y,matrix):
    
    for i in range(board_x): # 가로줄 전체에 대해서
        matrix[i][y] = mino_zero
    
        
def gravity(x, y, mino, r, matrix):
    grid = tetrimino.mino_map[mino - mino_x][r] #grid : 출력할 테트리스

    for j in range(mino_matrix_x-mino_r, -mino_r, -mino_r): #mino_matrix 4*4 배열이므로 -1 해서 3, 2, 1, 0 index로 for문을 돎
        for i in range(mino_matrix_y-mino_r, -mino_r, -mino_r):  #mino_matrix 4*4 배열이므로 -1 해서 3, 2, 1, 0 index로 for문을 돎
            if grid[i][j] != mino_zero: #테트리스 블록에서 해당 행렬위치에 블록 존재하면
                dy = y
                if ((dy + i) == board_y or (matrix[x + j][dy + i+mino_r] != mino_zero)) : #바닥에 닿았거나, 해당 위치 아랫칸에 블록이 이미 존재하는 경우
                    matrix[x+j][dy+i] = grid[i][j] #그 위치에 그대로 테트리스 블록을 둠
                else :
                    while((dy + mino_r + i) <= board_y and (matrix[x + j][dy + i + mino_r] == 0)): #바닥에 닿지 않았으며, 해당 위치 아랫칸에 블록이 없는 경우 (= 공중에 떠있는 경우)
                        dy+=1 #이 조건에서 벗어날 때까지 계속해서 한 칸씩 밑으로 떨어뜨림
                        matrix[x+j][dy+i] = f_mino  #떨어지는 블록은 장애물 블록으로 표현
                        matrix[x+j][dy+i-mino_r] = mino_zero  #블록이 한칸 떨어졌으니, 그 위의 기존블록 또는 만들어두었던 장애물 블록은 빈칸으로 처리함(없앰)

def attack(y,matrix):
    for i in range(board_x): # 가로줄 전체에 대해서
        matrix[i][y] = f_mino # 맨 밑줄부터 장애물 블록으로 채워짐

# Returns true if mino is at the left edge
def is_leftedge(x, y, mino, r, matrix):
    grid = tetrimino.mino_map[mino - mino_r][r] #grid : 출력할 테트리스

    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            if grid[i][j] != mino_zero: #테트리스 블록에서 해당 행렬위치에 블록 존재하면
                if (x + j - mino_r) < mino_zero:  #맨 왼쪽에 위치함
                    return True
                elif matrix[x + j - mino_r][y + i] != mino_zero:  #그 위치의 왼쪽에 이미 무엇인가 존재함
                    return True

    return False

# Returns true if mino is at the right edge
def is_rightedge(x, y, mino, r, matrix):
    grid = tetrimino.mino_map[mino - mino_r][r] #grid : 출력할 테트리스

    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            if grid[i][j] != mino_zero: #테트리스 블록에서 해당 행렬위치에 블록 존재하면
                if (x + j + mino_r) >= board_x :  #맨 오른쪽에 위치
                    return True
                elif matrix[x + j + mino_r][y + i] != mino_zero:   #그 위치의 오른쪽에 이미 무엇인가 존재함
                    return True

    return False

def is_turnable_r(x, y, mino, r, matrix):
    if r != 3:  #회전모양 총 0, 1, 2, 3번째 총 4가지 있음
        grid = tetrimino.mino_map[mino - mino_x][r + mino_r] #3이 아니면 그 다음 모양
    else:
        grid = tetrimino.mino_map[mino - mino_x][mino_y] #3이면 0번째 모양으로

    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            if grid[i][j] != mino_zero:  #테트리스 블록에서 해당 행렬위치에 블록 존재하면
                if (x + j) < mino_zero or (x + j) >= board_x or (y + i) < mino_zero or (y + i) > board_y :  #테트리스 matrix크기 벗어나면 못돌림
                    return False
                elif matrix[x + j][y + i] != mino_zero:  #해당 자리에 이미 블록이 있으면 못돌림
                    return False
    return True

# Returns true if turning left is possible
def is_turnable_l(x, y, mino, r, matrix):
    if r != mino_zero:  #회전모양 총 0, 1, 2, 3번째 총 4가지 있음
        grid = tetrimino.mino_map[mino - mino_r][r - mino_r]  #0이 아니면 그 다음 모양
    else:
        grid = tetrimino.mino_map[mino - mino_r][mino_3] #0이면 3번째 모양으로

    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            if grid[i][j] != mino_zero:  #테트리스 블록에서 해당 행렬위치에 블록 존재하면
                if (x + j) < mino_zero or (x + j) >= board_x or (y + i) < mino_zero or (y + i) > board_y:  #테트리스 matrix크기 벗어나면 못돌림
                    return False
                elif matrix[x + j][y + i] != mino_zero: #해당 자리에 이미 블록이 있으면 못돌림
                    return False

    return True

# Returns true if new block is drawable
def is_stackable(mino, matrix):
    grid = tetrimino.mino_map[mino - mino_x][mino_zero] #grid : 출력할 테트리스

    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            if grid[i][j] != mino_zero and matrix[mino_3 + j][i] != mino_zero: ###
                return False

    return True




def set_vol(val):
    volume = int(val) / vol_range #set_volume argenment로 넣기 위해서(소수점을 만들어주기 위해서) 100으로 나눠줌
    print(volume)
    ui_variables.click_sound.set_volume(volume)


def set_music_playing(CHANNELS, swidth):
    spf = wave.open('assets/sounds/SFX_BattleMusic.wav', 'rb')
    RATE = spf.getframerate()
    signal = spf.readframes(minus)
    if os.path.isfile('assets/sounds/SFX_BattleMusic_Changed.wav'):
        pygame.mixer.quit()
        os.remove('assets/sounds/SFX_BattleMusic_Changed.wav')
        pygame.mixer.init()
    wf = wave.open('assets/sounds/SFX_BattleMusic_Changed.wav', 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(swidth)
    wf.setframerate(RATE * (level+plus))
    wf.writeframes(signal)
    wf.close()
    pygame.mixer.music.load('assets/sounds/SFX_BattleMusic_Changed.wav')
    pygame.mixer.music.play(minus) #위 노래를 반복재생하기 위해 play(-1)로 설정

set_initial_values():
    global r_n,r_s,rank, main, signin, signup, combo_status, combo_count, score, level, goal, bottom_count, hard_drop, attack_point, dx, dy, rotation, mino, next_mino1, next_mino2, hold, hold_mino, framerate, matrix, blink, start, pause, done, game_over, leader_board, setting, volume_setting, screen_setting, help, gravity_mode, time_attack, time_attack_time, start_ticks, textsize, attack_mode, attack_mode_time, attack_board_y, CHANNELS, swidth, name_location, name, previous_time, current_time, pause_time, lines, leaders, volume, game_status, framerate_blockmove, game_speed, sandbox,sandbox_mode, difficulty, difficulty_mode, shop, challenge, single, game, gold, s_gold, item, item_mino, light_mino, earth_mino, tnt_mino, ch_1, ch_2, ch_3, num_light, num_earthquake, num_tnt


    framerate = 30 # Bigger -> Slower  기본 블록 하강 속도, 2도 할만 함, 0 또는 음수 이상이어야 함
    framerate_blockmove = framerate * 3 # 블록 이동 시 속도
    game_speed = framerate * 20 # 게임 기본 속도
 


    # Initial values
    blink = False
    start = False
    sandbox = False
    sandbox_mode = False
    difficulty = False
    difficulty_mode = False
    shop = False
    challenge = False
    pause = False
    done = False
    game_over = False
    leader_board = False
    setting = False
    volume_setting = False
    screen_setting = False
    single = False
    game = False
    help = False
    gravity_mode = False #이 코드가 없으면 중력모드 게임을 했다가 Restart해서 일반모드로 갈때 중력모드로 게임이 진행됨#
    time_attack = False
    time_attack_time = False
    start_ticks = pygame.time.get_ticks()
    textsize = False
    ch_1 = False
    ch_2 = False
    ch_3 = False
    signin = False
    signup = False
    main = False
    rank = [0,1,2]

    attack_mode = False # 어택모드
    attack_mode_time = False # 어택모드 30초마다 시간 초기화하도록
    attack_board_y = 20  #장애물 블록 밑에서부터 생성하도록 board_y와 똑같이 설정
    

    # 게임 음악 속도 조절 관련 변수
    CHANNELS = 1
    swidth = 2
    

    combo_status = False
    combo_count = 0
    score = 0
    level = 1
    goal = level * 5
    bottom_count = 0
    hard_drop = False
    attack_point = 0

    dx, dy = 3, 0  # Minos location status
    rotation = 0  # Minos rotation status
    mino = randint(1, 7)  # Current mino #테트리스 블록 7가지 중 하나
    next_mino1 = randint(1, 7)  # Next mino1 # 다음 테트리스 블록 7가지 중 하나
    next_mino2 = randint(1, 7)  # Next mino2 # 다음 테트리스 블록 7가지 중 하나
    hold = False  # Hold status
    hold_mino = -1  # Holded mino #현재 hold하는 것 없는 상태

    # 게임 시 생기는 돈
    s_gold = 0

    # 아이템 관련 블럭
    item = True
    light_mino = 10 # 번개 블럭 10
    tnt_mino = 11 # tnt 블럭 11
    item_mino = -2 #아이템을 사용 안한 상태

    name_location = 0
    name = [65, 65, 65]

    previous_time = pygame.time.get_ticks()
    current_time = pygame.time.get_ticks()
    pause_time = pygame.time.get_ticks()

    leaders = ['1st','2nd','3rd']
    r_n = ['n1','n2','n3']
    r_s = ['0','0','0']

    matrix = [[0 for y in range(height + 1)] for x in range(width)]  # Board matrix

    volume = 1.0 # 필요 없는 코드, effect_volume으로 대체 가능
    ui_variables.click_sound.set_volume(volume) # 필요 없는 코드, 전체 코드에서 click_sound를 effect_volume로 설정하는 코드 하나만 있으면 됨
    pygame.mixer.init()
    ui_variables.intro_sound.set_volume(music_volume / 10)
    ui_variables.break_sound.set_volume(effect_volume / 10) # 소리 설정 부분도 set_volume 함수에 넣으면 됨
    ui_variables.intro_sound.play()
    game_status = ''

def set_initial_values2():
    hold = False
    dx, dy = 3, 0
    rotation = 0
    mino = randint(1,7)
    next_mino1=randint(1,7)
    next_mino2=randint(1,7)
    hold_mino = -1
    framerate = 30
    score = 0
    level = 1
    combo_count = 0
    hard_drop = False
    goal = level *5
    bottom_count = 0
    name_location = 0
    name = [65, 65, 65]
    matrix = [[0 for y in range(height + 1)] for x in range(width)]
    ui_variables.click_sound.play()
    


def set_initial_items():
    global num_light, num_earthquake, num_tnt
    num_light = no_item
    num_earthquake = no_item
    num_tnt = no_item

# item 사용 금지
def item_off():
    item = False
    if item == False:
        num_light = no_item
        num_earthquake = no_item
        num_tnt = no_item


set_initial_values()
pygame.time.set_timer(pygame.USEREVENT, 10)

###########################################################
# Loop Start
###########################################################

while not done:

    # Pause screen
    # ui_variables.click_sound.set_volume(volume)

    if volume_setting: #volume board complete
        if start:
            draw_image(screen, gamebackground_image, board_width * 0.5, board_height * 0.5, board_width, board_height) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
            draw_board(next_mino1, next_mino2, hold_mino, score, level, goal)
        else:
            draw_image(screen, background_image, board_width*0.5, board_height*0.5,
            board_width, board_height)
        #draw_image(window, 이미지주소, x좌표, y좌표, 너비, 높이)
        draw_image(screen, board_volume, board_width * 0.5, board_height * 0.4,
                     int(board_width*0.8), int(board_height*0.8))
        draw_image(screen, board_number, board_width * 0.46, board_height * 0.38,
                    int(board_width * 0.0625), int(board_height * 0.1111))
        # music board
        draw_image(screen, board_number, board_width * 0.46, board_height * 0.52,
                    int(board_width * 0.0625), int(board_height * 0.1111))
        # effect board
        allmute_button.draw(screen, (0, 0, 0))
        effect_plus_vector.draw(screen, (0, 0, 0))
        effect_minus_vector.draw(screen, (0, 0, 0))
        music_plus_vector.draw(screen, (0, 0, 0))
        music_minus_vector.draw(screen, (0, 0, 0))
        effect_on_button.draw(screen,(0,0,0))
        music_on_button.draw(screen,(0,0,0))
        back_button.draw(screen, (0, 0, 0))
        allmute_button.draw(screen, (0, 0, 0))

        #render("텍스트이름", 안티에일리어싱 적용, 색깔), 즉 아래의 코드에서 숫자 1=안티에일리어싱 적용에 관한 코드
        music_volume_text = ui_variables.h5.render('Music Volume', 1, ui_variables.grey_1)
        effect_volume_text = ui_variables.h5.render('Effect Volume', 1, ui_variables.grey_1)
        screen.blit(music_volume_text, (board_width * 0.4, board_height * 0.43)) #위치 비율 고정
        screen.blit(effect_volume_text, (board_width * 0.4, board_height * 0.57)) #위치 비율 고정

        music_volume_text = ui_variables.h5.render('Music On/Off', 1, ui_variables.grey_1)
        effect_volume_text = ui_variables.h5.render('Effect On/Off', 1, ui_variables.grey_1)
        screen.blit(music_volume_text, (board_width * 0.57, board_height * 0.43)) #위치 비율 고정
        screen.blit(effect_volume_text, (board_width * 0.57, board_height * 0.57)) #위치 비율 고정

        music_volume_size_text = ui_variables.h4.render(str(music_volume), 1, ui_variables.grey_1)
        effect_volume_size_text = ui_variables.h4.render(str(effect_volume), 1, ui_variables.grey_1)
        screen.blit(music_volume_size_text, (board_width * 0.454, board_height * 0.34)) #위치 비율 고정
        screen.blit(effect_volume_size_text, (board_width * 0.454, board_height * 0.48)) #위치 비율 고정

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                pygame.time.set_timer(pygame.USEREVENT, set_300) #0.3초로 설정

                pygame.display.update()

            elif event.type == pygame.MOUSEMOTION:
                if back_button.isOver_2(pos):
                    back_button.image = button_back_clicked
                else:
                    back_button.image = button_back

                if allmute_button.isOver_2(pos):
                    allmute_button.image = button_allmute_clicked
                else:
                    if (effect_volume == volume_z) and (music_volume ==volume_z):
                        allmute_button.image = button_allmute_on
                    else:
                        allmute_button.image = button_allmute

                if effect_plus_vector.isOver(pos):
                    effect_plus_vector.image = vector_plus_clicked
                else:
                    effect_plus_vector.image = vector_plus

                if effect_minus_vector.isOver(pos):
                    effect_minus_vector.image = vector_minus_clicked
                else:
                    effect_minus_vector.image = vector_minus

                if music_plus_vector.isOver(pos):
                    music_plus_vector.image = vector_plus_clicked
                else:
                    music_plus_vector.image = vector_plus

                if music_minus_vector.isOver(pos):
                    music_minus_vector.image = vector_minus_clicked
                else:
                    music_minus_vector.image = vector_minus

                pygame.display.update()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.isOver_2(pos):
                    ui_variables.click_sound.play()
                    volume_setting = False
                    setting = True
                if music_plus_vector.isOver(pos):
                    ui_variables.click_sound.play()
                    if music_volume >= volume_f: #음량 최대크기
                        music_volume = volume_f
                    else:
                        music_on_button.image = vector_sound_on
                        music_volume += plus
                if music_minus_vector.isOver(pos):
                    ui_variables.click_sound.play()
                    if music_volume <= volume_z: #음량 최소크기
                        music_volume = volume_z
                        music_on_button.image=vector_sound_off
                    else:
                        if music_volume == plus:
                            music_on_button.image=vector_sound_off
                            music_volume -= plus
                        else:
                            music_on_button.image=vector_sound_on
                            music_volume -= plus
                if effect_plus_vector.isOver(pos):
                    ui_variables.click_sound.play()
                    if effect_volume >= volume_f: #음량 최대크기
                        effect_volume = volume_f
                    else:
                        effect_on_button.image=vector_sound_on
                        effect_volume += plus
                if effect_minus_vector.isOver(pos):
                    ui_variables.click_sound.play()
                    if effect_volume <= volume_z: #음량 최소크기
                        effect_volume = volume_z
                        effect_on_button.image=vector_sound_off
                    else:
                        if effect_volume == plus:
                            effect_on_button.image=vector_sound_off
                            effect_volume -= plus
                        else:
                            effect_on_button.image=vector_sound_on
                            effect_volume -= plus
                #음소거 추가#
                if music_on_button.isOver(pos):
                    ui_variables.click_sound.play()
                    if music_volume == volume_z :
                        music_volume = volume_m #중간 음량으로
                        music_on_button.image=vector_sound_on
                    else:
                        music_volume = volume_z
                        music_on_button.image=vector_sound_off
                if effect_on_button.isOver(pos):
                    ui_variables.click_sound.play()
                    if effect_volume == volume_z :
                        effect_volume = volume_m  #중간 음량으로
                        effect_on_button.image=vector_sound_on
                    else:
                        effect_volume = volume_z
                        effect_on_button.image=vector_sound_off
                if allmute_button.isOver_2(pos):
                    ui_variables.click_sound.play()
                    if (effect_volume == volume_z) and (music_volume == volume_z):
                        music_volume = volume_m  #중간 음량으로
                        effect_volume = volume_m  #중간 음량으로
                        allmute_button.image=button_allmute
                    else:
                        music_volume = volume_z #최소 음량으로
                        effect_volume = volume_z #최소 음량으로
                        allmute_button.image=button_allmute_on

                set_volume()
            elif event.type == VIDEORESIZE:
                board_width = event.w
                board_height = event.h
                if board_width < min_width or board_height < min_height: #최소 너비 또는 높이를 설정하려는 경우
                    board_width = min_width
                    board_height = min_height
                if not ((board_rate-0.1) < (board_height/board_width) < (board_rate+0.05)): #높이 또는 너비가 비율의 일정수준 이상을 넘어서게 되면
                    board_width = int(board_height / board_rate) #너비를 적정 비율로 바꿔줌
                    board_height = int(board_width*board_rate) #높이를 적정 비율로 바꿔줌


                block_size = int(board_height * 0.045) #블록 크기비율 고정
                screen = pygame.display.set_mode((board_width, board_height), pygame.RESIZABLE)

                for i in range(len(button_list)):
                        button_list[i].change(board_width, board_height)

    elif screen_setting: # screen board complete 
        if start:
            draw_image(screen, gamebackground_image, board_width * 0.5, board_height * 0.5, board_width, board_height) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
            draw_board(next_mino1, next_mino2, hold_mino, score, level, goal)
        else:
            draw_image(screen, background_image, board_width*0.5, board_height*0.5,
            board_width, board_height)

        draw_image(screen, board_screen, board_width * 0.5, board_height * 0.4,
                     int(board_width*0.8), int(board_height*0.8))

        smallsize_button.draw(screen, (0, 0, 0))
        bigsize_button.draw(screen, (0, 0, 0))
        midiumsize_button.draw(screen, (0, 0, 0))
        back_button.draw(screen, (0, 0, 0))

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                pygame.time.set_timer(pygame.USEREVENT, set_300) #0.3초로 설정
                pygame.display.update()

            elif event.type == pygame.MOUSEMOTION:
                if back_button.isOver_2(pos):
                    back_button.image = button_back_clicked
                else:
                    back_button.image = button_back

                pygame.display.update()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.isOver_2(pos):
                    ui_variables.click_sound.play()
                    screen_setting = False
                    setting = True
                if smallsize_button.isOver_2(pos):
                    ui_variables.click_sound.play()
                    board_width = s_w
                    board_height = s_h
                    block_size = int(board_height * 0.045) #블록 크기 비율 고정
                    screen = pygame.display.set_mode((board_width, board_height), pygame.RESIZABLE)

                    for i in range(len(button_list)):
                        button_list[i].change(board_width, board_height)
                    pygame.display.update()

                if midiumsize_button.isOver_2(pos):
                    ui_variables.click_sound.play()
                    board_width = m_w
                    board_height = m_h
                    block_size = int(board_height * 0.045) #블록 크기 비율 고정
                    screen = pygame.display.set_mode((board_width, board_height), pygame.RESIZABLE)

                    for i in range(len(button_list)):
                        button_list[i].change(board_width, board_height)

                    pygame.display.update()

                if bigsize_button.isOver_2(pos):
                    ui_variables.click_sound.play()
                    board_width = b_w
                    board_height = b_h
                    block_size = int(board_height * 0.045) #블록 크기 비율 고정
                    screen = pygame.display.set_mode((board_width, board_height), pygame.RESIZABLE)

                    for i in range(len(button_list)):
                        button_list[i].change(board_width, board_height)
                    pygame.display.update()
            elif event.type == VIDEORESIZE:
                board_width = event.w
                board_height = event.h
                if board_width < min_width or board_height < min_height: #최소 너비 또는 높이를 설정하려는 경우
                    board_width = min_width
                    board_height = min_height
                if not ((board_rate-0.1) < (board_height/board_width) < (board_rate+0.05)): #높이 또는 너비가 비율의 일정수준 이상을 넘어서게 되면
                    board_width = int(board_height / board_rate) #너비를 적정 비율로 바꿔줌
                    board_height = int(board_width*board_rate) #높이를 적정 비율로 바꿔줌


                block_size = int(board_height * 0.045) #블록 크기비율 고정
                screen = pygame.display.set_mode((board_width, board_height), pygame.RESIZABLE)

                for i in range(len(button_list)):
                        button_list[i].change(board_width, board_height)

    elif setting: # setting board complete
        if start:
            draw_image(screen, gamebackground_image, board_width * 0.5, board_height * 0.5, board_width, board_height) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
            draw_board(next_mino1, next_mino2, hold_mino, score, level, goal)
        else:
            draw_image(screen, background_image, board_width*0.5, board_height*0.5,
            board_width, board_height)

        draw_image(screen, board_setting, board_width * 0.5, board_height * 0.4,
          int(board_width*0.8), int(board_height*0.8)) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)

        screen_vector.draw(screen, (0, 0, 0)) #rgb(0,0,0) = 검정색
        volume_vector.draw(screen, (0, 0, 0))

        back_button.draw(screen, (0, 0, 0))

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                pygame.time.set_timer(pygame.USEREVENT, 300) #0.3초로 설정
                pygame.display.update()

            elif event.type == pygame.MOUSEMOTION:
                if back_button.isOver_2(pos):
                    back_button.image = button_back_clicked
                else:
                    back_button.image = button_back

                if volume_vector.isOver(pos):
                    volume_vector.image = vector_volume_clicked
                else:
                    volume_vector.image = vector_volume

                if screen_vector.isOver(pos):
                    screen_vector.image = vector_screen_clicked
                else:
                    screen_vector.image = vector_screen

                pygame.display.update()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.isOver_2(pos):
                    ui_variables.click_sound.play()
                    setting = False

                if volume_vector.isOver(pos):
                    ui_variables.click_sound.play()
                    setting = False
                    volume_setting = True

                if screen_vector.isOver(pos):
                    ui_variables.click_sound.play()
                    setting = False
                    screen_setting = True


            elif event.type == VIDEORESIZE:
                board_width = event.w
                board_height = event.h
                if board_width < min_width or board_height < min_height: #최소 너비 또는 높이를 설정하려는 경우
                    board_width = min_width
                    board_height = min_height
                if not ((board_rate-0.1) < (board_height/board_width) < (board_rate+0.05)): #높이 또는 너비가 비율의 일정수준 이상을 넘어서게 되면
                    board_width = int(board_height / board_rate) #너비를 적정 비율로 바꿔줌
                    board_height = int(board_width*board_rate) #높이를 적정 비율로 바꿔줌


                block_size = int(board_height * 0.045) #블록 크기 고정
                screen = pygame.display.set_mode((board_width, board_height), pygame.RESIZABLE)

                for i in range(len(button_list)):
                        button_list[i].change(board_width, board_height)

    elif pause: # pause board in game little complete
        pygame.mixer.music.pause()

        draw_image(screen, gamebackground_image, board_width * 0.5, board_height * 0.5, board_width, board_height) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
        draw_board(next_mino1, next_mino2, hold_mino, score, level, goal)
        
        draw_image(screen, board_pause, board_width * 0.5, board_height * 0.5, int(board_height * 0.7428), board_height) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
        resume_button.draw(screen, (0, 0, 0)) #rgb(0,0,0) = 검정색
        restart_button.draw(screen, (0, 0, 0))
        setting_button.draw(screen, (0, 0, 0))
        quit_game_button.draw(screen, (0, 0, 0))

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                pygame.time.set_timer(pygame.USEREVENT, 300) #0.3초
                pygame.display.update()
            elif event.type == KEYDOWN:
                erase_mino(dx, dy, mino, rotation, matrix)
                if event.key == K_ESCAPE:
                    pause = False
                    ui_variables.click_sound.play()
                    pygame.mixer.music.unpause()
                    pygame.time.set_timer(pygame.USEREVENT, 1) #0.001초

            elif event.type == pygame.MOUSEMOTION:
                if resume_button.isOver(pos):
                    resume_button.image = button_resume_clicked
                else:
                    resume_button.image = button_resume

                if restart_button.isOver(pos):
                    restart_button.image = button_restart_clicked
                else:
                    restart_button.image = button_restart

                if setting_button.isOver(pos):
                    setting_button.image = button_setting_clicked
                else:
                    setting_button.image = button_setting_clicked
                if quit_game_button.isOver(pos):
                    quit_game_button.image = button_quit_clicked
                else:
                    quit_game_button.image = button_quit
                pygame.display.update()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if quit_game_button.isOver_2(pos):
                    ui_variables.click_sound.play()
                    pause = False
                    start = False
                if setting_button.isOver_2(pos):
                    ui_variables.click_sound.play()
                    setting = True
                if restart_button.isOver_2(pos):
                    if game_status == 'single':
                        start = True
                        pygame.mixer.music.play(minus) #play(-1) = 노래 반복재생
                    if game_status == 'time_attack':
                        time_attack = True
                        pygame.mixer.music.play(minus)
                    if game_status == 'easy':
                        attack_mode = True
                        gravity_mode = False
                        pygame.mixer.music.play(minus)
                    if game_status == 'normal':
                        attack_mode = False
                        gravity_mode = True
                        pygame.mixer.music.play(minus)
                    if game_status == 'hard':
                        attack_mode = True
                        gravity_mode = True
                        pygame.mixer.music.play(minus)


                    set_initial_values2()
                    pause = False

                if resume_button.isOver(pos):
                    pygame.mixer.music.unpause()
                    pause = False
                    ui_variables.click_sound.play()
                    pygame.time.set_timer(pygame.USEREVENT, set_1) #0.001초

            elif event.type == VIDEORESIZE:
                board_width = event.w
                board_height = event.h
                if board_width < min_width or board_height < min_height: #최소 너비 또는 높이를 설정하려는 경우
                    board_width = min_width
                    board_height = min_height
                if not ((board_rate-0.1) < (board_height/board_width) < (board_rate+0.05)): #높이 또는 너비가 비율의 일정수준 이상을 넘어서게 되면
                    board_width = int(board_height / board_rate) #너비를 적정 비율로 바꿔줌
                    board_height = int(board_width*board_rate) #높이를 적정 비율로 바꿔줌


                block_size = int(board_height * 0.045)
                screen = pygame.display.set_mode((board_width, board_height), pygame.RESIZABLE)

                for i in range(len(button_list)):
                        button_list[i].change(board_width, board_height)

    elif help: # help board complete
        draw_image(screen, background_image, board_width * 0.5, board_height * 0.5,
        board_width, board_height) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)

        draw_image(screen, board_help, board_width * 0.5, board_height * 0.4, 
        int(board_width * 0.8), int(board_height * 0.8)) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)

        back_button.draw(screen, (0, 0, 0))

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                pygame.time.set_timer(pygame.USEREVENT, set_300) #0.3초
                pygame.display.update()

            elif event.type == pygame.MOUSEMOTION:
                if back_button.isOver_2(pos):
                    back_button.image = button_back_clicked
                else:
                    back_button.image = button_back
                pygame.display.update()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.isOver_2(pos):
                    ui_variables.click_sound.play()
                    help = False

            elif event.type == VIDEORESIZE:
                board_width = event.w
                board_height = event.h
                if board_width < min_width or board_height < min_height: #최소 너비 또는 높이를 설정하려는 경우
                    board_width = min_width
                    board_height = min_height
                if not ((board_rate-0.1) < (board_height/board_width) < (board_rate+0.05)): #높이 또는 너비가 비율의 일정수준 이상을 넘어서게 되면
                    board_width = int(board_height / board_rate) #너비를 적정 비율로 바꿔줌
                    board_height = int(board_width*board_rate) #높이를 적정 비율로 바꿔줌


                block_size = int(board_height * 0.045) #board 세로길이에 원하는 비율을 곱해줌
                screen = pygame.display.set_mode((board_width, board_height), pygame.RESIZABLE)

                for i in range(len(button_list)):
                        button_list[i].change(board_width, board_height)

    elif game: # start board complete
        draw_image(screen, background_image, board_width * 0.5, board_height * 0.5, board_width, board_height) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
        draw_image(screen, board_start, board_width * 0.5, board_height * 0.4,  int(board_width*0.8), int(board_height*0.8)) 
        single_button.draw(screen, (0, 0, 0))
        timeattack_button.draw(screen, (0, 0, 0))
        sandbox_button.draw(screen, (0, 0, 0))
        difficulty_button.draw(screen, (0, 0, 0))
        back_button.draw(screen, (0, 0, 0))


        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == QUIT:
                done = True
            
            elif event.type == USEREVENT:
                pygame.time.set_timer(pygame.USEREVENT, set_300) #0.3초로 설정
                pygame.display.update()

            elif event.type == pygame.MOUSEMOTION:
                if back_button.isOver_2(pos):
                    back_button.image = button_back_clicked
                else:
                    back_button.image = button_back

                if single_button.isOver_2(pos):
                    single_button.image = button_single_clicked
                else:
                    single_button.image = button_single

                if timeattack_button.isOver_2(pos):
                    timeattack_button.image = button_timeattack_clicked
                else:
                    timeattack_button.image = button_timeattack

                if sandbox_button.isOver_2(pos):
                    sandbox_button.image = button_sandbox_clicked
                else:
                    sandbox_button.image = button_sandbox

                if difficulty_button.isOver_2(pos):
                    difficulty_button.image = button_difficulty_clicked
                else:
                    difficulty_button.image = button_difficulty

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.isOver_2(pos):
                    ui_variables.click_sound.play()
                    game = False
                if single_button.isOver_2(pos):
                    ui_variables.click_sound.play()
                    item_off()
                    game = False
                    single = True
                    start = True
                    previous_time = pygame.time.get_ticks()
                    initalize = True
                    game_status == 'single'
                    set_music_playing(CHANNELS, swidth)
                    ui_variables.intro_sound.stop()
                if timeattack_button.isOver_2(pos):
                    ui_variables.click_sound.play()
                    item_off()
                    time_attack = True
                    game = False
                    start = True
                    previous_time = pygame.time.get_ticks()
                    initalize = True
                    game_status == 'time_attack'
                    set_music_playing(CHANNELS, swidth)
                    ui_variables.intro_sound.stop()
                if difficulty_button.isOver_2(pos):
                    ui_variables.click_sound.play()
                    game = False
                    difficulty = True
                if sandbox_button.isOver_2(pos):
                    item_off()
                    ui_variables.click_sound.play()
                    game = False
                    sandbox = True
 

                pygame.display.update()
            elif event.type == VIDEORESIZE:
                board_width = event.w
                board_height = event.h
                if board_width < min_width or board_height < min_height: #최소 너비 또는 높이를 설정하려는 경우
                    board_width = min_width
                    board_height = min_height
                if not ((board_rate-0.1) < (board_height/board_width) < (board_rate+0.05)): #높이 또는 너비가 비율의 일정수준 이상을 넘어서게 되면
                    board_width = int(board_height / board_rate) #너비를 적정 비율로 바꿔줌
                    board_height = int(board_width*board_rate) #높이를 적정 비율로 바꿔줌


                block_size = int(board_height * 0.045) #블록 크기비율 고정
                screen = pygame.display.set_mode((board_width, board_height), pygame.RESIZABLE)

                for i in range(len(button_list)):
                        button_list[i].change(board_width, board_height)

        # Game screen
    
    elif sandbox: # sandbox board little complete
        draw_image(screen, background_image, board_width * 0.5, board_height * 0.5,
        board_width, board_height) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
        draw_image(screen, board_sandbox, board_width * 0.5, board_height * 0.4,
             int(board_width*0.8), int(board_height*0.8)) 
        attack_button.draw(screen, (0, 0, 0))
        gravity_button.draw(screen, (0, 0, 0))
        back_right_button.draw(screen, (0, 0, 0))
        start_left_button.draw(screen, (0, 0, 0))
        draw_image(screen, icon_level, board_width * 0.6, board_height * 0.43,
        int(board_width*0.16), int(board_height*0.084))
        draw_image(screen, board_number, board_width * 0.7875, board_height * 0.43,
        int(board_width*0.0625), int(board_height*0.1111))
        level_minus_vector.draw(screen,(0,0,0))
        level_plus_vector.draw(screen,(0,0,0))
        level_size_text = ui_variables.h4.render(str(level),1,ui_variables.grey_1)
        screen.blit(level_size_text, (board_width * 0.78, board_height * 0.4))


        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == QUIT:
                done = True
            
            elif event.type == USEREVENT:
                pygame.time.set_timer(pygame.USEREVENT, set_300) #0.3초로 설정
                pygame.display.update()

            elif event.type == pygame.MOUSEMOTION:
                if back_right_button.isOver_2(pos):
                    back_right_button.image = button_back_clicked
                else:
                    back_right_button.image = button_back 

                if start_left_button.isOver_2(pos):
                    start_left_button.image = button_start_clicked
                else:
                    start_left_button.image = button_start

                if attack_button.isOver_2(pos):
                    attack_button.image = button_attack_clicked
                else:
                    if attack_mode:
                        attack_button.image = button_attack_on
                    else:
                        attack_button.image = button_attack

                if gravity_button.isOver_2(pos):
                    gravity_button.image = button_gravity_clicked
                else:
                    if gravity_mode:
                        gravity_button.image = button_gravity_on
                    else:
                        gravity_button.image = button_gravity

                if level_minus_vector.isOver(pos):
                    level_minus_vector.image = vector_minus_clicked
                else:
                    level_minus_vector.image = vector_minus

                if level_plus_vector.isOver(pos):
                    level_plus_vector.image = vector_plus_clicked
                else:
                    level_plus_vector.image = vector_plus

                pygame.display.update()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_right_button.isOver_2(pos):
                    ui_variables.click_sound.play()
                    sandbox = False
                    game = True
                                
                if start_left_button.isOver_2(pos):
                    ui_variables.click_sound.play()
                    game = False
                    sandbox = False
                    sandbox_mode = True
                    start = True
                    previous_time = pygame.time.get_ticks()
                    initalize = True
                    set_music_playing(CHANNELS, swidth)
                    ui_variables.intro_sound.stop()

                if attack_button.isOver_2(pos):
                    if attack_mode:
                        ui_variables.click_sound.play()
                        attack_mode = False
                        attack_button.image = button_attack
                    else:
                        ui_variables.click_sound.play()
                        attack_mode = True
                        attack_button.image = button_attack_on
                                    
                if gravity_button.isOver_2(pos):
                    if gravity_mode:
                        ui_variables.click_sound.play()
                        gravity_mode = False
                        gravity_button.image = button_gravity
                    else :
                        ui_variables.click_sound.play()
                        gravity_mode = True
                        gravity_button.image = button_gravity_on
                                  
                if level_minus_vector.isOver(pos):
                    ui_variables.click_sound.play()
                    if level >level_1:
                        level -= level_1
                        goal -= level * 5
                        game_speed = int(game_speed + speed_change)
                        pygame.time.set_timer(pygame.USEREVENT, game_speed)
                        #Change_RATE += 1
                        

                if level_plus_vector.isOver(pos):
                    ui_variables.click_sound.play()
                    if level < level_15:
                        level += level_1
                        goal += level * level_5
                        game_speed = int(game_speed - speed_change)
                        pygame.time.set_timer(pygame.USEREVENT, game_speed)
                        
                        #Change_RATE -= 1
            elif event.type == VIDEORESIZE:
                board_width = event.w
                board_height = event.h
                if board_width < min_width or board_height < min_height: #최소 너비 또는 높이를 설정하려는 경우
                    board_width = min_width
                    board_height = min_height
                if not ((board_rate-0.1) < (board_height/board_width) < (board_rate+0.05)): #높이 또는 너비가 비율의 일정수준 이상을 넘어서게 되면
                    board_width = int(board_height / board_rate) #너비를 적정 비율로 바꿔줌
                    board_height = int(board_width*board_rate) #높이를 적정 비율로 바꿔줌


                block_size = int(board_height * 0.045) #블록 크기비율 고정
                screen = pygame.display.set_mode((board_width, board_height), pygame.RESIZABLE)

                for i in range(len(button_list)):
                        button_list[i].change(board_width, board_height)
                        
    elif difficulty: # diff board little complete
        draw_image(screen, board_difficulty, board_width * 0.5, board_height * 0.4,
         int(board_width * 0.8), int(board_height * 0.8))
        back_button.draw(screen, (0, 0, 0))
        easy_button.draw(screen, (0, 0, 0))
        normal_button.draw(screen, (0, 0, 0))
        hard_button.draw(screen, (0,0,0))


        for event in pygame.event.get():
            pos=pygame.mouse.get_pos()

            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                pygame.time.set_timer(pygame.USEREVENT, set_300)
                pygame.display.update()

            elif event.type == pygame.MOUSEMOTION:
                if back_button.isOver_2(pos):
                    back_button.image = button_back_clicked
                else:
                    back_button.image = button_back

                if easy_button.isOver_2(pos):
                    easy_button.image = button_easy_clicked
                else:
                    easy_button.image = button_easy

                if normal_button.isOver_2(pos):
                    normal_button.image = button_normal_clicked
                else:
                    normal_button.image = button_normal

                if hard_button.isOver_2(pos):
                    hard_button.image = button_hard_clicked
                else:
                    hard_button.image = button_hard

            elif event.type == pygame.MOUSEBUTTONDOWN:

                if back_button.isOver_2(pos):
                    ui_variables.click_sound.play()
                    difficulty = False
                    game = True

                if easy_button.isOver_2(pos):
                    # 도전과제 3 도전시
                    if ch_3 :
                        item_off()
                    ui_variables.click_sound.play()
                    difficulty = False
                    difficulty_mode = True
                    attack_mode = True
                    start = True
                    previous_time = pygame.time.get_ticks()
                    initalize = True
                    game_status == 'easy'
                    set_music_playing(CHANNELS, swidth)

                if normal_button.isOver_2(pos):
                    # 도전과제 3 도전시
                    if ch_3 :
                        item_off()
                    ui_variables.click_sound.play()
                    difficulty = False
                    difficulty_mode = True
                    gravity_mode = True
                    start = True
                    previous_time = pygame.time.get_ticks()
                    initalize = True
                    game_status == 'normal'
                    set_music_playing(CHANNELS, swidth)

                if hard_button.isOver_2(pos):
                    # 도전과제 3 도전시
                    if ch_3 :
                        item_off()
                    ui_variables.click_sound.play()
                    difficulty = False
                    difficulty_mode = True
                    gravity_mode = True
                    attack_mode = True
                    start = True
                    previous_time = pygame.time.get_ticks()
                    initalize = True
                    game_status == 'hard'
                    set_music_playing(CHANNELS, swidth)
            elif event.type == VIDEORESIZE:
                board_width = event.w
                board_height = event.h
                if board_width < min_width or board_height < min_height: #최소 너비 또는 높이를 설정하려는 경우
                    board_width = min_width
                    board_height = min_height
                if not ((board_rate-0.1) < (board_height/board_width) < (board_rate+0.05)): #높이 또는 너비가 비율의 일정수준 이상을 넘어서게 되면
                    board_width = int(board_height / board_rate) #너비를 적정 비율로 바꿔줌
                    board_height = int(board_width*board_rate) #높이를 적정 비율로 바꿔줌


                block_size = int(board_height * 0.045) #블록 크기비율 고정
                screen = pygame.display.set_mode((board_width, board_height), pygame.RESIZABLE)

                for i in range(len(button_list)):
                        button_list[i].change(board_width, board_height)
                                   
    elif leader_board: # complete        

        draw_image(screen, background_image, board_width*0.5, board_height*0.5,
        board_width, board_height)
        draw_image(screen, board_leader, board_width * 0.5, board_height * 0.4,
            int(board_width * 0.8),int(board_height*0.8))

        back_button.draw(screen, (0, 0, 0))
        rank_single.draw(screen,(0,0,0))
        rank_easy.draw(screen,(0,0,0))
        rank_normal.draw(screen,(0,0,0))
        rank_hard.draw(screen,(0,0,0))
        rank_ta.draw(screen,(0,0,0))
        cb = ui_variables.h1_b.render("Click any button",1,ui_variables.skyblue)
        l1 = ui_variables.h1_b.render(leaders[0]+" "+r_n[0]+" "+r_s[0],1,ui_variables.skyblue)
        l2 = ui_variables.h1_b.render(leaders[1]+" "+r_n[1]+" "+r_s[1],1,ui_variables.skyblue)
        l3 = ui_variables.h1_b.render(leaders[2]+" "+r_n[2]+" "+r_s[2],1,ui_variables.skyblue)
        no = ui_variables.h1_b.render("No rank",1,ui_variables.skyblue)
        if game_status == "":
            screen.blit(cb, (int(board_width*0.35),int(board_height*0.45)))
        else:
            screen.blit(l1, (int(board_width*0.4),int(board_height*(0.35))))
            screen.blit(l2, (int(board_width*0.4),int(board_height*(0.45))))
            screen.blit(l3, (int(board_width*0.4),int(board_height*(0.55))))
            

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                pygame.time.set_timer(pygame.USEREVENT, set_300) #0.3초
                pygame.display.update()
            elif event.type == KEYDOWN:
                erase_mino(dx, dy, mino, rotation, matrix)
                if event.key == K_ESCAPE:
                    pause = False
                    ui_variables.click_sound.play()
                    pygame.time.set_timer(pygame.USEREVENT, set_1) #0.001초

            elif event.type == pygame.MOUSEMOTION:
                if back_button.isOver_2(pos):
                    back_button.image = button_back_clicked
                else:
                    back_button.image = button_back
                if rank_single.isOver_2(pos):
                    rank_single.image = button_single_clicked
                else:
                    rank_single.image = button_single
                if rank_easy.isOver_2(pos):
                    rank_easy.image = button_easy_clicked
                else:
                    rank_easy.image = button_easy
                if rank_normal.isOver_2(pos):
                    rank_normal.image = button_normal_clicked
                else:
                    rank_normal.image = button_normal
                if rank_hard.isOver_2(pos):
                    rank_hard.image = button_hard_clicked
                else:
                    rank_hard.image = button_hard
                if rank_ta.isOver_2(pos):
                    rank_ta.image = button_timeattack_clicked
                else:
                    rank_ta.image = button_timeattack
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.isOver_2(pos):
                    ui_variables.click_sound.play()
                    game_status = ''
                    leader_board = False
                if rank_single.isOver_2(pos):
                    ui_variables.click_sound.play()
                    game_status = 'single'
                    single_data = load_rank_data(game_status)
                    if len(single_data)>len(rank):
                        for i in rank:
                            r_n[i] = str(list(single_data)[i]["user_id"])
                            r_s[i] = str(list(single_data)[i]["score"])
                    elif len(single_data) == 0:
                        screen.blit(no, (int(board_width*0.4),int(board_height*0.45)))
                    else:
                        for i in range(len(single_data)):
                            r_n[i] = str(list(single_data)[i]["user_id"])
                            r_s[i] = str(list(single_data)[i]["score"])
                if rank_easy.isOver_2(pos):
                    ui_variables.click_sound.play()
                    game_status = 'easy'
                    easy_data = load_rank_data(game_status)
                    if len(easy_data)>len(rank):
                        for i in rank:
                            r_n[i] = str(list(easy_data)[i]["user_id"])
                            r_s[i] = str(list(easy_data)[i]["easy_mode_score"])
                    elif len(easy_data) == 0:
                        screen.blit(no, (int(board_width*0.4),int(board_height*0.45)))
                    else:
                        for i in range(len(easy_data)):
                            r_n[i] = str(list(easy_data)[i]["user_id"])
                            r_s[i] = str(list(easy_data)[i]["easy_mode_score"])
                if rank_normal.isOver_2(pos):
                    ui_variables.click_sound.play()
                    game_status = 'normal'
                    normal_data = load_rank_data(game_status)
                    if len(normal_data)>len(rank):
                        for i in rank:
                            r_n[i] = str(list(normal_data)[i]["user_id"])
                            r_s[i] = str(list(normal_data)[i]["normal_mode_score"])
                    elif len(normal_data) == 0:
                        screen.blit(no, (int(board_width*0.4),int(board_height*0.45)))
                    else:
                        for i in range(len(normal_data)):
                            r_n[i] = str(list(normal_data)[i]["user_id"])
                            r_s[i] = str(list(normal_data)[i]["normal_mode_score"])
                if rank_hard.isOver_2(pos):
                    ui_variables.click_sound.play()
                    game_status = 'hard'
                    hard_data = load_rank_data(game_status)
                    if len(hard_data)>len(rank):
                        for i in rank:
                            r_n[i] = str(list(hard_data)[i]["user_id"])
                            r_s[i] = str(list(hard_data)[i]["hard_mode_score"])
                    elif len(hard_data) == 0:
                        screen.blit(no, (int(board_width*0.4),int(board_height*0.45)))
                    else:
                        for i in range(len(hard_data)):
                            r_n[i] = str(list(hard_data)[i]["user_id"])
                            r_s[i] = str(list(hard_data)[i]["hard_mode_score"])
                if rank_ta.isOver_2(pos):
                    ui_variables.click_sound.play()
                    game_status = 'time_attack'
                    ta_data = load_rank_data(game_status)
                    if len(ta_data)>len(rank):
                        for i in rank:
                            r_n[i] = str(list(ta_data)[i]["user_id"])
                            r_s[i] = str(list(ta_data)[i]["timeattack_score"])
                    elif len(ta_data) == 0:
                        screen.blit(no, (int(board_width*0.4),int(board_height*0.45)))
                    else:
                        for i in range(len(ta_data)):
                            r_n[i] = str(list(ta_data)[i]["user_id"])
                            r_s[i] = str(list(ta_data)[i]["timeattack_score"])
                    

            elif event.type == VIDEORESIZE:
                board_width = event.w
                board_height = event.h
                if board_width < min_width or board_height < min_height: #최소 너비 또는 높이를 설정하려는 경우
                    board_width = min_width
                    board_height = min_height
                if not ((board_rate-0.1) < (board_height/board_width) < (board_rate+0.05)): #높이 또는 너비가 비율의 일정수준 이상을 넘어서게 되면
                    board_width = int(board_height / board_rate) #너비를 적정 비율로 바꿔줌
                    board_height = int(board_width*board_rate) #높이를 적정 비율로 바꿔줌


                block_size = int(board_height * 0.045)
                screen = pygame.display.set_mode((board_width, board_height), pygame.RESIZABLE)

                for i in range(len(button_list)):
                        button_list[i].change(board_width, board_height)

    elif shop: # shop little complete
        draw_image(screen, background_image, board_width * 0.5, board_height * 0.5, board_width, board_height)
        draw_image(screen, board_shop, board_width * 0.5, board_height * 0.4, int(board_width * 0.8), int(board_height * 0.8))

        back_button.draw(screen, (0, 0, 0))
        light_buy_button.draw(screen, (0, 0, 0))
        tnt_buy_button.draw(screen, (0, 0, 0))
        earth_buy_button.draw(screen, (0, 0, 0))

        draw_image(screen, item_tnt, board_width*0.28, board_height*0.3, int(board_width*0.08),int(board_height*0.1422))
        draw_image(screen, item_light, board_width*0.28, board_height*0.45, int(board_width*0.08),int(board_height*0.1422))
        draw_image(screen, item_earth, board_width*0.28, board_height*0.6, int(board_width*0.08),int(board_height*0.1422))
        draw_image(screen, item_gold, board_width*0.735, board_height*0.15, int(board_width*0.025),int(board_height*0.0444))
        draw_image(screen, item_tnt_info, board_width*0.5, board_height*0.3, int(board_width*0.315),int(board_height*0.1267))
        draw_image(screen, item_light_info, board_width*0.5, board_height*0.45, int(board_width*0.315),int(board_height*0.1267))
        draw_image(screen, item_earth_info, board_width*0.5, board_height*0.6, int(board_width*0.315),int(board_height*0.1267))
        text_gold = ui_variables.h2.render(str(gold), 1, ui_variables.real_white)
        screen.blit(text_gold, (int(board_width*0.770), int(board_height * 0.1)))

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                pygame.time.set_timer(pygame.USEREVENT, set_300)
                pygame.display.update()

            elif event.type == pygame.MOUSEMOTION:
                if back_button.isOver_2(pos):
                    back_button.image=button_back_clicked
                else:
                    back_button.image=button_back

                if light_buy_button.isOver_2(pos):
                    light_buy_button.image=button_buy_clicked
                else:
                    light_buy_button.image=button_buy

                if tnt_buy_button.isOver_2(pos):
                    tnt_buy_button.image=button_buy_clicked
                else:
                    tnt_buy_button.image=button_buy

                if earth_buy_button.isOver_2(pos):
                    earth_buy_button.image=button_buy_clicked
                else:
                    earth_buy_button.image=button_buy

                pygame.display.update()



            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.isOver_2(pos):
                    ui_variables.click_sound.play()
                    shop = False

                if light_buy_button.isOver_2(pos):
                    ui_variables.click_sound.play()
                    if gold > gold_0 :
                        gold -= gold_100
                        num_light += item_r
                        update_light_data(num_light,user_id)
                        update_gold_data(gold,user_id)

                if tnt_buy_button.isOver_2(pos):
                    ui_variables.click_sound.play()
                    if gold > gold_100 :
                        gold -= gold_200
                        num_tnt += item_r
                        update_tnt_data(num_tnt,user_id)
                        update_gold_data(gold,user_id)

                if earth_buy_button.isOver_2(pos):
                    ui_variables.click_sound.play()
                    if gold > gold_0 :
                        gold -= gold_100
                        num_tnt += item_r
                        update_earthquake_data(num_earthquake,user_id)
                        update_gold_data(gold,user_id)

            elif event.type == VIDEORESIZE:
                board_width = event.w
                board_height = event.h
                if board_width < min_width or board_height < min_height: #최소 너비 또는 높이를 설정하려는 경우
                    board_width = min_width
                    board_height = min_height
                if not ((board_rate-0.1) < (board_height/board_width) < (board_rate+0.05)): #높이 또는 너비가 비율의 일정수준 이상을 넘어서게 되면
                    board_width = int(board_height / board_rate) #너비를 적정 비율로 바꿔줌
                    board_height = int(board_width*board_rate) #높이를 적정 비율로 바꿔줌


                block_size = int(board_height * 0.045) #블록 크기비율 고정
                screen = pygame.display.set_mode((board_width, board_height), pygame.RESIZABLE)

                for i in range(len(button_list)):
                        button_list[i].change(board_width, board_height)

    elif challenge: # challenge little complete
        draw_image(screen, background_image, board_width * 0.5, board_height * 0.5, board_width, board_height) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
        draw_image(screen, board_challenge, board_width * 0.5, board_height * 0.4, int(board_width * 0.8), int(board_height * 0.8)) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)

        draw_image(screen, challenge_info1, board_width*0.4, board_height*0.28, int(board_width *45/80), int(board_height * 75/450))
        draw_image(screen, challenge_info2, board_width*0.4, board_height*0.44, int(board_width * 45/80), int(board_height * 75/450))
        draw_image(screen, challenge_info3, board_width*0.4, board_height*0.6, int(board_width * 45/80), int(board_height * 75/450))

        back_button.draw(screen,(0, 0, 0))
        off1_button.draw(screen,(0,0,0))
        off2_button.draw(screen,(0,0,0))
        off3_button.draw(screen,(0,0,0))

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                pygame.time.set_timer(pygame.USEREVENT, set_300)
                pygame.display.update()

            elif event.type == pygame.MOUSEMOTION:
                if back_button.isOver_2(pos):
                    back_button.image = button_back_clicked
                else:
                    back_button.image = button_back
                if off1_button.isOver_2(pos):
                    if ch_1:
                       off1_button.image = on_clicked
                    else:
                       off1_button.image = off_clicked

                else:
                    if ch_1:
                        off1_button.image = on
                    else:
                        off1_button.image = off


                if off2_button.isOver_2(pos):
                    if ch_2:
                       off2_button.image = on_clicked
                    else:
                       off2_button.image = off_clicked

                else:
                     if ch_2:
                       off2_button.image = on
                     else:
                       off2_button.image = off


                if off3_button.isOver_2(pos):
                    if ch_3:
                       off3_button.image = on_clicked
                    else:
                       off3_button.image = off_clicked

                else:
                     if ch_3:
                       off3_button.image = on
                     else:
                       off3_button.image = off
               

            elif event.type == pygame.MOUSEBUTTONDOWN:

                if back_button.isOver_2(pos):
                    ui_variables.click_sound.play()
                    challenge = False

                if off1_button.isOver_2(pos):
                    ui_variables.click_sound.play()
                    if ch_1 == False :
                        ch_1 = True
                        if gold > gold_100 :
                            gold -= gold_200
                            update_gold_data(gold,user_id)
                    else :
                        ch_1 = False 
                        gold += gold_200
                        update_gold_data(gold,user_id)

                if off2_button.isOver_2(pos):
                    ui_variables.click_sound.play()
                    if ch_2 == False :
                        ch_2 = True
                        if gold > gold_100 :
                            gold -= gold_200
                            update_gold_data(gold,user_id)
                    else :
                        ch_2 = False
                        gold += gold_200
                        update_gold_data(gold,user_id)

                if off3_button.isOver_2(pos):
                    ui_variables.click_sound.play()
                    if ch_3 == False :
                        ch_3 = True
                        if gold > gold_100 :
                            gold -= gold_200
                            update_gold_data(gold,user_id)
                    else :
                        ch_3 = False
                        gold += gold_200
                        update_gold_data(gold,user_id)

            elif event.type == VIDEORESIZE:
                board_width = event.w
                board_height = event.h
                if board_width < min_width or board_height < min_height: #최소 너비 또는 높이를 설정하려는 경우
                    board_width = min_width
                    board_height = min_height
                if not ((board_rate-0.1) < (board_height/board_width) < (board_rate+0.05)): #높이 또는 너비가 비율의 일정수준 이상을 넘어서게 되면
                    board_width = int(board_height / board_rate) #너비를 적정 비율로 바꿔줌
                    board_height = int(board_width*board_rate) #높이를 적정 비율로 바꿔줌


                block_size = int(board_height * 0.045) #블록 크기비율 고정
                screen = pygame.display.set_mode((board_width, board_height), pygame.RESIZABLE)

                for i in range(len(button_list)):
                        button_list[i].change(board_width, board_height)

    elif start:
        if sandbox_mode:
            level_plus_button.draw(screen, (0, 0, 0))
            level_minus_button.draw(screen, (0,0, 0))
        
        if time_attack:
            if time_attack_time == False:
                start_ticks = pygame.time.get_ticks() # 현재시간을 타임어택모드 진입했을 때 시간으로 설정
                time_attack_time = True
            elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000 # 경과 시간 계산

        if attack_mode:
            if attack_mode_time == False:
                current_attack_ticks = pygame.time.get_ticks() # 현재시간을 어택모드 진입했을 때 시간으로 설정
                attack_mode_time = True
            elapsed_attack_time = (pygame.time.get_ticks() - current_attack_ticks) / set_1000 # 경과 시간 계산

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == QUIT:
                done = True

            elif event.type == USEREVENT:
                # Set speed
                if not game_over:
                    keys_pressed = pygame.key.get_pressed()
                    if keys_pressed[K_DOWN]:
                        pygame.time.set_timer(pygame.USEREVENT, framerate) #프레임 시간만큼 빠르게 소프트드롭
                    else:
                        pygame.time.set_timer(pygame.USEREVENT, game_speed)

                # Draw a mino
                draw_mino(dx, dy, mino, rotation, matrix)
                screen.fill(ui_variables.real_white)
                draw_image(screen, gamebackground_image , board_width * 0.5, board_height * 0.5, board_width, board_height) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
                draw_board(next_mino1, next_mino2, hold_mino, score, level, goal)
                pygame.display.update()

                current_time = pygame.time.get_ticks()
                # Erase a mino
                if not game_over:
                    erase_mino(dx, dy, mino, rotation, matrix)

                # Move mino down
                if not is_bottom(dx, dy, mino, rotation, matrix):
                    dy += 1

                # Create new mino: 중력 모드
                elif gravity_mode:
                    if hard_drop or bottom_count == bc:
                        if gravity(dx, dy, mino, rotation, matrix):
                            erase_mino(dx, dy, mino, rotation, matrix)
                        hard_drop = False
                        bottom_count = mino_zero
                        score += score_r * level
                        screen.fill(ui_variables.real_white)
                        draw_image(screen, gamebackground_image , board_width * 0.5, board_height * 0.5, board_width, board_height) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
                        draw_board(next_mino1, next_mino2, hold_mino, score, level, goal)
                        pygame.display.update()
                        if is_stackable(next_mino1, matrix):
                            mino = next_mino1
                            next_mino1 = next_mino2
                            next_mino2 = randint(1, 7)
                            dx, dy = 3, 0
                            rotation = 0
                            hold = False
                        else:
                            ui_variables.GameOver_sound.play()
                            start = False
                            game_status = 'normal'
                            game_over = True
                            gravity_mode = False
                            pygame.time.set_timer(pygame.USEREVENT, set_1) #0.001초
                    else:
                        bottom_count += plus

                # Create new mino: 일반 모드
                else:
                    if hard_drop or bottom_count == bc:
                        hard_drop = False
                        bottom_count = mino_zero
                        score += score_r * level
                        draw_mino(dx, dy, mino, rotation, matrix)
                        screen.fill(ui_variables.real_white)
                        draw_image(screen, gamebackground_image , board_width * 0.5, board_height * 0.5, board_width, board_height) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
                        draw_board(next_mino1, next_mino2, hold_mino, score, level, goal)
                        pygame.display.update()
                        if is_stackable(next_mino1, matrix):
                            mino = next_mino1
                            next_mino1 = next_mino2
                            next_mino2 = randint(1, 7)
                            dx, dy = 3, 0
                            rotation = 0
                            hold = False
                        else:
                            ui_variables.GameOver_sound.play()
                            start = False
                            game_status = 'single'
                            game_over = True
                            pygame.time.set_timer(pygame.USEREVENT, 1) #0.001초
                    else:
                        bottom_count += plus

                # Erase line
                erase_count = mino_zero
                rainbow_count = mino_zero
                matrix_contents = []
                combo_value = zero

                for j in range(board_y+one):
                    is_full = True
                    for i in range(board_x):
                        if matrix[i][j] == mino_zero or matrix[i][j] == f_mino : #빈 공간이거나, 장애물블록
                            is_full = False
                    if is_full: # 한 줄 꽉 찼을 때
                        erase_count += one
                        k = j
                        combo_value += one
                        combo_status = True
                        combo_count += one 
                        total_time += five # 콤보 시 시간 5초 연장

                        #rainbow보너스 점수
                        rainbow = [1,2,3,4,5,6,7] #각 mino에 해당하는 숫자
                        for i in range(board_x):
                            matrix_contents.append(matrix[i][j]) #현재 클리어된 줄에 있는 mino 종류들 저장
                        rainbow_check = list(set(matrix_contents).intersection(rainbow)) #현재 클리어된 줄에 있는 mino와 mino의 종류중 겹치는 것 저장
                        if rainbow == rainbow_check: #현재 클리어된 줄에 모든 종류 mino 있다면
                            rainbow_count += plus

                        while k > zero:
                            for i in range(board_x):
                                matrix[i][k] = matrix[i][k - one]  # 남아있는 블록 한 줄씩 내리기(덮어쓰기)
                            k -= one
                if erase_count >= one:
                    if rainbow_count >= one:
                        score += rainbow_score * rainbow_count #임의로 rainbow는 한 줄당 500점으로 잡음
                        rainbow_count = zero #다시 초기화
                        screen.blit(ui_variables.rainbow_vector,
                         (board_width * 0.3175, board_height * 0.25)) #blit(이미지, 위치)
                        pygame.display.update()
                        pygame.time.delay(set_400) #0.4초

                    previous_time = current_time
                    
                    #점수 계산
                    if erase_count == ec_1:
                        ui_variables.break_sound.play()
                        ui_variables.single_sound.play()
                        score += ec_1_score * level * erase_count + combo_count
                        
                    elif erase_count == ec_2:
                        ui_variables.break_sound.play()
                        ui_variables.double_sound.play()
                        ui_variables.double_sound.play()
                        score += ec_2_score * level * erase_count + ec_2 * combo_count
                        
                    elif erase_count == ec_3:
                        ui_variables.break_sound.play()
                        ui_variables.triple_sound.play()
                        ui_variables.triple_sound.play()
                        ui_variables.triple_sound.play()
                        score += ec_3_score * level * erase_count + ec_3 * combo_count
                        
                    elif erase_count == ec_4:
                        ui_variables.break_sound.play()
                        ui_variables.tetris_sound.play()
                        ui_variables.tetris_sound.play()
                        ui_variables.tetris_sound.play()
                        ui_variables.tetris_sound.play()
                        score += ec_4_score * level * erase_count + ec_4 * combo_count
                        
                        screen.blit(ui_variables.combo_4ring,
                         (int(board_width*0.24), int(board_height*0.2))) #blit(이미지, 위치)
                    
                    # 도전과제 2 달성시 골드 777 추가
                    if combo_count == combo_7 :
                        if ch_2 :
                            gold += gold_777
                            update_gold_data(gold,user_id)

                    for i in range(one, eleven):
                        if combo_count == i:  # 1 ~ 10 콤보 이미지
                            screen.blit(ui_variables.large_combos[i - one],
                            (board_width * 0.27, board_height * 0.35))
                            #각 콤보 이미지에 대해 blit(이미지, 위치)
                            pygame.display.update()
                            pygame.time.delay(set_500)
                        elif combo_count > ten:  # 11 이상 콤보 이미지
                            screen.blit(tetris4,
                            (board_width*0.27, board_height * 0.35))
                            pygame.display.update()
                            pygame.time.delay(set_300)

                    for i in range(one, nine): # 1~8의 콤보 사운드
                        if combo_count == i + two:  # 3 ~ 11 콤보 사운드
                            ui_variables.combos_sound[i - one].play()
                        if combo_count > eleven:
                            ui_variables.combos_sound[8].play()
                if current_time - previous_time > set_10000: #10초가 지나면
                    previous_time = current_time #현재 시간을 과거시간으로 하고
                    combo_count = 0 #콤보 수 초기화
                if current_time - previous_time > set_1000: #콤보만들고 1초 뒤에
                    combo_status = False #combo_Status가 true가 된 걸 false로 바꿔줌


                # Increase level
                goal -= erase_count
                if goal < one and level < level_15:
                    level += level_1
                    ui_variables.LevelUp_sound.play()
                    goal += level * level_5
                    game_speed = int(game_speed - speed_change)
                    pygame.time.set_timer(pygame.USEREVENT, game_speed)
                    #Change_RATE += 1
                    #set_music_playing(CHANNELS, swidth)
                    set_music_playing(CHANNELS, swidth)

            elif event.type == KEYDOWN:
                erase_mino(dx, dy, mino, rotation, matrix)
                if event.key == K_ESCAPE:
                    ui_variables.click_sound.play()
                    pause = True
                # Hard drop
                elif event.key == K_SPACE:
                    ui_variables.fall_sound.play()
                    ui_variables.drop_sound.play()
                    while not is_bottom(dx, dy, mino, rotation, matrix):
                        dy += plus
                    hard_drop = True
                    pygame.time.set_timer(pygame.USEREVENT, framerate)
                    draw_mino(dx, dy, mino, rotation, matrix)
                    screen.fill(ui_variables.real_white)
                    draw_image(screen, gamebackground_image , board_width * 0.5, board_height * 0.5, board_width, board_height) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
                    draw_board(next_mino1, next_mino2, hold_mino, score, level, goal)
                    pygame.display.update()
                elif event.key == K_j :
                    framerate = int(framerate-speed_change)
                    print(framerate)

                # Hold
                elif event.key == K_RSHIFT : #keyboard 변경하기
                    if hold == False:
                        ui_variables.move_sound.play()
                        if hold_mino == h_mino:
                            hold_mino = mino
                            mino = next_mino1
                            next_mino1 = next_mino2
                            next_mino2 = randint(1, 7)
                        else:
                            hold_mino, mino = mino, hold_mino
                        dx, dy = 3, 0
                        rotation = 0
                        hold = True
                    draw_mino(dx, dy, mino, rotation, matrix)
                    screen.fill(ui_variables.real_white)
                    draw_image(screen, gamebackground_image , board_width * 0.5, board_height * 0.5, board_width, board_height) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
                    draw_board(next_mino1, next_mino2, hold_mino, score, level, goal)

                #dx, dy는 각각 좌표위치 이동에 해당하며, rotation은 mino.py의 테트리스 블록 회전에 해당함
                # Turn right
                elif event.key == K_UP:
                    if is_turnable_r(dx, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        rotation += one
                    # Kick
                    elif is_turnable_r(dx, dy - one, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dy -= one
                        rotation += one
                    elif is_turnable_r(dx + one, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx += one
                        rotation += one
                    elif is_turnable_r(dx - one, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx -= one
                        rotation += one
                    elif is_turnable_r(dx, dy - two, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dy -= two
                        rotation += one
                    elif is_turnable_r(dx + two, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx += two
                        rotation += one
                    elif is_turnable_r(dx - two, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx -= two
                        rotation += one
                    if rotation == r_4:
                        rotation = one
                    draw_mino(dx, dy, mino, rotation, matrix)
                    screen.fill(ui_variables.real_white)
                    draw_image(screen, gamebackground_image , board_width * 0.5, board_height * 0.5, board_width, board_height) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
                    draw_board(next_mino1, next_mino2, hold_mino, score, level, goal)
                # Turn left
                elif event.key == K_m:
                    if is_turnable_l(dx, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        rotation -= one
                    # Kick
                    elif is_turnable_l(dx, dy - one, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dy -= one
                        rotation -= one
                    elif is_turnable_l(dx + one, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx += one
                        rotation -= one
                    elif is_turnable_l(dx - one, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx -= one
                        rotation -= one
                    elif is_turnable_l(dx, dy - two, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dy -= two
                        rotation += one
                    elif is_turnable_l(dx + two, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx += two
                        rotation += one
                    elif is_turnable_l(dx - two, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx -= two
                    if rotation == h_mino:
                        rotation = r_3
                    draw_mino(dx, dy, mino, rotation, matrix)
                    screen.fill(ui_variables.real_white)
                    draw_image(screen, gamebackground_image , board_width * 0.5, board_height * 0.5, board_width, board_height) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
                    draw_board(next_mino1, next_mino2, hold_mino, score, level, goal)

                # Move left
                elif event.key == K_LEFT:
                    if not is_leftedge(dx, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx -= one
                    draw_mino(dx, dy, mino, rotation, matrix)
                    screen.fill(ui_variables.real_white)
                    draw_image(screen, gamebackground_image , board_width * 0.5, board_height * 0.5, board_width, board_height) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
                    draw_board(next_mino1, next_mino2, hold_mino, score, level, goal)
                # Move right
                elif event.key == K_RIGHT:
                    if not is_rightedge(dx, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx += one
                    draw_mino(dx, dy, mino, rotation, matrix)
                    screen.fill(ui_variables.real_white)
                    draw_image(screen, gamebackground_image , board_width * 0.5, board_height * 0.5, board_width, board_height) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
                    draw_board(next_mino1, next_mino2, hold_mino, score, level, goal)
                # rainbow test
                elif event.key == K_F1:
                    ui_variables.click_sound.play()
                    matrix[0][20] = 7 #빨
                    matrix[1][20] = 7 #빨
                    matrix[2][20] = 3#주
                    matrix[3][20] = 3#주
                    matrix[4][20] = 4#노
                    matrix[5][20] = 5#초
                    matrix[6][20] = 5#초
                    matrix[7][20] = 1#하
                    matrix[8][20] = 2#파
                    mino = 6
                # item click
                # light item use
                elif event.key == K_z :
                    if num_light>no_item :
                        mino = light_mino
                        num_light -= item_r
                        update_light_data(num_light,id_text)
                        erase_mino(dx, dy, mino, rotation, matrix)
                        
                    
                    draw_mino(dx, dy, mino, rotation, matrix)
                    screen.fill(ui_variables.real_white)
                    draw_image(screen, gamebackground_image , board_width * 0.5, board_height * 0.5, board_width, board_height) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
                    draw_board(next_mino1, next_mino2, hold_mino, score, level, goal)
                    
                # tnt item use
                elif event.key == K_x :
                    if num_tnt>no_item :
                        mino = tnt_mino
                        num_tnt -= item_r
                        update_tnt_data(num_tnt,id_text)
                        erase_mino(dx, dy, mino, rotation, matrix)
                    
                    
                    draw_mino(dx, dy, mino, rotation, matrix)
                    screen.fill(ui_variables.real_white)
                    draw_image(screen, gamebackground_image , board_width * 0.5, board_height * 0.5, board_width, board_height) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
                    draw_board(next_mino1, next_mino2, hold_mino, score, level, goal)
                # earthquake use
                elif event.key == K_c :
                    if num_earthquake>no_item :
                        earthquake(board_y, matrix)
                        num_earthquake -= item_r
                        update_earthquake_data(num_earthquake,id_text)
                        score += erase_score
                        k=board_y
                        while k > zero:
                            for i in range(board_x):
                                matrix[i][k] = matrix[i][k - one]  # 남아있는 블록 한 줄씩 내리기(덮어쓰기)
                            k -= one
                    
                    draw_mino(dx, dy, mino, rotation, matrix)
                    screen.fill(ui_variables.real_white)
                    draw_image(screen, gamebackground_image , board_width * 0.5, board_height * 0.5, board_width, board_height) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
                    draw_board(next_mino1, next_mino2, hold_mino, score, level, goal)

            elif event.type == VIDEORESIZE:
                board_width = event.w
                board_height = event.h
                if board_width < min_width or board_height < min_height: #최소 너비 또는 높이를 설정하려는 경우
                    board_width = min_width
                    board_height = min_height
                if not ((board_rate-0.1) < (board_height/board_width) < (board_rate+0.05)): #높이 또는 너비가 비율의 일정수준 이상을 넘어서게 되면
                    board_width = int(board_height / board_rate) #너비를 적정 비율로 바꿔줌
                    board_height = int(board_width*board_rate) #높이를 적정 비율로 바꿔줌


                block_size = int(board_height * 0.045)
                screen = pygame.display.set_mode((board_width, board_height), pygame.RESIZABLE)

                for i in range(len(button_list)):
                        button_list[i].change(board_width, board_height)

            elif event.type == pygame.MOUSEMOTION:
                if sandbox_mode:
                    if level_plus_button.isOver(pos):
                        level_plus_button.image = vector_plus_clicked
                    else:
                        level_plus_button.image = vector_plus
                    if level_minus_button.isOver(pos):
                        level_minus_button.image = vector_minus_clicked
                    else:
                        level_minus_button.image = vector_minus

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if sandbox_mode:
                    if level_plus_button.isOver(pos):
                        ui_variables.click_sound.play()
                        if level < level_15:
                            level += level_1
                            goal += level * level_5
                            #Change_RATE = level + 1
                            #set_music_playing(CHANNELS, swidth)
                            set_music_playing(CHANNELS, swidth)
                    if level_minus_button.isOver(pos):
                        ui_variables.click_sound.play()
                        if level > level_1:
                            level -= level_1
                            goal += level * level_5
                            #Change_RATE = level + 1
                            set_music_playing(CHANNELS, swidth)

        if time_attack and total_time - elapsed_time < 0: #타임어택 모드이면서, 60초가 지났으면
            ui_variables.GameOver_sound.play()
            start = False
            game_status = 'time_attack'
            game_over = True
            time_attack = False
            pygame.time.set_timer(pygame.USEREVENT, set_1)

        if attack_mode: #어택모드일 때 
            if attack_time - elapsed_attack_time < zero: # attack_time이 다 지났을 때 
                attack(attack_board_y,matrix) 
                attack_mode_time = False #elapsed_attack_time 초기화 
                attack_board_y -= one #장애물 블록 만든 윗 줄에 다음 장애물블록 생성하도록
            elif combo_status == True: #콤보 만들어졌을 때
                attack_mode_time = False #elapsed_attack_time 초기화

        pygame.display.update()
    elif login:
        draw_image(screen, login_bg, board_width*0.5, board_height*0.5,
        board_width, board_height)
        draw_image(screen, log_board, board_width*0.5, board_height*0.5,
        int(board_width*3/8), int(board_height*2/9))
        sign_up_button1.draw(screen,(0,0,0))
        sign_in_button1.draw(screen,(0,0,0))
        log_quit.draw(screen,(0,0,0))

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                pygame.time.set_timer(pygame.USEREVENT, set_300)
                pygame.display.update()
            elif event.type == pygame.MOUSEMOTION:
                if sign_up_button1.isOver_2(pos):
                    sign_up_button1.image = button_sign_up_clicked
                else:
                    sign_up_button1.image = button_sign_up
                if sign_in_button1.isOver_2(pos):
                    sign_in_button1.image = button_sign_in_clicked
                else:
                    sign_in_button1.image = button_sign_in
                if log_quit.isOver_2(pos):
                    log_quit.image = button_quit_clicked
                else:
                    log_quit.image = button_quit

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if sign_up_button1.isOver_2(pos):
                    ui_variables.click_sound.play()
                    signup = True
                    login = False
                if sign_in_button1.isOver_2(pos):
                    ui_variables.click_sound.play()
                    signin = True
                    login = False
                if log_quit.isOver_2(pos):
                    ui_variables.click_sound.play()
                    done = True
    elif signup:
        draw_image(screen, login_bg, board_width*0.5, board_height*0.5,
        board_width, board_height)
        draw_image(screen, signup_board, board_width*0.5, board_height*0.55,
        int(board_width*3/8),int(board_height*24/45))
        sign_up_button2.draw(screen,(0,0,0))
        log_back.draw(screen,(0,0,0))
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == QUIT:
                done = True
            for box in input_boxes_signup:
                box.handle_event(event)
            for box in input_boxes_signup:
                box.update()
            for box in input_boxes_signup:
                box.draw(screen)
            pygame.display.update()

            if event.type == USEREVENT:
                pygame.time.set_timer(pygame.USEREVENT, set_300)
            elif event.type == pygame.MOUSEMOTION:
                if sign_up_button2.isOver_2(pos):
                    sign_up_button2.image = button_sign_up_clicked
                else:
                    sign_up_button2.image = button_sign_up
                if log_back.isOver_2(pos):
                    log_back.image = button_log_back_clicked
                else:
                    log_back.image = button_log_back
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if sign_up_button2.isOver_2(pos):
                    ui_variables.click_sound.play()
                    id_text = input_box1.text
                    pw_text = input_box2.text
                    add_id(id_text)
                    add_pw(id_text, pw_text)
                    signup = False
                if log_back.isOver_2(pos):
                    ui_variables.click_sound.play()
                    signup = False

    elif signin:
        draw_image(screen, login_bg, board_width*0.5, board_height*0.5,
        board_width, board_height)
        draw_image(screen, signin_board, board_width*0.5, board_height*0.55,
        int(board_width*3/8),int(board_height*24/45))
        sign_in_button2.draw(screen,(0,0,0))
        log_back.draw(screen,(0,0,0))
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == QUIT:
                done = True
            for box in input_boxes_signin:
                box.handle_event(event)
            for box in input_boxes_signin:
                box.update()
            for box in input_boxes_signin:
                box.draw(screen)
            pygame.display.update()
            if event.type == USEREVENT:
                pygame.time.set_timer(pygame.USEREVENT, set_300)
                pygame.display.update()
            elif event.type == pygame.MOUSEMOTION:
                if sign_in_button2.isOver_2(pos):
                    sign_in_button2.image = button_sign_in_clicked
                else:
                    sign_in_button2.image = button_sign_in
                if log_back.isOver_2(pos):
                    log_back.image = button_log_back_clicked
                else:
                    log_back.image = button_log_back

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if sign_in_button2.isOver_2(pos):
                    ui_variables.click_sound.play()
                    id_text = input_box3.text
                    pw_text = input_box4.text
                    if check_info(id_text, pw_text):
                        signin= False
                        main = True
                        num_earthquake = load_earthquake_data(id_text)
                        num_light = load_light_data(id_text)
                        num_tnt = load_tnt_data(id_text)
                        gold = load_gold_data(id_text)
                        user_id = id_info(id_text)

                if log_back.isOver_2(pos):
                    ui_variables.click_sound.play()
                    signin = False

    # Game over screen
    elif game_over:

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                pygame.mixer.music.stop()
                pygame.time.set_timer(pygame.USEREVENT, set_300) #0.3초

                draw_image(screen, board_gameover, board_width * 0.5, board_height * 0.5, int(board_height * 0.7428), board_height) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
                menu_button.draw(screen, (0, 0, 0)) #rgb(0,0,0) = 검정색
                restart_button.draw(screen, (0, 0, 0))
                ok_button.draw(screen, (0, 0, 0))



            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    ui_variables.click_sound.play()
                    game_over = False
                    pygame.time.set_timer(pygame.USEREVENT, set_1) #0.001초

            elif event.type == pygame.MOUSEMOTION:
                if resume_button.isOver_2(pos):
                    menu_button.image = button_menu_clicked
                else:
                    menu_button.image = button_menu

                if restart_button.isOver_2(pos):
                    restart_button.image = button_restart_clicked
                else:
                    restart_button.image = button_restart

                if ok_button.isOver_2(pos):
                    ok_button.image = button_ok_clicked
                else:
                    ok_button.image = button_ok

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if ok_button.isOver(pos):
                    ui_variables.click_sound.play()

                    # 도전과제 1 활성화시
                    if ch_1 :
                        # 3만점 달성시
                        if score >= score_ch1 :
                            # 모든 아이템 1개 증가
                            num_light += item_r
                            num_earthquake += item_r
                            num_tnt += item_r
                            update_light_data(num_light,id_text)
                            update_earthquake_data(num_earthquake,id_text)
                            update_tnt_data(num_tnt,id_text)

                    # 도전과제 3 활성화시
                    if ch_3 :
                        # 5만점 달성시
                        if score >= score_ch3 :
                            # 1000골드 증가
                            gold += gold_1000
                            update_gold_data(gold,user_id)

                    if difficulty_mode:  # 난이도모드였을 때
                        # 점수에 따라서 골드 획득량 달라지게
                        if game_status == 'easy':  # easy모드일때
                            s_gold = int(score * easy_r)  # score*0.1 만큼 판골드 획득
                            gold += s_gold  # 기존 골드에 판골드 더하기
                            update_gold_data(gold, id_text)
                        elif game_status == 'normal':  # normal모드일때
                            s_gold = int(score * mid_r)  # score*0.2 만큼 판골드 획득
                            gold += s_gold  # 기존 골드에 판골드 더하기
                            update_gold_data(gold, id_text)
                        elif game_status == 'hard':  # hard모드일때
                            s_gold = int(score * hard_r)  # score*0.5 만큼 판골드 획득
                            gold += s_gold  # 기존 골드에 판골드 더하기
                            update_gold_data(gold, id_text)
 
                    if game_status == 'single':
                        add_score(game_status,  user_id, score)
                    if game_status == 'time_attack':
                        add_score(game_status,  user_id, score)
                    if game_status == 'easy':
                        add_score(game_status,  user_id, score)
                    if game_status == 'normal':
                        add_score(game_status,  user_id, score)
                    if game_status == 'hard':
                        add_score(game_status,  user_id, score)
        
                if menu_button.isOver(pos):
                    ui_variables.click_sound.play()
                    game_over = False

                if restart_button.isOver_2(pos):
                    if game_status == 'single':
                        start = True
                        pygame.mixer.music.play(minus) #play(-1) = 노래 반복재생
                    if game_status == 'time_attack':
                        time_attack = True
                        pygame.mixer.music.play(minus)
                    if game_status == 'easy':
                        attack_mode = True
                        gravity_mode = False
                        pygame.mixer.music.play(minus)
                    if game_status == 'normal':
                        attack_mode = False
                        gravity_mode = True
                        pygame.mixer.music.play(minus)
                    if game_status == 'hard':
                        attack_mode = True
                        gravity_mode = True
                        pygame.mixer.music.play(minus)
                    ui_variables.click_sound.play()
                    set_initial_values2()

                    game_over = False
                    pause = False

            elif event.type == VIDEORESIZE:
                board_width = event.w
                board_height = event.h
                if board_width < min_width or board_height < min_height: #최소 너비 또는 높이를 설정하려는 경우
                    board_width = min_width
                    board_height = min_height
                if not ((board_rate-0.1) < (board_height/board_width) < (board_rate+0.05)): #높이 또는 너비가 비율의 일정수준 이상을 넘어서게 되면
                    board_width = int(board_height / board_rate) #너비를 적정 비율로 바꿔줌
                    board_height = int(board_width*board_rate) #높이를 적정 비율로 바꿔줌


                block_size = int(board_height * 0.045) #블록 크기비율 고정
                screen = pygame.display.set_mode((board_width, board_height), pygame.RESIZABLE)

                for i in range(len(button_list)):
                        button_list[i].change(board_width, board_height)

    # Start screen
    elif main:
        # 변수 선언 및 초기화
        if initalize:
            set_initial_values()
        initalize = False
        main = True

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                pygame.time.set_timer(pygame.USEREVENT, 300) #0.3초

            elif event.type == pygame.MOUSEMOTION:
                if game_button.isOver_2(pos):
                    game_button.image = button_game_clicked
                else:
                    game_button.image = button_game

                if shop_button.isOver_2(pos):
                    shop_button.image = button_shop_clicked
                else:
                    shop_button.image = button_shop

                if help_button.isOver_2(pos):
                    help_button.image = button_help_clicked
                else:
                    help_button.image = button_help

                if quit_button.isOver_2(pos):
                    quit_button.image = button_quit_clicked
                else:
                    quit_button.image = button_quit

                if setting_vector.isOver(pos):
                    setting_vector.image = vector_setting_clicked
                else:
                    setting_vector.image = vector_setting

                if leader_vector.isOver(pos):
                    leader_vector.image = vector_leader_clicked
                else:
                    leader_vector.image = vector_leader

                if challenge_vector.isOver(pos):
                    challenge_vector.image = vector_challenge_clicked
                else:
                    challenge_vector.image = vector_challenge
                pygame.display.update()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game_button.isOver_2(pos):
                    ui_variables.click_sound.play()
                    game = True
                if shop_button.isOver_2(pos):
                    ui_variables.click_sound.play()
                    shop = True
                if leader_vector.isOver(pos):
                    ui_variables.click_sound.play()
                    leader_board = True
                if setting_vector.isOver(pos):
                    ui_variables.click_sound.play()
                    setting = True
                if quit_button.isOver_2(pos):
                    ui_variables.click_sound.play()
                    done = True
                if help_button.isOver_2(pos):
                    ui_variables.click_sound.play()
                    help = True
                if challenge_vector.isOver(pos):
                    ui_variables.click_sound.play()
                    challenge = True
                pygame.display.update()


            elif event.type == VIDEORESIZE:
                board_width = event.w
                board_height = event.h
                if board_width < min_width or board_height < min_height: #최소 너비 또는 높이를 설정하려는 경우
                    board_width = min_width
                    board_height = min_height
                if not ((board_rate-0.1) < (board_height/board_width) < (board_rate+0.05)): #높이 또는 너비가 비율의 일정수준 이상을 넘어서게 되면
                    board_width = int(board_height / board_rate) #너비를 적정 비율로 바꿔줌
                    board_height = int(board_width*board_rate) #높이를 적정 비율로 바꿔줌


                block_size = int(board_height * 0.045) #board 세로길이에 대해 원하는 비율로 곱해줌
                screen = pygame.display.set_mode((board_width, board_height), pygame.RESIZABLE)

                for i in range(len(button_list)):
                        button_list[i].change(board_width, board_height)

            # login page 예시
            elif event.type == KEYDOWN:
                if event.key == K_F1:
                    login = True

        draw_image(screen, background_image, board_width * 0.5, board_height * 0.5,
         board_width, board_height)

        game_button.draw(screen, (0, 0, 0)) #rgb(0,0,0) = 검정색
        shop_button.draw(screen, (0, 0, 0))
        help_button.draw(screen, (0, 0, 0))
        quit_button.draw(screen, (0, 0, 0))
        leader_vector.draw(screen, (0, 0, 0))
        challenge_vector.draw(screen, (0, 0, 0))
        setting_vector.draw(screen, (0, 0, 0))


        if not game:
            pygame.display.update()

    else:
        draw_image(screen, login_bg, board_width*0.5, board_height*0.5,
        board_width, board_height)
        draw_image(screen, log_board, board_width*0.5, board_height*0.5,
        int(board_width*3/8), int(board_height*2/9))
        sign_up_button1.draw(screen,(0,0,0))
        sign_in_button1.draw(screen,(0,0,0))
        log_quit.draw(screen,(0,0,0))

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                pygame.time.set_timer(pygame.USEREVENT, 300)
                pygame.display.update()
            elif event.type == pygame.MOUSEMOTION:
                if sign_up_button1.isOver_2(pos):
                    sign_up_button1.image = button_sign_up_clicked
                else:
                    sign_up_button1.image = button_sign_up
                if sign_in_button1.isOver_2(pos):
                    sign_in_button1.image = button_sign_in_clicked
                else:
                    sign_in_button1.image = button_sign_in
                if log_quit.isOver_2(pos):
                    log_quit.image = button_quit_clicked
                else:
                    log_quit.image = button_quit

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if sign_up_button1.isOver_2(pos):
                    ui_variables.click_sound.play()
                    signup = True
                if sign_in_button1.isOver_2(pos):
                    ui_variables.click_sound.play()
                    signin = True
                if log_quit.isOver_2(pos):
                    ui_variables.click_sound.play()
                    done = True



pygame.quit()
