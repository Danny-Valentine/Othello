"""
A Python module for the Othello game.

TODO: Add a description of the module.
Full name: Danny Valentine
StudentId: u82754dv
Email: danny.valentine@student.manchester.ac.uk
"""

from copy import deepcopy # you may use this for copying a board

def newGame(player1,player2):
    """
    Make sure you write meaningful docstrings!
    """
    game = {
            'player1' : player1,
            'player2' : player2,
            'who' : 1,
            'board' : [[0,0,0,0,0,0,0,0],
                       [0,0,0,0,0,0,0,0],
                       [0,0,0,0,0,0,0,0],
                       [0,0,0,2,1,0,0,0],
                       [0,0,0,1,2,0,0,0],
                       [0,0,0,0,0,0,0,0],
                       [0,0,0,0,0,0,0,0],
                       [0,0,0,0,0,0,0,0]]}

    # TODO: Initialize dictionary for a new game
    return game

#game = newGame('Danny1','Danny1')
#board = game['board']
# TODO: All the other functions of Tasks 2-12 go here.
# USE EXACTLY THE PROVIDED FUNCTION NAMES AND VARIABLES!

def printBoard(board):
    print(' |a|b|c|d|e|f|g|h|')
    #print(' +-+-+-+-+-+-+-+-+')
    for y in range(8):
        print(str(y+1) + str('|'), end='')
        for x in range(8):
            if board[y][x] == 0:
                print(' |', end='')
            elif board[y][x] == 1:
                print('X|', end='')
            else:
                print('O|', end='')
        print()
    #print(' +-+-+-+-+-+-+-+-+')

def scoreboard(board,player1,player2):
    print(str(player1) + "'s Score: " + str(player1scoreBoard(board,player1)))
    print(str(player2) + "'s Score: " + str(player2scoreBoard(board,player2)))
    
def strToIndex(s):
    s=str(s)
    s=s.replace(" ", "")
    lst=list(s)
    
    if len(lst) != 2:
        raise ValueError ('Invalid input. Incorrect number. Must be exactly one letter and exactly one number.')
    
    for i in range(len(lst)):
        lst[i]=lst[i].capitalize()
        if lst[i] in ['1','2','3','4','5','6','7','8']:
            r=int(lst[i])-1
        elif lst[i] in ['A','B','C','D','E','F','G','H']:
            c=int(ord(lst[i])-65)
        else:
            print('Invalid input')
            raise ValueError('Invalid input. Letters and numbers must correspond to those on the board.')
    try:
        return (r,c)
    except UnboundLocalError:
        raise ValueError ('Invalid input. Must be a letter and a number.')
        

def indexToStr(t):
    lst=list(t)
    print(lst)
    r=lst[0]
    c=chr(lst[1]+97)
    return str(c) + str(r+1)

def loadGame():
    #Try to open the file
    try:
        f = open("game.txt", mode="rt", encoding="utf8")
    except FileNotFoundError:
        raise FileNotFoundError ("File 'game.txt' not found.")
    
    flist=f.readlines()
    
    #Check file has 11 lines
    if len(flist) != 11:
        raise ValueError ('Invalid Format: Incorrect number of lines in file')
    
    #Remove \n from each line
    for i in range(len(flist)):
        flist[i]=flist[i].replace("\n", "")
    
    #Check valid input of "who"
    try:
        int(flist[2])
    except ValueError:
        raise ValueError ('Invalid Format: Value of "who" must be an integer')
    
    #Check "who" is 1 or 2
    if int(flist[2]) not in [1,2]:
        raise ValueError ('Invalid Format: Value of "who" must be 1 or 2')
    
    fboard=[[],[],[],[],[],[],[],[]]
    #Check each line of "board" is valid
    for i in range(3, 11):
        #print('\n i', i)
        temp =list(flist[i])
        if len(temp) != 15: #Check length
            raise ValueError ("Invalid Format: Length error in line", i-3, ". Each line of board must each be a comma-separated string of 8 characters, each character being either 0, 1, or 2")
        
        for j in range(0, 15, 2):
            #print('j', j)
            #print(int(temp[j]))
            if int(temp[j]) not in [0,1,2]: #Check each value is 0, 1 or 2
                raise ValueError ('Invalid Format: Values of "board" must be 0 or 1 or 2')
            fboard[i-3].append(int(temp[j]))
        for j in range (1, 14, 2):
            #print('j', j)
            #print(temp[j])
            if temp[j] != ',': #Check that they are separated by commas
                raise ValueError ('Invalid Format: Comma error. Each line of "board" must each be a comma-separated string of 8 characters, each character being either 0, 1, or 2')

    game = {
            'player1' : str(flist[0]),
            'player2' : str(flist[1]),
            'who' : int(str(flist[2])),
            'board' : [fboard[0],
                       fboard[1],
                       fboard[2],
                       fboard[3],
                       fboard[4],
                       fboard[5],
                       fboard[6],
                       fboard[7]]
            }
        
        
    f.close()
    #check format of game.txt?
    return game

