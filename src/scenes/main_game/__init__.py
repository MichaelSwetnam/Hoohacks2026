from Button import Button 
from scene import Scene

from constants import *
from scenes.main_game.health import draw_health

from scenes.end_game_failure import EndGame as EndGameFailure
from scenes.end_game_success import EndGame as EndGameSuccess

class MainGame(Scene):   
    # Game state 
    isPlayerAlive: bool
    isEnemyAlive: bool

    # X out of 3 hearts
    playerMaxHealth: int
    enemyMaxHealth: int
    playerHealth: int
    enemyHealth: int

    def __init__(self):
        self.isPlayerAlive = True
        self.isEnemyAlive = True

        self.playerMaxHealth = 3
        self.enemyMaxHealth = 3
        self.playerHealth = self.playerMaxHealth
        self.enemyHealth = self.enemyMaxHealth

    def draw(self, screen, events):
        draw_health(screen, self.playerMaxHealth, self.enemyMaxHealth, self.playerHealth, self.enemyHealth)

        # Test buttons
        test_button = Button(500, 500, 40, 40)
        test_button.draw(screen, events)
        if test_button.isClicked:
            self.playerHealth -= 1

        test_button_2 = Button(600, 500, 40, 40)
        test_button_2.draw(screen, events)
        if test_button_2.isClicked:
            self.enemyHealth -= 1
                               
        # Update state
        if self.playerHealth <= 0:
            self.isPlayerAlive = False

        if self.enemyHealth <= 0:
            self.isEnemyAlive = False

    def next_scene(self):
        if not self.isPlayerAlive:
            return EndGameFailure()

        if not self.isEnemyAlive:
            return EndGameSuccess()

        return super().next_scene()
    