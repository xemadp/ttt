# New Year Project 
# AP 2023 KNTU
# Emad Pourhassani 
# Computer Science

# Libraries
import tkinter as tk
from tkinter import ttk
from tkinter import font
import random as r

# Create a tkinter based xo game using object oriented concepts

# This program is going to be compromised of two sections 
# An XO engine made with OOP in mind, to play xo utilizing a player and computer 
# And another section that is tkinter interface connecting the player to our engine.



# ------------------------ ENGINE ------------------------

# The Board is going to be a class that has it's own special methods and attributes
# The Board is basically a 2d matrix that is x * y in size.

class Board:
    def __init__(self, x):
        self.x = x # Rows
        self.y = x # Columns

        self.grid = []
        for i in range(self.x):
            self.grid.append([0 for j in range(self.y)])

    # Prints our board in a beautified way, used for debugging purposes
    def Print(self):
        print("---------Board----------")
        for i in self.grid:
            print(' '*6,i)
        print("----------END-----------")

    # Update i,j position of the board with the new value
    # Indices start at zero
    def Update(self, ind, val):
        if self.grid[ind[0]][ind[1]]==0:
            self.grid[ind[0]][ind[1]] = val

    # Gives the value at i,j
    def Value(self, i, j):
        return self.grid[i][j]


    # Check if val is one move from winning
    def PossibleWinner(self, val):
        for i in range(self.x):
            for j in range(self.y):
                if self.grid[i][j]==0:
                    self.grid[i][j]=val
                    if self.CheckForWinner()==val:
                        self.grid[i][j]=0 # if winner found, set the board to initial phase and then return
                        return (i,j)

                    self.grid[i][j]=0

    # Cheks if there is a winner in the board
    # Returns the winning value if winner found
    # Otherwise returns None
    def CheckForWinner(self):
        # ---Check if winner is in rows
        for r in self.grid:
            if (len(set(r))==1) and (r[0]!=0):
                return r[0]

        # ---Check Columns for winner
        # We Rotate the matrix and then check for rows again.
        tempgrid = [[0 for i in range(self.y)] for i in range(self.x)]


        # Let's Rotate the matrix
        for i in range(self.x):
            for j in range(self.y):
                tempgrid[i][j] = self.grid[j][i]

        # Checking for rows in new rotated matrix
        for r in tempgrid:
            if (len(set(r))==1) and (r[0]!=0):
                return r[0]


        # ---Checking Diagonals
        if (len({self.grid[0][0], self.grid[1][1], self.grid[2][2]})==1 or
                len({self.grid[0][2], self.grid[1][1], self.grid[2][0]})==1) and self.grid[1][1]!=0:
            return self.grid[1][1]

    # Check If at list of the (i,j) indices on the list of given indices is free.
    # Return all the free indices.
    def CheckIfFree(self,ps):
        fs = [] # free indices
        for i,j in ps:
            if self.grid[i][j] == 0:
                fs.append((i,j))

        return fs

# A Player takes a board and a value and change the board with its methods
class Player:
    def __init__(self, board,val):
        self.val = val # The Value used to indicate this player
        Player.board = board

    # play val at board[i][j]
    def play(self, ind):
        Player.board.Update(ind,self.val)

    def ComputerMove(self, v):
        pcm = Player.board.PossibleWinner(self.val) # Possible Computer move
        if pcm!=None:
            self.play(pcm)
            return pcm

        ppm = Player.board.PossibleWinner(v) # Possible Player move
        if ppm!=None:
            self.play(ppm)
            return ppm


        # Check Free Corners
        freecorners = Player.board.CheckIfFree([(0,0),(0,2),(2,0),(2,2)])
        if len(freecorners)!=0:
            randomIndex = r.choice(freecorners)
            Player.board.Update(randomIndex, self.val)
            return randomIndex
        else:
            # Check CENTER
            center = (1,1)
            if len(Player.board.CheckIfFree([center]))!=0:
                Player.board.Update(center, self.val)
                return randomIndex
            else:
                freesides = Player.board.CheckIfFree([(0,1),(1,0),(1,2),(2,1)])
                if len(freesides)!=0:
                    randomIndex = r.choice(freesides)
                    Player.board.Update(randomIndex, self.val)
                    return randomIndex


# ----- SET UP TKINTER CLASSES -----