def getLine(board,who,pos,dir):
    #from pos we want to move in the direction d and check whether we get to a piece of the current player
    opponentspieces=list()
    if who == 1:
        opp = 2
    else: opp = 1
    
    #printBoard(board)
    i=1
    j=0
    while -1 < pos[0]+i*dir[0] < 8 and -1 < pos[1]+i*dir[1] < 8:
        #print(pos[0]+i*dir[0], pos[1]+i*dir[1])
        if board[pos[0]+i*dir[0]][pos[1]+i*dir[1]] == 0:
            opponentspieces=list()
            j=0
            break
        elif board[pos[0]+i*dir[0]][pos[1]+i*dir[1]] == opp:
            opponentspieces.append((pos[0]+i*dir[0], pos[1]+i*dir[1]))
            i=i+1
        elif board[pos[0]+i*dir[0]][pos[1]+i*dir[1]] == who:
            j=2
            break
        j=1
        #print(j)
        
    if j == 1:
        opponentspieces=list()
    #This doesn't work because if there is an opponent piece at the edge of the baord then it is added to
    #the list and so i increases but then the loop ends before and the end piece is not checked
    
    return opponentspieces

def getValidMoves(board,who):
    #check if the position is occupied yet i.e. board[r][c]==0
    #getLine != [] in any possible direction
    #check all possible directions and add pos to the list if it is not empty
    validmoves=list()
    emptyspaces=list()
    
    for i in range(8):
        for j in range(8):
            if board[i][j] != 0:
                continue
            emptyspaces.append((i,j))
    
    for (i, j) in emptyspaces:
        for k in range (-1, 2):
            for l in range (-1, 2): 
                if getLine(board,who,(i, j),(k,l)) != []:
                    if (i,j) not in validmoves:
                        validmoves.append((i, j))
   
    #yprintBoard(board)
    return validmoves

def makeMove(board,move,who):
    r=move[0]
    c=move[1]
    board[r][c]=who
    pos=move
    
    for k in range (-1,2):
        for l in range (-1,2):
            for (i,j) in getLine(board,who,pos,(k,l)):
                board[i][j]=who
    
    return board

def scoreBoard(board):
    #printBoard(board)
    player1score = 0
    player2score = 0
    for i in range(8):
        for j in range(8):
            if board[i][j] == 1:
                player1score += 1
            elif board[i][j] == 2:
                player2score += 1
            
    return player1score - player2score

def player1scoreBoard(board,player1):
    player1score = 0
    for i in range(8):
        for j in range(8):
            if board[i][j] == 1:
                player1score += 1
    return player1score

def player2scoreBoard(board,player2):
    player2score = 0
    for i in range(8):
        for j in range(8):
            if board[i][j] == 2:
                player2score += 1
    return player2score

