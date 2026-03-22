# Example file showing a circle moving on screen
import pygame
from scenes.start_menu import StartMenu
from scenes.main_game import MainGame
from scenes.end_menu import EndMenu

from scene import Scene, SceneName

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# pygame setup
pygame.init()
pygame.display.set_caption("Type Faster")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True
dt = 0

def get_scene(sceneRef: SceneName):
    if sceneRef == SceneName.START_MENU:
        return StartMenu()
    elif sceneRef == SceneName.MAIN_GAME:
        return MainGame(1)
    elif sceneRef == SceneName.EXIT_MENU_LOST:
        return EndMenu(False)
    else:
        return EndMenu(True)

current_scene: Scene = StartMenu() 
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    # Draw the scene
    current_scene.draw(screen, events)
    next = current_scene.next_scene()
    if next is not None:
        current_scene = get_scene(next)

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000


pygame.quit()