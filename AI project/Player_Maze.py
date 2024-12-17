#import random for
import random
#Import pygame for game mechanics
import pygame
#Import Choice form random for 
from random import choice

#Intialize pygame
pygame.init()

TILE_SIZE = 40

#Load goal icon
goal_icon = pygame.image.load("star.png")
goal_icon = pygame.transform.scale(goal_icon, (TILE_SIZE, TILE_SIZE))

#Load player icon
player_icon = pygame.image.load("rocket.png")  
player_icon = pygame.transform.scale(player_icon, (TILE_SIZE , TILE_SIZE ))

#Intiallize maze tile size and screen dimensions 
TILE_SIZE = 40
WIDTH, HEIGHT = 1000, 600

#Intialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))

#Intiallize game clock
clock = pygame.time.Clock()

#Intiallizing buttons used on mode screen in a dictionary
Mode_buttons = {
    "Easy": pygame.Rect(400, 200, 200, 50),
    "Hard": pygame.Rect(400, 270, 200, 50),
    "Go to Home": pygame.Rect(400, 340, 200, 50),
}

#Intialize difficulty menu for player mode background
Maze_Player_background = pygame.image.load("8-bit-space-console-v0-zjbpg4wmdfvc1.webp")
Maze_Player_background = pygame.transform.scale(Maze_Player_background, (1000, 600))

#Intialize maze background in player mode
Maze_background = pygame.image.load("ThePinkClouds.jpeg")
Maze_background = pygame.transform.scale(Maze_background, (1000, 600))

#Intiallizing colors used in maze generation 
PINK = (255, 192, 203)
PURPLE = pygame.Color("purple")
WHITE = pygame.Color("white")
GREY = pygame.Color("grey")
BLACK = pygame.Color("black")

#Intiallizing button font
Button_font = pygame.font.Font("pixeboy-font/Pixeboy-z8XGD.ttf", 30)

#Function that opens difficulty menu (Builds background, generates buttons and returns difficulty level)
def difficulty_menu():
    while True:
        #Get mouse position
        mouse_pos = pygame.mouse.get_pos()

        #Build difficulty menu background
        screen.blit(Maze_Player_background, (0, 0))

        #Generate buttons
        for text, rect in Mode_buttons.items():
            color = (200, 200, 200) if rect.collidepoint(mouse_pos) else (108, 115, 212)
            pygame.draw.rect(screen, color, rect, border_radius=15)
            pygame.draw.rect(screen, (108, 115, 212), rect, 3, border_radius=15)
            text_surface = Button_font.render(text, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=rect.center)
            screen.blit(text_surface, text_rect)

        #For loop for getting actions
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for text, rect in Mode_buttons.items():
                    if rect.collidepoint(mouse_pos):
                        if text == "Easy":
                            return "easy"
                        elif text == "Hard":
                            return "hard"
                        elif text == "Go to Home":
                            import Main
                            Main.main()

        pygame.display.flip()



#Function that changes tile size and intializes columns and rows after getting difficulty level
def set_difficulty(level):
    global TILE_SIZE, cols, rows
    if level == "easy":
        TILE_SIZE = 80
    elif level == "hard":
        TILE_SIZE = 40

    cols, rows = WIDTH // TILE_SIZE, HEIGHT // TILE_SIZE

#Cell object (Basic building block of maze)
class Cell:

    #Cell constructor
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.walls = {"top": True, "down": True, "left": True, "right": True}
        self.visited = False

    #Function that draws the current cell of the maze (DFS)
    def draw_current_cell(self):
        x, y = self.x * TILE_SIZE, self.y * TILE_SIZE
        pygame.draw.rect(screen, BLACK, (x + 2, y + 2, TILE_SIZE - 2, TILE_SIZE - 2))

    #Function that draws lines of the maze
    def draw(self):
        x, y = self.x * TILE_SIZE, self.y * TILE_SIZE
        if self.visited:
            pygame.draw.rect(screen, BLACK, (x, y, TILE_SIZE, TILE_SIZE))
        if self.walls["top"]:
            pygame.draw.line(screen, GREY, (x, y), (x + TILE_SIZE, y), 2)
        if self.walls["right"]:
            pygame.draw.line(screen, GREY, (x + TILE_SIZE, y), (x + TILE_SIZE, y + TILE_SIZE), 2)
        if self.walls["down"]:
            pygame.draw.line(screen, GREY, (x + TILE_SIZE, y + TILE_SIZE), (x, y + TILE_SIZE), 2)
        if self.walls["left"]:
            pygame.draw.line(screen, GREY, (x, y + TILE_SIZE), (x, y), 2)

    #Function that checks if cell is visited
    def check_cell(self, x, y):
        find_index = lambda x, y: x + y * cols
        if x < 0 or x > cols - 1 or y < 0 or y > rows - 1:
            return False
        return grid_cells[find_index(x, y)]


    def check_neighbors(self):
        neighbors = []
        top = self.check_cell(self.x, self.y - 1)
        right = self.check_cell(self.x + 1, self.y)
        down = self.check_cell(self.x, self.y + 1)
        left = self.check_cell(self.x - 1, self.y)
        if top and not top.visited:
            neighbors.append(top)
        if right and not right.visited:
            neighbors.append(right)
        if down and not down.visited:
            neighbors.append(down)
        if left and not left.visited:
            neighbors.append(left)
        return choice(neighbors) if neighbors else False



