# -*- coding: utf-8 -*-
"""
Created on Wed Sep 15 21:14:42 2021

@author: grimb
"""
from random import randint

class Dungeonroom:
    def __init__(self):
        self.has_stinker = NO_STINKER		# Stinkerがいる
        self.has_superstinker = False	# Super Stinkerがいる
        self.has_prince = False			# プリンスがいる
        self.prince_visited = False		# 部屋にプリンスが訪問したか
        self.door_info = {NORTH: NO_DOOR, 
                          SOUTH: NO_DOOR, 
                          WEST: NO_DOOR, 
                          EAST: NO_DOOR} # ドアの情報
        self.stinker_smell = False		# Stinkerの匂いの情報
        self.superstinker_smell = False	# Super Stinkerの匂いの情報
        self.has_sword = False			# 刀がある
        self.has_potion = False		    # 健康ポーションがある

class Hero:
    def __init__(self):
        self.room_x = 0			# プリンスがいる部屋のX軸
        self.room_y = 0			# プリンスがいる部屋のY軸
        self.has_sword = False	# 刀を持っているか
        self.key_no = 0		    # キーの数
        self.hit_points = 0     # プリンスのＨＰ

# Stinkerの区別
NO_STINKER = 0
STINKER1 = 1
STINKER2 = 2

# プリンスとStinkerの最大ＨＰ
PRINCE_MAX_HP = 20
STINKER_MAX_HP = 25
SUPERSTINKER_MAX_HP = 30

# ドアの状況
NO_DOOR = 0
OPEN_DOOR = 1
LOCKED_DOOR = 2

# 方向
NORTH = 0
SOUTH = 1
WEST = 2
EAST = 3

# ダンジョンの大きさ
DUNGEON_X = 5
DUNGEON_Y = 5

# 攻撃のダメージを決めるパラメター
PRINCE_ATTACK_RANGE = 8
SWORD_DAMAGE_RATIO = 3
STINKER_ATTACK_RANGE = 11
SUPER_STINKER_ATTACK_RANGE = 12

# 戦闘の結果
NO_BATTLE = 0
PRINCE_DEAD = 1
STINKER_DEAD = 2
PRINCESS_RESCUED = 3

