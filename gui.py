import pygame
import gen
import solver
import classes
import random
import time

WIDTH = 1200
HEIGHT = 850


GRID_WIDTH = 1200
GRID_HEIGHT = 700
GRID_SHIFT = 0
GRID_SIZE = -1


#     2
#   1   0
#     3
def addCage(points):
    # draw a rectangle border
    # pygame.draw.rect(screen, (0, 0, 0), (points[1]*(GRID_WIDTH/GRID_SIZE), points[0]*(GRID_HEIGHT/GRID_SIZE), (points[3]-points[1]+1)*(GRID_WIDTH/GRID_SIZE), (points[2]-points[0]+1)*(GRID_HEIGHT/GRID_SIZE)), 5)

    pointsLen = len(points)
    for i in  range(len(points)):        
        pointFlags = [True]*4
        # check sides
        if points[i][0] == points[(i + 1) % pointsLen][0]:
            # check right or left using y
            if points[i][1] - points[(i + 1) % pointsLen][1] < 0:
                # dont draw right
                pointFlags[0] = False
            else:
                # dont draw left
                pointFlags[1] = False

        if points[i][0] == points[(i - 1) % pointsLen][0]:
            # check right or left using y
            if points[i][1] - points[(i - 1) % pointsLen][1] < 0:
                # dont draw right
                pointFlags[0] = False
            else:
                # dont draw left
                pointFlags[1] = False
        # check top or bottom
        if points[i][1] == points[(i + 1) % pointsLen][1]:
            # check right or left using y
            if points[i][0] - points[(i + 1) % pointsLen][0] < 0:
                # dont draw bottom
                pointFlags[3] = False
            else:
                # dont draw top
                pointFlags[2] = False
        if points[i][1] == points[(i - 1) % pointsLen][1]:
            # check right or left using y
            if points[i][0] - points[(i - 1) % pointsLen][0] < 0:
                # dont draw bottom
                pointFlags[3] = False
            else:
                # dont draw top
                pointFlags[2] = False

        if pointFlags[0] == True:
            # right
            pygame.draw.line(screen, (0, 0, 0), ((points[i][1]+1)*(GRID_WIDTH/GRID_SIZE), (points[i][0])*(GRID_HEIGHT/GRID_SIZE)), ((points[i][1] + 1)*(GRID_WIDTH/GRID_SIZE), (points[i][0]+1)*(GRID_HEIGHT/GRID_SIZE)), 7)
        if pointFlags[1] == True:
            # left
            pygame.draw.line(screen, (0, 0, 0), ((points[i][1])*(GRID_WIDTH/GRID_SIZE), points[i][0]*(GRID_HEIGHT/GRID_SIZE)), (points[i][1]*(GRID_WIDTH/GRID_SIZE), (points[i][0]+1)*(GRID_HEIGHT/GRID_SIZE)), 7)
        if pointFlags[2] == True:
            # top
            pygame.draw.line(screen, (0, 0, 0), (points[i][1]*(GRID_WIDTH/GRID_SIZE), (points[i][0])*(GRID_HEIGHT/GRID_SIZE)), ((points[i][1]+1)*(GRID_WIDTH/GRID_SIZE), points[i][0]*(GRID_HEIGHT/GRID_SIZE)), 7)
        if pointFlags[3] == True:
            # bottom
            pygame.draw.line(screen, (0, 0, 0), (points[i][1]*(GRID_WIDTH/GRID_SIZE), (points[i][0]+1)*(GRID_HEIGHT/GRID_SIZE)), ((points[i][1]+1)*(GRID_WIDTH/GRID_SIZE), (points[i][0] + 1)*(GRID_HEIGHT/GRID_SIZE)), 7)

