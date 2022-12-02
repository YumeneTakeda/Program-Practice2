# -*- coding: utf-8 -*-
"""
@author: grimbergen
"""
from pydoc import doc
import random
import numpy as np

# 盤面の大きさ
BOARD_SIZE = 5

# マスの要素
#[ENEMY_VOL,ENEMY_STR,GAS,BOSS_PLACE,SINK,MATTERIAL,WEAPON]
ENEMY_VOL = 0
ENEMY_STR = 1
GAS_MAS = 2
BOSS_PLACE = 3
SINK_PLACE = 4
MATTERIAL_PLACE = 5
WEAPON = 6

NOT_GAME_END = 0
WIN = 1
LOSE = 2

SINK_FALSE = 0
SINK_TRUE = "×"

BOSS_INAI = 0
BOSS_IRU = "B"

SIZAI_NAI = 0
SIZAI_ARU = 1
BUKI_NAI = 0
BUKI_ARU = "W"


#ゲームの勝敗確認
winlose = NOT_GAME_END
#経過日数
day = 0

def make_flat_board():
    flat_board = [[0] * 7 for i in range(BOARD_SIZE)
                  for j in range(BOARD_SIZE)]
    return flat_board


def print_board(board):
    print()
    i = 1
    for line in board:
        print(line, end="")
        if i % 5 == 0:
            print()
        i = i+1


#一部例外を作る
def without_rand(player_place, board):
    result = random.randint(0, 24)

    #プレイヤーと被ったらやり直し
    while result == player_place or board[result][SINK_PLACE] == SINK_TRUE:
        result = random.randint(0, 24)
    return result

#敵の配置


def put_enemies(board, day, player_p):
    if day == 5:
        #ボスと資材の配置
        boss_p = without_rand(player_p, board)
        while board[boss_p][MATTERIAL_PLACE] >= 1:
            boss_p = without_rand(player_p, board)
        board[boss_p][BOSS_PLACE] = BOSS_IRU
        board[boss_p][MATTERIAL_PLACE] += 1
        #武器をボスと重ならないように配置
        weapon_p = without_rand(player_p, board)
        while weapon_p == boss_p:
            weapon_p = without_rand(player_p, board)
        board[weapon_p][WEAPON] = BUKI_ARU
    else:
        #資材の配置
        without_matt = without_rand(player_p, board)
        while board[without_matt][MATTERIAL_PLACE] >= 1:
            without_matt = without_rand(player_p, board)
        board[without_rand(player_p, board)][MATTERIAL_PLACE] += 1

    #ガスの配置 2回
    for i in range(2):
        put_gas = without_rand(player_p, board)
        while board[put_gas][GAS_MAS] == "G":
            put_gas = without_rand(player_p, board)
        board[put_gas][GAS_MAS] ="G"
    #敵2体の配置
    str_2_enemy = without_rand(player_p, board)
    board[str_2_enemy][ENEMY_VOL] += 1
    board[str_2_enemy][ENEMY_STR] += 2
    str_3_enemy = without_rand(player_p, board)
    board[str_3_enemy][ENEMY_VOL] += 1
    board[str_3_enemy][ENEMY_STR] += 3

    #print("タイミングの確認")
    #print_board(board)

    return board

#島沈む
def board_sink(board, day):
    if day == 4:
        for i in [20, 21, 22, 23, 24]:
            board[i][SINK_PLACE] = SINK_TRUE
            for youso in [ENEMY_VOL, ENEMY_STR, GAS_MAS, BOSS_PLACE, MATTERIAL_PLACE, WEAPON]:
                if board[i][youso] != 0:
                    board[i-5][youso] = board[i][youso]
                    board[i][youso] = 0

    elif day == 7:
        for i in [4, 9, 14, 19, 24]:
            board[i][SINK_PLACE] = SINK_TRUE
            for youso in [ENEMY_VOL, ENEMY_STR, GAS_MAS, BOSS_PLACE, MATTERIAL_PLACE, WEAPON]:
                if board[i][youso] != 0:
                    board[i-1][youso] = board[i][youso]
                    board[i][youso] = 0
    elif day == 10:
        for i in [0, 1, 2, 3, 4]:
            board[i][SINK_PLACE] = SINK_TRUE
            for youso in [ENEMY_VOL, ENEMY_STR, GAS_MAS, BOSS_PLACE, MATTERIAL_PLACE, WEAPON]:
                if board[i][youso] != 0:
                    board[i+5][youso] = board[i][youso]
                    board[i][youso] = 0
    return board


