import pygame
from pygame import Vector2
from scene import Scene, SceneName
from load_image import load_image
from components.Button import Button
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, CENTER_OF_SCREEN

OLD_PAPER = load_image("oldpaper.png", Vector2(800, 500))

STORY_LINES = [
    "It's high noon in the wild west...",
    "Your belly's rumblin' like thunder.",
    "You stumble into the nearest saloon",
    "lookin' for a hot meal and cold drink.",
    "",
    "But as you push through the doors...",
    "BUMP!",
    "You walk straight into another cowboy.",
    "He don't look too pleased about it.",
]

CONTINUE_Y = 510
CONTINUE_WIDTH = 220
CONTINUE_HEIGHT = 50

class Narrator(Scene):

    def __init__(self):
        self.__font = pygame.font.SysFont("couriernew", 26, bold=True)
        self.__title_font = pygame.font.SysFont("couriernew", 36, bold=True)
        self.__next_button = Button(
            CENTER_OF_SCREEN[0] - CONTINUE_WIDTH / 2,
            CONTINUE_Y, 
            CONTINUE_WIDTH,
            CONTINUE_HEIGHT,
            "CONTINUE"
        )
        self.__next_scene = None

    def draw(self, screen, events):
        screen.fill((30, 20, 10))

        # Draw old paper in center
        paper_x = (1280 - 800) // 2
        paper_y = (720 - 500) // 2 - 30
        screen.blit(OLD_PAPER, (paper_x, paper_y))

        # Title on paper
        title = self.__title_font.render("~ A Hungry Cowboy ~", True, (80, 40, 10))
        screen.blit(title, (paper_x + 800 // 2 - title.get_width() // 2, paper_y + 30))

        # Story lines on paper
        for i, line in enumerate(STORY_LINES):
            text = self.__font.render(line, True, (60, 30, 10))
            screen.blit(text, (paper_x + 60, paper_y + 100 + i * 36))

        self.__next_button.draw(screen, events)
        if self.__next_button.isClicked:
            self.__next_scene = SceneName.DECISION

    def next_scene(self):
        return self.__next_scene