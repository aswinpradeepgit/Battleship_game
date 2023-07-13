def main_menu():
    print("              ~ Welcome to battleship ~")
    print('\n')
    print("ChatGPT has gone rogue and commandeered a space strike")
    print("fleet. It's on a mission to take over the world. We've")
    print("located the stolen ships, but we need your superior")
    print("intelligence to help us destroy them before it's too")
    print("late.")
    print("\n")
    while True:
        print("Menu")
        print("        1 : Instructions")
        print("        2 : View Example Map")
        print("        3 : New Game")
        print("        4 : Hall of Fame")
        print("        5 : Quit")
        choice = input("What would you like to do? ")
        if choice=="5":
            print("Goodbye")
            break
        if choice not in ["1","2","3","4",'5']:
            print("Invalid selection. Please choose a number from the menu.")

        if choice=="1":
            instructions()

        if choice=="2":
            example_grid()

        if choice=="3":
            play_battleship()

        if choice=="4":
            load_hall_of_fame()
            display_hall_of_fame()



def instructions():
        print('Instructions:')
        print("\n")
        print('Ships are positioned at fixed locations in a 10-by-10 grid.')
        print('The rows of the grid are labeled A through J, and the columns are labeled 0 through 9.')
        print('Use menu option "2" to see an example.')
        print('Target the ships by entering the row and column of the location you wish to shoot.')
        print('A ship is destroyed when all of the spaces it fills have been hit.')
        print('Try to destroy the fleet with as few shots as possible.')
        print('The fleet consists of the following 5 ships:')

def example_grid():
    print("  0 1 2 3 4 5 6 7 8 9")
    print("A ~ ~ M ~ ~ ~ ~ ~ ~ ~")
    print("B ~ M M M ~ P P ~ ~ ~")
    print("C ~ ~ M ~ ~ ~ ~ ~ ~ ~")
    print("D ~ D ~ ~ ~ ~ ~ ~ ~ ~")
    print("E ~ D D ~ ~ ~ ~ ~ ~ ~")
    print("F ~ ~ ~ ~ ~ ~ ~ ~ ~ ~")
    print("G ~ ~ B B ~ ~ ~ ~ ~ ~")
    print("H ~ ~ B B ~ ~ ~ ~ ~ ~")
    print("I ~ ~ ~ ~ S S S ~ ~ ~")
    print("J ~ ~ ~ ~ ~ ~ ~ ~ ~ ~")




import random
import operator

# Function to create the game grid
HOF_FILE = 'battleship_hof.txt'
def is_boundary_exceeded(grid_length, row, col):
    return (row >= grid_length or row < 0 or col >= grid_length or col < 0)

# Function to create the game grid
def make_grid():
    grid = [['~' for _ in range(10)] for _ in range(10)]
    return grid


# Function to place ships randomly on the grid
def place_ships(grid):
    grid_length = len(grid)
    coordinates = {
        'mothership': [[-1, 0], [0, -1], [0, 0], [0, 1], [1, 0]],
        'battleship': [[0, 0], [0, 1], [1, 0], [1, 1]],
        'destroyer': [[0, 0], [-1, 0], [0, 1]],
        'stealthship': [[0, 0], [0, 1], [0, 2]],
        'patrolship': [[0, 0], [0, 1]]
    }
    for ship, positions in coordinates.items():
        while True:
            row_center = random.randint(0, grid_length)
            col_center = random.randint(0, grid_length)
            placement_success = True
            for position in positions:
                row_inc, col_inc = position
                x = row_center + row_inc
                y = col_center + col_inc
                if (is_boundary_exceeded(grid_length, x, y) or grid[x][y] != '~'):
                    placement_success = False
                    break
            if placement_success:
                for position in positions:
                    row_inc, col_inc = position
                    grid[row_center + row_inc][col_center + col_inc] = ship[0].capitalize()
                break
    return grid

def print_grid(grid):
    print("  0 1 2 3 4 5 6 7 8 9")
    for i, row in enumerate(grid):
        print(chr(i + ord('A')), ' '.join(row))