#!/usr/bin/env python
# coding: utf-8


HP = 10
STAMINA = 6
OWEND_PARTS = 0
GUN = 0
ZAHYOU = 0

DAY = 0
WIN_LOSE = 0

ENEMIES_NUM = 0
ENEMIES_POWER = 0
GAS = 0
PARTS = 0
BOSS = 0
SINK = 0
ITEM = 0


player = [HP, STAMINA, OWEND_PARTS, GUN, ZAHYOU]
Board = [[ENEMIES_NUM, ENEMIES_POWER, GAS, PARTS, BOSS, SINK, ITEM]]*5
Board = Board * 5
#print(Board)

#HP回復
def Heal(player):
    n = random.randint(2, 4)
    for i in range(n):
        if player[0] >= 10:
            break
        else:
            player[0] += 1
    return n

#移動
def Move(player, way, Board):
    zahyou = player[4]
    if zahyou > 24 or zahyou < 0:
        return "正しい座標を入力してください"
    if way == "W":
        if zahyou < 5:
            print("その方向へは進めません")
        elif Board[zahyou - 5][4] == "×":
            print("その方向へは進めません")
        else:
            zahyou -= 5
            player[1] -= 1
    elif way == "A":
        if zahyou % 5 == 0:
            print("その方向へは進めません")
        elif Board[zahyou - 1][4] == "×":
            print("その方向へは進めません")
        else:
            zahyou -= 1
            player[1] -= 1
    elif way == "S":
        if zahyou > 20:
            print("その方向へは進めません")
        elif Board[zahyou + 5][4] == "×":
            print("その方向へは進めません")
        else:
            zahyou += 5
            player[1] -= 1
    elif way == "D":
        if zahyou % 5 == 4:
            print("その方向へは進めません")
        elif zahyou == 24:
            print("その方向へは進めません")
        elif Board[zahyou + 1][4] == "×":
            print("その方向へは進めません")
        else:
            zahyou += 1
            player[1] -= 1
    player[4] = zahyou
    return player

BOARD_SIZE=25
win_lose=0
player=[0,0,0,0,0]
board=[[]]

#マップ初期化
def make_flat_board():
    flat_board = [[0] * 7 for i in range(BOARD_SIZE)]
    return flat_board

#戦闘
def Fight(player,board):
    win_lose=0
    if board[player[4]][3]=="B":
        if player[3]==1:
            #ボス倒し
            print("【ボス戦勝利】")
            board[player[4]][3] = 0
            board[player[4]][0] = 0
        else:
            player[0] = 0
            print("【ボス戦敗北】")  
            win_lose=2  
    if board[player[4]][1]>0:
        if player[0] > board[player[4]][1]:
            print("戦闘に勝利")
            #スタミナ回復
            for i in range(board[player[4]][1]):
                player[1]+=1
            if player[1]>6:
                player[1]=6    
            #HP減る
            player[0] -= board[player[4]][1]
            board[player[4]][1]=0
            board[player[4]][0]=0
        else:
            player[0] = 0
            print("戦闘に敗北") 
            win_lose=2    
    return win_lose         

#マップ表示
def Displaydangeon(player,board):

    for j in range(5):
        for i in range(5):
            i_j_map = j*5+i
            print("|", board[i_j_map][0], board[i_j_map][1], board[i_j_map][2], "|", end="")
        print()
        for i in range(5):
            i_j_map = j*5+i
            print("|", board[i_j_map][3], board[i_j_map][4], board[i_j_map][5], "|", end="")
        print()
        for i in range(5):
            i_j_map = j*5+i
            print("|", board[i_j_map][6],end=" ") 
            if i_j_map == player[4]:
                print("p", " ", "|", end="")
            else:
                print(" ", " ", "|", end="")
        print("\n―――――――――――――――――――――――――――――――――――――――――――――")

