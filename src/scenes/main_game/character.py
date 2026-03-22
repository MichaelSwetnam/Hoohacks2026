import pygame
import enum
from constants import CHARACTER_SIZE, CHARACTER_SIDE_PADDING, SCREEN_HEIGHT, SCREEN_WIDTH
from random import random
from load_image import load_image

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
    ENEMY_2 = 3
    ENEMY_3 = 4

class SpriteState(enum.Enum):
    IDLE = 1
    DAMAGE = 2
    SHOOT = 3

def get_sprite_state_suffix(state: SpriteState) -> str: 
    if state == SpriteState.IDLE:
        return "_idle.png"
    elif state == SpriteState.DAMAGE:
        return "_damage.png"
    else:
        return "_shoot.png"

def get_sprite_prefix(spriteName: SpriteName) -> str:
    if spriteName == SpriteName.PLAYER:
        return "player"
    elif spriteName == SpriteName.ENEMY_1:
        return "enemy1"
    elif spriteName == SpriteName.ENEMY_2:
        return "enemy2"
    else:
        return "enemy3"

ASSET_CACHE: dict[str, pygame.Surface] = {}
def get_sprite_asset(name: SpriteName, state: SpriteState, flipped: bool) -> pygame.Surface:    
    """ Important! Flipped is only processed the first time a surface is loaded. On repeated loads it will STAY flipped or not flipped"""

    asset_name = get_sprite_prefix(name) + get_sprite_state_suffix(state)

    # Get from cache
    if asset_name in ASSET_CACHE:
        return ASSET_CACHE[asset_name]

    # Load sprite
    surface = load_image(asset_name, pygame.Vector2(SIZE_X, SIZE_Y))
    if flipped:
        surface = pygame.transform.flip(surface, flipped, False)

    ASSET_CACHE[asset_name] = surface
    return surface

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

# Damage animation
DAMAGE_ATTACK = 0.1 * 1000
DAMAGE_RECOVERY = 0.2 * 1000
DAMAGE_POWER = 50

# Attack animation
ATTACK_DURATION = 0.5 * 1000

def lerp(a: pygame.Vector2, b: pygame.Vector2, t: float):
    return a + (b - a) * t

class Character:
    __sprite: SpriteName
    __state: SpriteState
    __flipped: bool
    __rect: pygame.Rect

    __last_hit: int
    __hit_shake: pygame.Vector2
    __last_attack: int

    def __init__(self, sprite: SpriteName):
        self.__sprite = sprite
        self.__state = SpriteState.IDLE

        if sprite == SpriteName.PLAYER:
            self.__flipped = False
            self.__rect = PLAYER_RECT
        else:
            self.__flipped = True
            self.__rect = ENEMY_RECT

        self.__last_hit = 0
        self.__last_attack = 0
        self.__hit_shake = pygame.Vector2(0, 0)

    def hit(self):
        self.__last_hit = pygame.time.get_ticks()
        self.__hit_shake = pygame.Vector2(random() * DAMAGE_POWER, random() * DAMAGE_POWER)

    def attack(self):
        self.__last_attack = pygame.time.get_ticks()

    def __render(self, screen: pygame.Surface, offset: pygame.Vector2):
         # Apply offset to rect
        position_rect = pygame.Rect(
            self.__rect.x + offset.x,
            self.__rect.y + offset.y,
            self.__rect.width,
            self.__rect.height
        )
        
        screen.blit(get_sprite_asset(self.__sprite, self.__state, self.__flipped), position_rect)

    def draw(self, screen: pygame.Surface, events: list[pygame.event.Event]):
        now = pygame.time.get_ticks()
        damageElapsed = now - self.__last_hit
        attackElapsed = now - self.__last_attack

        offset = pygame.Vector2(0, 0)

        isDamage = damageElapsed <= DAMAGE_ATTACK + DAMAGE_RECOVERY
        isAttack = attackElapsed <=  ATTACK_DURATION

        # Playing idle animation
        if not isDamage and not isAttack:
            self.__state = SpriteState.IDLE
            self.__render(screen, offset)
            return

        # Playing hurt
        if isAttack:
            self.__state = SpriteState.SHOOT
            self.__render(screen, offset)
            return

        # Playing damage    
        self.__state = SpriteState.DAMAGE

        # HIT ATTACK PHASE (shake outward)
        if damageElapsed < DAMAGE_ATTACK:
            t = damageElapsed / DAMAGE_ATTACK
            offset = lerp(pygame.Vector2(0, 0), self.__hit_shake, t)

        # HIT RECOVERY PHASE (shake returns to normal)
        else:
            t = (damageElapsed - DAMAGE_ATTACK) / DAMAGE_RECOVERY
            offset = lerp(self.__hit_shake, pygame.Vector2(0, 0), t)

        self.__render(screen, offset)

       