def drawGrid(smallArr = None, largeArr = None):
    LARGE_FONT = int(220/GRID_SIZE)
    SMALL_FONT = int(160/GRID_SIZE)
    # Draw the grid with outline    
    for x in range(GRID_SIZE + 1):
        pygame.draw.line(screen, (0, 0, 0), ((x * GRID_WIDTH / GRID_SIZE) + GRID_SHIFT, GRID_SHIFT), ((x * GRID_WIDTH / GRID_SIZE) + GRID_SHIFT, GRID_HEIGHT), 2)
        pygame.draw.line(screen, (0, 0, 0), (GRID_SHIFT, (x * GRID_HEIGHT / GRID_SIZE) + GRID_SHIFT), (GRID_WIDTH , (x * GRID_HEIGHT / GRID_SIZE) + GRID_SHIFT), 2)
    # Add the large font
    if largeArr != None:
        for x in range(GRID_SIZE):            
            for y in range(GRID_SIZE):
            # if(largeArr[x] != -1):
                        # add text                 
                font = pygame.font.SysFont(None, LARGE_FONT)
                text = font.render(str(largeArr[(x*GRID_SIZE) + y]), True, (0, 0, 0))
                screen.blit(text, ((y * GRID_WIDTH / GRID_SIZE) + GRID_SHIFT + (GRID_WIDTH / GRID_SIZE / 2) - (text.get_width() / 2), (x * GRID_HEIGHT / GRID_SIZE) + GRID_SHIFT + (GRID_HEIGHT / GRID_SIZE / 2) - (text.get_height() / 2)))
    # Add the small font
    if smallArr != None:
        for x in range(len(smallArr)):
            for y in range(len(smallArr)):
                if(smallArr[y][x] != -1):
                    # add text 
                    font = pygame.font.SysFont(None, SMALL_FONT)
                    text = font.render(str(smallArr[y][x]), True, (0, 0, 0))
                    screen.blit(text, ((x * GRID_WIDTH / GRID_SIZE) + GRID_SHIFT + (GRID_WIDTH / GRID_SIZE / 2) - (GRID_WIDTH/(GRID_SIZE*2.7)), (y * GRID_HEIGHT / GRID_SIZE) + GRID_SHIFT + (GRID_HEIGHT / GRID_SIZE / 2) - (GRID_HEIGHT/(GRID_SIZE*4))))

def addButton(x, y, width, height, color, text, textColor):
    pygame.draw.rect(screen, color, (x, y, width, height))
    font = pygame.font.SysFont(None, 30)
    text = font.render(text, True, textColor)
    screen.blit(text, (x + (width / 2) - (text.get_width() / 2), y + (height / 2) - (text.get_height() / 2)))
    return x, y, x + width, y + height


def perfomanceAnalysis(testNo):
    time1 = 0
    time2 = 0
    time3 = 0
    avgGridSize = 0


    # clear screen
    screen.fill((255, 255, 255))
    pygame.display.update() 
    
    font = pygame.font.SysFont(None, 25)

    for i in range(testNo):
        # generate random number
        num = random.randint(2, 6)
        avgGridSize += num        

        # write text to screen
        text = font.render("Running test " + str(i+1) + " on size: " + str(num), True, (0, 0, 0))
        screen.blit(text, ((WIDTH/2) - 130, (HEIGHT/2) - 50))
        pygame.display.update()

        size, currentBoard = gen.generate(num)
        Kenken = classes.Kenken(num, currentBoard)  
        
        start = time.time()
        assignment = solver.backtracking_search(Kenken)                                    
        end = time.time()
        time1 += (end - start)

        start = time.time()
        assignment = solver.backtracking_search(Kenken, inference = solver.mac)                                       
        end = time.time()
        time2 += (end - start)

        start = time.time()
        assignment = solver.backtracking_search(Kenken, inference = solver.forward_checking)        
        end = time.time()
        time3 += (end - start)

        screen.fill((255, 255, 255))
        pygame.display.update()

    # write text to screen
    screen.fill((255, 255, 255))
    pygame.display.update()    
    text = font.render("Total Backtracking Search: " + '{:04.4f}'.format(time1) + " Seconds", True, (0, 0, 0))
    screen.blit(text, ((WIDTH/2) - 295, (HEIGHT/2) - 200 + 10))
    text = font.render("Total Backtracking Search with MAC: " + '{:04.4f}'.format(time2) + " Seconds", True, (0, 0, 0))
    screen.blit(text, ((WIDTH/2) - 295, (HEIGHT/2) - 200 + 40))
    text = font.render("Total Backtracking Search with Forward Checking: " + '{:04.4f}'.format(time3) + " Seconds", True, (0, 0, 0))
    screen.blit(text, ((WIDTH/2) - 295, (HEIGHT/2) - 200 + 70))
    text = font.render("Average Backtracking Search Per Test: " + '{:04.4f}'.format(time1/testNo) + " Seconds", True, (0, 0, 0))
    screen.blit(text, ((WIDTH/2) - 295, (HEIGHT/2) - 200 + 130))
    text = font.render("Average Backtracking Search with MAC Per Test: " + '{:04.4f}'.format(time2/testNo) + " Seconds", True, (0, 0, 0))
    screen.blit(text, ((WIDTH/2) - 295, (HEIGHT/2) - 200 + 160))
    text = font.render("Average Backtracking Search with Forward Checking Per Test: " + '{:04.4f}'.format(time3/testNo) + " Seconds", True, (0, 0, 0))
    screen.blit(text, ((WIDTH/2) - 295, (HEIGHT/2) - 200 + 190))
    text = font.render("Average Grid Size: " + str(int(avgGridSize/testNo)), True, (0, 0, 0))
    screen.blit(text, ((WIDTH/2) - 295, (HEIGHT/2) - 200 + 240))
    pygame.display.update()