# ダンジョンの初期化
def init_dungeon():
    dungeon = [[0]*DUNGEON_Y for i in range(DUNGEON_X)]
    for x in range(DUNGEON_Y):
        for y in range(DUNGEON_X):
            dungeon[x][y] = Dungeonroom()
	# プリンスは最初(0,0)の部屋にいる
    dungeon[0][0].has_prince = True
	# プリンスは(0,0)の部屋を訪問している
    dungeon[0][0].prince_visited = True
	# Stinker1は(1,4)の部屋にいる
    dungeon[1][4].has_stinker = STINKER1
	# Stinker1の匂いの情報を隣の部屋に追加
    dungeon[0][4].stinker_smell = True
    dungeon[2][4].stinker_smell = True
    dungeon[1][3].stinker_smell = True
	# Stinker2は(2,1)の部屋にいる
    dungeon[2][1].has_stinker = STINKER2
	# Stinker2の匂いの情報を隣の部屋に追加
    dungeon[1][1].stinker_smell = True
    dungeon[3][1].stinker_smell = True
    dungeon[2][2].stinker_smell = True
    dungeon[2][0].stinker_smell = True
	# Super Stinkerは(3,3)の部屋にいる
    dungeon[3][3].has_superstinker = True
	# Super Stinkerの匂いの情報を隣の部屋に追加
    dungeon[2][3].superstinker_smell = True
    dungeon[4][3].superstinker_smell = True
    dungeon[3][2].superstinker_smell = True
    dungeon[3][4].superstinker_smell = True
	# 刀は(0,3)の部屋にある
    dungeon[0][3].has_sword = True
	# 健康ポーションは(4,2)と(2,4)の部屋にある
    dungeon[4][2].has_potion = True
    dungeon[2][4].has_potion = True

	# ドアの情報

	# 1列目のドア情報
    dungeon[0][0].door_info[EAST] = OPEN_DOOR
    dungeon[0][0].door_info[SOUTH] = OPEN_DOOR

    dungeon[1][0].door_info[EAST] = OPEN_DOOR
    dungeon[1][0].door_info[SOUTH] = OPEN_DOOR
    dungeon[1][0].door_info[WEST] = OPEN_DOOR
    dungeon[2][0].door_info[EAST] = OPEN_DOOR
    dungeon[2][0].door_info[SOUTH] = OPEN_DOOR
    dungeon[2][0].door_info[WEST] = OPEN_DOOR
    dungeon[3][0].door_info[EAST] = OPEN_DOOR
    dungeon[3][0].door_info[SOUTH] = OPEN_DOOR
    dungeon[3][0].door_info[WEST] = OPEN_DOOR
    
    dungeon[4][0].door_info[SOUTH] = OPEN_DOOR
    dungeon[4][0].door_info[WEST] = OPEN_DOOR

	# 2列目から4列目までの情報は同じのでforループで初期化
    for y in range(1, 4):
        dungeon[0][y].door_info[NORTH] = OPEN_DOOR
        dungeon[0][y].door_info[EAST] = OPEN_DOOR
        dungeon[0][y].door_info[SOUTH] = OPEN_DOOR

        dungeon[1][y].door_info[NORTH] = OPEN_DOOR
        dungeon[1][y].door_info[EAST] = OPEN_DOOR
        dungeon[1][y].door_info[SOUTH] = OPEN_DOOR
        dungeon[1][y].door_info[WEST] = OPEN_DOOR
        dungeon[2][y].door_info[NORTH] = OPEN_DOOR
        dungeon[2][y].door_info[EAST] = OPEN_DOOR
        dungeon[2][y].door_info[SOUTH] = OPEN_DOOR
        dungeon[2][y].door_info[WEST] = OPEN_DOOR
        dungeon[3][y].door_info[NORTH] = OPEN_DOOR
        dungeon[3][y].door_info[EAST] = OPEN_DOOR
        dungeon[3][y].door_info[SOUTH] = OPEN_DOOR
        dungeon[3][y].door_info[WEST] = OPEN_DOOR

        dungeon[4][y].door_info[NORTH] = OPEN_DOOR
        dungeon[4][y].door_info[SOUTH] = OPEN_DOOR
        dungeon[4][y].door_info[WEST] = OPEN_DOOR
        
	# 5列目のドア情報
    dungeon[0][4].door_info[NORTH] = OPEN_DOOR
    dungeon[0][4].door_info[EAST] = OPEN_DOOR

    dungeon[1][4].door_info[NORTH] = OPEN_DOOR
    dungeon[1][4].door_info[EAST] = OPEN_DOOR
    dungeon[1][4].door_info[WEST] = OPEN_DOOR
    dungeon[2][4].door_info[NORTH] = OPEN_DOOR
    dungeon[2][4].door_info[EAST] = OPEN_DOOR
    dungeon[2][4].door_info[WEST] = OPEN_DOOR
    dungeon[3][4].door_info[NORTH] = OPEN_DOOR
    dungeon[3][4].door_info[EAST] = OPEN_DOOR
    dungeon[3][4].door_info[WEST] = OPEN_DOOR

    dungeon[4][4].door_info[NORTH] = OPEN_DOOR
    dungeon[4][4].door_info[WEST] = OPEN_DOOR

	# ドアがないところの情報を修正
    dungeon[3][3].door_info[NORTH] =  NO_DOOR
    dungeon[3][3].door_info[SOUTH] =  NO_DOOR
    dungeon[3][3].door_info[WEST] =  NO_DOOR
    dungeon[3][2].door_info[SOUTH] =  NO_DOOR
    dungeon[3][4].door_info[NORTH] =  NO_DOOR
    dungeon[2][3].door_info[EAST] =  NO_DOOR
	# ロックされているドアの情報を修正
    dungeon[3][3].door_info[EAST] =  LOCKED_DOOR
    dungeon[4][3].door_info[WEST] =  LOCKED_DOOR
    
    return dungeon

