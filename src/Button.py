import pygame, sys
import pygame.font
class Button():
    """Draws the button and checks if clicked """
    isClicked: bool
    def __init__(self, x: int, y: int, width, height):
        """Intialze button attributes"""
        
        # Dimensions of the button  EX. 200 x 50
        self.width= width
        self.height = height
        self.x = x 
        self.y = y 


        self.button_color = (164, 26, 138)
        self.text_color = (255, 255, 255)
        
        # label the button (e.g, "START")
        self.font = pygame.font.SysFont(None, 48)
    

        # This defines the button's size and clickable area.
        self.rect = pygame.Rect(x, y, self.width, self.height)


    def draw(self, screen: pygame.Surface, events: list[pygame.event.Event]):
        """ Draws blank button"""
        # Draw blank button and then draw message.
        screen.fill(self.button_color, self.rect)
        
        # Check if the event is mousebuttondown then print event
        self.isClicked = False
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
                self.isClicked = True
                break



        
        
        




# Draw the bu