def main():
    global screen   
    global GRID_SIZE
    global currentBoard 
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("KenKen Puzzle")
    screen.fill((255, 255, 255))
    font = pygame.font.SysFont(None, 30)   
             
    while True:
        if GRID_SIZE == -1:

            performance = False            
        
            input_box = pygame.Rect((WIDTH - 140)/2, (HEIGHT - 10)/2, 250, 30)
            active = False
            text = ''
            done = False

            while True:
                for event in pygame.event.get():
                    # button clicked
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        if performance:
                            if pos[0] > (WIDTH/2) - 270 and pos[1] > (HEIGHT/2) + 100 and pos[0] < (WIDTH/2) - 270 + 250 and pos[1] < (HEIGHT/2) + 100 + 25:
                                screen.fill((255, 255, 255))
                                pygame.display.update()
                                perfomanceAnalysis(100)
                                performance = True 
                            elif pos[0] > (WIDTH/2) + 30 and pos[1] > (HEIGHT/2) + 100 and pos[0] < (WIDTH/2) + 30 + 250 and pos[1] < (HEIGHT/2) + 100 + 25:
                                performance = False
                                screen.fill((255, 255, 255))
                                pygame.display.update()
                        if pos[0] > (WIDTH - 140)/2 and pos[1] > (HEIGHT - 10)/2 and pos[0] < ((WIDTH - 140)/2)+200 and pos[1] < ((HEIGHT - 10)/2) + 30:                   
                            # Toggle the active variable.
                            active = not active
                        elif pos[0] > ((WIDTH)/2) - 170 and pos[1] > (HEIGHT - 250)/2 and pos[0] < (((WIDTH)/2) - 175) + 300 and pos[1] < ((HEIGHT - 250)/2) + 30:
                            perfomanceAnalysis(100)
                            performance = True                            
                        else:
                            active = False
                        # Change the current color of the input box.
                        color = (150, 150, 150) if active else (0, 0, 0)
                    if event.type == pygame.KEYDOWN:
                        if active:
                            if event.key == pygame.K_RETURN:                                
                                GRID_SIZE = int(text)
                                break
                                text = ''
                            elif event.key == pygame.K_BACKSPACE:
                                text = ''                         
                            else:
                                # check that the input is a number                                
                                if event.unicode.isdigit():                                    
                                    text += event.unicode
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()     
                    pygame.display.update()                             

                if(not performance):                                        
                    addButton(((WIDTH)/2) - 170 , (HEIGHT - 250)/2, 300, 25, (130,130,130), "Run Performance Analysis", (255,255,255))
                    label = font.render("Enter Grid Size:", True, (0, 0, 0))
                    screen.blit(label, ((WIDTH - 200 )/2 , (HEIGHT/2) - 40))
                    # Render the current text.                    
                    txt_surface = font.render(text, True, (0, 0, 0))
                    # Resize the box if the text is too long.
                    input_box.w = 100
                    # Blit the text
                    screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
                    # Blit the input_box rect.
                    pygame.draw.rect(screen, (0, 0, 0), input_box, 2)    
                                        
                    if GRID_SIZE != -1:
                        # clear screen                                      
                        screen.fill((255, 255, 255))
                        pygame.display.update()
                        break
                else:
                    addButton((WIDTH/2) - 270, (HEIGHT/2) + 100, 250, 25, (130,130,130), "Re-run Tests", (255,255,255))
                    addButton((WIDTH/2) + 30, (HEIGHT/2) + 100, 250, 25, (130,130,130), "Run Game", (255,255,255))
                pygame.display.update()

        else:

            # initalize the board
            size, currentBoard = gen.generate(GRID_SIZE)
            Kenken = classes.Kenken(GRID_SIZE, currentBoard)
            smallArr = [[''] * GRID_SIZE for i in range(GRID_SIZE)]            
            for x in currentBoard:
                operation = x[1]
                operationNo = x[2]                
                cages = []
                if operation == '.':
                    operation = ''
                smallArr[int(x[0][0][0])-1][int(x[0][0][1])-1] = str(abs(operationNo)) + operation
                for y in x[0]:
                    tmp = tuple(i - 1 for i in y)
                    cages.append(tmp) 
                addCage(cages)                         
            drawGrid(smallArr=smallArr)
            buttonX = HEIGHT - 90
            b11, b12, b13, b14 = addButton((WIDTH / 2) - 250, buttonX - 40, 500, 25, (130, 130, 130), "Solve Using Backtracking Only", (255, 255, 255))
            b21, b22, b23, b24 = addButton((WIDTH / 2) - 250, buttonX, 500, 25, (130, 130, 130), "Solve Using Backtracking With Arc Consistency ", (255, 255, 255))
            b31, b32, b33, b34 = addButton((WIDTH / 2) - 250, buttonX + 40, 500, 25, (130, 130, 130), "Solve Using Backtracking With Forward Checking ", (255, 255, 255))
            b41, b42, b43, b44 = addButton(WIDTH - 200, buttonX, 150, 25, (130, 130, 130), "New Game ", (255, 255, 255))
        
            pygame.display.update()

            while True:
                for event in pygame.event.get():
                    # button clicked
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        if pos[0] > b11 and pos[1] > b12 and pos[0] < b13 and pos[1] < b14:                             
                            assignment = solver.backtracking_search(Kenken)                            
                            solution = solver.gui_input(assignment, GRID_SIZE)                              
                            drawGrid(smallArr=smallArr, largeArr=solution)                                                            
                            break  
                        if pos[0] > b21 and pos[1] > b22 and pos[0] < b23 and pos[1] < b24:
                            assignment = solver.backtracking_search(Kenken, inference = solver.mac)                            
                            solution = solver.gui_input(assignment, GRID_SIZE)                              
                            drawGrid(smallArr=smallArr, largeArr=solution)                  
                            break  
                        if pos[0] > b31 and pos[1] > b32 and pos[0] < b33 and pos[1] < b34:
                            assignment = solver.backtracking_search(Kenken, inference = solver.forward_checking)                            
                            solution = solver.gui_input(assignment, GRID_SIZE)                              
                            drawGrid(smallArr=smallArr, largeArr=solution)                  
                            break     
                        if pos[0] > b41 and pos[1] > b42 and pos[0] < b43 and pos[1] < b44:
                            GRID_SIZE = -1
                            break                                          
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()     
                if GRID_SIZE == -1:
                    screen.fill((255, 255, 255))
                    pygame.display.update()
                    break
                pygame.display.update()
main()