# プリンスの情報を初期化
def init_prince():
    prince = Hero()
    prince.room_x = 0
    prince.room_y = 0
    prince.hit_points = PRINCE_MAX_HP
    return prince

# ゲームの説明を出力
def print_game_explanation():
    print("*"*40)
    print("*" + ' '*38 + "*")
    print("*" + ' '*5 + "Welcome to Stinkin' Dungeon" + ' '*6 + "*")
    print("*" + ' '*38 + "*")
    print("*" + ' '*7 + "A simple text-based RPG" + ' '*8 + "*")
    print("*" + ' '*38 + "*")
    print("*" + ' '*7 + "Design: Reijer Grimbergen" + ' '*6 + "*")
    print("*" + ' '*38 + "*")
    print("*"*40)

    print("\n")
    print("1) Show the rules of the game")
    print("2) Start the game")
    selection = int(input("Please enter your selection: "))
    if selection == 1:
        print("Rules of Stinkin' Dungeon:")
        print("==========================")
        print("1) You are a prince and in room (1,1) of the Dungeon of the Stinkers.")
        print("2) Somewhere in this dungeon there is a princess that you must rescue from the Stinkers.")
        print("3) There are two Stinkers and one Super Stinker in this dungeon.")
        print("4) When you enter a room with a Stinker, you must fight him.")
        print("5) When fighting a Stinker, your hit points will go down.")
        print("6) To improve your chances of beating a Stinker, you need a sword that is somewhere in the dungeon.")
        print("7) If you survive a Stinker fight, you can restore your health by drinking an health potion that is somewhere in the dungeon.")
        print("8) You cannot carry a health potion with you. If you want to use it you must go back to the room you found it.")
        print("9) The princess is in the room with the Super Stinker.")
        print("10) To enter the room with the Super Stinker you need two keys.")
        print("11) Each Stinker holds one of the keys. If you defeat a Stinker, you will get the key he carries.")
        print("12) Each room has a number of doors through which you can go to get to the other rooms.")
        print("13) Only by visiting a room, you will get access to the information about this room.")
        print("14) The Stinkers smell so bad that you can smell them in the neighboring room.")
        input("Press any key to start the game.\n")
    print("Good luck with your quest to save the princess!")
    
