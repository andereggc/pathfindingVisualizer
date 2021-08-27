import pygame, sys, random, math

pygame.init() # initializing the constructor    

# global variables
size = (width, height) = 600, 600 # window dimensions
win = pygame.display.set_mode(size)
cols, rows = 50, 50  # cols and rows of grid
grid, openSet, closeSet, path, visited  = [], [], [], [], [] # arrays used for board creation and algorithm
gridWidth = width//cols
gridHeight = height//rows # width and height of grid
colorLight = (170,170,170) # light shade of the button 
colorDark = (100,100,100) # dark shade of the button  
txtColor = (64,224,208) # text color

class Spot:
    # Spot class represents a tile on the grid
    def __init__(self, i, j):
        # constructor
        self.x, self.y = i, j # used for (x,y) position on grid
        self.f, self.g, self.h = 0, 0, 0
        # An important aspect of A* is F = G + H: f is the total cost of the node, g is the distance between the 
        # current node and the start node, and h is the heuristic (estimated distance from the current node to the end node). 
        # I can use this f value to look at all the nodes and determine which node will get me closer to the end node
        self.neighbors = [] # neighbors of a node
        self.prev = None # previous nodes
        self.wall = False # if a tile is a wall or not
        self.visited = False # if a tile has been visited or not

    def show(self, win, col):
        # updates tiles colors
        if self.wall == False: # with the help of createGrid(), this allows us to create the wall on the bottom for text
            pygame.draw.rect(win, col, (self.x*gridWidth, self.y*gridHeight, gridWidth-1, gridHeight-1))    

    def add_neighbors(self, grid):
        # appends neighbors for pathfinding algorithm
        # adds tiles up, down, left, and right
        if self.x < cols - 1:
            self.neighbors.append(grid[self.x+1][self.y])
        if self.x > 0:
            self.neighbors.append(grid[self.x-1][self.y])
        if self.y < rows - 1:
            self.neighbors.append(grid[self.x][self.y+1])
        if self.y > 0:
            self.neighbors.append(grid[self.x][self.y-1])     
        # adds diagonal tiles   
        if self.x < cols - 1 and self.y < rows - 1:
            self.neighbors.append(grid[self.x+1][self.y+1])
        if self.x < cols - 1 and self.y > 0:
            self.neighbors.append(grid[self.x+1][self.y-1])
        if self.x > 0 and self.y < rows - 1:
            self.neighbors.append(grid[self.x-1][self.y+1])
        if self.x > 0 and self.y > 0:
            self.neighbors.append(grid[self.x-1][self.y-1])

