# -*- coding: utf-8 -*-
"""
@author: grimbergen
"""
import random
import numpy as np

# 盤面の大きさ
BOARD_SIZE = 5

# マスの要素
#[ENEMY_VOL,ENEMY_STR,GAS,BOSS_PLACE,SINK,MATTERIAL,WEAPON]
ENEMY_VOL = 0
ENEMY_STR = 1
GAS = 2
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

#プレイヤーのステータス
MAX_HP = 10
MAX_SP = 6
HAVE_MATT = 0
HAVE_MATT_TRUE = 1
HAVE_WEAPON = 0
HAVE_WEAPON_TRUE = 1
PLAYER_PLACE = 0


#ゲームの勝敗確認
winlose = NOT_GAME_END
#経過日数
day = 0

player_status = [MAX_HP,MAX_SP,HAVE_MATT,HAVE_WEAPON,PLAYER_PLACE]

def make_flat_board():
    flat_board = [[0] * 7 for i in range(BOARD_SIZE) for j in range(BOARD_SIZE)]
    return flat_board

def print_board(board):
    print()
    i = 1
    for line in board:
        print(line,end="")
        if i%5==0:
            print()
        i = i+1


def without_p_rand(player_place):
    result = random.randint(0,24)

    while result == player_place:
        result = random.randint(0,24)
    return result

#敵の配置
def put_enemies(board,day,player_p):
    
    if day == 5:
        #ボスと資材の配置
        boss_p = without_p_rand(player_p)
        board[boss_p][BOSS_PLACE] = BOSS_IRU
        board[boss_p][MATTERIAL_PLACE] += 1
        #武器をボスと重ならないように配置
        weapon_p = without_p_rand(player_p)
        while weapon_p == boss_p:
            weapon_p = without_p_rand(player_p)
        board[weapon_p][WEAPON] = BUKI_ARU
    else:
        board[without_p_rand(player_p)][MATTERIAL_PLACE] += 1

    
    #ガスの配置 2回
    board[without_p_rand(player_p)][GAS] += 1  
    board[without_p_rand(player_p)][GAS] += 1
    #敵2体の配置
    str_2_enemy = without_p_rand(player_p)
    str_3_enemy = without_p_rand(player_p)
    board[str_2_enemy][ENEMY_VOL] += 1  
    board[str_2_enemy][ENEMY_STR] += 2
    board[str_3_enemy][ENEMY_VOL] += 1  
    board[str_3_enemy][ENEMY_STR] += 3

    return board

def board_sink(board,day):
    if day == 4:
        for i in [20,21,22,23,24]:
            board[i][SINK] = SINK_TRUE
            for youso in [ENEMY_VOL,ENEMY_STR,GAS,BOSS_PLACE,MATTERIAL_PLACE,WEAPON]:
                if board[i][youso] != 0:
                    board[i-5][youso] = board[i][youso]
                    board[i][youso] = 0
        
    elif day == 7:
        for i in [4,9,14,19,24]:
            board[i][SINK] = SINK_TRUE
            for youso in [ENEMY_VOL,ENEMY_STR,GAS,BOSS_PLACE,MATTERIAL_PLACE,WEAPON]:
                if board[i][youso] != 0:
                    board[i-1][youso] = board[i][youso]
                    board[i][youso] = 0
    elif day == 10:
        for i in [0,1,2,3,4]:
            board[i][SINK] = SINK_TRUE
            for youso in [ENEMY_VOL,ENEMY_STR,GAS,BOSS_PLACE,MATTERIAL_PLACE,WEAPON]:
                if board[i][youso] != 0:
                    board[i+5][youso] = board[i][youso]
                    board[i][youso] = 0
    return board

def main():
    board = make_flat_board()
    day = 4
    print("[ENEMY_VOL,ENEMY_STR,GAS,BOSS_PLACE,SINK,MATTERIAL,WEAPON]")
    put_enemies(board,day,0)
    print_board(board)

    board_sink(board,4)
    board_sink(board,7)
    board_sink(board,10)

    print_board(board)

    return 0

main()

