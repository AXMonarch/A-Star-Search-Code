import pygame
import math
from queue import PriorityQueue

WIDTH = 500
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Pathfinder Algorithm")

barrier_coords = [
    (0,0),(0,1),(0,2),(0,3),(0,5),(0,6),(0,7),(0,9),(0,10),(0,11),(0,15),
    (1,0),(1,1),(1,2),(1,3),(1,5),(1,6),(0,7),(1,9),(1,10),(1,11),(1,15),
    (2,0),(2,1),(2,5),(2,9),(2,10),(2,11),(2,14),(2,15),
    (3,13),(3,14),(3,15),
    (4,1),(4,5),(4,10),(4,11),(4,12),(4,13),(4,14),(4,15),
    (5,1),(5,5),
    (6,1),(6,2),(6,3),(6,5),(6,6),(6,7),(6,8),(6,10),(6,11),
    (7,5),(7,6),(7,7),(7,8),(7,10),(7,11),
    (8,5),(8,6),(8,7),(8,8),(8,10),(8,11),
    (9,15),
    (10,3),(10,7),(10,8),(10,10),(10,11),(10,15),
    (11,0),(11,3),(11,7),(11,8),(11,10),(11,11),(11,15),
    (12,3),(12,7),(12,8),(12,10),(12,11),(12,15),
    (13,8),(13,10),(13,11),(13,15),
    (14,0),(14,1),(14,2),(14,3),(14,5),(14,6),(14,7),(14,8),
    (15,0),(15,1),(15,2),(15,3),(15,4),(15,5),(15,6),(15,7),(15,8),(15,10),(15,11)
]

# COLORS
CUSTOM_COLORS = {
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0),
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "purple": (128, 0, 128),
    "orange": (255, 165, 0),
    "grey": (128, 128, 128),
    "turquoise": (64, 224, 208)
}

class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = CUSTOM_COLORS["white"]
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows
        self.node_type = "normal"

    def get_position(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == CUSTOM_COLORS["red"]

    def is_open(self):
        return self.color == CUSTOM_COLORS["green"]

    def is_barrier(self):
        return self.color == CUSTOM_COLORS["black"]

    def is_start(self):
        return self.color == CUSTOM_COLORS["orange"]

    def is_end(self):
        return self.color == CUSTOM_COLORS["turquoise"]

    def reset(self):
        self.color = CUSTOM_COLORS["white"]

    def make_closed(self):
        self.color = CUSTOM_COLORS["red"]

    def make_open(self):
        self.color = CUSTOM_COLORS["green"]

    def make_start(self):
        self.color = CUSTOM_COLORS["orange"]
        self.node_type = "home"

    def make_barrier(self):
        self.color = CUSTOM_COLORS["black"]

    def make_end(self):
        self.color = CUSTOM_COLORS["turquoise"]
        self.node_type = "restaurant"

    def make_path(self):
        self.color = CUSTOM_COLORS["purple"]

    def make_driver(self):
        self.color = CUSTOM_COLORS["grey"]
        self.node_type = "driver"

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False

def create_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            if (i, j) in barrier_coords:
                node.make_barrier()
            grid[i].append(node)

    homes = [(0,4), (9, 7), (2, 13)]
    restaurants = [(0, 8), (13, 0), (15, 15)]
    drivers = [(0, 14), (5, 15), (13, 7)]

    for row in range(rows):
        for col in range(rows):
            node = grid[row][col]
            if (row, col) in homes:
                node.make_start()
            elif (row, col) in restaurants:
                node.make_end()
            elif (row, col) in drivers:
                node.make_driver()

    return grid

def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, CUSTOM_COLORS["grey"], (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, CUSTOM_COLORS["grey"], (j * gap, 0), (j * gap, width))

def draw(win, grid, rows, width):
    win.fill(CUSTOM_COLORS["white"])

    for row in grid:
        for node in row:
            node.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()

def get_clicked_position(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col

def heuristic(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def main(win, width):
    ROWS = 16
    grid = create_grid(ROWS, width)

    start = None
    end = None

    run = True
    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_position(pos, ROWS, width)
                node = grid[row][col]
                if not start and node != end:
                    start = node
                    start.make_start()

                elif not end and node != start:
                    end = node
                    end.make_end()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)

                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = create_grid(ROWS, width)

    pygame.quit()

def algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = heuristic(start.get_position(), end.get_position())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + heuristic(neighbor.get_position(), end.get_position())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False

def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

main(WIN, WIDTH)