def check_walls(current, next):
    dx = current.x - next.x
    if dx == 1:
        current.walls["left"] = False
        next.walls["right"] = False
    elif dx == -1:
        current.walls["right"] = False
        next.walls["left"] = False

    dy = current.y - next.y
    if dy == 1:
        current.walls["top"] = False
        next.walls["down"] = False
    elif dy == -1:
        current.walls["down"] = False
        next.walls["top"] = False


#Call difficulty menu and set difficulty of game
level = difficulty_menu()
set_difficulty(level)

#Intiallize grid cells
grid_cells = [Cell(col, row) for row in range(rows) for col in range(cols)]

#Intiallize stack
stack = []


used_cells = set()

#Intiallize player position at first cell of the maze
player_position = [0, 0]  

#Function that generates the goal at a random position
def set_goal():

    #Declare global goal position
    global goal_position

    while True:

        #Choose random cell as goal position as long as it is not at start of grid
        random_cell = random.choice(grid_cells)
        if random_cell != grid_cells[0]:
            goal_position = (
                random_cell.x * TILE_SIZE + TILE_SIZE // 2,
                random_cell.y * TILE_SIZE + TILE_SIZE // 2,
            )
            break

#Draw goal 
def draw_goal():
    if goal_position:
        goal_x, goal_y = goal_position
        icon_rect = goal_icon.get_rect(center=(goal_x, goal_y))
        screen.blit(goal_icon, icon_rect)

#Draw player 
def draw_player():
    player_x = player_position[0] * TILE_SIZE + TILE_SIZE // 2
    player_y = player_position[1] * TILE_SIZE + TILE_SIZE // 2
    player_rect = player_icon.get_rect(center=(player_x, player_y))
    screen.blit(player_icon, player_rect)

#Call set goal
set_goal()

#Main function
def main():
    colors, color = [], 40
    current_cell = grid_cells[0]
    while True:
        #Build Maze background
        screen.blit(Maze_background, (0, 0))

        #Player movement mechanics 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                current_cell = grid_cells[player_position[1] * cols + player_position[0]]
                if event.key == pygame.K_UP and not current_cell.walls["top"]:
                    player_position[1] -= 1
                elif event.key == pygame.K_DOWN and not current_cell.walls["down"]:
                    player_position[1] += 1
                elif event.key == pygame.K_LEFT and not current_cell.walls["left"]:
                    player_position[0] -= 1
                elif event.key == pygame.K_RIGHT and not current_cell.walls["right"]:
                    player_position[0] += 1

        
        [cell.draw() for cell in grid_cells]
        current_cell.visited = True
        current_cell.draw_current_cell()

        [pygame.draw.rect(screen, colors[i],
                          (cell.x * TILE_SIZE + 5, cell.y * TILE_SIZE + 5, TILE_SIZE - 10, TILE_SIZE - 10),
                          border_radius=12) for i, cell in enumerate(stack)]

        next_cell = current_cell.check_neighbors()
        if next_cell:
            stack.append(current_cell)
            next_cell.visited = True
            check_walls(current_cell, next_cell)
            colors.append((min(color, 255), 10, 100))
            color += 1
            current_cell = next_cell
        elif stack:
            current_cell = stack.pop()

        #Draw goal icon
        draw_goal()

        #Draw player icon
        draw_player()
        
        #Intialize player x and y position
        player_x = player_position[0] * TILE_SIZE + TILE_SIZE // 2
        player_y = player_position[1] * TILE_SIZE + TILE_SIZE // 2

        

        if abs(player_x - goal_position[0]) < TILE_SIZE // 2 and abs(player_y - goal_position[1]) < TILE_SIZE // 2:
            import Player_won
            Player_won.main()
            pygame.time.delay(2000)
            return

        
        pygame.display.flip()

        #Setting clock to 80 increases maze generation
        clock.tick(80)


main()
