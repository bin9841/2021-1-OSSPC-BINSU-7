# 2021-1-OSSPC-BINSU-7
-------------
[![GitHub license](https://img.shields.io/badge/license-MIT-lightgrey.svg)](https://github.com/CSID-DGU/2021-1-OSSPC-BINSU-7/blob/develop/LICENSE)
[![OS](https://img.shields.io/badge/OS-ubuntu-red)](https://ubuntu.com)
[![Python version](https://img.shields.io/badge/python-3.5.2-brightgreen.svg)](https://www.python.org)
[![Pygame version](https://img.shields.io/badge/pygame-2.0.0-yellow.svg)](http://pygame.org)  
**Team Leader**:  Yun Sangwoo [[Awarduuu](https://github.com/Awarduuu)]   
**Team Member**: Park Shinyoung [[shxnyoung](https://github.com/shxnyoung)], Ahn Subin[[bin9841](https://github.com/bin9841)]

## How to play
### Installation (OS: Ubuntu)
1. 터미널에 `git clone https://github.com/CSID-DGU/2021-1-OSSPC-BINSU-7.git ` 입력  
(터미널 실행 경로에서 Binsu라는 이름의 폴더에 해당 프로젝트 복사)

2. `pip3 install pygame` 입력  
(게임에 활용될 pygame package 설치)

3. `pip3 install pymysql` , `pip3 install bcrypt` 입력  
(DB에 활용될 pymysql, bcrypt package 설치)

3. `cd PBSPYTRIS` 입력  
(PBSPYTRIS 디렉토리로 이동)

4. `python3 pbspytris.py` 입력   
(게임 실행)

### 조작키 안내
<img src="PBSPYTRIS/assets/vector/board_help.png" width="500" height="250"> 

## Introduce
### 게임 소개
지난 학기 오픈소스 테트리스 프로젝트인 [Tetris-Kingdom](https://github.com/CSID-DGU/2020-2-OSSP-CP-17woljang-9)의 코드를 base code로 하여 기능을 추가하고, 오류를 보완하여 만든 게임

Single, Difficulty, Time attack, Sandbox 총 네가지 플레이모드로 구성되어 있으며, Difficulty mode와 Sandbox모드를 만드는 Gravity mode와 Attack mode가 존재한다. 

#### <구성모드>
- Gravity mode : 블록이 쌓일 때 아래가 빈칸일 시, 블록이 아래 비워진 빈칸을 채우며  
동시에 쌓인 블록이 장애물 블록으로 변하는 모드  
- Attack mode : PBSPYTRIS에서 만든 모드로 제한시간 (30초) 내에 콤보를 만들지 못하면 맨 밑에 장애물 블록 줄이 생성되는 모드  

#### <플레이모드>
- Single mode : 일반 테트리스 게임 모드
- Difficulty mode : easy, normal, hard 총 세가지 플레이모드가 있는 난이도 모드
  - easy mode : Attack mode on
  - normal mode : Gravity mode on
  - hard mode : Attack mode, Gravity mode on
- Time attack mode : 제한시간 60초가 주어지는 모드 
- Sandbox mode : 게임모드와 레벨을 플레이어가 조작할 수 있는 연습 모드
  - 게임 시작 전 모드와 레벨 지정 가능
  - 인게임에서 레벨 변경 가능  
  
  | Attack    | Gravity   |                   |  
  |-----------|-----------|-------------------|   
  | off       | off       | Single mode       |  
  | on        | off       | Easy mode         |  
  | off       | on        | Normal mode       |  
  | on        | on        | Hard mode         |  

  
## 새로운 기능

### 1. 회원가입 및 로그인  
게임 시작 첫화면인 회원가입 및 로그인 선택 페이지    
  
<img src="PBSPYTRIS/assets/Screenshots/login1.png" width="500" height="250">   
  
singup 클릭시 회원가입을 할 수 있는 페이지   
  
<img src="PBSPYTRIS/assets/Screenshots/signup.png" width="500" height="250">  
  
 signup 완료시 로그인을 할 수 있는 페이지  
    
<img src="PBSPYTRIS/assets/Screenshots/signin.png" width="500" height="250">  

### 2. 상점 & 아이템

#### <상점>
gold를 소모해 item을 구매하는 창  
<img src="PBSPYTRIS/assets/Screenshots/shop.png" width="500" height="250">    
#### <아이템>
gold를 소모해 구매한 후 Difficulty mode 에서 사용 가능한 아이템   
- Lightning  
<img src="PBSPYTRIS/assets/vector/item_lightning.png" width="50" height="50"> : z버튼을 눌러 lightning 블록중심으로 3x3 위치의 블록 삭제  
- TNT   
<img src="PBSPYTRIS/assets/vector/item_tnt.png" width="50" height="50"> : x버튼을 눌러 TNT 블록을 중심으로 5x5 위치의 블록 삭제
- Earthquake  
<img src="PBSPYTRIS/assets/vector/item_earth.png" width="50" height="50"> : c버튼을 누르는 즉시 맨 아랫줄 블록 모두 삭제 및 score 100점 증가 

### 3. challenge
PBSPYTRIS만의 특징적인 기능으로 on으로 설정해둔 도전과제를 게임 내에서 달성하면 보상을 받을 수 있음  
200 gold를 소모하여 도전과제 on 가능   
<img src="PBSPYTRIS/assets/Screenshots/challenge.png" width="500" height="250"> 

## Score board
| Action             | Score                              |
|--------------------|------------------------------------|
| Block drop         | 10 * level                         |
| Erase 1 line       | 50 * level * 1 + combo_count       |
| Erase 2 lines      | 150 * level * 2 + 2 * combo_count  |
| Erase 3 lines      | 350 * level * 3 + 3 * combo_count  |
| Erase 4 lines      | 1000 * level * 4 + 4 * combo_count |
| Erase Rainbow line | 500 * rainbow_count                |

* combo_count: 누적 콤보 수(10초 안에 콤보 실패 시 누적 콤보 수 초기화)
* Rainbow line: 서로 다른 7가지 블록 색을 포함한 라인(장애물 제외)
* Rainbow count: 누적 레인보우 달성 횟수(초기화 X)

## Etc
[Screenshot](https://github.com/CSID-DGU/2021-1-OSSPC-BINSU-7/tree/main/PBSPYTRIS/assets/Screenshots)  
[DOC(발표 자료)](https://github.com/CSID-DGU/2021-1-OSSPC-BINSU-7/tree/main/Doc)  
[협업 규칙](https://github.com/CSID-DGU/2021-1-OSSPC-BINSU-7/wiki/BINSU-%ED%98%91%EC%97%85%EA%B7%9C%EC%B9%99)
