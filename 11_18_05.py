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
#YUMETYAN
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

#YU-DAI
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

#SONOBE
#色
IRO_USIRO = '\033[0m'
BLACK = '\033[30m'  # (文字)黒
RED = '\033[31m'  # (文字)赤
GREEN = '\033[32m'  # (文字)緑
YELLOW = '\033[33m'  # (文字)黄
BLUE = '\033[34m'  # (文字)青
MAGENTA = '\033[35m'  # (文字)マゼンタ
CYAN = '\033[36m'  # (文字)シアン
WHITE = '\033[37m'  # (文字)白
BOLD = '\033[1m'  # 太字
UNDERLINE = '\033[4m'  # 下線
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


def hit_check(player,board):
    #ガスマス
    if board[player[4]][2] == '\033[31m'+'G'+'\033[0m':
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
        while board[put_gas][GAS_MAS] == '\033[31m'+'G'+'\033[0m':
            put_gas = without_rand(player_p, board)
        board[put_gas][GAS_MAS] = '\033[31m'+'G'+'\033[0m'
    #敵2体の配置
    str_2_enemy = without_rand(player_p, board)
    while board[str_2_enemy][ENEMY_VOL] >= 2:
            str_2_enemy = without_rand(player_p, board)
    board[str_2_enemy][ENEMY_VOL] += 1
    board[str_2_enemy][ENEMY_STR] += 2
    str_3_enemy = without_rand(player_p, board)
    while board[str_3_enemy][ENEMY_VOL] >= 2:
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
            for youso in [ENEMY_VOL, ENEMY_STR, BOSS_PLACE, MATTERIAL_PLACE, WEAPON]:
                if board[i][youso] != 0:
                    if board[i][youso] == SINK_TRUE or board[i][youso] == BOSS_IRU or board[i][youso] == BUKI_ARU:
                        board[i-5][youso] = board[i][youso]
                        board[i][youso] = 0
                    else:
                        board[i-5][youso] += board[i][youso]
                        board[i][youso] = 0

    elif day == 6:
        for i in [4, 9, 14, 19, 24]:
            board[i][SINK_PLACE] = SINK_TRUE
            for youso in [ENEMY_VOL, ENEMY_STR, BOSS_PLACE, MATTERIAL_PLACE, WEAPON]:
                if board[i][youso] != 0:
                    if board[i][youso] == SINK_TRUE or board[i][youso] == BOSS_IRU or board[i][youso] == BUKI_ARU:
                        board[i-1][youso] = board[i][youso]
                        board[i][youso] = 0
                    else:
                        board[i-1][youso] += board[i][youso]
                        board[i][youso] = 0
    elif day == 8:
        for i in [0, 1, 2, 3, 4]:
            board[i][SINK_PLACE] = SINK_TRUE
            for youso in [ENEMY_VOL, ENEMY_STR, BOSS_PLACE, MATTERIAL_PLACE, WEAPON]:
                if board[i][youso] != 0:
                    if board[i][youso] == SINK_TRUE or board[i][youso] == BOSS_IRU or board[i][youso] == BUKI_ARU:
                        board[i+5][youso] = board[i][youso]
                        board[i][youso] = 0
                    else:
                        board[i+5][youso] += board[i][youso]
                        board[i][youso] = 0
    elif day == 10:
        for i in [0, 5, 10, 15, 20]:
            board[i][SINK_PLACE] = SINK_TRUE
            for youso in [ENEMY_VOL, ENEMY_STR, BOSS_PLACE, MATTERIAL_PLACE, WEAPON]:
                if board[i][youso] != 0:
                    if board[i][youso] == SINK_TRUE or board[i][youso] == BOSS_IRU or board[i][youso] == BUKI_ARU:
                        board[i+1][youso] = board[i][youso]
                        board[i][youso] = 0
                    else:
                        board[i+1][youso] += board[i][youso]
                        board[i][youso] = 0
    hit_check(player,board)
    return board


#HP回復
def Heal(player):
    n = random.randint(1, 3)
    j = 0
    for i in range(n):
        if player[0] >= 10:
            break
        else:
            player[0] += 1
            j+=1
    return j

