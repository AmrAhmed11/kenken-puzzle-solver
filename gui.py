import pygame
import gen
import solver
import classes

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
            # add input field
            # add text     
            text = font.render("Enter Grid Size:", True, (0, 0, 0))
            screen.blit(text, ((WIDTH - 140 )/2 , (HEIGHT/2) - 40))
            input_box = pygame.Rect((WIDTH - 140)/2, (HEIGHT - 10)/2, 200, 30)
            active = False
            text = ''
            done = False

            while True:
                for event in pygame.event.get():
                    # button clicked
                    if event.type == pygame.MOUSEBUTTONDOWN:                 
                        pos = pygame.mouse.get_pos()
                        if pos[0] > (WIDTH - 140)/2 and pos[1] > (HEIGHT - 10)/2 and pos[0] < ((WIDTH - 140)/2)+200 and pos[1] < ((HEIGHT - 10)/2) + 30:                   
                            # Toggle the active variable.
                            active = not active
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
                                text = text[:-1]
                            else:
                                # check that the input is a number                                
                                if event.unicode.isdigit():                                    
                                    text += event.unicode
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()     
                    pygame.display.update()

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
    
            # points = [[0, 2], [0, 3], [1, 3]]
            # addCage(points)
            # points = [[2, 1], [2, 2], [3, 2]]
            # addCage(points)
            # points = [[0, 0], [0, 1], [1, 1], [1, 2]]
            # addCage(points)
        
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