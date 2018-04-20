import random
import os
import sys

CELLS = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0),
         (0, 1), (1, 1), (2, 1), (3, 1), (4, 1),
         (0, 2), (1, 2), (2, 2), (3, 2), (4, 2),
         (0, 3), (1, 3), (2, 3), (3, 3), (4, 3),
         (0, 4), (1, 4), (2, 4), (3, 4), (4, 4)]

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def get_locations():
    return random.sample(CELLS, 6)

def move_player(player, move):
    x, y = player
    if move == "LEFT":
        x -= 1
    if move == "RIGHT":
        x += 1
    if move == "UP":
        y -= 1
    if move == "DOWN":
        y += 1
    return (x, y)

def get_moves(player):
    moves = ["LEFT", "RIGHT", "UP", "DOWN"]
    x, y = player
    if x == 0:
        moves.remove("LEFT")
    if x == 4:
        moves.remove("RIGHT")
    if y == 0:
        moves.remove("UP")
    if y == 4:
        moves.remove("DOWN")
    return moves

def monster_movement(monster):
    x, y = monster
    x += random.randint(-1, 1)
    y += random.randint(-1, 1)
    if x < 0:
        x = 0
    if x > 4:
        x = 4
    if y < 0:
        y = 0
    if y > 4:
        y = 4
    return (x, y)

def draw_map(player, monsters, has_lantern, door, door_revealed):
    print(" _"*5)
    tile = "|{}"
    
    for cell in CELLS:
        x, y = cell
        if x < 4:
            line_end = ""
            if cell == player:
                output = tile.format("X")
            elif cell in monsters and has_lantern == True:
                output = tile.format("@")
            elif cell == door and door_revealed == True:
                output = tile.format("#")
            else:
                output = tile.format("_")
        else:
            line_end = "\n"
            if cell == player:
                output = tile.format("X|")
            elif cell in monsters and has_lantern == True:
                output = tile.format("@|")
            elif cell == door and door_revealed == True:
                output = tile.format("#|")
            else:
                output = tile.format("_|")
        print(output, end=line_end)

def game_loop(score, steps):
    monster1, door, player, monster2, sword, lantern = get_locations()
    playing = True
    has_sword = False
    has_lantern = False
    door_revealed = False
    if random.randint(1, 10) <= score:
        lantern = None
    if random.randint(1, 10) <= score:
        sword = None
    monsters = [monster1, monster2]
    if random.randint(1, 10) > score:
        monsters.pop()

    while playing:
        clear_screen()
        draw_map(player, monsters, has_lantern, door, door_revealed)
        moves = get_moves(player)
        print("You're currently in room {}".format(player))
        print("You can move {}".format(", ".join(moves)))
        print("Enter QUIT to quit")
        
        move = input("> ")
        move = move.upper()
        
        if move == 'QUIT':
            sys.exit()
        
        if move in moves:
            player = move_player(player, move)
            monsters = [monster_movement(monster) for monster in monsters]
            steps += 1
        elif move in ["LEFT", "RIGHT", "UP", "DOWN"]:
            input("\nThere's a solid wall there...")
        else:
            input("\nI'm sorry, I didn't understand that...")
        if player == lantern:
            print("\nCongratulations, you've found a lantern of true sight!")
            input("Now you can see where the monsters are on this floor!")
            has_lantern = True
            lantern = None
        if player == sword:
            print("\nCongratulations, you've found a brilliantly shining sword!")
            input("Next time you encounter a monster on this floor, you'll kill it first!")
            has_sword = True
            sword = None
        if player == door:
            if score == 10:
                input("You've done it! You open the dungeon's last door and find...")
                if random.randint(1, 5) < 3:
                    print("Another Monster! It eats you instantly and you die.\nI guess that's roguelikes for you.")
                else:
                    print("Limitless treasure! You're free to live the rest of your life in luxury and comfort, congratulations!")
                if input("Your journey took you {} steps to reach the end. Play again? (Y/n)\n> ".format(steps)).upper() == "N":
                    sys.exit()
                else:
                    game_loop(1, 0)
            else:
                print("\nCongratulations, you've found the exit and cleared floor {}!".format(score))
                if input("Would you like to continue further? (Y/n)\n> ").upper() == "N":
                    sys.exit()
                else:
                    game_loop(score+1, steps)
        if player in monsters:
            if has_sword == True:
                print("\nYou unleash the power of the sword and blow the Monster to pieces!")
                input("The sword's glow fades away, but the Monster is no more.")
                has_sword = False
                monsters.remove(player)
            else:
                print("\nOh no! You ran into a monster and got eaten...".format(score))
                print("Your journey lasted {} steps and ended on floor {}".format(steps, score))
                if input("Would you like to start from the beginning? (Y/n)\n> ").upper() == "N":
                    sys.exit()
                else:
                    game_loop(1, 0)
        if len(monsters) == 0 and door_revealed == False:
            print("\nWith all the monsters on the floor killed, you sense the danger pass")
            input("Having calmed down, you piece together clues and figure out where the door is.")
            door_revealed = True

clear_screen()
print("Welcome to the dungeon!")
input("Press enter to start!")
game_loop(1, 0)