#移動
def Move(player, way, Board):
    zahyou = player[4]
    if zahyou > 24 or zahyou < 0:
        return "正しい座標を入力してください"
    if way == "W" or way == "w":
        if zahyou < 5:
            print("その方向へは進めません")
        elif Board[zahyou - 5][4] == "×":
            print("その方向へは進めません")
        else:
            zahyou -= 5
            player[1] -= 1
    elif way == "A" or way == "a":
        if zahyou % 5 == 0:
            print("その方向へは進めません")
        elif Board[zahyou - 1][4] == "×":
            print("その方向へは進めません")
        else:
            zahyou -= 1
            player[1] -= 1
    elif way == "S" or way == "s":
        if zahyou >= 20:
            print("その方向へは進めません")
        elif Board[zahyou + 5][4] == "×":
            print("その方向へは進めません")
        else:
            zahyou += 5
            player[1] -= 1
    elif way == "D" or way == "d":
        if zahyou % 5 == 4:
            print("その方向へは進めません")
        elif zahyou == 24:
            print("その方向へは進めません")
        elif Board[zahyou + 1][4] == "×":
            print("その方向へは進めません")
        else:
            zahyou += 1
            player[1] -= 1
    elif way=="END" or way == "end":
        player[1]=0   
    elif way=="HELP" or way == "help":
        print("")
        print(" ————————————————————————ルール説明—————————————————————————————")
        print(""+UNDERLINE+"1"+IRO_USIRO+":10日経過するまでに10個の資材を集めて船を完成させましょう       ")
        print("・資材を10個集め、10日間生き残れたら脱出成功")
        print("・資材を10個集められずに10日経過してしまうと、島が沈んでしまう ")
        print(""+UNDERLINE+"2"+IRO_USIRO+":プレイヤー情報")
        print("・HPは初期値、最大値共に10")
        print("・スタミナは初期値、最大値共に6")
        print("・初期位置は左上で表示は[P]")
        print(""+UNDERLINE+"3"+IRO_USIRO+":Wで北、Aで西、Sで南、Dで東方向に移動可能")
        print("・スタミナを1消費して1マス移動")
        print(""+UNDERLINE+"4"+IRO_USIRO+":1マスの構造は7つの要素から成り立つ3×3のマスである")
        print("| "+GREEN+'W'+IRO_USIRO+" "+BLUE+'3'+IRO_USIRO+" "+RED+'G'+IRO_USIRO+
        " |・左から敵の"+BLUE+"数"+IRO_USIRO+"、敵の"+BLUE+"強さ"+IRO_USIRO+"、ガスの有無" +"("+RED+'G'+IRO_USIRO+")")
        print("| "+MAGENTA+'B'+IRO_USIRO+" × "+YELLOW+'1'+IRO_USIRO +
        " |・左からボスの有無("+MAGENTA+'B'+IRO_USIRO+")、沈没済か(×)、資材の"+YELLOW+"数"+IRO_USIRO+"")
        print("|       |・武器の有無("+GREEN+'W'+IRO_USIRO+")")
        print("(これはゲーム中でもHELPと入力すると表示される)")
        print(""+UNDERLINE+"5"+IRO_USIRO+":日数経過")
        print("・スタミナが0になるか、ENDと入力すると一日が経過")
        print("・一日経過するとスタミナが全回復し、HPが3~5ランダムな値回復")
        print("・日数経過につれ島がどんどん沈んでいく(南、東、北、西の順)")
        print(""+UNDERLINE+"6"+IRO_USIRO+":各要素")
        print("・ガスマスを通るとHPが1減る")
        print("・5日目にボスと武器が出現(5日目の資源はボスが持っている)")
        print("・ガスマス以外の各要素は出現以降残り続ける")
        print(""+UNDERLINE+"7"+IRO_USIRO+":戦闘システム")
        print("・敵の強さ分プレイヤーのHPを消費して倒し、その分スタミナが回復")
        print("・プレイヤーのHPが0になるとゲームオーバー")
        print("・ボスは武器がないと倒せない")
        print("・武器があればノーダメージで倒せる")
        print(" ——————————————————————————————————————————————————————————————")
        stop=input("ゲームに戻る場合はEnterキー")
        if Board[player[4]][2] == '\033[31m'+'G'+'\033[0m':
            player[0] += 1
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
def Displaydangeon(player,board,sink,day):
    print("\n―――――――――――――――――――――――――――――――――――――――――――――")
    for j in range(5):
        for i in range(5):
            i_j_map = j*5+i
            print("| ",end="")

            if board[i_j_map][WEAPON] == 0:
                print("  ",end="")
            else:
                print(GREEN+str(board[i_j_map][WEAPON])+IRO_USIRO,"",end="")

            if board[i_j_map][1] == 0:
                print("  ",end="")
            else :
                print(BLUE+str(board[i_j_map][1])+IRO_USIRO,end=" ")
            
            if board[i_j_map][2] == 0:
                print("  |",end="")
            else :
                print(YELLOW+str(board[i_j_map][2])+IRO_USIRO,"|",end="")
        print()

        for i in range(5):
            i_j_map = j*5+i
            print("| ",end="")
            if board[i_j_map][3] == 0:
                print("  ",end="")
            else:
                print(MAGENTA+str(board[i_j_map][3])+IRO_USIRO,"",end="")

            if board[i_j_map][4] == 0:
                print("  ",end="")
            else:
                print(board[i_j_map][4],"",end="")

            if board[i_j_map][5] == 0:
                print("  |",end="")
            else:
                print(YELLOW+str(board[i_j_map][5])+IRO_USIRO,"|",end="")
        print()
        for i in range(5):
            i_j_map = j*5+i
            print("| ",end="")
            print("  ",end="")


            #print("|", board[i_j_map][6],end=" ") 
            if i_j_map == player[4]:
                print("P", " ", "|", end="")
            else:
                print(" ", " ", "|", end="")
        print("\n―――――――――――――――――――――――――――――――――――――――――――――")
    print("経過日数 "+str(day)+"日目 (10日で終了)")
    print("武器の所持"+"〇"*player[3])
    print("資源の所持数"+str(player[2]))
    print("HP"+"♡"*player[0]+"("+str(player[0])+")")
    print("残りスタミナ"+"□"*player[1]+"("+str(player[1])+")")
    print("A,W,S,D,END or HELP")
    if sink == 1 and (player[4] == 20 or player[4] == 21 or player[4] == 22 or player[4] == 23 or player[4] == 24):
        print("#島に戻ってください#")
    if sink == 2 and (player[4] == 4 or player[4] == 9 or player[4] == 14 or player[4] == 19 or player[4] == 24):
        print("#島に戻ってください#")
    if sink == 3 and (player[4] == 0 or player[4] == 1 or player[4] == 2 or player[4] == 3 or player[4] == 4):
        print("#島に戻ってください#")
    if sink == 4 and (player[4] == 0 or player[4] == 5 or player[4] == 10 or player[4] == 15 or player[4] == 20):
        print("#島に戻ってください#")

