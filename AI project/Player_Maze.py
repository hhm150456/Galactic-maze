import random 
import pygame
from random import choice


pygame.init()

TILE_SIZE =40
goal_icon = pygame.image.load("depositphotos_705384476-stock-illustration-star-functional-game-related-sticker.jpg") 
goal_icon = pygame.transform.scale(goal_icon, (TILE_SIZE // 2, TILE_SIZE // 2))  

WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

Mode_buttons = {
    "Easy": pygame.Rect(400, 200, 200, 50),  
    "Hard": pygame.Rect(400, 270, 200, 50),
    "Go to Home": pygame.Rect(400, 340, 200, 50),
}

Maze_Player_background = pygame.image.load("8-bit-space-console-v0-zjbpg4wmdfvc1.webp")  
Maze_Player_background = pygame.transform.scale(Maze_Player_background, (1000, 600)) 
Maze_background = pygame.image.load("pixel-art-night-sky-starry-space-with-shooting-stars-8-bit-pixelated-game-galaxy-seamless-background-vector.jpg")  
Maze_background = pygame.transform.scale(Maze_background, (1000, 600)) 
PINK = (255, 192, 203)
PURPLE = pygame.Color('purple')

WHITE = pygame.Color('white')
GREY = pygame.Color('grey')
BLACK = pygame.Color('black')


Button_font = pygame.font.Font('pixeboy-font/Pixeboy-z8XGD.ttf',30)

def difficulty_menu():
    while True:
        # Continuously update the mouse position
        mouse_pos = pygame.mouse.get_pos()

        # Draw the background
        screen.blit(Maze_Player_background, (0, 0))

        # Draw the buttons and check for hover effects
        for text, rect in Mode_buttons.items():
            color = (200, 200, 200) if rect.collidepoint(mouse_pos) else (108, 115, 212)
            pygame.draw.rect(screen, color, rect, border_radius=15)
            pygame.draw.rect(screen, (108, 115, 212), rect, 3, border_radius=15)  

            # Render the text for each button
            text_surface = Button_font.render(text, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=rect.center)
            screen.blit(text_surface, text_rect)

        # Handle events
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

                        
                        



def set_difficulty(level):
    global TILE_SIZE, cols, rows
    if level == "easy":
        TILE_SIZE = 80
    elif level == "hard":
        TILE_SIZE = 40

    cols, rows = WIDTH // TILE_SIZE, HEIGHT // TILE_SIZE



class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.walls = {'top': True, 'down': True, 'left': True, 'right': True}
        self.visited = False

    def draw_current_cell(self):
        x, y = self.x * TILE_SIZE, self.y * TILE_SIZE
        pygame.draw.rect(screen, PINK, (x + 2, y + 2, TILE_SIZE - 2, TILE_SIZE - 2))

    def draw(self):
        x, y = self.x * TILE_SIZE, self.y * TILE_SIZE
        if self.visited:
            pygame.draw.rect(screen, BLACK, (x, y, TILE_SIZE, TILE_SIZE))
        if self.walls['top']:
            pygame.draw.line(screen, GREY, (x, y), (x + TILE_SIZE, y), 2)
        if self.walls['right']:
            pygame.draw.line(screen, GREY, (x + TILE_SIZE, y), (x + TILE_SIZE, y + TILE_SIZE), 2)
        if self.walls['down']:
            pygame.draw.line(screen, GREY, (x + TILE_SIZE, y + TILE_SIZE), (x, y + TILE_SIZE), 2)
        if self.walls['left']:
            pygame.draw.line(screen, GREY, (x, y + TILE_SIZE), (x, y), 2)

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
        current.walls['left'] = False
        next.walls['right'] = False
    elif dx == -1:
        current.walls['right'] = False
        next.walls['left'] = False

    dy = current.y - next.y
    if dy == 1:
        current.walls['top'] = False
        next.walls['down'] = False
    elif dy == -1:
        current.walls['down'] = False
        next.walls['top'] = False



level = difficulty_menu()
set_difficulty(level)

grid_cells = [Cell(col, row) for row in range(rows) for col in range(cols)]
stack = []


used_cells = set()

def set_goal():
    global goal_position
    while True:
        random_cell = random.choice(grid_cells)
        if random_cell != grid_cells[0]:  # Avoid start cell
            goal_position = (random_cell.x * TILE_SIZE + TILE_SIZE // 2, 
                             random_cell.y * TILE_SIZE + TILE_SIZE // 2)
            break


def draw_goal():
    if goal_position:
        goal_x, goal_y = goal_position
        icon_rect = goal_icon.get_rect(center=(goal_x, goal_y))
        screen.blit(goal_icon, icon_rect)
  

set_goal()

def main():
    colors,color=[],40
    current_cell = grid_cells[0]
    while True:
        screen.blit(Maze_background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

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
        
        draw_goal()
        pygame.display.flip()
        clock.tick(80)
      
main()