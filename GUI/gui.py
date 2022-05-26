import pygame

WIDTH = 1000
HEIGHT = 600


GRID_WIDTH = 1000
GRID_HEIGHT = 500
GRID_SHIFT = 0
GRID_SIZE = 4
LARGE_FONT = int(220/GRID_SIZE)
SMALL_FONT = int(160/GRID_SIZE)

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
            pygame.draw.line(screen, (0, 0, 0), ((points[i][1]+1)*(GRID_WIDTH/GRID_SIZE), (points[i][0])*(GRID_HEIGHT/GRID_SIZE)), ((points[i][1] + 1)*(GRID_WIDTH/GRID_SIZE), (points[i][0]+1)*(GRID_HEIGHT/GRID_SIZE)), 5)
        if pointFlags[1] == True:
            # left
            pygame.draw.line(screen, (0, 0, 0), ((points[i][1])*(GRID_WIDTH/GRID_SIZE), points[i][0]*(GRID_HEIGHT/GRID_SIZE)), (points[i][1]*(GRID_WIDTH/GRID_SIZE), (points[i][0]+1)*(GRID_HEIGHT/GRID_SIZE)), 5)
        if pointFlags[2] == True:
            # top
            pygame.draw.line(screen, (0, 0, 0), (points[i][1]*(GRID_WIDTH/GRID_SIZE), (points[i][0])*(GRID_HEIGHT/GRID_SIZE)), ((points[i][1]+1)*(GRID_WIDTH/GRID_SIZE), points[i][0]*(GRID_HEIGHT/GRID_SIZE)), 5)
        if pointFlags[3] == True:
            # bottom
            pygame.draw.line(screen, (0, 0, 0), (points[i][1]*(GRID_WIDTH/GRID_SIZE), (points[i][0]+1)*(GRID_HEIGHT/GRID_SIZE)), ((points[i][1]+1)*(GRID_WIDTH/GRID_SIZE), (points[i][0] + 1)*(GRID_HEIGHT/GRID_SIZE)), 5)

def drawGrid(smallArr = None, largeArr = None):
    # Draw the grid with outline    
    for x in range(GRID_SIZE + 1):
        pygame.draw.line(screen, (0, 0, 0), ((x * GRID_WIDTH / GRID_SIZE) + GRID_SHIFT, GRID_SHIFT), ((x * GRID_WIDTH / GRID_SIZE) + GRID_SHIFT, GRID_HEIGHT), 2)
        pygame.draw.line(screen, (0, 0, 0), (GRID_SHIFT, (x * GRID_HEIGHT / GRID_SIZE) + GRID_SHIFT), (GRID_WIDTH , (x * GRID_HEIGHT / GRID_SIZE) + GRID_SHIFT), 2)
    # Add the large font
    if largeArr != None:
        for x in range(len(largeArr)):
            for y in range(len(largeArr)):
                if(largeArr[y][x] != -1):
                    # add text 
                    font = pygame.font.SysFont(None, LARGE_FONT)
                    text = font.render(str(largeArr[y][x]), True, (0, 0, 0))
                    screen.blit(text, ((x * GRID_WIDTH / GRID_SIZE) + GRID_SHIFT + (GRID_WIDTH / GRID_SIZE / 2) - (text.get_width() / 2), (y * GRID_HEIGHT / GRID_SIZE) + GRID_SHIFT + (GRID_HEIGHT / GRID_SIZE / 2) - (text.get_height() / 2)))
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
    
def main():
    global screen
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("KenKen Puzzle")
    screen.fill((255, 255, 255))

    # initalize the board
    initArr = [[2, 2, 0, 12], [2, 2, 2, 2], [2, 2, 2, 2], [2, 2, 2, 2]]
    small = [['0+', '', 2, 3], [0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3]]
    drawGrid(smallArr=small, largeArr=initArr)
    addButton(20, 550, 200, 25, (130, 130, 130), "Start", (255, 255, 255))

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
                if pos[0] > 20 and pos[0] < 220 and pos[1] > 550 and pos[1] < 575:
                    print("Start")
                    break
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

main()