def suggestMove1(board,who):
    #Try all available moves
    validmoves=getValidMoves(board,who)
    
    if validmoves == []:
        return None
    
    maxscore = -100
    bestmove=validmoves[0]
    
    for (i,j) in validmoves:
        board2 = deepcopy(board)
        score=scoreBoard(makeMove(board2,(i,j),who))
        if who == 2:
            score *= -1
        if score > maxscore:
            maxscore=score
            bestmove=(i,j)
            
    return bestmove
                      
    
# ------------------- Main function --------------------
def play():
    """
    TODO in Task 11. Make sure to write meaningful docstrings!
    """
    print("*"*55)
    print("***"+" "*8+"WELCOME TO DANNY'S OTHELLO GAME!"+" "*8+"***")
    print("*"*55,"\n")
    print("Enter the players' names or type 'C' for computer or 'L'\nto load a game from file.\n")
    
    player1=input("Player 1: ").replace(" ", "")
    player1=player1.capitalize()
    
    while player1 == '':
            print("Please enter a username")
            player1=input("Player 1: ").replace(" ", "")
    
    if player1 == "L":
        print("\nLoading game from file game.txt \n")
        game=loadGame()
        who=game["who"]
        board=game["board"]
        player1=game["player1"].replace(" ", "")
        player2=game["player2"].replace(" ", "")
        print("Player 1:", player1)
        print("Player 2:", player2, "\n")
        printBoard(board)
    else:
        player2=input("Player 2: ").replace(" ", "")
        while player2 == '':
            print("Please enter a username")
            player2=input("Player 2: ").replace(" ", "")
        player2=player2.capitalize()
        game=newGame(player1,player2)
        who=game["who"]
        board=game["board"]
        print("\nNew game begun. \n")
        printBoard(board)
        
    
    
    while (getValidMoves(board,1) != []) or (getValidMoves(board,2) != []): #Check if there are any valid moves to be made by either player
        if who == 1:
            currentplayer = player1
            symbol = 'X'
        else:
            currentplayer = player2
            symbol = 'O'
        
        if getValidMoves(board,who) != []: #Check if there are any valid moves to be made by the current player
            if currentplayer == 'C':
                print("It is the computer's (" + str(symbol) + ") turn\n")
                print("The computer will make its move\n")
                move=suggestMove1(board,who)
                print("Computer's move: " + str(move))
                makeMove(board,move,who)
            else:
                print("\nIt is " + str(currentplayer) + "'s (" + str(symbol) + ") turn\n")
                while True: #Check move input is valid
                    try:
                        move=strToIndex(input("Enter the move you would like to make: "))
                        break
                    except ValueError or UnboundLocalError:
                        print("Invalid move input. Letters and numbers must correspond to those on the board.")
                    except UnboundLocalError:
                        print("Invalid move input. Make sure to select one number and one letter from the board.")
                    
                while move not in getValidMoves(board,who): #Check the move is valid
                    try:
                        print("Move invalid. You can only place a piece either side of opponent pieces.")
                        move=strToIndex(input("Enter the move you would like to make: "))
                    except ValueError:
                        continue
                
                makeMove(board,move,who)
                
        else:
            print("No valid moves for " + str(currentplayer) + ". Next player's turn")
        
        if who == 1:
            who = 2
        else:
            who = 1
        
        printBoard(board)
        scoreboard(board,player1,player2)
        print("\nEnd of turn\n")
        print("\nNext turn")


    print("Game over. No valid moves left for either player.")
    print("Final score: " + str(scoreBoard(board)))
    print(player1scoreBoard(board,player2))
    print(player2scoreBoard(board,player2))
    if player1scoreBoard(board,player1)>player2scoreBoard(board,player2):
        print(str(player1) + " (X) wins.")
    elif player1scoreBoard(board,player1)<player2scoreBoard(board,player2):
        print(str(player2) + " (O) wins.")
    else:
        print("The game is a draw.")



# the following allows your module to be run as a program
if __name__ == '__main__' or __name__ == 'builtins':
 play()
 
 """
 while True:
     try:
         strToIndex(input("Enter move: "))
         break
     except ValueError or UnboundLocalError:
         print("Caught")
 print("Successful move")
 """