# ダンジョンを表示
def show_dungeon():
    # 部屋を一つずつ表示す
    for y in range(DUNGEON_Y):
        # 1列目：北ドア
        outputstr = ""
        for x in range(DUNGEON_X):
            if dungeon[x][y].prince_visited:
                outputstr += print_door_info(dungeon[x][y].door_info[NORTH])
            else:
                outputstr += ' '*7
        print(outputstr)
        # 2列目：見やすくするための空きスペース
        outputstr = ""
        for x in range(DUNGEON_X):
            if dungeon[x][y].prince_visited:
                outputstr += "*" + ' '*5 + "*"
            else:
                outputstr += ' '*7
        print(outputstr)
        # 3列目：匂い
        outputstr = ""
        for x in range(DUNGEON_X):
            if dungeon[x][y].prince_visited:
                if dungeon[x][y].stinker_smell:
                    outputstr += "*" + ' '*2 + "&" + ' '*2 + "*"
                elif dungeon[x][y].superstinker_smell:
                    outputstr += "*" + ' '*2 + "#" + ' '*2 + "*"
                else:
                    outputstr += "*" + ' '*5 + "*"
            else:
                outputstr += ' '*7
        print(outputstr)
        # 4列目：西ドア、プリンスとStinker、東ドア
        outputstr = ""
        for x in range(DUNGEON_X):
            if dungeon[x][y].prince_visited:
                if dungeon[x][y].door_info[WEST] == NO_DOOR:
                    outputstr += "* "
                elif dungeon[x][y].door_info[WEST] == OPEN_DOOR:
                    outputstr += "D "
                elif dungeon[x][y].door_info[WEST] == LOCKED_DOOR:
                    outputstr += "L "
                if dungeon[x][y].has_prince:
                    if prince.has_sword:
                        outputstr += "P!"
                    else:
                        outputstr += "P "
                else:
                    outputstr += "  "
                if dungeon[x][y].has_stinker != NO_STINKER:
                    outputstr += "S "
                elif dungeon[x][y].has_superstinker:
                    outputstr += "$ "
                else:
                    outputstr += "  "
                if dungeon[x][y].door_info[EAST] == NO_DOOR:
                    outputstr += "*"
                elif dungeon[x][y].door_info[EAST] == OPEN_DOOR:
                    outputstr += "D"
                elif dungeon[x][y].door_info[EAST] == LOCKED_DOOR:
                    outputstr += "L"
            else:
                outputstr += ' '*7
        print(outputstr)
        # 5列目：刀と健康ポーション
        outputstr = ""
        for x in range(DUNGEON_X):
            if dungeon[x][y].prince_visited:
                if dungeon[x][y].has_sword:
                    outputstr += "* K "
                else:
                    outputstr += "*   "
                if dungeon[x][y].has_potion:
                    outputstr += "H *"
                else:
                    outputstr += "  *"
            else:
                outputstr += ' '*7
        print(outputstr)
        # 6列目：南ドア
        outputstr = ""
        for x in range(DUNGEON_X):
            if dungeon[x][y].prince_visited:
                outputstr += print_door_info(dungeon[x][y].door_info[SOUTH])
            else:
                outputstr += ' '*7
        print(outputstr)
        
    # 記号の説明
    print("P = Prince, S = Stinker, $ = Super Stinker")
    print("& = Stinker smell, # = Super Stinker smell")
    print("K = Sword, P! = Prince has sword, H = Health potion")
    print("D = Open Door, L = Locked door, * = Wall")
    
    # プリンスの健康状況を表示
    print(f"Prince HP: {prince.hit_points}")
            
# ドア情報を表示
def print_door_info(door):
    if door == NO_DOOR:
        return "*"*7    
    elif door == OPEN_DOOR:
       return "*"*3+"D"+"*"*3
    elif door == LOCKED_DOOR:
       return "*"*3+"L"+"*"*3
    return ""

# プリンスがいる部屋の情報を表示
def show_room_info(x, y):
    if(dungeon[x][y].has_stinker != NO_STINKER):
        print("There is a Stinker in this room")
    if(dungeon[x][y].has_superstinker):
        print("There is a Super Stinker in this room")
    if(dungeon[x][y].has_sword):
        print("There is a sword in this room")
    if(dungeon[x][y].has_potion):
        print("There is a health potion in this room")
    if(dungeon[x][y].stinker_smell):
        print("There is a bad smell in this room")
    elif(dungeon[x][y].superstinker_smell):
        print("There is a very foul stench in this room")
    else:
        print("There is no smell in this room")
    print(f"Number of keys: {prince.key_no}")
    if(dungeon[x][y].door_info[NORTH] == OPEN_DOOR):
        print("There is a door to the North")
    elif(dungeon[x][y].door_info[NORTH] == LOCKED_DOOR):
        print("There is a locked door to the North")
    if(dungeon[x][y].door_info[SOUTH] == OPEN_DOOR):
        print("There is a door to the South")
    elif(dungeon[x][y].door_info[SOUTH] == LOCKED_DOOR):
        print("There is a locked door to the South")
    if(dungeon[x][y].door_info[WEST] == OPEN_DOOR):
        print("There is a door to the West")
    elif(dungeon[x][y].door_info[WEST] == LOCKED_DOOR):
        print("There is a locked door to the West")
    if(dungeon[x][y].door_info[EAST] == OPEN_DOOR):
        print("There is a door to the East")
    elif(dungeon[x][y].door_info[EAST] == LOCKED_DOOR):
        print("There is a locked door to the East")
        