#ルール説明
def rule_setumei():
    print("")
    print(" ————————————————————————ルール説明—————————————————————————————")
    print(""+UNDERLINE+"1"+IRO_USIRO+":10日経過するまでに10個の資材を集めて船を完成させましょう       ")
    print("・資材を10個集め、10日間生き残れたら脱出成功")
    print("・資材を10個集められずに10日経過してしまうと、島が沈んでしまう ")
    print(""+UNDERLINE+"2"+IRO_USIRO+":プレイヤー情報")
    print("・HPは初期値、最大値共に10")
    print("・スタミナは初期値、最大値共に6")
    print("・初期位置は左上で表示は[P]")
    print(""+UNDERLINE+"3"+IRO_USIRO+":Wで北、Aで西、Sで南、Dで東方向に移動可能")
    print("・スタミナを1消費して1マス移動")
    print(""+UNDERLINE+"4"+IRO_USIRO+":1マスの構造は7つの要素から成り立つ3×3のマスである")
    print("| "+GREEN+'W'+IRO_USIRO+" "+BLUE+'3'+IRO_USIRO+" "+RED+'G'+IRO_USIRO+
        " |・左から敵の"+BLUE+"数"+IRO_USIRO+"、敵の"+BLUE+"強さ"+IRO_USIRO+"、ガスの有無" +"("+RED+'G'+IRO_USIRO+")")
    print("| "+MAGENTA+'B'+IRO_USIRO+" × "+YELLOW+'1'+IRO_USIRO +
        " |・左からボスの有無("+MAGENTA+'B'+IRO_USIRO+")、沈没済か(×)、資材の"+YELLOW+"数"+IRO_USIRO+"")
    print("|       |・武器の有無("+GREEN+'W'+IRO_USIRO+")")
    print("(これはゲーム中でもHELPと入力すると表示される)")
    print(""+UNDERLINE+"5"+IRO_USIRO+":日数経過")
    print("・スタミナが0になるか、ENDと入力すると一日が経過")
    print("・一日経過するとスタミナが全回復し、HPが2~4ランダムな値回復")
    print("・日数経過につれ島がどんどん沈んでいく(南、東、北、西の順)")
    print(""+UNDERLINE+"6"+IRO_USIRO+":各要素")
    print("・ガスマスを通るとHPが1減る")
    print("・5日目にボスと武器が出現(5日目の資源はボスが持っている)")
    print("・ガスマス以外の各要素は出現以降残り続ける")
    print(""+UNDERLINE+"7"+IRO_USIRO+":戦闘システム")
    print("・敵の強さ分プレイヤーのHPを消費して倒し、その分スタミナが回復")
    print("・プレイヤーのHPが0になるとゲームオーバー")
    print("・ボスは武器がないと倒せない")
    print(" ——————————————————————————————————————————————————————————————")