class Game(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("XO Game")
        self._cells = {}
        self.board = Board(3) # CREATE A 3X3 BOARD
        self.winnerfound = 0

        # Set Up Player and Computer
        self.dcs = r.randint(0,1) # Does Computer start (0 or 1)
        self.p1 = Player(self.board,"x") # first player plays X 
        self.p2 = Player(self.board,"o") # second player plays O
        self.char1 = ["o","x"][self.dcs]
        self.curplayer = "Your"

        for p in [self.p1,self.p2]:
            if p.val == self.char1:
                self.computer = p
                self.computer.name = "Computer "
            else:
                self.player = p
                self.player.name = "You "

        self.GenerateDisplay()
        self.GenerateGrid()
        # Make First Move if Computer Starts first
        if self.dcs==1:
            index = self.computer.ComputerMove(self.player.val)
            for i,t in enumerate(self._cells):
                values = list(self._cells.values())
                if values[i]==index:
                    self.board.Update(self._cells[t], self.computer.val)
                    if t["text"]=="":
                        t.config(text=self.computer.val, fg = ["red","blue"][self.dcs])


    def GenerateDisplay(self):
        display_frame = tk.Frame(master=self)

        display_frame.pack()
        display_frame2 = tk.Frame(master=self)
        display_frame3 = tk.Frame(master=self)
        reset_frame = tk.Frame(master=self)
        display_frame2.pack()
        display_frame3.pack()
        reset_frame.pack()

        self.display = tk.Label(master = display_frame,
                                text="Ready?",
                                font=font.Font(size=28,weight="bold"))
        starter = [("You", ""), ("Computer","s") ][self.dcs]
        self.display2 = tk.Label(master = display_frame2,
                                text=f"{starter[0]} Start{starter[1]}",
                               font=font.Font(size=22,weight="bold"))

        self.display3 = tk.Label(master = display_frame3,
                                 text=f"Computer : { self.computer.val}     Player : { self.player.val} ",
                               font=font.Font(size=12,weight="bold"))

        self.reset_button = tk.Button(
                    master=reset_frame,
                    text="Quit",
                    font=font.Font(size=16, weight="bold"),
                    fg="black",
                    width=5,
                    height=1,
                    highlightbackground="lightblue"
                )

        self.reset_button.bind("<ButtonPress-1>",self.quit)
        self.reset_button.pack()
        self.display.pack()
        self.display2.pack()
        self.display3.pack()

    def GenerateGrid(self):
        grid_frame = tk.Frame(master=self)
        grid_frame.pack()
        for row in range(3):
            self.rowconfigure(row, weight=1, minsize=50)
            self.columnconfigure(row, weight=1, minsize=75)
            for col in range(3):
                button = tk.Button(
                    master=grid_frame,
                    text="",
                    font=font.Font(size=36, weight="bold"),
                    fg="black",
                    width=3,
                    height=2,
                    highlightbackground="lightblue"
                )
                self._cells[button] = (row,col)
                button.bind("<ButtonPress-1>",self.Play)


                button.grid(
                    row=row,
                    column=col,
                    padx=5,
                    pady=5,
                    sticky="nsew"
                )

    def Play(self,event):
        if self.winnerfound != 1:
            self.display.config(text="")
            button = event.widget
            self.board.Update(self._cells[button], self.player.val)
            played = 0;
            if button["text"]=="":
                button.config(text=self.player.val, fg="red")
                self.display2.config(text=f"{self.curplayer} turn")
                self.curplayer = "Computer's"
                played = 1

            if self.board.CheckForWinner():
                print("Player Won!")
                self.FinishGame(self.player.name + "Won!")
                return None

            if played != 1:
                return played

            index = self.computer.ComputerMove(self.player.val)
            for i,t in enumerate(self._cells):
                values = list(self._cells.values())
                if values[i]==index:
                    self.board.Update(self._cells[t], self.computer.val)
                    if t["text"]=="":
                        t.config(text=self.computer.val, fg="blue")
                        self.curplayer = "Your"
                        self.display2.config(text=f"{self.curplayer} turn")

            if self.board.CheckForWinner():
                print("Computer Won!")
                self.FinishGame(self.computer.name + "Won!")
                return None

            if not self.board.CheckIfFree(list(self._cells.values())) and not self.board.CheckForWinner():
                print("ITS A TIE!")
                self.FinishGame("Tie!")



    def FinishGame(self, name):
        self.display2.config(text=name)
        self.winnerfound = 1

    def quit(self,event):
        self.destroy()

# ------------------------ MAIN ------------------------

game = Game()

game.mainloop()
