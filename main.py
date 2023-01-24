import random as r

### TIC TAC TOE GAME
### KNTU FALL 2022 Project
### Program Written by Emad Pourhassani 
### Student No. 40116623
### Computer Science major

## -------------- Helper Functions -------------- ##

def DrawBoard(board):
    for i,row in enumerate(board):
        for j,s in enumerate(row):
            # If s is already played,
            # set sym as X or O depending on what
            # has been played on s
            # otherwise just set sym to the number
            # corresponding to that space on the board (0 - 8) 
            if s==0:
                sym=(i*3)+j # if we have the board spaces as (i,j) we can find the number by i*3 + j e.g: (1,1) <-> 4
            else:
                #sym = ['X','O'][s-1] # Without Coloring X and O
                sym = ["\033[0;31m",'\033[0;34m'][s-1]+['X','O'][s-1]+"\033[0m" # Add Ansi Color red to symbols 

            # Add | only if the space is not on the right sides, other wise put sym and go to next line
            if ((i*3)+j+1)%3==0:
                print(sym)
            else:
                print(sym,end='|')

        print('-'*5)


# Return 1 if there is a free space available on the board otherwise return 0
def BoardPosIsAvailable(board):
    if 0 in board[0]+board[1]+board[2]:
        return 1

    return 0


# Get Player input and check for availability of the given spot in the board
# Modify the board accordingly
def PlayerMove(board,player):
    inp = int(input("select spot to play : "))
    if type(inp) != int:
        print("Must Give Integer!")
        PlayerMove(board,player)
    elif inp<0 or inp>=9:
        print("Must be between 0 and 8!")
        PlayerMove(board,player)
    else:
        board[inp//3][inp%3] = player
        print("Player Played:")
        DrawBoard(board)
        print()

def PossibleWin(board,t):
    # We define possible win as a scenario within which
    # an entity ( either the player or the computer ) is one 
    # move away from winning and give the position of that move
    # if more than one such exists return any of them
    PossibleWinLayouts = [[t,t,0],[t,0,t],[0,t,t]]

    # Defining the rows , columns and diagonals from board
    rows = [i for i in board]
    cols = [[board[i][j] for i in range(3)] for j in range(3)]
    diags = [[board[i][i]    for i in range(3)],
             [board[i][2-i]  for i in range(3)]]

    for p in PossibleWinLayouts:
        if p in rows:
            for i,row in enumerate(rows):
                if row==p:
                    for j in range(3):
                        if row[j]==0:
                            return (i,j%3)
        if p in cols:
            for i,col in enumerate(cols):
                if col==p:
                    for j in range(3):
                        if col[j]==0:
                            return (j,i%3)

        if p in diags:
            for i,diag in enumerate(diags):
                if diag==p:
                    if i==0:
                        for j in range(3):
                            if diag[j]==0:
                                return (j,j)
                    else:
                        for j in range(3):
                            if diag[j]==0:
                                return (j,2-j)

    return (-1,-1)

# Decide on what the computer should do based 
# on the given algorithm in the pdf,
# modify the board accordingly
def ComputerMove(board,computer):
    # Check if computer can win within the next move and if so
    # make that winning move this turn
    pcw=PossibleWin(board,computer)
    if pcw!=(-1,-1):
        board[pcw[0]][pcw[1]]=computer
        print("Computer Played:")
        DrawBoard(board)
        print()
        return None # finish the function

    # Check if player can win within the next move and if so
    # block player and terminate the possible player win
    ppw=PossibleWin(board,player)
    if ppw!=(-1,-1):
        board[ppw[0]][ppw[1]]=computer
        print("Computer Played:")
        DrawBoard(board)
        print()
        return None # finish the function
    Corners = [board[0][0], board[0][2], board[2][0], board[2][2]]
    CornerIndices = list(filter(lambda x : board[x[0]][x[1]]==0, [(0,0),(0,2),(2,0),(2,2)]))
    r.shuffle(CornerIndices)
    if 0 in Corners:
        for i,j in CornerIndices:
            board[i][j]=computer
            print("Computer Played:")
            DrawBoard(board)
            print()
            return None


    if board[1][1]==0:
        board[1][1]=computer
        print("Computer Played:")
        DrawBoard(board)
        print()
        return None

    # Check And see if sides are available and if so 
    # select th
    Sides = [board[1][0], board[0][1], board[1][2], board[2][1]]
    # Get side indices that are available and shuffle them 
    SidesIndices = list(filter(lambda x : board[x[0]][x[1]]==0, [(1,0),(0,1),(1,2),(2,1)]))
    r.shuffle(SidesIndices)
    if 0 in Sides:
        for i,j in SidesIndices:
            board[i][j]=computer
            print("Computer Played:")
            DrawBoard(board)
            print()
            return None


# Check and see if either the computer or the player have won in the past moves
# return the winner if it exists
def CheckWin(board,player,computer):
    # Defining the rows , columns and diagonals from board
    rows = [i for i in board]
    cols = [[board[i][j] for i in range(3)] for j in range(3)]
    diags = [[board[i][i]    for i in range(3)],
             [board[i][2-i]  for i in range(3)]]

    ComputerWon = [computer,computer,computer]
    PlayerWon   = [player,player,player]

    if ComputerWon in rows+cols+diags:
        return 'computer'

    if PlayerWon in rows+cols+diags:
        return 'player'

    return None



## -------------- Main -------------- ##


# Create the initial state of the board
# where 0 means empty
# 1 means X
# 2 means O

board = [[0,0,0],
         [0,0,0],
         [0,0,0]]

# determine randomly whether computer or player goes first
# 1 meaning X
# 2 meaning O

computer = r.choice([1,2])
if computer==1:
    player=2
else:
    player=1

print("Computer plays", ['X','O'][computer-1])
print("Player plays", ['X','O'][player-1])
print()

DrawBoard(board)
while BoardPosIsAvailable(board):
    ## Play X first and then O Each Round
    ## Each round consists of a move by X followed by a move by O:
    if computer==1:
        # Check to see if either the computer or the player won after the previous move
        # If so, announce the winner and exit the program
        ComputerMove(board,computer)
        if CheckWin(board,player,computer)=='computer':
            print("Computer Won!")
            DrawBoard(board)
            exit()
        PlayerMove(board,player)
        if CheckWin(board,player,computer)=='player':
            print("Player Won!")
            DrawBoard(board)
            exit()
    else:
        # Check to see if either the computer or the player won after the previous move
        # If so, announce the winner and exit the program
        PlayerMove(board,player)
        if CheckWin(board,player,computer)=='player':
            print("Player Won!")
            DrawBoard(board)
            exit()
        ComputerMove(board,computer)
        if CheckWin(board,player,computer)=='computer':
            print("Computer Won!")
            DrawBoard(board)
            exit()


## If the winner was announced in the main loop, the program would've ended
## Since we got to this line of our program that means we have a Tie!
print("Tie!")
DrawBoard(board)
