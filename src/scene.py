from typing import Self
import pygame

class Scene:
    def draw(screen: pygame.Surface, events: list[pygame.event.Event]):
        pass
    
    def next_scene(self) -> Self | None:
        pass