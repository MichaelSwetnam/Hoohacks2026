import pygame
from components.LoadingBar import LoadingBar

BUBBLE_COLOR = (255, 255, 240)
BUBBLE_BORDER = (80, 50, 20)
TEXT_COLOR    = (30, 20, 10)
TYPED_COLOR   = (60, 140, 60)    # green = correct
ERROR_COLOR   = (200, 40, 40)    # red   = wrong character
GHOST_COLOR   = (180, 160, 120)  # untyped characters


class TypingChallenge:
    """
    Speech bubble typing widget.
    Call draw() every frame — returns:
        None        while player is still typing
        "success"   prompt fully matched in time
        "fail"      timer ran out
    """

    def __init__(self, prompt: str, time_limit: float = 6.0):
        self.prompt     = prompt
        self.time_limit = time_limit
        self.time_left  = time_limit
        self.typed      = ""
        self.result     = None
        self.done       = False

        self.font_prompt = pygame.font.SysFont("couriernew", 28, bold=True)
        self.font_input  = pygame.font.SysFont("couriernew", 28)
        self.font_timer  = pygame.font.SysFont("couriernew", 22)

        # Reuses your existing LoadingBar for the countdown
        self.timer_bar = LoadingBar(
            x=80, y=178,
            width=1120, height=18,
            border_margin=3,
            fill_color=(50, 200, 50),
            border_color=(60, 40, 20)
        )
        self.timer_bar.set_progress(1.0)

    # ------------------------------------------------------------------
    def draw(self, screen: pygame.Surface,
             events: list[pygame.event.Event], dt: float) -> str | None:
        if self.done:
            return self.result

        # Tick timer
        self.time_left -= dt
        if self.time_left <= 0:
            self.time_left = 0.0
            self.result    = "fail"
            self.done      = True

        self._handle_events(events)

        # Update LoadingBar progress and colour
        ratio = max(0.0, self.time_left / self.time_limit)
        self.timer_bar.set_progress(ratio)
        if ratio > 0.5:
            self.timer_bar._LoadingBar__fill_color = (50,  200, 50)
        elif ratio > 0.25:
            self.timer_bar._LoadingBar__fill_color = (255, 180, 0)
        else:
            self.timer_bar._LoadingBar__fill_color = (220, 40,  40)

        self._draw_bubble(screen)
        self.timer_bar.draw(screen, events)
        self._draw_timer_label(screen)
        self._draw_input_line(screen)

        return self.result if self.done else None

    # ------------------------------------------------------------------
    def _handle_events(self, events):
        for event in events:
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_BACKSPACE:
                self.typed = self.typed[:-1]
            elif event.unicode and len(self.typed) < len(self.prompt):
                self.typed += event.unicode
                if self.typed == self.prompt:
                    self.result = "success"
                    self.done   = True

    # ------------------------------------------------------------------
    def _draw_bubble(self, screen: pygame.Surface):
        bubble_x, bubble_y = 80, 60
        bubble_w, bubble_h = 1120, 100
        padding = 24

        # Shadow
        pygame.draw.rect(screen, (160, 130, 90),
                         pygame.Rect(bubble_x + 4, bubble_y + 4, bubble_w, bubble_h),
                         border_radius=16)
        # Bubble body
        bubble_rect = pygame.Rect(bubble_x, bubble_y, bubble_w, bubble_h)
        pygame.draw.rect(screen, BUBBLE_COLOR, bubble_rect, border_radius=16)
        pygame.draw.rect(screen, BUBBLE_BORDER, bubble_rect, width=3, border_radius=16)

        # Tail
        tx = bubble_x + bubble_w - 80
        ty = bubble_y + bubble_h + 18
        pygame.draw.polygon(screen, BUBBLE_COLOR, [
            (tx - 14, bubble_y + bubble_h - 2),
            (tx + 14, bubble_y + bubble_h - 2),
            (tx,      ty),
        ])
        pygame.draw.polygon(screen, BUBBLE_BORDER, [
            (tx - 14, bubble_y + bubble_h - 2),
            (tx + 14, bubble_y + bubble_h - 2),
            (tx,      ty),
        ], 2)

        # Prompt text
        surf = self.font_prompt.render(self.prompt, True, TEXT_COLOR)
        screen.blit(surf, (bubble_x + padding,
                           bubble_y + bubble_h // 2 - surf.get_height() // 2))

    # ------------------------------------------------------------------
    def _draw_timer_label(self, screen):
        label = self.font_timer.render(f"{self.time_left:.1f}s", True, (230, 210, 170))
        screen.blit(label, (1210, 176))

    # ------------------------------------------------------------------
    def _draw_input_line(self, screen):
        x, y = 80, 210
        for i, char in enumerate(self.prompt):
            if i < len(self.typed):
                color = TYPED_COLOR if self.typed[i] == char else ERROR_COLOR
                surf  = self.font_input.render(self.typed[i], True, color)
            else:
                surf = self.font_input.render(char, True, GHOST_COLOR)
            screen.blit(surf, (x, y))
            x += surf.get_width()

        # Blinking cursor
        if not self.done and (pygame.time.get_ticks() // 500) % 2 == 0:
            pygame.draw.rect(screen, (220, 200, 140),
                             pygame.Rect(x, y + 2, 2, self.font_input.get_height() - 4))