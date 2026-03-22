import pygame
import random
from pygame import Vector2
from scene import Scene, SceneName
from load_image import load_image
from draw_menu_background import draw_menu_background
from components.Button import Button
from components.LoadingBar import LoadingBar
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, HEART_ALIVE, HEART_DEAD
from scenes.main_game.character import Character, SpriteName

# ---------------------------------------------------------------------------
# Insult pool — also used as typing prompts
# ---------------------------------------------------------------------------
INSULTS = [
    "Git along, dusty fool!",
    "Ya yellow-bellied skunk!",
    "Slow as a dead mule!",
    "Quit yer snivelin', worm!",
    "Lower than a snake's belly!",
    "You ain't worth the dust!",
    "Ride off, you mangy cur!",
    "Dumber than a fence post!",
]

TYPING_TIME = 5.0

PLAYER_BUBBLE_CX = 250
ENEMY_BUBBLE_CX  = 1000
BUBBLE_Y = 150

# ---------------------------------------------------------------------------
# Pre-load heart assets
# ---------------------------------------------------------------------------
_heart_img  = load_image(HEART_ALIVE, Vector2(40, 40))
_dead_heart = load_image(HEART_DEAD,  Vector2(40, 40))


# ---------------------------------------------------------------------------
# Standalone speech-bubble helper
# ---------------------------------------------------------------------------
def draw_speech_bubble(screen: pygame.Surface, text: str, font: pygame.font.Font,
                        center_x: int, y: int, color=(255, 255, 255)) -> None:
    PAD = 12
    text_surf = font.render(text, True, (0, 0, 0))
    bw = max(200, text_surf.get_width() + PAD * 2)
    bh = text_surf.get_height() + PAD * 2

    rect = pygame.Rect(center_x - bw // 2, y, bw, bh)

    pygame.draw.rect(screen, color, rect, border_radius=16)
    pygame.draw.rect(screen, (160, 160, 160), rect, width=2, border_radius=16)

    tail_pts = [
        (center_x - 10, rect.bottom),
        (center_x + 10, rect.bottom),
        (center_x,      rect.bottom + 14),
    ]
    pygame.draw.polygon(screen, color, tail_pts)

    screen.blit(text_surf, (rect.x + PAD, rect.y + PAD))


# ---------------------------------------------------------------------------
# MainGame scene
# ---------------------------------------------------------------------------
class MainGame(Scene):

    def __init__(self, _unused=None):
        # ── Game state ──────────────────────────────────────────────────────
        self.__player_hearts   = 3
        self.__enemy_hearts    = 3
        self.__phase           = "dialogue"
        self.__round           = 0
        self.__next_scene_name = None

        self.__current_insult = ""
        self.__typed_text     = ""
        self.__time_left      = TYPING_TIME
        self._last_tick: int | None = None

        # ── Characters (use existing Character class) ────────────────────────
        self.__player = Character(SpriteName.PLAYER)
        self.__enemy  = Character(SpriteName.ENEMY_1)

        # ── UI ───────────────────────────────────────────────────────────────
        self.__fight_button = Button(
            SCREEN_WIDTH // 2 - 100, 600, 200, 50, "FIGHT BACK"
        )
        self.__timer_bar = LoadingBar(
            x=0, y=660, width=SCREEN_WIDTH, height=30,
            fill_color=(95, 159, 250)
        )

        # ── Fonts ────────────────────────────────────────────────────────────
        self.__bubble_font = pygame.font.SysFont("couriernew", 22, bold=True)
        self.__type_font   = pygame.font.SysFont("couriernew", 26, bold=True)

        self.__start_round()

    # ── Public interface ─────────────────────────────────────────────────────

    def draw(self, screen: pygame.Surface, events: list[pygame.event.Event]) -> None:
        draw_menu_background(screen)
        self.__draw_hearts(screen)

        # Character.draw() handles sprite state + shake animation internally
        self.__player.draw(screen, events)
        self.__enemy.draw(screen, events)

        if self.__phase == "dialogue":
            self.__draw_dialogue_phase(screen, events)
        else:
            self.__draw_typing_phase(screen, events)

    def next_scene(self) -> SceneName | None:
        return self.__next_scene_name

    # ── Round management ─────────────────────────────────────────────────────

    def __start_round(self) -> None:
        self.__current_insult = random.choice(INSULTS)
        self.__typed_text     = ""
        self.__time_left      = TYPING_TIME
        self.__phase          = "dialogue"
        self._last_tick       = None

    def __resolve_round(self, success: bool) -> None:
        if success:
            self.__enemy_hearts -= 1
            self.__player.attack()
            self.__enemy.hit(final_hit=self.__enemy_hearts <= 0)
        else:
            self.__player_hearts -= 1
            self.__enemy.attack()
            self.__player.hit(final_hit=self.__player_hearts <= 0)

        self.__typed_text = ""
        self.__round += 1
        self.__check_end_conditions()

        if self.__next_scene_name is None:
            self.__start_round()

    def __check_end_conditions(self) -> None:
        if self.__player_hearts <= 0 and self.__enemy_hearts <= 0:
            self.__next_scene_name = SceneName.EXIT_MENU_LOST
        elif self.__player_hearts <= 0:
            self.__next_scene_name = SceneName.EXIT_MENU_LOST
        elif self.__enemy_hearts <= 0:
            self.__next_scene_name = SceneName.EXIT_MENU_WON

    # ── Draw helpers ──────────────────────────────────────────────────────────

    def __draw_hearts(self, screen: pygame.Surface) -> None:
        for i in range(3):
            img = _heart_img if i < self.__player_hearts else _dead_heart
            screen.blit(img, (30 + i * 50, 20))
        for i in range(3):
            img = _heart_img if i < self.__enemy_hearts else _dead_heart
            screen.blit(img, (1150 + i * 50, 20))

    # ── Dialogue phase ────────────────────────────────────────────────────────

    def __draw_dialogue_phase(self, screen: pygame.Surface,
                               events: list[pygame.event.Event]) -> None:
        draw_speech_bubble(screen, "Back off, varmint!",
                           self.__bubble_font, PLAYER_BUBBLE_CX, BUBBLE_Y)
        draw_speech_bubble(screen, self.__current_insult,
                           self.__bubble_font, ENEMY_BUBBLE_CX, BUBBLE_Y)

        self.__fight_button.draw(screen, events)
        if self.__fight_button.isClicked:
            self.__phase    = "typing"
            self._last_tick = None
            self.__timer_bar.set_progress(1.0)

    # ── Typing phase ──────────────────────────────────────────────────────────

    def __draw_typing_phase(self, screen: pygame.Surface,
                             events: list[pygame.event.Event]) -> None:
        self.__tick_timer()

        draw_speech_bubble(screen, self.__current_insult,
                           self.__bubble_font, PLAYER_BUBBLE_CX, BUBBLE_Y)

        self.__draw_input_box(screen)
        self.__timer_bar.draw(screen, events)
        self.__handle_typing_input(events)

        if self.__typed_text.lower().strip() == self.__current_insult.lower().strip():
            self.__resolve_round(success=True)
        elif self.__time_left <= 0:
            self.__resolve_round(success=False)

    def __draw_input_box(self, screen: pygame.Surface) -> None:
        # Positioned below the player speech bubble
        box = pygame.Rect(60, 310, 380, 44)
        pygame.draw.rect(screen, (30, 30, 30), box, border_radius=6)
        pygame.draw.rect(screen, (200, 200, 200), box, width=2, border_radius=6)
        text_surf = self.__type_font.render(self.__typed_text, True, (255, 255, 255))
        screen.blit(text_surf, (box.x + 8, box.y + 8))

    def __handle_typing_input(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.__typed_text = self.__typed_text[:-1]
                elif event.unicode.isprintable():
                    self.__typed_text += event.unicode

    # ── Timer ─────────────────────────────────────────────────────────────────

    def __tick_timer(self) -> None:
        now = pygame.time.get_ticks()
        if self._last_tick is None:
            self._last_tick = now
        elapsed = (now - self._last_tick) / 1000.0
        self._last_tick = now
        self.__time_left = max(0.0, self.__time_left - elapsed)
        self.__timer_bar.set_progress(self.__time_left / TYPING_TIME)
