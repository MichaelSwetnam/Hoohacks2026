import enum;
import pygame

class SceneName(enum.Enum):
    START_MENU = 0
    MAIN_GAME = 1
    EXIT_MENU_WON = 2
    EXIT_MENU_LOST = 3
    DECISION = 4
    NARRATOR = 5


class Scene:
    def draw(screen: pygame.Surface, events: list[pygame.event.Event]):
        pass
    
    def next_scene(self) -> SceneName | None:
        pass

    

