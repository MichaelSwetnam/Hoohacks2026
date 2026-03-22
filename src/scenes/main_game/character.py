import pygame
import enum
from constants import CHARACTER_SIZE, CHARACTER_SIDE_PADDING, SCREEN_HEIGHT, SCREEN_WIDTH
from random import random
# Both should be equall yseparated
# [ X  X ]

# i suppose with a padding

# Enemy will always be on the RIGHT (high X)
# They go from bottom -> top

SIZE_X = CHARACTER_SIZE[0]
SIZE_Y = CHARACTER_SIZE[1]

class SpriteName(enum.Enum):
    PLAYER = 1
    ENEMY_1 = 2
    ENEMY_2 = 2
    ENEMY_3 = 3


ENEMY_RECT = pygame.Rect(
    SCREEN_WIDTH - CHARACTER_SIDE_PADDING - SIZE_X,
    SCREEN_HEIGHT - SIZE_Y,
    SIZE_X,
    SIZE_Y
)
PLAYER_RECT = pygame.Rect(
    CHARACTER_SIDE_PADDING,
    SCREEN_HEIGHT - SIZE_Y,
    SIZE_X, 
    SIZE_Y
)

HIT_ATTACK = 0.05 * 1000
HIT_RECOVERY = 0.1 * 1000
HIT_POWER = 50

def lerp(a: pygame.Vector2, b: pygame.Vector2, t: float):
    return a + (b - a) * t

class Character:
    __sprite: SpriteName
    __flipped: bool
    __rect: pygame.Rect

    __last_hit: int
    __hit_shake: pygame.Vector2

    def __init__(self, sprite: SpriteName):
        self.__sprite = sprite
        if sprite == SpriteName.PLAYER:
            self.__flipped = False
            self.__rect = PLAYER_RECT
        else:
            self.__flipped = True
            self.__rect = ENEMY_RECT

        self.__last_hit = 0
        self.__hit_shake = pygame.Vector2(0, 0)

    def hit(self):
        self.__last_hit = pygame.time.get_ticks()
        self.__hit_shake = pygame.Vector2(random() * HIT_POWER, random() * HIT_POWER)

    def draw(self, screen: pygame.Surface, events: list[pygame.event.Event]):
        now = pygame.time.get_ticks()
        elapsed = now - self.__last_hit
        offset = pygame.Vector2(0, 0)

        if elapsed < HIT_ATTACK + HIT_RECOVERY:
            # HIT ATTACK PHASE (shake outward)
            if elapsed < HIT_ATTACK:
                t = elapsed / HIT_ATTACK
                offset = lerp(pygame.Vector2(0, 0), self.__hit_shake, t)

            # HIT RECOVERY PHASE (shake returns to normal)
            else:
                t = (elapsed - HIT_ATTACK) / HIT_RECOVERY
                offset = lerp(self.__hit_shake, pygame.Vector2(0, 0), t)

        # Apply offset to rect
        position_rect = pygame.Rect(
            self.__rect.x + offset.x,
            self.__rect.y + offset.y,
            self.__rect.width,
            self.__rect.height
        )

        color = (0, 255, 0) if self.__sprite == SpriteName.PLAYER else (255, 0, 0)
        pygame.draw.rect(screen, color, position_rect)
