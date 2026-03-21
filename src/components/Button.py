import pygame, sys
import pygame.font
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

DEFAULT_TEXT_COLOR = (255, 255, 255)
DEFAULT_BUTTON_COLOR = (139, 69, 19)
class Button():
    """Draws the button and checks if clicked """
    isClicked: bool
    width: int 
    height: int 
    x_pos: int # positon
    y_pos: int
    button_color: any
    text_color: any
    font: str

    

    def __init__(self, x_pos: int, y_pos: int, width: int, height: int, msg: str, text_color = DEFAULT_TEXT_COLOR, button_color = DEFAULT_BUTTON_COLOR):
        """Intialze button attributes: location on grid, size (width, height), message, textcore, buttoncolor"""
        
        # Dimensions of the button  EX. 200 x 50
        self.width= width
        self.height = height
        self.x_pos = x_pos
        self.y_pos = y_pos


        self.button_color = button_color
        self.text_color = text_color
        
        # label the button (e.g, "START")
        self.font = pygame.font.SysFont(None, 48)

        # This defines the button's size and clickable area.
        self.rect = pygame.Rect(x_pos,  y_pos, self.width, self.height)

        self.rect.center = self.rect.center

       
       

        self.write_msg(msg)


    


    def write_msg(self, msg):
        """Renders and message on the button"""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

  

    def draw(self, screen: pygame.Surface, events: list[pygame.event.Event]):
        """ Draws blank button"""
        # Draw blank button and then draw message.
        screen.fill(self.button_color, self.rect)
        screen.blit(self.msg_image, self.msg_image_rect)
        
        # Check if the event is mousebuttondown then print event
        self.isClicked = False
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
                self.isClicked = True
                break



        
        
        


# import pygame
# pygame.init()
# print(pygame.font.get_fonts())

# Draw the bu