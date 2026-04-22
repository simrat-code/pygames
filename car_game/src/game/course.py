import pygame
import math

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE    = (255, 255, 255)
BLACK    = (0,   0,   0)
GRAY     = (100, 100, 100)
DARK_GRAY= (60,  60,  60)
GREEN    = (34,  139, 34)
YELLOW   = (255, 220, 0)
RED      = (220, 50,  50)


class Course:
    # def __init__(self):
    #     self.obstacles = []

    # def generate_course(self):
    #     # Logic to generate the layout of obstacles
    #     pass

    # def draw(self, screen):
    #     # Logic to draw the entire course and obstacles on the screen
    #     pass


    """
    Draws a simple oval/loop race track on an 800×600 screen.

    Track layout is defined by:
      - An outer polygon  (track boundary)
      - An inner polygon  (the "island" / infield)
    Everything outside the outer poly → green grass.
    The band between outer and inner → tarmac.
    """

    def __init__(self):
        # Outer boundary of the track
        self.outer_points = [
            (50,  50),
            (750, 50),
            (750, 550),
            (50,  550),
        ]

        # Inner boundary (the island in the middle)
        self.inner_points = [
            (180, 160),
            (620, 160),
            (620, 440),
            (180, 440),
        ]

        # Checkered start/finish line
        self.start_line = pygame.Rect(390, 50, 20, 110)

        # A few decorative track markings (dashed centre line segments)
        self.centre_dashes = self._build_centre_dashes()

    # ------------------------------------------------------------------
    def _build_centre_dashes(self):
        """Return a list of small Rects that form a dashed centre line."""
        dashes = []
        # Approximate midpoints between outer and inner boundary
        mid_y_top    = (50  + 160) // 2   # ≈ 105
        mid_y_bottom = (550 + 440) // 2   # ≈ 495
        mid_x_left   = (50  + 180) // 2   # ≈ 115
        mid_x_right  = (750 + 620) // 2   # ≈ 685

        # Top straight dashes  (horizontal)
        x = 100
        while x < 700:
            dashes.append(pygame.Rect(x, mid_y_top, 30, 6))
            x += 50

        # Bottom straight dashes (horizontal)
        x = 100
        while x < 700:
            dashes.append(pygame.Rect(x, mid_y_bottom, 30, 6))
            x += 50

        # Left straight dashes (vertical)
        y = 100
        while y < 500:
            dashes.append(pygame.Rect(mid_x_left, y, 6, 30))
            y += 50

        # Right straight dashes (vertical)
        y = 100
        while y < 500:
            dashes.append(pygame.Rect(mid_x_right, y, 6, 30))
            y += 50

        return dashes

    # ------------------------------------------------------------------
    def draw(self, surface):
        # 1. Background grass
        surface.fill(GREEN)

        # 2. Tarmac (outer polygon filled black, then inner polygon punched
        #    out by filling GREEN again – simple painter's algorithm)
        pygame.draw.polygon(surface, DARK_GRAY, self.outer_points)
        pygame.draw.polygon(surface, GREEN,     self.inner_points)

        # 3. White edge lines
        pygame.draw.polygon(surface, WHITE, self.outer_points, 3)
        pygame.draw.polygon(surface, WHITE, self.inner_points, 3)

        # 4. Dashed centre line (yellow)
        for dash in self.centre_dashes:
            pygame.draw.rect(surface, YELLOW, dash)

        # 5. Checkered start / finish line
        self._draw_start_line(surface)

    # ------------------------------------------------------------------
    def _draw_start_line(self, surface):
        """Draw a small black-and-white checkered rectangle."""
        rect  = self.start_line
        tile  = 10                     # size of each checker square
        cols  = rect.width  // tile
        rows  = rect.height // tile

        for row in range(rows):
            for col in range(cols):
                color = WHITE if (row + col) % 2 == 0 else BLACK
                r = pygame.Rect(
                    rect.x + col * tile,
                    rect.y + row * tile,
                    tile, tile
                )
                pygame.draw.rect(surface, color, r)

    # ------------------------------------------------------------------
    def is_on_track(self, x, y):
        """
        Returns True when the point (x, y) is on the tarmac.
        Uses pygame's collidepoint on the bounding polygons via a
        Surface-based mask approach (fast-enough for a hobby project).
        """
        # Simple AABB approximation — replace with polygon point-in-poly
        # test for production code.
        inside_outer = (
            self.outer_points[0][0] < x < self.outer_points[1][0] and
            self.outer_points[0][1] < y < self.outer_points[2][1]
        )
        inside_inner = (
            self.inner_points[0][0] < x < self.inner_points[1][0] and
            self.inner_points[0][1] < y < self.inner_points[2][1]
        )
        return inside_outer and not inside_inner