def check_guess(guess, grid, masked_grid):
    row = ord(guess[0].upper()) - ord('A')
    col = int(guess[1])
    if grid[row][col] != '~' and masked_grid[row][col] != 'x' and masked_grid[row][col] != 'o':
        return "hit"
    elif masked_grid[row][col] == 'x' or masked_grid[row][col] == 'o':
        return "taken"
    else:
        return "miss"


# def check_guess(guess, grid):
#     row = ord(guess[0].upper()) - ord('A')
#     col = int(guess[1])
#     if grid[row][col] != '~':
#         return "hit"
#     else:
#         return "miss"

def count_occurrences(grid):
    count = 0
    for sublist in grid:
        count += sublist.count("x")
    return count

def play_battleship():
    load_hall_of_fame()
    grid = make_grid()
    grid=place_ships(grid)
    #print_grid(grid)
    masked_grid=make_grid()
    print_grid(masked_grid)

    shots=0

    while True:
        shots+=1
        guess = input("Where should we target next (q to quit)? ")
        if guess=="q":
            break
        if len(guess) != 2 and guess.isalpha():
            print("Please enter exactly two characters.")
            continue
        if len(guess)==2 and (guess[0].isalpha() or guess[1].isdigit()) and (guess[0].upper() not in ["A","B","C","D","E","F","G","H","I","J"] or int(guess[1]) not in [0,1,2,3,4,5,6,7,8,9]):
            print('Please enter a location in the form "G6"')


            continue

        result = check_guess(guess, grid,masked_grid)
        if result == "hit":

            print("It's a hit!")
            row = ord(guess[0].upper()) - ord('A')
            col = int(guess[1])
            masked_grid[row][col] = 'x'
        elif result=="taken":
            print("You've already targeted that location")
        else:
            print("It's a miss!")
            row = ord(guess[0].upper()) - ord('A')
            col = int(guess[1])
            masked_grid[row][col] = 'o'
        #print_grid(grid)
        print_grid(masked_grid)




        if count_occurrences(masked_grid)==17:
            print("IT'S A HIT")
            print("The enemy's Stealth Ship has been destroyed.")
            print('\n')
            print("You've destroyed the enemy fleet!")
            print("Humanity has been saved from the threat of AI.")
            print("\n")
            print("For now...")
            print("\n")
            accuracy = 17 / shots
            print(f'Congratulations Congratulations, you have achieved a targeting accuracy of {round(accuracy*100,2)}% and earned a spot in the Hall of Fame.')
            name = input("Enter your name: ")
            update_hall_of_fame(name,17,shots)
            display_hall_of_fame()
            save_hall_of_fame(shots)



            break

hall_of_fame = []

def update_hall_of_fame(player_name, hits, shots):
    global hall_of_fame
    accuracy = (hits / shots) * 100
    if len(hall_of_fame) < 10 or accuracy > hall_of_fame[-1][0]:
        hall_of_fame.append((accuracy, player_name))
        hall_of_fame.sort(key=operator.itemgetter(0, 1), reverse=True)
        hall_of_fame = hall_of_fame[:10]

def display_hall_of_fame():
    print("~~~~~~~~ Hall of Fame ~~~~~~~~")
    print("Rank : Accuracy : Player Name")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    for rank, (accuracy, player_name) in enumerate(hall_of_fame, start=1):
        print(f"{rank} {accuracy:.2f}% {player_name}")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

def save_hall_of_fame(shots):
    with open("hall_of_fame.txt", "w") as file:
        file.write("name,hits,misses\n")
        for accuracy, player_name in hall_of_fame:
            hits = 17
            misses = shots - 17
            file.write(f"{player_name},{hits},{misses}\n")

def load_hall_of_fame():
    try:
        with open("hall_of_fame.txt", "r") as file:
            lines = file.readlines()
            for line in lines[1:]:
                line = line.strip().split(",")
                player_name = line[0]
                hits = int(line[1])
                misses = int(line[2])
                shots = hits + misses
                accuracy = (hits / shots) * 100
                hall_of_fame.append((accuracy, player_name))
            hall_of_fame.sort(key=operator.itemgetter(0, 1), reverse=True)
    except FileNotFoundError:
        print("Hall of Fame file not found. Starting with an empty Hall of Fame.")





main_menu()