#　プレイヤーから移動方向の入力
def get_player_move(x, y):
    while True:
        input_dir = input("Enter door direction (N,S,W,E):")
        if input_dir == 'N' and check_door_status(x, y, NORTH) != -1:
            return NORTH
        elif input_dir == 'S' and check_door_status(x, y, SOUTH) != -1:
            return SOUTH
        elif input_dir == 'W' and check_door_status(x, y, WEST) != -1:
            return WEST
        elif input_dir == 'E' and check_door_status(x, y, EAST) != -1:
            return EAST
    return -1

# プレイヤーが行きたい方向のドア情況を確認
def check_door_status(x, y, player_dir):
    if dungeon[x][y].door_info[player_dir] == OPEN_DOOR:
        return player_dir
    elif dungeon[x][y].door_info[player_dir] == LOCKED_DOOR:
        if prince.key_no == 2:
            return player_dir
        else:
            print("This door is locked. You need two keys to enter.")
    else:
        print("You cannot move in this direction. Try again.")
    return -1

# プリンスを移動する
def move_prince(x, y, move_dir):
    dungeon[x][y].has_prince = False
    if move_dir == NORTH:
        prince.room_y -= 1
    elif move_dir == SOUTH:
        prince.room_y += 1
    elif move_dir == WEST:
        prince.room_x -= 1
    elif move_dir == EAST:
        prince.room_x += 1
    dungeon[prince.room_x][prince.room_y].has_prince = True
    dungeon[prince.room_x][prince.room_y].prince_visited = True
    
# この部屋に刀があれば刀を獲得
def try_pick_up_sword(x, y):
    if dungeon[x][y].has_sword:
        prince.has_sword = True
        dungeon[x][y].has_sword = False
        print("===========================")
        print("You have picked up a sword!")
        print("===========================")
        
# この部屋に健康ポーションがあれば、HPが満点じゃないと飲む
def try_drink_potion(x, y):
    if dungeon[x][y].has_potion and prince.hit_points < PRINCE_MAX_HP:
        prince.hit_points = PRINCE_MAX_HP
        dungeon[x][y].has_potion = False
        print("=========================================")
        print("You drink a health potion and feel great!")
        print("=========================================")
        
# Stinkerと戦闘
def stinker_fight(x, y):
    result = NO_BATTLE
    if dungeon[x][y].has_stinker != NO_STINKER:
        if prince.has_sword:
            print("I see you have sword, but I am going to kill you anyway!!")
            input("Press any key to attack Stinker...")
        else:
            print("You come to fight me with your bare hands? Prepare to die!!")
            input("Press any key to attack Stinker...")
        result = stinker_vs_prince(dungeon[x][y].has_stinker, prince.has_sword)
        if result == STINKER_DEAD:
            print("After a brave fight you have killed a Stinker. You get the key he holds!")
            prince.key_no += 1
            dungeon[x][y].has_stinker = NO_STINKER
            if x > 0:
                dungeon[x-1][y].stinker_smell = False
            if x < (DUNGEON_X - 1):
                dungeon[x+1][y].stinker_smell = False
            if y > 0:
                dungeon[x][y-1].stinker_smell = False
            if y < (DUNGEON_Y - 1):
                dungeon[x][y+1].stinker_smell = False
        elif result == PRINCE_DEAD:
            print("I am so sorry, my princess...")
    elif dungeon[x][y].has_superstinker:
        if prince.has_sword:
            print("I see you have sword, but you will never get the Princess!!")
            input("Press any key to attack Super Stinker...")
        else:
            print("No weapons? HA HA HA HA HA!!")
            input("Press any key to attack Super Stinker...")
        result = super_stinker_vs_prince(prince.has_sword)
        if result == STINKER_DEAD:
            print("You brave prince. Thank you for rescuing me from these awful Stinkers!")
            result = PRINCESS_RESCUED
            dungeon[x][y].has_superstinker = False
            if x > 0:
                dungeon[x-1][y].superstinker_smell = False
            if x < (DUNGEON_X - 1):
                dungeon[x+1][y].superstinker_smell = False
            if y > 0:
                dungeon[x][y-1].superstinker_smell = False
            if y < (DUNGEON_Y - 1):
                dungeon[x][y+1].superstinker_smell = False        
        elif result == PRINCE_DEAD:
            print("I tried everyting, but all was in vain...")
    return result

