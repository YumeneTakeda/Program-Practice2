# -*- coding: utf-8 -*-
"""
@author: grimbergen
"""
from pydoc import doc
import random
from telnetlib import GA
import numpy as np

# 盤面の大きさ
BOARD_SIZE = 5

# マスの要素
#[ENEMY_VOL,ENEMY_STR,GAS,BOSS_PLACE,SINK,MATTERIAL,WEAPON]
ENEMY_VOL = 0
ENEMY_STR = 1
GAS_MAS = 2
BOSS_PLACE = 3
SINK = 4
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


#ゲームの勝敗確認
winlose = NOT_GAME_END
#経過日数
day = 0

player_status = [0, 0, 0, 0, 0]


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
def without_rand(player_place,day):
    result = random.randint(0, 24)
    #日付によってプレイヤーか沈没マスと被ったらやり直し
    if day >= 4:
        while result == player_place and result in [20,21,22,23,24]:
            result = random.randint(0, 24)
    if day >= 7:
        while result == player_place and result in [4,9,14,20,21,22,23,24]:
            result = random.randint(0, 24)
    if day >= 10:
        while result == player_place and result in [0,1,2,3,4,9,14,20,21,22,23,24]:
            result = random.randint(0, 24)
    #プレイヤーと被ったらやり直し
    while result == player_place:
        result = random.randint(0, 24)
    return result

#敵の配置
def put_enemies(board, day, player_p):
    if day == 5:
        #ボスと資材の配置
        boss_p = without_rand(player_p,day)
        board[boss_p][BOSS_PLACE] = BOSS_IRU
        board[boss_p][MATTERIAL_PLACE] += 1
        #武器をボスと重ならないように配置
        weapon_p = without_rand(player_p,day)
        while weapon_p == boss_p:
            weapon_p = without_rand(player_p,day)
        board[weapon_p][WEAPON] = BUKI_ARU
    else:
        board[without_rand(player_p,day)][MATTERIAL_PLACE] += 1

    #ガスの配置 2回
    print("GAS",GAS)
    board[without_rand(player_p,day)][GAS_MAS] += 1
    board[without_rand(player_p,day)][GAS_MAS] += 1
    #敵2体の配置
    str_2_enemy = without_rand(player_p,day)
    board[str_2_enemy][ENEMY_VOL] += 1
    board[str_2_enemy][ENEMY_STR] += 2
    str_3_enemy = without_rand(player_p,day)
    board[str_3_enemy][ENEMY_VOL] += 1
    board[str_3_enemy][ENEMY_STR] += 3

    print("タイミングの確認")
    print_board(board)

    return board


def board_sink(board, day):
    if day == 4:
        for i in [20, 21, 22, 23, 24]:
            board[i][SINK] = SINK_TRUE
            for youso in [ENEMY_VOL, ENEMY_STR, GAS_MAS, BOSS_PLACE, MATTERIAL_PLACE, WEAPON]:
                if board[i][youso] != 0:
                    board[i-5][youso] = board[i][youso]
                    board[i][youso] = 0

    elif day == 7:
        for i in [4, 9, 14, 19, 24]:
            board[i][SINK] = SINK_TRUE
            for youso in [ENEMY_VOL, ENEMY_STR, GAS, BOSS_PLACE, MATTERIAL_PLACE, WEAPON]:
                if board[i][youso] != 0:
                    board[i-1][youso] = board[i][youso]
                    board[i][youso] = 0
    elif day == 10:
        for i in [0, 1, 2, 3, 4]:
            board[i][SINK] = SINK_TRUE
            for youso in [ENEMY_VOL, ENEMY_STR, GAS, BOSS_PLACE, MATTERIAL_PLACE, WEAPON]:
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
print(Board)



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
    return player



player[4] = 10
Move(player, "D", Board)



BOARD_SIZE=25
win_lose=0
player=[0,0,0,0,0]
board=[[]]


def make_flat_board():
    flat_board = [[0] * 7 for i in range(BOARD_SIZE)]
    return flat_board


def Fight(player,board):
    if board[player[4]][3]==1:
        if player[3]==1:
            #ボス倒し
            print("ボス戦勝利")
            #資材ゲット 
            player[2]=+1 
        else:
            print("ボス戦敗北")  
            win_lose=2  
    if board[player[4]][1]>0:
        if player[0] > board[player[4]][1]:
            print("戦闘に勝利")
            #スタミナ回復
            player[1] = +board[player[4]][1]
        else:
            print("戦闘に敗北") 
            win_lose=2     
        

def Displaydangeon(borad):
    for i in range(5):
        i=i*5
        print(borad[i],borad[i+1],borad[i+2],borad[i+3],borad[i+4])


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
            if i_j_map == player[ZAHYOU]:
                print("p", " ", "|", end="")
            else:
                print(" ", " ", "|", end="")
        print("\n―――――――――――――――――――――――――――――――――――――――――――――")




def main():
    board = make_flat_board()
    player=[10,6,0,0,1]
    print("[ENEMY_VOL,ENEMY_STR,GAS,BOSS_PLACE,SINK,MATTERIAL,WEAPON]")
    while True:
        put_enemies(board, 5, 0)
        while player[1]>0:
            print("player_place ")#player[4].to_s)
            print("A,W,S,D")
            move = input("")
            Move(player,move,board)
            print_board(board)
            Displaydangeon_2(player, board)
    return 0


main()
