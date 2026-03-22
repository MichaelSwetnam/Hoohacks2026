import pygame
from pygame import Vector2
from scene import Scene, SceneName
from load_image import load_image
from components.Button import Button

OLD_PAPER = load_image("oldpaper.png", Vector2(800, 500))

COWBOY_INSULT = "You clumsy varmint! Watch where\nyou're walkin' before I put a hole\nin them raggedy boots of yours!"

class Decision(Scene):

    def __init__(self):
        self.__font        = pygame.font.SysFont("couriernew", 26, bold=True)
        self.__title_font  = pygame.font.SysFont("couriernew", 32, bold=True)
        self.__insult_font = pygame.font.SysFont("couriernew", 24, bold=True)

        self.__sorry_button   = Button(350, 510, 210, 50, "APOLOGISE")
        self.__insult_button  = Button(750, 510, 180, 50, "INSULT")

        self.__cowboy_responded = False   # flips True after player picks
        self.__next_scene = None

    def draw(self, screen, events):
        screen.fill((30, 20, 10))

        paper_x = (1280 - 800) // 2
        paper_y = (720 - 500) // 2 - 30
        screen.blit(OLD_PAPER, (paper_x, paper_y))

        # Title
        title = self.__title_font.render("What do you do?", True, (80, 40, 10))
        screen.blit(title, (paper_x + 800 // 2 - title.get_width() // 2, paper_y + 30))

        if not self.__cowboy_responded:
            # Show the two choices
            prompt = self.__font.render("The cowboy stares you down...", True, (60, 30, 10))
            screen.blit(prompt, (paper_x + 60, paper_y + 120))

            prompt2 = self.__font.render("Do you apologise or insult him?", True, (60, 30, 10))
            screen.blit(prompt2, (paper_x + 60, paper_y + 165))

            self.__sorry_button.draw(screen, events)
            self.__insult_button.draw(screen, events)

            if self.__sorry_button.isClicked or self.__insult_button.isClicked:
                self.__cowboy_responded = True

        # else:
        #     # Show the cowboy's insult response regardless of what player picked
        #     header = self.__font.render("The cowboy snarls back at you:", True, (60, 30, 10))
        #     screen.blit(header, (paper_x + 60, paper_y + 100))

        #     # Draw each line of the insult
        #     for i, line in enumerate(COWBOY_INSULT.split("\n")):
        #         insult = self.__insult_font.render(f'"{line}"', True, (140, 20, 20))
        #         screen.blit(insult, (paper_x + 60, paper_y + 170 + i * 40))

        #     # Continue button to go to the typing challenge
        #     continue_btn = Button(570, 560, 160, 50, "CONTINUE")
        #     continue_btn.draw(screen, events)
        #     if continue_btn.isClicked:
        #         self.__next_scene = SceneName.DUEL

    def next_scene(self):
        if self.__cowboy_responded:
            return SceneName.MAIN_GAME