import pymysql
import bcrypt
import pygame
import operator
import wave
import os
from pygame.locals import *

database = pymysql.connect(
    user='admin',
    password='qwqw7113',
    host='database-1.caujngehv3l9.ap-northeast-2.rds.amazonaws.com',
    db='users',
    charset='utf8'
)

def add_id(id_text):
    curs = database.cursor()
    sql = "INSERT INTO users (user_id) VALUES (%s)"
    curs.execute(sql, id_text)
    database.commit()  #서버로 추가 사항 보내기
    curs.close()

def add_pw(id_text, pw_text):
    #회원가입시 초기 아이템 수는 0으로 설정
    #추가하기
    initial_earthquake = 0
    initial_light  = 0
    initial_tnt = 0
    initial_gold = 0
    hashed_pw = bcrypt.hashpw(pw_text.encode('utf-8'), bcrypt.gensalt())#비밀번호를 encoding해서 type를 byte로 바꿔서 hashpw함수에 넣기
    decode_hash_pw = hashed_pw.decode('utf-8') #비밀번호 확인할 때는 str값으로 받아 매칭해서 비번을 데베에 저장할 때 decoding 해야함
    curs = database.cursor()
    sql = "UPDATE users SET user_pw= %s WHERE user_id=%s"
    curs.execute(sql,(decode_hash_pw,id_text))
    database.commit()
    print(hashed_pw)
    print(decode_hash_pw)
    curs = database.cursor()
    sql = "UPDATE users SET user_earthquake= %s, user_light= %s, user_tnt= %s, user_gold= %s WHERE user_id=%s"
    curs.execute(sql, (initial_earthquake,initial_light, initial_tnt, initial_gold, id_text))
    database.commit()
    curs.close()

# 입력받은 아이디가 데이터베이스에 있는지 확인, 아이디와 비밀번호가 일치하는지 확인
def check_info(id_text, pw_text):
    input_pw = pw_text.encode('utf-8')
    curs = database.cursor(pymysql.cursors.DictCursor)
    sql = "SELECT * FROM users WHERE user_id=%s"
    curs.execute(sql ,id_text)
    data = curs.fetchone()  # 리스트 안에 딕셔너리가 있는 형태
    curs.close()
    check_password=bcrypt.checkpw(input_pw,data['user_pw'].encode('utf-8'))
    return check_password

def id_info(id_text):
    global user_id
    user_id = id_text
    return user_id

def load_earthquake_data(user_id):
    curs = database.cursor(pymysql.cursors.DictCursor)
    sql = "SELECT * FROM users WHERE user_id=%s"
    curs.execute(sql, user_id)
    data = curs.fetchone()
    curs.close()
    return data['user_earthquake']

def load_light_data(user_id):
    curs = database.cursor(pymysql.cursors.DictCursor)
    sql = "SELECT * FROM users WHERE user_id=%s"
    curs.execute(sql, user_id)
    data = curs.fetchone()
    curs.close()
    return data['user_light']

def load_tnt_data(user_id):
    curs = database.cursor(pymysql.cursors.DictCursor)
    sql = "SELECT * FROM users WHERE user_id=%s"
    curs.execute(sql, user_id)
    data = curs.fetchone()
    curs.close()
    return data['user_tnt']

def load_gold_data(user_id):
    curs = database.cursor(pymysql.cursors.DictCursor)
    sql = "SELECT * FROM users WHERE user_id=%s"
    curs.execute(sql, user_id)
    data = curs.fetchone()
    curs.close()
    return data['user_gold']

# gameover쪽에 있음
def update_gold_data(user_gold,user_id):
    curs = database.cursor()
    sql = "UPDATE users SET user_gold= %s WHERE user_id=%s"
    curs.execute(sql, (user_gold, user_id))
    database.commit()
    curs.close()
# 상점이랑 아이템 사용했을 때
def update_earthquake_data(user_earthquake,user_id):
    curs = database.cursor()
    sql = "UPDATE users SET user_earthquake= %s WHERE user_id=%s"
    curs.execute(sql, (user_earthquake, user_id))
    database.commit()
    curs.close()
def update_light_data(user_light,user_id):
    curs = database.cursor()
    sql = "UPDATE users SET user_light= %s WHERE user_id=%s"
    curs.execute(sql, (user_light, user_id))
    database.commit()
    curs.close()
def update_tnt_data(user_tnt,user_id):
    curs = database.cursor()
    sql = "UPDATE users SET user_tnt= %s WHERE user_id=%s"
    curs.execute(sql, (user_tnt, user_id))
    database.commit()
    curs.close()

'''이거는 game status 확인하고 고치기'''
def add_score(game_status,  ID, score): #랭크 점수 기록
    #추가하기
    curs = database.cursor()
    if game_status == 'single':
        sql = "INSERT INTO single_rank (user_id, score) VALUES (%s, %s)"
    elif game_status == 'easy':
        sql = "INSERT INTO easy_mode_rank (user_id, easy_mode_score) VALUES (%s, %s)"
    elif game_status == 'normal':
        sql = "INSERT INTO normal_mode_rank (user_id, normal_mode_score) VALUES (%s, %s)"
    elif game_status == 'hard':
        sql = "INSERT INTO hard_mode_rank (user_id, hard_mode_score) VALUES (%s, %s)"
    elif game_status == 'time_attack':
        sql = "INSERT INTO timeattack_rank (user_id, timeattack_score) VALUES (%s, %s)"
    curs.execute(sql, (ID, score))
    database.commit()  #서버로 추가 사항 보내기
    curs.close()


def load_rank_data(game_status):                                             #데이터 베이스에서 데이터 불러오기
    
    curs = database.cursor(pymysql.cursors.DictCursor)
    if game_status == 'single':
        sql = "select * from single_rank order by score desc "
    elif game_status == 'easy':
        sql = "select * from easy_mode_rank order by easy_mode_score desc"
    elif game_status == 'normal':
        sql = "select * from normal_mode_rank order by normal_mode_score desc"
    elif game_status == 'hard':
        sql = "select * from hard_mode_rank order by hard_mode_score desc"
    elif game_status == 'time_attack':
        sql = "select * from timeattack_rank order by timeattack_score desc"
    curs.execute(sql)
    data = curs.fetchall()
    curs.close()
    return data
