import pygame

#intiallizing pygame
pygame.init()

# setting game screen
screen = pygame.display.set_mode((1000,600))

pygame.display.set_caption("Galactic Maze")

Game_font = pygame.font.Font("pixeboy-font/Pixeboy-z8XGD.ttf", 100)  
Maze_win = Game_font.render("You won!", True, (255, 255, 255))  
Maze_win_rect = Maze_win.get_rect(center=(1000 // 2, 150))

win_background = pygame.image.load("download (2).jpeg")  
win_background = pygame.transform.scale(win_background, (1000, 600)) 
Button_font = pygame.font.Font('pixeboy-font/Pixeboy-z8XGD.ttf',30)

End_buttons = {
    "Quit": pygame.Rect(400, 390, 200, 50)
}

def Generate_buttons(buttons, mouse_pos):
    for text, rect in buttons.items():
        color =  (200, 200, 200) if rect.collidepoint(mouse_pos) else (108, 115, 212)
        pygame.draw.rect(screen, color, rect, border_radius=15)
        pygame.draw.rect(screen, color, rect, 3, border_radius=15)  

        text_surface = Button_font.render(text, True, (0,0,0))
        text_rect = text_surface.get_rect(center=rect.center)
        screen.blit(text_surface, text_rect)


def main():
    Playing = True
    while Playing:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get ():
            if event.type == pygame.QUIT:
                Playing = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for text, rect in End_buttons.items():
                    if rect.collidepoint(mouse_pos):
                        if text == "Quit":
                            pygame.quit()
                            running = False
    
    
        screen.blit(win_background, (0, 0))
        screen.blit(Maze_win, Maze_win_rect)
        Generate_buttons(End_buttons, mouse_pos)
        pygame.display.flip()
        
main()    