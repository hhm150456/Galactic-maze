#Import pygame for game mechanics
import pygame

#intiallizing pygame
pygame.init()

# setting game screen
screen = pygame.display.set_mode((1000,600))

#Game caption
pygame.display.set_caption("Galactic Maze")

#Intiallizing buttons used on home screen in a dictionary
Home_screen_buttons = {
    "Play": pygame.Rect(400, 250, 200, 50),  
    "Maze solver": pygame.Rect(400, 320, 200, 50),
    "Quit": pygame.Rect(400, 390, 200, 50)
}

#Importing game logo
logo = pygame.image.load('space.png')
pygame.display.set_icon(logo)

#Intiallizing game font and rendering game title 'Galactic maze'
Game_font = pygame.font.Font("pixeboy-font/Pixeboy-z8XGD.ttf", 100)  
Title = Game_font.render("Galactic Maze", True, (255, 255, 255))  
title_rect = Title.get_rect(center=(1000 // 2, 150))

#Intiallizing lHome screen background and rendering it
Home_screen_background = pygame.image.load("Screenshot 2024-12-14 131048.png")  
Home_screen_background = pygame.transform.scale(Home_screen_background, (1000, 600)) 
Button_font = pygame.font.Font('pixeboy-font/Pixeboy-z8XGD.ttf',30)

#Function to generate buttons takes the buttons and mouse position as arguments
def Generate_buttons(buttons, mouse_pos):
    for text, rect in buttons.items():
        #Change colour when mouse hovers over button
        color =  (200, 200, 200) if rect.collidepoint(mouse_pos) else (108, 115, 212)

        #Draw button and add border of same color (border is visible when mouse hovers over button)
        pygame.draw.rect(screen, color, rect, border_radius=15)
        pygame.draw.rect(screen, color, rect, 5, border_radius=15)  

        #Render text over buttons
        text_surface = Button_font.render(text, True, (0,0,0))
        text_rect = text_surface.get_rect(center=rect.center)
        screen.blit(text_surface, text_rect)

#Main function (Called when we change pages)
def main():
    Playing = True

    #Game while loop
    while Playing:

        #Get mouse position
        mouse_pos = pygame.mouse.get_pos()

        #Events for loop
        for event in pygame.event.get ():
            #If we press x and exit game
            if event.type == pygame.QUIT:
                Playing = False
            #If we press a button
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for text, rect in Home_screen_buttons.items():
                    if rect.collidepoint(mouse_pos):
                        if text == "Play":
                            import Player_Maze
                            Player_Maze.main()
                        elif text == "Maze solver":
                           import Maze_Solver
                           Maze_Solver.main()
                        elif text == "Quit":
                            pygame.quit()
                            Playing = False
    
        #Build home screen and title
        screen.blit(Home_screen_background, (0, 0))
        screen.blit(Title, title_rect)
        
        #Call to generate buttons 
        Generate_buttons(Home_screen_buttons, mouse_pos)
        pygame.display.flip()

#Call main function        
main()    