def clickWall(pos):
    # turns blank tiles into walls when mouse is clicked and in motion
    i = (pos[0] // gridWidth)
    j = (pos[1] // gridHeight) 
    grid[i][j].wall = True # setting .wall = True creates a wall
            
def heuristics(a, b): 
    # heuristics, important for aStar pathfinding algorithm
    return math.sqrt((a.x - b.x)**2 + abs(a.y - b.y)**2) # uses Pythagorean Theorem to find estimated distance from current node to end node

def createGrid():
    # completely resets grid and relevant arrays. Creates new grid ready for use
    for i in range(cols):
        arr = []
        for j in range(rows):
            arr.append(Spot(i, j)) # creates blank 2D board
        grid.append(arr) # nested for loop is used to add the 2D array arr to our 2D array grid 

    for i in range(cols):
        for j in range(rows):
            grid[i][j].add_neighbors(grid) # adds all surrounding tiles to the neighbors array

    global end, start # global so they can be used in other functions
    startRand = [(grid[0][0]),(grid[49][0]),(grid[49][40]),(grid[0][40])]
    start = random.choice(startRand) # randomizes start point's location
    rowRand = random.randint(15,25)
    colRand = random.randint(10,20)
    end = grid[rowRand][colRand] # randomizes end point's location
    """
    Code below resets the board/relevant arrays every time function is called 
    """
    start.wall = False
    end.wall = False
    start.visited = True
    openSet.clear()        
    openSet.append(start) # openSet starts with only the starting node
    closeSet.clear()
    path.clear()
    for i in range(cols):
        for j in range(rows):
            spot = grid[i][j]
            grid[i][j].wall = False 
            grid[i][j].visited = False 
            spot.visited = False
            if (j>40): # creates wall on the bottom which allows space for text
                grid[i][j].wall = True

def aStar():
    # main aStar pathfinding function
    finishFlag = False # when True we have found the shortest path
    startflag = False # when True the program will start finding the shortest path
    createGrid() # sets important variables to default values then creates grid
    while True:
        pathCount = 0 # counter variable for number of blocks in shortest path
        mouse = pygame.mouse.get_pos() # stores the (x,y) coordinates into the variable as a tuple 
        for event in pygame.event.get():    # mouse code
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if 14 <= mouse[0] <= 160 and 528 <= mouse[1] <= 562:
                    aStar() # starts pathfinding game
                if 404 <= mouse[0] <= 545 and 528 <= mouse[1] <= 562:
                    main() # main menu
            elif event.type == pygame.MOUSEMOTION and (event.buttons[0] or event.buttons[1] or event.buttons[2]): # mouse clicked
                clickWall(mouse) # creates walls while mouse is clicked and in motion
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN: 
                startflag = True   # this starts the pathfinding algorithm

        win.fill((0, 0, 0)) # grid and wall color
        for i in range(cols):    # creates the grid
            for j in range(rows):
                spot = grid[i][j] # individual tile
                spot.show(win, (255, 255, 255)) # background color
                if finishFlag and spot in path:
                    pathCount += 1 # if finishFlag is True and spot is in path then this must be in the shortest path so we increment
                    spot.show(win, (0, 255, 0)) # shortest path
                elif spot in closeSet:
                    spot.show(win, (255, 136, 25)) # potential paths
 
        # if mouse is hovered on a button it changes to lighter shade
        if 14 <= mouse[0] <= 160 and 528 <= mouse[1] <= 562: # text boxes at bottom 
            pygame.draw.rect(win, colorLight,[16,530,144,34])
            pygame.draw.rect(win, colorDark,[404,530,144,34]) 
        elif 404 <= mouse[0] <= 545 and 528 <= mouse[1] <= 562:
            pygame.draw.rect(win, colorLight,[404,530,144,34]) 
            pygame.draw.rect(win, colorDark,[16,530,144,34]) 
        else:
            pygame.draw.rect(win, colorDark, [404,530,144,34]) 
            pygame.draw.rect(win, colorDark, [16,530,144,34]) 
              
        start.show(win, (252, 23, 57)) # start point
        end.show(win, (25, 152, 255)) # end point

        tBox = pygame.font.SysFont('Verdana', 25) # font for text at bottom
        newGrid = tBox.render("New Grid", True , txtColor) 
        mainBut = tBox.render("Main Menu", True, txtColor) 
        countBox = tBox.render("Shortest Path: ", True, txtColor) 
        count2Box = tBox.render("" + str(pathCount) + " blocks", True, txtColor) # casts a string on the int pathcount so it can be printed
        # superimposing the text onto our buttons 
        win.blit(newGrid, (28,529))
        win.blit(mainBut, (408, 530))
        win.blit(countBox, (190,510))
        win.blit(count2Box,(210, 540))
        pygame.display.update()          
        pygame.display.flip() # updates the frames of the game

        if startflag:   # shortest path code
            if len(openSet) > 0: # if openSet contains anything then proceed
                winner = 0 # best node for closest path
                for i in range(len(openSet)):
                    if openSet[i].f < openSet[winner].f: # algorithm prioritizes node with the lowest f value
                        winner = i # winner will equal the lowest f value

                current = openSet[winner] # creates node current with lowest f value 
                
                if current == end: # current node is equal to the end node
                    temp = current # create temporary node
                    while temp.prev: # we have found the end node so now we must backtrack and find the shortest path
                        path.append(temp.prev) # add the temp node to our array path
                        temp = temp.prev # finds previous temp node
                        finishFlag = True # we have found the end point so set finishFlag to True so algorithm stops running
  
                if finishFlag == False: # current node is not the end node, finishFlag is Flase
                    openSet.remove(current) # removes current node from openSet 
                    closeSet.append(current) # and adds it to closeSet

                    for neighbor in current.neighbors: # iterates through all of current node's neighbors, eventually finding the best node to proceed
                        if neighbor in closeSet or neighbor.wall:
                            continue # if the neighbor is in closeSet or a wall then continue to next neighbor

                        # once we have a neighbor that either isn't a wall or in closeSet we set tempG to the current node's g value +1 and set newPath to False 
                        tempG = current.g + 1
                        newPath = False

                        if neighbor in openSet:
                            # newPath will only evaluate to False if tempG >= neighbor.g
                            if tempG < neighbor.g:
                                neighbor.g = tempG # we want the lowest g value
                                newPath = True
                        else:
                            neighbor.g = tempG
                            newPath = True
                            openSet.append(neighbor) # add the neighbor to the openSet

                        # either neighbor isn't in the openSet or it is in the openSet and tempG < neighbor.g
                        # if it isn't in the openSet then we will append it and check if it's the closest
                        # if tempG < neighbor.g then we have found a lower g value and thus may have found the best node to proceed
                        if newPath: 
                            neighbor.h = heuristics(neighbor, end) # updates h to the heuristically estimated distance from the current node to the end node 
                            neighbor.f = neighbor.g + neighbor.h # f = g + h
                            neighbor.prev = current # updates neighbor.prev so it's our current node            

            else: # openSet does not contain anything then there must not be a path
                noPath() # noPath menu

def noPath():
    # menu for when there is no path found
    pygame.init() # initializing the constructor   
    res = (600,600) # screen resolution 
    screen = pygame.display.set_mode(res) # opens up a window 
    screen.fill((0,0,0)) # fills the screen with a color 
    title = pygame.font.SysFont('Georgia', 75)
    but = pygame.font.SysFont('Verdana',25)  # fonts for text 
    titleCard = title.render("No Path Found", False, txtColor)
    startButton = but.render('New Grid' , True, txtColor) 
    quitButton = but.render('Quit', True, txtColor) 
    mainBut = but.render('Main Menu', True, txtColor) 

    while True: 
        mouse = pygame.mouse.get_pos() # stores the (x,y) coordinates into the variable as a tuple 
        for ev in pygame.event.get(): # any action from user
            if ev.type == pygame.QUIT: # quits game
                pygame.quit()       
            if ev.type == pygame.MOUSEBUTTONDOWN: #checks if a mouse is clicked 
                if 217 <= mouse[0] <= 359 and 207 <= mouse[1] <= 239:
                    aStar() # starts pathfinding game
                if 217 <= mouse[0] <= 359 and 290<= mouse[1] <= 322: 
                    main() # main menu
                if 251 <= mouse[0] <= 326 and 375 <= mouse[1] <= 407:
                    pygame.quit() # quit
          
          # if mouse is hovered on a button it changes to lighter shade 
        if 217 <= mouse[0] <= 359 and 207 <= mouse[1] <= 239: 
            pygame.draw.rect(screen,colorLight,[217,207,145,32]) 
        elif 217 <= mouse[0] <= 359 and 290 <= mouse[1] <= 322: 
            pygame.draw.rect(screen,colorLight,[217,290,145,32]) 
        elif 217 <= mouse[0] <= 326 and 375 <= mouse[1] <= 407:
            pygame.draw.rect(screen, colorLight, [251,375,75,32])
        else:
            pygame.draw.rect(screen,colorDark,[217,207,145,32]) 
            pygame.draw.rect(screen,colorDark,[217,290,145,32]) 
            pygame.draw.rect(screen,colorDark,[251,375,75,32])

        # superimposing the text onto screen
        screen.blit(startButton, (229,207))
        screen.blit(mainBut, (223,290))
        screen.blit(quitButton, (261,373))
        screen.blit(titleCard, (55, 86))
        pygame.display.update() # updates the frames of the game   

def main():
    # main menu
    pygame.init() # initializing the constructor
    res = (600,600) # screen resolution 
    pygame.display.set_caption("Main Menu")
    screen = pygame.display.set_mode(res) # opens up a window 
    screen.fill((0,0,0)) # fills the screen with a color 
    title = pygame.font.SysFont('Georgia', 75)
    but = pygame.font.SysFont('Verdana', 28) # fonts for text
    titleCard = title.render("Cam's Pathfinder", False, txtColor)
    startButton = but.render('Start', True, txtColor) 
    quitButton = but.render('Quit', True, txtColor)
    info1Button = but.render('Click the board while moving your', True, txtColor) 
    info2Button = but.render('mouse to draw walls. My pathfinding', True, txtColor)
    info3Button = but.render('algorithm will avoid the walls. The start', True, txtColor) 
    info4Button = but.render('point is red and the end point is blue', True, txtColor) 
    info5Button = but.render('Press the return key at any time to', True, txtColor) 
    info6Button = but.render('start the A Star pathfinding algorithm', True, txtColor) 
    
    while True: 
        mouse = pygame.mouse.get_pos() # stores the (x,y) coordinates into the variable as a tuple 
        for ev in pygame.event.get(): # any action from user
            if ev.type == pygame.QUIT: # quits game
                pygame.quit()       
            if ev.type == pygame.MOUSEBUTTONDOWN: # checks if a mouse is clicked 
                if 131 <= mouse[0] <= 206 and 200 <= mouse[1] <=240: 
                    aStar() # starts pathfinding game
                if 400 <= mouse[0] <= 475 and 200<= mouse[1] <= 240: 
                    pygame.quit() # quit

        # if mouse is hovered on a button it changes to lighter shade 
        if 131 <= mouse[0] <= 206 and 200 <= mouse[1] <= 240: 
            pygame.draw.rect(screen,colorLight,[131,207,75,32])
        elif 400 <= mouse[0] <= 526 and 200 <= mouse[1] <= 240: 
            pygame.draw.rect(screen,colorLight,[400,207,75,32]) 
        else:
            pygame.draw.rect(screen,colorDark,[131,207,75,32]) 
            pygame.draw.rect(screen,colorDark,[400,207,75,32]) 
    
        # superimposing the text onto screen
        screen.blit(startButton, (133,205))
        screen.blit(quitButton, (407,202))
        screen.blit(info1Button, (20,280)) 
        screen.blit(info2Button, (20,315)) 
        screen.blit(info3Button, (20,350)) 
        screen.blit(info4Button, (20,385)) 
        screen.blit(info5Button, (20,450)) 
        screen.blit(info6Button, (20,485)) 
        screen.blit(titleCard, (15, 86))
        pygame.display.update() # updates the frames of the game  

main() # runs program