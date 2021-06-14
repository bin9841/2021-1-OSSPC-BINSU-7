import pygame
import operator
import wave
import os
from mino import *
from random import *
from pygame.locals import *

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

max_score = 999999

# button_size
s_w = 800
s_h = 450
m_w = 1200
m_h = 675
b_w = 1600
b_h = 900

# mino
mino_r = 1 # mino 한칸 내리거나 올리는 단위
mino_x = 1 # grid x 좌표
mino_y = 0 # grid y 좌표
mino_3 = 3 # 3rd mino
mino_zero = 0 # 해당 블록 없음 표기
h_mino = -1 # hold 상태
g_mino = 8 # ghost block
f_mino = 9 # 장애물 block
l_range = 3 # ligth block range
t_range = 5 # tnt block range
r_3 = 3 # rotation 초기화
r_4 = 4 # rotation 마지막

# difficulty
easy_r = 0.1
mid_r = 0.2
hard_r = 0.5

# 아이템
no_item = 0 # item이 0개일때
item_r = 1 # item 증감단위

# gold
gold_0 = 0
gold_100 = 100
gold_200 = 200

# set
set_300 = 300
set_400 = 400
set_500 = 500
set_1000 =1000
set_10000 = 10000
set_1 = 1

# level
level_1 = 1
level_5 = 5
level_15 = 15

# erase
zero = 0
one = 1
two = 2
five = 5
eight = 8
nine = 9
ten = 10
eleven = 11
ec_1 = 1
ec_1_score = 50
ec_2 = 2
ec_2_score = 150
ec_3 = 3
ec_3_score = 350
ec_4 = 4
ec_4_score = 1000

# challenge
# ch1
score_ch1 = 30000 # 도전과제 1 목표점수
# ch2
combo_7 = 7 # combo count 7일때
gold_777 = 777 # ch2 보상
# ch3
score_ch3 = 50000 # 도전과제 3 목표점수
gold_1000 = 1000 # ch3 보상

# score
bc = 6
score_r = 10 # 1레벨 증가시 score
erase_score = 100
rainbow_score = 500

# leader board
loc_0 = 0 # 첫글자
loc_1 = 1 # 두번째 글자
loc_2 = 2 # 세번째 글자
asc_1 = 65 # 아스키코드 시작
asc_2 = 90# 아스키코드 끝

# 기본 볼륨
vol_range = 100
plus = 1
minus = -1
volume_z = 0 # volume = 0
volume_m = 5 # volume = 5
volume_f = 10 # volume = 10
music_volume = 5
effect_volume = 5

initalize = True


#각 이미지 주소
# background
background_image = 'assets/vector/Background.png' #홈 배경화면
gamebackground_image = 'assets/vector/Background_game.png' #게임 배경화면

# board
board_challenge = 'assets/vector/board_challenge.png'
board_gameover = 'assets/vector/board_gameover.png'
board_help = 'assets/vector/board_help.png'
board_leader = 'assets/vector/board_leader.png'
board_number = 'assets/vector/board_number.png'
board_pause = 'assets/vector/board_pause.png'
board_setting = 'assets/vector/board_setting.png'
board_shop = 'assets/vector/board_shop.png'
board_start = 'assets/vector/board_start.png'
board_sandbox = 'assets/vector/board_sandbox.png'
board_difficulty = 'assets/vector/board_difficulty.png'
board_volume = 'assets/vector/board_volume.png'
board_screen = 'assets/vector/board_screen.png'

#button
button_allmute = 'assets/vector/button_allmute.png'
button_allmute_clicked = 'assets/vector/button_allmute_clicked.png'
button_allmute_on = 'assets/vector/button_allmute_on.png'

button_back = 'assets/vector/button_back.png'
button_back_clicked = 'assets/vector/button_back_clicked.png'

button_default = 'assets/vector/button_default.png'
button_default_clicked = 'assets/vector/button_default_clicked.png'
button_default_on = 'assets/vector/button_default_on.png'

button_gravity = 'assets/vector/button_gravity.png'
button_gravity_clicked = 'assets/vector/button_gravity_clicked.png'
button_gravity_on = 'assets/vector/button_gravity_on.png'

button_help = 'assets/vector/button_help.png'
button_help_clicked = 'assets/vector/button_help_clicked.png'

button_menu = 'assets/vector/button_menu.png'
button_menu_clicked = 'assets/vector/button_menu_clicked.png'

button_ok = 'assets/vector/button_ok.png'
button_ok_clicked = 'assets/vector/button_ok_clicked.png'

button_pvp = 'assets/vector/button_pvp.png'
button_pvp_clicked = 'assets/vector/button_pvp_clicked.png'

button_quit = 'assets/vector/button_quit.png'
button_quit_clicked = 'assets/vector/button_quit_clicked.png'

button_restart = 'assets/vector/button_restart.png'
button_restart_clicked = 'assets/vector/button_restart_clicked.png'

