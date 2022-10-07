from ipaddress import collapse_addresses
import math
import queue
import pygame

width = 500
box = pygame.display.set_mode((width, width)) #display is square
pygame.display.set_caption("Path Finding Visualizer")

ORANGE = (253, 132, 31)
BLUE = (39, 123, 192)
PINK = (205, 16, 77)
PURPLE = (156, 44, 119)
DARKPURPLE = (65, 21, 48)
DARKYELLOW = (250, 194, 19)
BROWN = (135, 100, 69)
BORDER = (139, 188, 204)
BLACK = (6, 40, 61)
GREEN = (127, 183, 126)
LIGHT = (247, 246, 220)

class Node:

    def __init__(self, row, col, width, rowsCount):
        self.adjacent = []
        self.xCordinate = row*width
        self.yCordinate = col*width
        self.row = row
        self.col = col
        self.rowsCount = rowsCount
        self.color = LIGHT
        self.width = width
    
    def getPosition(self):
        return self.row, self.col

    def is_blank(self):
        if self.color == LIGHT:
            return True
        else:
            return False
    
    def is_filled(self):
        if self.color == BLUE:
            return True
        else:
            return False
            
    
    def is_inSet(self):
        if self.color == GREEN:
            return True
        else:
            return False

    def is_blocked(self):
        if self.color == BLACK:
            return True
        else:
            return False

    def is_startingPoint(self):
        if self.color == ORANGE:
            return True
        else:
            return False

    def is_stopPoint(self):
        if self.color == PINK:
            return True
        else:
            return False

    def reset(self):
        self.color=LIGHT

    def setStop(self):
        self.color = PINK

    def setStart(self):
        self.color = ORANGE

    def setBlock(self):
        self.color = BLACK

    def setFill(self):
        self.color = BLUE

    def setInSet(self):
        self.color = GREEN

    def setPath(self):
        self.color = PURPLE

    def makeRect(self, box):
        pygame.draw.rect(box, self.color, (self.xCordinate, self.yCordinate, self.width, self.width))

    def make_adjacents(self, mat):
        self.adjacent = []
        if self.col < self.rowsCount-1 and not mat[self.row][self.col+1].is_blocked():
            self.adjacent.append(mat[self.row][self.col+1])
        if self.col >0 and not mat[self.row][self.col-1].is_blocked():
            self.adjacent.append(mat[self.row][self.col-1])
        if self.row < self.rowsCount-1 and not mat[self.row+1][self.col].is_blocked():
            self.adjacent.append(mat[self.row+1][self.col])
        if self.row >0  and not mat[self.row-1][self.col].is_blocked():
            self.adjacent.append(mat[self.row-1][self.col])

    def __lt__(self, other):
        return False


#Function to create the grid
def drawMatrix(numRow, width):
    mat = []
    widthRow = width//numRow
    for i in range(numRow):
        mat.append([])
        for j in range(numRow):
            node = Node(i,j,widthRow, numRow)
            mat[i].append(node)
    return mat

#Function to draw the grid lines
def drawLines(box, numRow, width):
    widthRow = width//numRow
    for i in range(numRow):
        pygame.draw.line(box, BORDER, (0, i*widthRow), (width, i*widthRow))
        for j in range(numRow):
            pygame.draw.line(box, BORDER, (j*widthRow,0), (j*widthRow, width))

#Function to draw everything
def draw(box, matrix, numRow, width):
        box.fill(LIGHT)
        for i in matrix:
            for node in i:
                node.makeRect(box)
        drawLines(box, numRow, width)
        pygame.display.update()

#Function to get clicked postion of mouse in the grid
def mouse_pos(pos, rows,width):
    widthRow = width//rows
    (x, y) = pos
    row = x//widthRow
    col = y//widthRow
    return (row, col)


def makePath(origin, curr, draw):
    while curr in origin:
        curr = origin[curr]
        curr.setPath()
        draw()

#Manhatten distance between two nodes
#We assume the distance between these two nodes as following
def Estimation(c, d):
    x1, y1 = c
    x2, y2 = d
    return abs(y2-y1) + abs(x1-x2)

def dijkstra(draw, mat, start, stop):
    count = 0 #a tie breaker
    pri = queue.PriorityQueue()
    pri.put((0, count, start))
    origin = {}
    a = {node: float("inf") for row in mat for node in row}
    a[start]=0
    b = {node: float("inf") for row in mat for node in row}
    b[start]= Estimation(start.getPosition(), stop.getPosition())
    #set so that it can give smallest element
    pri_track = {start} #to keep track of all the items in the priority queue and not in the priority queue
    while not pri.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        curr = pri.get()[2]
        pri_track.remove(curr)
        if curr == stop:
            stop.setPath()
            makePath(origin, stop, draw) #we should make path
            return True
        for adj in curr.adjacent:
            temp_a = a[curr] + 1
            if temp_a < a[adj]:
                origin[adj] = curr
                a[adj] = temp_a
                b[adj] = temp_a + Estimation(adj.getPosition(), stop.getPosition())
                if adj not in pri_track:
                    count = count+1
                    pri.put((b[adj], count, adj))
                    pri_track.add(adj)
                    adj.setInSet()
        draw()
        if curr!=start:
            curr.setFill()
    return False

def main(box, width):
    ROWS = 40
    mat = drawMatrix(ROWS, width)
    start = None
    stop = None
    run = True
    started = False
    while run:
        draw(box, mat, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            #To continue if the algorithm has started already
            #we cannot change the color of the tiles once the algorithm starts
            if started:
                continue
            if pygame.mouse.get_pressed()[0]: #left mouse button
                pos = pygame.mouse.get_pos()
                (row,col) = mouse_pos(pos, ROWS, width)
                node = mat[row][col]
                if not start and node!= stop:
                    start = node
                    start.setStart()
                elif not stop and node != start:
                    stop = node
                    stop.setStop()
                elif node != stop and node != start:
                    node.setBlock()

            elif pygame.mouse.get_pressed()[2]: #right mouse button
                pos = pygame.mouse.get_pos()
                (row,col) = mouse_pos(pos,ROWS,width)
                node = mat[row][col]
                node.reset() #for erasing the color if right click
                if node == start:
                    start = None
                if node == stop:
                    stop = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not started and start and stop:
                    for row in mat:
                        for node in row:
                            node.make_adjacents(mat)
                    dijkstra(lambda: draw(box, mat, ROWS, width), mat, start, stop)

                if event.key == pygame.K_c:
                    start = None
                    stop = None
                    mat = drawMatrix(ROWS, width)
    pygame.quit()


main(box, width)