#ルール説明
def rule_setumei():
    print("")
    print(" ————————————————————————ルール説明—————————————————————————————")
    print("1:10日経過するまでに10個の資材を集めて船を完成させましょう       ")
    print("・資材を10個集め、10日間生き残れたら脱出成功")
    print("・資材を10個集められずに10日経過してしまうと、島が沈んでしまう ")
    print("2:プレイヤー情報")
    print("・HPは初期値、最大値共に10")
    print("・スタミナは初期値、最大値共に6")
    print("・初期位置は左上で表示は[P]")
    print("3:Wで北、Aで西、Sで南、Dで東方向に移動可能")
    print("・スタミナを1消費して1マス移動")
    print("4:1マスの構造は7つの要素から成り立つ3×3のマスである")
    print("| 1 3 0 |・左から敵の数、敵の強さ、ガスの数")
    print("| B 0 1 |・左からボスの有無(B)、沈没済か(×)、資材の数")
    print("| 0     |・武器の有無(W)")
    print("(この場合は1マスに強さ3の敵とボスと資材が一つずつ存在している)")
    print("5:日数経過")
    print("・スタミナが0になると一日が経過")
    print("・一日経過するとスタミナが全回復し、HPが2~4ランダムな値回復")
    print("・4日,7日10日ごとに島の辺が沈んでいく(南,東,北の順)")
    print("・沈む際、そのマスにあったすべての要素は一番近いマスに移動される")
    print("6:各要素の出現")
    print("・毎日強さ2と3の敵1体ずつランダムな位置に出現")
    print("・毎日ガスマスが2マス出現")
    print("・ガスマスを通るとHPが1減る")
    print("・毎日資源が一つずつ出現")
    print("・5日目にボスと武器が出現(5日目の資源はボスが持っている)")
    print("・ガスマス以外の各要素は出現以降残り続ける")
    print("7:戦闘システム")
    print("・敵がいるマスにプレイヤーが入ると戦闘開始")
    print("・敵の強さ分プレイヤーのHPを消費して倒し、その分スタミナが回復")
    print("・プレイヤーのHPが0になるとゲームオーバー")
    print("・ボスは武器がないと倒せない")
    print("8:プレイヤー情報")
    print("・HPは初期値、最大値共に10")
    print("・スタミナは初期値、最大値共に6")
    print(" ——————————————————————————————————————————————————————————————")



def main():
    win_lose=0
    day=0
    board = make_flat_board()
    player=[10,6,0,0,0]
    while True:
        if day==10:
            if player[2]==10:
                print("₋₋₋₋₋₋₋₋₋₋₋₋₋")
                print("| GAME CREAR |")
                print("⁻⁻⁻⁻⁻⁻⁻⁻⁻⁻⁻⁻⁻")
                break
            else:
                print("₋₋₋₋₋₋₋₋₋₋₋₋₋")
                print("| GAME OVER |")
                print("⁻⁻⁻⁻⁻⁻⁻⁻⁻⁻⁻⁻⁻")
                break   
        else:
            day+=1   
            if day==4:
                board_sink(board,4)    
            elif day==7:
                board_sink(board,7)
            elif day==10:
                board_sink(board,10)       
            #スタミナHP回復
            healnum=Heal(player)
            if day>1:
                print("〈日付が変わった〉")
                print("〈HPが"+str(healnum)+"回復した〉")
            player[1]=6
        #ガスマス消去    
        for i in range(25):
            board[i][GAS_MAS] = 0
        put_enemies(board, day, player[4])
        while player[1]>0:
            Displaydangeon(player, board)
            # player[4].to_s)
            print("経過日数"+str(day))
            print("武器の所持"+"〇"*player[3])
            print("資源の所持数"+str(player[2]))
            print("HP"+"♡"*player[0])
            print("残りスタミナ"+"□"*player[1])
            print("A,W,S,D")
            move = input("")
            Move(player,move,board)
            #ガスマス
            if board[player[4]][2]=="G":
                player[0]-=1
            #資材        
            if board[player[4]][5]>0:
                player[2]+=board[player[4]][5]
                board[player[4]][5]=0
            #アイテム    
            if board[player[4]][6] == "W":
                player[3] += 1
                board[player[4]][6] = 0
            #戦闘    
            win_lose = Fight(player, board)
            if player[0]<=0:
                Displaydangeon(player, board)
                print("経過日数"+str(day))
                print("武器の所持"+"〇"*player[3])
                print("資源の所持数"+str(player[2]))
                print("HP"+"♡"*player[0])
                print("残りスタミナ"+"□"*player[1])
                print("₋₋₋₋₋₋₋₋₋₋₋₋₋")
                print("| GAME OVER |")
                print("⁻⁻⁻⁻⁻⁻⁻⁻⁻⁻⁻⁻⁻")
                break
            else:
                pass 
        if player[0]<=0:
            break
        else:
            pass 
    return 0





##########################################
print(" [無人島脱出ゲーム]")
print("1→ルール")
print("2→ゲームスタート")
print("")
select=int(input("1か2を選択して下さい"))
if select==1:
    rule_setumei()
    select=int(input("2を選択して下さい"))

if select==2:
    main()
else:
    pass    
##########################################
