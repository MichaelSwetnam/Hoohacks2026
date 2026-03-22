import pygame

from components.Button import Button
from scene import SceneName, Scene

from random import random
from math import floor

from constants import SCREEN_WIDTH, SCREEN_HEIGHT, TIME_BAR_COLOR
from scenes.main_game.health import draw_health, calculate_enemy_bounding, calculate_player_bounding, HEART_SIZE
from scenes.main_game.character import Character, SpriteName
from load_image import load_image

from components.LoadingBar import LoadingBar

def get_random_enemy_sprite():
    rand = floor(random() * 3)
    if rand == 0:
        return SpriteName.ENEMY_1
    elif rand == 1:
        return SpriteName.ENEMY_2
    else:
        return SpriteName.ENEMY_3

BACKGROUND = load_image("saloon_night.jpg", pygame.Vector2(SCREEN_WIDTH, SCREEN_HEIGHT))
LOADING_BAR_MARGIN = 20

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

        self.__enemy = Character(get_random_enemy_sprite())
        self.__player = Character(SpriteName.PLAYER)

        self.__is_player_alive = True
        self.__is_enemy_alive = True

        self.__player_max_health = 3
        self.__enemy_max_health = 3
        self.__player_health = self.__player_max_health
        self.__enemy_health = self.__enemy_max_health

        player_heart_bounding = calculate_player_bounding(self.__player_max_health)
        enemy_heart_bounding = calculate_enemy_bounding(self.__enemy_max_health)

        loading_bar_x = player_heart_bounding.w + player_heart_bounding.x + LOADING_BAR_MARGIN
        self.__loading_bar = LoadingBar(
            player_heart_bounding.w + player_heart_bounding.x + LOADING_BAR_MARGIN,
            player_heart_bounding.y,
            enemy_heart_bounding.x - LOADING_BAR_MARGIN - loading_bar_x,
            HEART_SIZE,
            fill_color=TIME_BAR_COLOR
        )
        
        self.__loading_bar.set_progress(0.7)

    def draw(self, screen, events):
        screen.blit(BACKGROUND, (0, 0))
        draw_health(screen, self.__player_max_health, self.__enemy_max_health, self.__player_health, self.__enemy_health)
        self.__loading_bar.draw(screen, events)
        self.__enemy.draw(screen, events)
        self.__player.draw(screen, events)

        is_game_over = self.__player_health <= 0 or self.__enemy_health <= 0

        # Test buttons
        hit_player = Button(500, 500, 40, 40, "Hit Player")
        hit_player.draw(screen, events)
        if hit_player.isClicked and not is_game_over:
            # This hit will cause the player's health to become 0 -- final hit
            final_hit = self.__player_health <= 1
            self.__player_health -= 1

            self.__player.hit(final_hit)
            self.__enemy.attack()

        hit_enemy = Button(600, 500, 40, 40, "Hit Enemy")
        hit_enemy.draw(screen, events)
        if hit_enemy.isClicked and not is_game_over:
            # This hit will cause the enemy's health to become 0 -- final hit

            final_hit = self.__enemy_health <= 1
            self.__enemy_health -= 1

            self.__enemy.hit(final_hit)
            self.__player.attack()
                               
        # Update state
        if self.__player_health <= 0:
            self.__is_player_alive = False

        if self.__enemy_health <= 0:
            self.__is_enemy_alive = False

    def next_scene(self):
        # Don't advance until animations are done
        if self.__enemy.is_animation_running() or self.__player.is_animation_running():
            return None

        if not self.__is_player_alive:
            return SceneName.EXIT_MENU_LOST

        if not self.__is_enemy_alive:
            return SceneName.EXIT_MENU_WON

        return super().next_scene()
    