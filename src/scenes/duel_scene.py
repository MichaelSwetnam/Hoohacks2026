import pygame
import random

from scene import Scene, SceneName
from components.Button import Button
from components.TypingChallenge import TypingChallenge
from draw_menu_background import draw_darkened_background

INSULTS = [
    "You're slower than a dead mule!",
    "Nice hat, did yer horse pick it?",
    "I've seen tumbleweeds with more grit!",
    "Your draw is slower than molasses!",
    "You smell worse than my saddle!",
]

BEAT_DURATION_MS = 2500   # how long each story screen shows before advancing


class DuelScene(Scene):
    """
    Flow:
        COLLISION → CHOICE → RETORT → TYPING → OUTCOME
        then hands off to EXIT_MENU_WON or EXIT_MENU_LOST
    """

    _STATE_COLLISION = "collision"
    _STATE_CHOICE    = "choice"
    _STATE_RETORT    = "retort"
    _STATE_TYPING    = "typing"
    _STATE_OUTCOME   = "outcome"

    def __init__(self):
        self._state      = self._STATE_COLLISION
        self._beat_start = pygame.time.get_ticks()
        self._prev_ms    = pygame.time.get_ticks()
        self._outcome    = None       # "win" | "lose"
        self._next       = None       # SceneName returned to main loop

        self._enemy_line    = random.choice(INSULTS)
        remaining           = [i for i in INSULTS if i != self._enemy_line]
        self._typing_prompt = random.choice(remaining or INSULTS)

        self._challenge = None   # TypingChallenge, created when TYPING begins

        self._btn_insult    = Button(390, 400, 180, 55, "INSULT")
        self._btn_apologise = Button(620, 400, 240, 55, "APOLOGISE")

        self._font_title  = pygame.font.SysFont("couriernew", 42, bold=True)
        self._font_body   = pygame.font.SysFont("couriernew", 28)
        self._font_result = pygame.font.SysFont("couriernew", 58, bold=True)

    # ------------------------------------------------------------------
    def draw(self, screen: pygame.Surface, events: list[pygame.event.Event]):
        now           = pygame.time.get_ticks()
        dt            = (now - self._prev_ms) / 1000.0
        self._prev_ms = now

        draw_darkened_background(screen)

        if   self._state == self._STATE_COLLISION: self._draw_collision(screen)
        elif self._state == self._STATE_CHOICE:    self._draw_choice(screen, events)
        elif self._state == self._STATE_RETORT:    self._draw_retort(screen)
        elif self._state == self._STATE_TYPING:    self._draw_typing(screen, events, dt)
        elif self._state == self._STATE_OUTCOME:   self._draw_outcome(screen)

    def next_scene(self) -> SceneName | None:
        return self._next

    # ------------------------------------------------------------------
    def _draw_collision(self, screen):
        self._centre(screen, "* B U M P *",
                     self._font_title, (230, 200, 100), 260)
        self._centre(screen, "Two cowboys collide on the dusty trail...",
                     self._font_body,  (220, 200, 160), 330)
        self._advance_after(self._STATE_CHOICE)

    def _draw_choice(self, screen, events):
        self._centre(screen, "What do you do?",
                     self._font_title, (230, 200, 100), 320)
        self._btn_insult.draw(screen, events)
        self._btn_apologise.draw(screen, events)

        if self._btn_insult.isClicked or self._btn_apologise.isClicked:
            self._set_state(self._STATE_RETORT)

    def _draw_retort(self, screen):
        self._centre(screen, "The stranger sneers at you...",
                     self._font_body, (200, 180, 140), 240)
        self._centre(screen, f'"{self._enemy_line}"',
                     self._font_body, (230, 80,  80),  300)
        self._centre(screen, "Type the comeback — fast!",
                     self._font_body, (230, 220, 100), 360)

        if pygame.time.get_ticks() - self._beat_start >= BEAT_DURATION_MS:
            self._challenge = TypingChallenge(self._typing_prompt, time_limit=6.0)
            self._set_state(self._STATE_TYPING)

    def _draw_typing(self, screen, events, dt):
        result = self._challenge.draw(screen, events, dt)
        if result == "success":
            self._outcome = "win"
            self._set_state(self._STATE_OUTCOME)
        elif result == "fail":
            self._outcome = "lose"
            self._set_state(self._STATE_OUTCOME)

    def _draw_outcome(self, screen):
        if self._outcome == "win":
            self._centre(screen, "DRAW!",
                         self._font_result, (255, 220, 50),  240)
            self._centre(screen, "The stranger hits the dirt.",
                         self._font_body,   (220, 200, 160), 320)
        else:
            self._centre(screen, "TOO SLOW!",
                         self._font_result, (220, 50,  50),  240)
            self._centre(screen, "You took a bullet. That's gonna leave a mark.",
                         self._font_body,   (220, 200, 160), 320)

        if pygame.time.get_ticks() - self._beat_start >= BEAT_DURATION_MS:
          self._next = (SceneName.MAIN_GAME       # ← win = proceed to shooting mechanic
                if self._outcome == "win"
                else SceneName.EXIT_MENU_LOST)

    # ------------------------------------------------------------------
    def _set_state(self, new_state: str):
        self._state      = new_state
        self._beat_start = pygame.time.get_ticks()

    def _advance_after(self, next_state: str):
        if pygame.time.get_ticks() - self._beat_start >= BEAT_DURATION_MS:
            self._set_state(next_state)

    def _centre(self, screen, text, font, color, y):
        surf = font.render(text, True, color)
        screen.blit(surf, (screen.get_width() // 2 - surf.get_width() // 2, y))