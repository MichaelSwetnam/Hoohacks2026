from components.Button import Button
from scene import Scene, SceneName
import pygame
from constants import CENTER_OF_SCREEN

class EndMenu(Scene):
    __end_button: Button
    __has_won: bool
    
    def __init__(self, has_won: bool):
        self.__end_button = Button(540, 335, 200,50, "Return to Start")
        self.__has_won = has_won
        self.font = pygame.font.SysFont(None, 72)


    def draw(self, screen, events):
        label = None
        if self.__has_won: 
            label = self.font.render("WINNER!", True, (0,255,0)) # green win 
        else:
            label = self.font.render("Loser!", True, (225,0,0)) # red for loss
        
        label_rect = label.get_rect()
        screen.blit(label, label_rect)

        # Draw the return button
        self.__end_button.draw(screen, events)

    def next_scene(self):
        if self.__end_button.isClicked:
            return SceneName.START_MENU

    pass