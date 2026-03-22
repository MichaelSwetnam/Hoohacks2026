import pygame

from components.Button import Button
from scene import SceneName, Scene

from constants import SCREEN_WIDTH, SCREEN_HEIGHT, TIME_BAR_COLOR
from scenes.main_game.health import draw_health
from scenes.main_game.character import Character, SpriteName
from load_image import load_image

from components.LoadingBar import LoadingBar


BACKGROUND = load_image("saloon_night.jpg", pygame.Vector2(SCREEN_WIDTH, SCREEN_HEIGHT))

class MainGame(Scene):   
    # Game state 
    __is_player_alive: bool
    __is_enemy_alive: bool

    __level: int
    __enemy: Character
    __player: Character

    # X out of 3 hearts
    __player_max_health: int
    __enemy_max_health: int
    __player_health: int
    __enemy_health: int

    __loading_bar: LoadingBar

    def __init__(self, level: int):
        self.__level = level
        self.__enemy = Character(SpriteName.ENEMY_1)
        self.__player = Character(SpriteName.PLAYER)

        self.__is_player_alive = True
        self.__is_enemy_alive = True

        self.__player_max_health = 3
        self.__enemy_max_health = 3
        self.__player_health = self.__player_max_health
        self.__enemy_health = self.__enemy_max_health

        self.__loading_bar = LoadingBar(20, 70, SCREEN_WIDTH - 40, 40, fill_color=TIME_BAR_COLOR)
        self.__loading_bar.set_progress(0.7)

    def draw(self, screen, events):
        screen.blit(BACKGROUND, (0, 0))
        draw_health(screen, self.__player_max_health, self.__enemy_max_health, self.__player_health, self.__enemy_health)
        self.__loading_bar.draw(screen, events)
        self.__enemy.draw(screen, events)
        self.__player.draw(screen, events)

        # Test buttons
        hit_player = Button(500, 500, 40, 40, "Hit Player")
        hit_player.draw(screen, events)
        if hit_player.isClicked:
            self.__player_health -= 1
            self.__player.hit()

        hit_enemy = Button(600, 500, 40, 40, "Hit Enemy")
        hit_enemy.draw(screen, events)
        if hit_enemy.isClicked:
            self.__enemy_health -= 1
            self.__enemy.hit()
                               
        # Update state
        if self.__player_health <= 0:
            self.__is_player_alive = False

        if self.__enemy_health <= 0:
            self.__is_enemy_alive = False

    def next_scene(self):
        if not self.__is_player_alive:
            return SceneName.EXIT_MENU_LOST

        if not self.__is_enemy_alive:
            return SceneName.EXIT_MENU_WON

        return super().next_scene()
    