def main():
    day=0
    board = make_flat_board()
    player=[10,6,0,0,0]
    sink=0
    while True:
        if day==10:
            if player[2]==10:
                #print("₋₋₋₋₋₋₋₋₋₋₋₋₋₋")
                #print("| "+YELLOW+"GAME CLEAR"+IRO_USIRO+" |")
                #print("⁻⁻⁻⁻⁻⁻⁻⁻⁻⁻⁻⁻⁻⁻")
                print(" _______  _______  __   __  _______  _______  ___      _______  _______  ______")
                print("|       ||   _   ||  |_|  ||       ||       ||   |    |       ||   _   ||    _ |")
                print("|    ___||  | |  ||       ||    ___||       ||   |    |    ___||  | |  ||   | ||")
                print("|   | __ |  |_|  ||       ||   |___ |       ||   |    |   |___ |  |_|  ||   |_||")
                print("|   ||  ||       ||       ||    ___||      _||   |___ |    ___||       ||    __ |")
                print("|   |_| ||   _   || ||_|| ||   |___ |     |_ |       ||   |___ |   _   ||   |  ||")
                print("|_______||__| |__||_|   |_||_______||_______||_______||_______||__| |__||___|  ||")
                break
            else:
                #print("₋₋₋₋₋₋₋₋₋₋₋₋₋")
                #print("| "+RED+"GAME OVER"+IRO_USIRO+" |")
                #print("⁻⁻⁻⁻⁻⁻⁻⁻⁻⁻⁻⁻⁻")
                print(" _______  _______  __   __  _______  _______  __   __  _______  ______")
                print("|       ||   _   ||  |_|  ||       ||       ||  | |  ||       ||    _ |")
                print("|    ___||  | |  ||       ||    ___||   _   ||  |_|  ||    ___||   | ||")
                print("|   | __ |  |_|  ||       ||   |___ |  | |  ||       ||   |___ |   |_||")
                print("|   ||  ||       ||       ||    ___||  |_|  ||       ||    ___||    __ |")
                print("|   |_| ||   _   || ||_|| ||   |___ |       | |     | |   |___ |   |  ||")
                print("|_______||__| |__||_|   |_||_______||_______|  |___|  |_______||___|  ||")
                break   
        else:
            day+=1   
            if day==4:
                board_sink(board,4)   
                sink=1 
            elif day==5:
                print("〈[BOSS](B)が出現しました。[WEAPON](W)を入手し、倒せ。〉")
            elif day == 6:
                board_sink(board, 6)
                sink=2
            elif day==8:
                board_sink(board,8)
                sink=3
            elif day==10:
                board_sink(board,10)
                sink=4       
            #スタミナHP回復
            healnum=Heal(player)
            hit_check(player,board)
            if day>1:
                print("〈日付が変わった〉")
                print("〈HPが"+str(healnum)+"回復した〉")
            player[1]=6
        #ガスマス消去    
        for i in range(25):
            board[i][GAS_MAS] = 0
        put_enemies(board, day, player[4])
        while player[1]>0:
            Displaydangeon(player, board,sink,day)
            move = input("")
            Move(player,move,board)
            #オブジェクトと接触したときの処理
            hit_check(player,board)
            if player[0]<=0:
                Displaydangeon(player, board,sink,day)
                #print("₋₋₋₋₋₋₋₋₋₋₋₋₋")
                #print("| "+RED+"GAME OVER"+IRO_USIRO+" |")
                #print("⁻⁻⁻⁻⁻⁻⁻⁻⁻⁻⁻⁻⁻")
                print(" _______  _______  __   __  _______  _______  __   __  _______  ______")
                print("|       ||   _   ||  |_|  ||       ||       ||  | |  ||       ||    _ |")
                print("|    ___||  | |  ||       ||    ___||   _   ||  |_|  ||    ___||   | ||")
                print("|   | __ |  |_|  ||       ||   |___ |  | |  ||       ||   |___ |   |_||")
                print("|   ||  ||       ||       ||    ___||  |_|  ||       ||    ___||    __ |")
                print("|   |_| ||   _   || ||_|| ||   |___ |       | |     | |   |___ |   |  ||")
                print("|_______||__| |__||_|   |_||_______||_______|  |___|  |_______||___|  ||")
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
