from Button import Button 
from scene import Scene

from constants import *
from scenes.main_game.health import draw_health

from scenes.end_game_failure import EndGame as EndGameFailure
from scenes.end_game_success import EndGame as EndGameSuccess

from components.LoadingBar import LoadingBar

class MainGame(Scene):   
    # Game state 
    is_player_alive: bool
    is_enemy_alive: bool

    # X out of 3 hearts
    player_max_health: int
    enemy_max_health: int
    player_health: int
    enemy_health: int

    loading_bar: LoadingBar


    def __init__(self):
        self.is_player_alive = True
        self.is_enemy_alive = True

        self.player_max_health = 3
        self.enemy_max_health = 3
        self.player_health = self.player_max_health
        self.enemy_health = self.enemy_max_health

        self.loading_bar = LoadingBar(20, 70, SCREEN_WIDTH - 40, 40)

    def draw(self, screen, events):
        draw_health(screen, self.player_max_health, self.enemy_max_health, self.player_health, self.enemy_health)
        self.loading_bar.draw(screen, events)

        # Test buttons
        test_button = Button(500, 500, 40, 40, "Hit Player")
        test_button.draw(screen, events)
        if test_button.isClicked:
            self.player_health -= 1

        test_button_2 = Button(600, 500, 40, 40, "Hit Enemy")
        test_button_2.draw(screen, events)
        if test_button_2.isClicked:
            self.enemy_health -= 1
                               
        # Update state
        if self.player_health <= 0:
            self.is_player_alive = False

        if self.enemy_health <= 0:
            self.is_enemy_alive = False

    def next_scene(self):
        if not self.is_player_alive:
            return EndGameFailure()

        if not self.is_enemy_alive:
            return EndGameSuccess()

        return super().next_scene()
    