# 雑魚Stinkerと戦う
def stinker_vs_prince(stinker_id, sword):
    stinker1_hp = STINKER_MAX_HP
    stinker2_hp = STINKER_MAX_HP
    while True:
        if stinker_id == STINKER1:
            stinker1_hp -= prince_attack(sword)
            print(f"Stinker HP: {stinker1_hp}")
            if stinker1_hp <= 0:
                return STINKER_DEAD
        elif stinker_id == STINKER2:
            stinker2_hp -= prince_attack(sword)
            print(f"Stinker HP: {stinker2_hp}")
            if stinker2_hp <= 0:
                return STINKER_DEAD
        prince.hit_points -= stinker_attack()
        print(f"Prince HP: {prince.hit_points}")
        if prince.hit_points <= 0:
            return PRINCE_DEAD
        input("Press any key to continue to continue the battle.")

# ボスバトル
def super_stinker_vs_prince(sword):
    superstinker_hp = SUPERSTINKER_MAX_HP
    while True:
        superstinker_hp -= prince_attack(sword)
        print(f"Stinker HP: {superstinker_hp}")
        if superstinker_hp <= 0:
            return STINKER_DEAD
        prince.hit_points -= super_stinker_attack()
        print(f"Prince HP: {prince.hit_points}")
        if prince.hit_points <= 0:
            return PRINCE_DEAD
        input("Press any key to continue to continue the battle.")

# プリンスの攻撃のダメージ計算
def prince_attack(sword):
    damage = randint(0, PRINCE_ATTACK_RANGE)
    if sword:
        damage *= SWORD_DAMAGE_RATIO
    print(f"Prince attacks, damage: {damage}")
    return damage

# Stinkerの攻撃のダメージ計算
def stinker_attack():
    damage = randint(0, STINKER_ATTACK_RANGE)
    print(f"Stinker attacks, damage: {damage}")
    return damage
    
# Stinkerの攻撃のダメージ計算
def super_stinker_attack():
    damage = randint(0, SUPER_STINKER_ATTACK_RANGE)
    print(f"Super Stinker attacks, damage: {damage}")
    return damage

while True:
    # ゲームのルールを表示		
    print_game_explanation()
    # ダンジョンの初期化
    dungeon = init_dungeon()
    # プリンスの情報を初期化
    prince = init_prince()
    # ゲームループ
    while True:
        # ダンジョンと部屋の情報を表示
        show_dungeon()
        show_room_info(prince.room_x, prince.room_y)
        
        battle_result = stinker_fight(prince.room_x, prince.room_y)
        if battle_result == PRINCE_DEAD:
            # 敗北条件達成。ゲームループ脱出。
            break
        elif battle_result == PRINCESS_RESCUED:
            # 勝利条件達成。ゲームループ脱出。
            break
        try_pick_up_sword(prince.room_x, prince.room_y)
        try_drink_potion(prince.room_x, prince.room_y)
        
        mv_dir = get_player_move(prince.room_x, prince.room_y)
        if mv_dir == -1:
            print("Error with user input")
            break
        move_prince(prince.room_x, prince.room_y, mv_dir)
    if battle_result == PRINCESS_RESCUED:
        print("*"*22)
        print("* GAME OVER: YOU WIN *")
        print("*"*22)
        print("You have defeated the Stinkers and saved your princess.")
        print("Of course, you and your princess live happily ever after.")
    elif battle_result == PRINCE_DEAD:
        print("*"*23)
        print("* GAME OVER: YOU LOSE *")
        print("*"*23)
        print("You died in battle and the Stinkers dance happily on your grave.")
        print("Of course, they keep the princess in their dungeon forever.")
    choice = input("Do you want to play again? (Y/N): ")
    if choice == 'N' or choice == 'n':
        print("Thank you for playing Stinkin' Dungeon")
        break