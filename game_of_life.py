grid = [] #Grid that will be displayed and read from

tempgrid=[] #Grid that will temporarily hold the updates
#to the grid to avoid interference 

l=3 #Height

w=3 #Width

steps=5 #Number of frames

igrid=[(0,1),(1,1),(2,1)] #Initial live cells

neighbors=[(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1)]
validneighbors=[] #neighbors is a list containing the relative positions of each neighbor
#valid neighbors contains the values of the neighbors that exist on the grid

def printgrid(grid):
    """Prints the grid in an easy to read way
    """
    Print("-------")
    for y in grid:
        for x in y:
            print(x," ", end="")
        print("\n")


def initgrid():
    """Starts the grid and calls the other functions
    To continue the game """
    grid=[[0]*w for i in range(l)]
    tempgrid=[[0]*w for i in range(l)]
    for r,c in igrid:
        grid[r][c] = 1
    printgrid(grid)
    updategrid(grid,validneighbors,tempgrid)

def updategrid(grid,validneighbors,tempgrid):
    for i in range(steps):
        for y_idx, y in enumerate(grid): #iterate the row and index
            for x_idx, x in enumerate(y):#iterate elements in row and index
                for p,q in neighbors: #checks which neighbors the cell has (not all cells have all 8)
                    try:
                        if (y_idx > 0 or p>=0) and (x_idx > 0 or q>=0):
                            validneighbors.append(grid[y_idx+p][x_idx+q])
                    except IndexError:
                        pass
                if (sum(validneighbors) == 3) or (x==1 and sum(validneighbors)==2):
                    tempgrid[y_idx][x_idx]=1
                else:
                    tempgrid[y_idx][x_idx]=0
                validneighbors=[]
        grid=tempgrid #update the grid so that now it has the 2nd frame
        tempgrid=[[0]*w for i in range(l)] #Before I added this line grid would change every time
#tempgrid was changed and when I added this line it somehow fixed it... I'm not sure why.
        printgrid(grid)

initgrid()