button_resume = 'assets/vector/button_resume.png'
button_resume_clicked = 'assets/vector/button_resume_clicked.png'

button_sandbox = 'assets/vector/button_sandbox.png'
button_sandbox_clicked = 'assets/vector/button_sandbox_clicked.png'
button_sandbox_on = 'assets/vector/button_sandbox_on.png'

button_setting = 'assets/vector/button_setting.png'
button_setting_clicked = 'assets/vector/button_setting_clicked.png'

button_shop = 'assets/vector/button_shop.png'
button_shop_clicked = 'assets/vector/button_shop_clicked.png'

button_single = 'assets/vector/button_single.png'
button_single_clicked = 'assets/vector/button_single_clicked.png'

button_start = 'assets/vector/button_start.png'
button_start_clicked = 'assets/vector/button_start_clicked.png'

button_timeattack = 'assets/vector/button_timeattack.png'
button_timeattack_clicked = 'assets/vector/button_timeattack_clicked.png'

button_attack = 'assets/vector/button_attack.png'
button_attack_clicked = 'assets/vector/button_attack_clicked.png'
button_attack_on = 'assets/vector/button_attack_on.png'

button_difficulty = 'assets/vector/button_difficulty.png'
button_difficulty_clicked = 'assets/vector/button_difficulty_clicked.png'

button_easy = 'assets/vector/button_easy.png'
button_easy_clicked = 'assets/vector/button_easy_clicked.png'

button_normal = 'assets/vector/button_normal.png'
button_normal_clicked = 'assets/vector/button_normal_clicked.png'

button_hard = 'assets/vector/button_hard.png'
button_hard_clicked = 'assets/vector/button_hard_clicked.png'

button_buy = 'assets/vector/button_buy.png'
button_buy_clicked = 'assets/vector/button_buy_clicked.png'

button_game = 'assets/vector/button_game.png'
button_game_clicked = 'assets/vector/button_game_clicked.png'

# icon : 버튼이 아닌 아이콘, 이벤트 없음
icon_combo = 'assets/vector/icon_combo.png'
icon_level = 'assets/vector/icon_level.png'
icon_speed = 'assets/vector/icon_speed.png'

# item
item_earth = 'assets/vector/item_earth.png'
item_gold = 'assets/vector/item_gold.png'
item_tnt = 'assets/vector/item_tnt.png'
item_light = 'assets/vector/item_lightning.png'
item_tnt_info = 'assets/vector/tnt_info.PNG'
item_light_info='assets/vector/light_info.PNG'
item_earth_info='assets/vector/earth_info.PNG'

# screensize
size_s = 'assets/vector/screensize1.png'
size_m = 'assets/vector/screensize2.png'
size_b = 'assets/vector/screensize3.png'

# vector : 이벤트 존재하는 아이콘
vector_challenge = 'assets/vector/vector_challenge.png'
vector_challenge_clicked = 'assets/vector/vector_challenge_clicked.png'

vector_leader = 'assets/vector/vector_leaderboard.png'
vector_leader_clicked = 'assets/vector/vector_leader_clicked.png'

vector_minus = 'assets/vector/vector_minus.png'
vector_minus_clicked = 'assets/vector/vector_minus_clicked.png'

vector_plus = 'assets/vector/vector_plus.png'
vector_plus_clicked = 'assets/vector/vector_plus_clicked.png'

vector_screen = 'assets/vector/vector_screen.png'
vector_screen_clicked = 'assets/vector/vector_screen_clicked.png'

vector_setting = 'assets/vector/vector_setting.png'
vector_setting_clicked = 'assets/vector/vector_setting_clicked.png'

vector_sound_off = 'assets/vector/vector_sound_off.png'
vector_sound_on = 'assets/vector/vector_sound_on.png'

vector_volume = 'assets/vector/vector_volume.png'
vector_volume_clicked = 'assets/vector/vector_volume_clicked.png'

tetris = "assets/Combo/tetris4.png"

challenge_info1 = 'assets/vector/challenge_info1.PNG'
challenge_info2 = 'assets/vector/challenge_info2.PNG'
challenge_info3 = 'assets/vector/challenge_info3.PNG'

on = 'assets/vector/button_on.png'
on_clicked = 'assets/vector/button_on_clicked.png'
off = 'assets/vector/button_off.png'
off_clicked = 'assets/vector/button_off_clicked.png'

signup_board = 'assets/vector/signup.png'
signin_board = 'assets/vector/signin.png'
login_bg = 'assets/vector/Background_login.png'
log_board = 'assets/vector/log_or_sign_board.png'

button_log_back = 'assets/vector/button_l_back.png'
button_log_back_clicked = 'assets/vector/button_l_back_clicked.png'
button_sign_up = 'assets/vector/button_sign_up.png'
button_sign_up_clicked = 'assets/vector/button_sign_up_clicked.png'
button_sign_in = 'assets/vector/button_sign_in.png'
button_sign_in_clicked = 'assets/vector/button_sign_in_clicked.png'