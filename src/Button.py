import pygame, sys
import pygame.font
class Button():
    """Draws the button and checks if clicked """
    isClicked: bool
    def __init__(self, width: int, height: int):
        """Intialze button attributes"""
        
        # Dimensions of the button  EX. 200 x 50
        self.width = width 
        self.height = height 


        self.button_color = (164, 26, 138)
        self.text_color = (255, 255, 255)
        
        # label the button (e.g, "START")
        self.font = pygame.font.SysFont(None, 48)
    

        # This defines the button's size and clickable area.
        self.rect = pygame.Rect(0, 0, self.width, self.height)

    def draw(self, screen: pygame.Surface):
        """ Draws blank button"""
        # Draw blank button and then draw message.
        screen.fill(self.button_color, self.rect)
        

    # while isClicked: 
    #     if event.type == pygame.MOUSEBUTTONDOWN:
    #         if start_button_rect.collide(even.pos):
    #             print("Game is Starting...")
        



        




# Draw the bu