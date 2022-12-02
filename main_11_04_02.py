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
SINK_TRUE = 1

BOSS_INAI = 0
BOSS_IRU = 1

SIZAI_NAI = 0
SIZAI_ARU = 1
BUKI_NAI = 0
BUKI_ARU = 1



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
        board[boss_p][BOSS_PLACE] = BOSS_IRU
        board[boss_p][MATTERIAL_PLACE] += 1
        #武器をボスと重ならないように配置
        weapon_p = without_rand(player_p, board)
        while weapon_p == boss_p:
            weapon_p = without_rand(player_p, board)
        board[weapon_p][WEAPON] = BUKI_ARU
    else:
        board[without_rand(player_p, board)][MATTERIAL_PLACE] += 1

    #ガスの配置 2回
    board[without_rand(player_p, board)][GAS_MAS] += 1
    board[without_rand(player_p, board)][GAS_MAS] += 1
    #敵2体の配置
    str_2_enemy = without_rand(player_p, board)
    board[str_2_enemy][ENEMY_VOL] += 1
    board[str_2_enemy][ENEMY_STR] += 2
    str_3_enemy = without_rand(player_p, board)
    board[str_3_enemy][ENEMY_VOL] += 1
    board[str_3_enemy][ENEMY_STR] += 3

    print("タイミングの確認")
    print_board(board)

    return board


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




def Heal(player):
    n = random.randint(3, 5)
    for i in range(n):
        if player[0] >= 10:
            break
        else:
            player[0] += 1
    return player


player[0] = 4
Heal(player)



def Move(player, way, Board):
    zahyou = player[4]
    if zahyou > 24 or zahyou < 0:
        return "正しい座標を入力してください"
    if way == "W":
        if zahyou < 5:
            print("その方向へは進めません")
        elif Board[zahyou - 5][6] == 1:
            print("その方向へは進めません")
        else:
            zahyou -= 5
    elif way == "A":
        if zahyou % 5 == 0:
            print("その方向へは進めません")
        elif Board[zahyou - 1][6] == 1:
            print("その方向へは進めません")
        else:
            zahyou -= 1
    elif way == "S":
        if zahyou > 20:
            print("その方向へは進めません")
        elif Board[zahyou + 5][6] == 1:
            print("その方向へは進めません")
        else:
            zahyou += 5

    elif way == "D":
        if zahyou % 5 == 4:
            print("その方向へは進めません")
        elif zahyou == 24:
            print("その方向へは進めません")
        elif Board[zahyou + 1][6] == 1:
            print("その方向へは進めません")
        else:
            zahyou += 1
    player[4] = zahyou
    player[1]-=1
    return player




BOARD_SIZE=25
win_lose=0


def make_flat_board():
    flat_board = [[0] * 7 for i in range(BOARD_SIZE)]
    return flat_board


def Fight(player,board):
    if board[player[4]][3]==1:
        if player[3]==1:
            #ボス倒し
            print("ボス戦勝利")
            board[player[4]][3] = 0
            board[player[4]][0] = 0
            #資材ゲット 
            player[2]=+1 
        else:
            print("ボス戦敗北")  
            win_lose=2  
    if board[player[4]][1]>0:
        if player[0] > board[player[4]][1]:
            print("戦闘に勝利")
            #スタミナ回復
            player[1] += board[player[4]][1]
            #HP減る
            player[0] -= board[player[4]][1]
            board[player[4]][1]=0
            board[player[4]][0]=0
        else:
            print("戦闘に敗北") 
            win_lose=2     


def Displaydangeon_2(player,board):

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




def main():
    day=0
    board = make_flat_board()
    player=[10,6,0,0,0]
    print("[ENEMY_VOL,ENEMY_STR,GAS,BOSS_PLACE,SINK,MATTERIAL,WEAPON]")
    while True:
        if day==10:
            if win_lose==1:
                print("win")
                break
            else:
                print("lose")
                break   
        else:
            day+=1    
            board_sink(board,day)     
            for i in range(24):
                board[i][GAS_MAS] = 0
            #スタミナHP回復
            player[1]=6    
            Heal(player)
            put_enemies(board, day, player[ZAHYOU])
        while player[1]>0:
            Displaydangeon_2(player, board)
            print("player_place "+str(player[4]),
                  "経過日数"+str(day), "HP"+str(player[0]))
            print("残りスタミナ"+str(player[1]))
            print("A,W,S,D")
            move = input("")
            Move(player,move,board)
            Fight(player,board)
    return 0


main()
