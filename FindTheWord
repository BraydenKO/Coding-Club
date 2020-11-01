
board = [["a","b","c"],["a","c","b"],["a","d","c"]]
neighbors=[(0,1),(1,0),(0,-1),(-1,0)] #Helps for loop check the surrounding blocks
workingboard=[]
word = ""
found=False

def printboard():
    for y in board:
        for x in y:
            print(x, "", end="")
        print("\n")

def initBoard(): 
    """ Adds padding so that when surrounding letters are checked
        letters outside the list aren't checked (ERROR) nor that 
        letters from the other side of the board are checked (negative index).
        Also, it creates a 'workingboard' so that used letters can be deleted
        and not checked in the search but not deleted from the template in case
        the search went the wrong direction and needs to be rebuilt
    """
    global board
    global workingboard
    global word
    printboard()
    board.insert(0,[""]*(len(board[0])))
    board.insert(len(board),[""]*(len(board[1])))
    for i in board:
       i.insert(0,"")
       i.insert(len(i),"")
    workingboard = [i[:] for i in board] #'deepcopies' board to workingboard
    word = input("Enter a word to search:")


def followingSearch(x_idx,y_idx,place): 
    """Looks for the 2nd letter and beyond by checking if the adjacent
       blocks match the next letter in the list. It calls itself when
       more letters need to be found, and it reverts itself back
       one step if it headed in the wrong direction
    """
    global workingboard
    global found
    workingboard[y_idx][x_idx]="" #This is done so that the same letter cant be used twice
    for neighborY,neighborX in neighbors:
        if workingboard[y_idx+neighborY][x_idx+neighborX]== word[place]: 
            if (len(word)-1)>place: 
                followingSearch(x_idx+neighborX, y_idx+neighborY, place+1)
            else: 
                found = True
                break
    else:
        workingboard[y_idx][x_idx]=board[y_idx][x_idx]

def totalSearch():
    global workingboard
    for y_idx, y in enumerate(board):
        for x_idx, x in enumerate(y):
            if x == word[0]:
                followingSearch(x_idx,y_idx,1)
    print(found)
        

initBoard()
totalSearch()
