import pygame

DEFAULT_FILL = (255, 0, 0)
DEFAULT_BORDER = (255, 255, 255)
class LoadingBar:
    __x: int
    __y: int 
    __width: int
    __height: int

    __border_margin: int

    __progress: float = 0

    __border_color: any
    __fill_color: any

    def __init__(self, x: int, y: int, width: int, height: int, border_margin = 5, fill_color = DEFAULT_FILL, border_color = DEFAULT_BORDER):
        self.__progress = 0
        self.__x = x
        self.__y = y
        self.__width = width
        self.__height = height
        self.__border_margin = border_margin
        self.__border_color = border_color
        self.__fill_color = fill_color

    def set_progress(self, new: float):
        self.__progress = max(min(new, 1), 0)

    def get_progress(self) -> float:
        return self.__progress

    def __get_outer_rect(self) -> pygame.Rect:
        return pygame.Rect(self.__x, self.__y, self.__width, self.__height)

    def __get_inner_rect(self) -> pygame.Rect:
        bm = self.__border_margin

        max_inner_width = self.__width - bm * 2
        lerped_width = max_inner_width * self.__progress

        return pygame.Rect(self.__x + bm, self.__y + bm, lerped_width, self.__height - bm * 2)
    
    def draw(self, screen: pygame.Surface, events: list[pygame.event.Event]):
        screen.fill(self.__border_color, self.__get_outer_rect())
        screen.fill(self.__fill_color, self.__get_inner_rect())