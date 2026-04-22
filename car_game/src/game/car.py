import pygame
import math
from . import utils

class Car:
    # def __init__(self, position=(0, 0), speed=0):
    #     self.position = position
    #     self.speed = speed

    # def move(self, direction):
    #     if direction == "up":
    #         self.position = (self.position[0], self.position[1] - self.speed)
    #     elif direction == "down":
    #         self.position = (self.position[0], self.position[1] + self.speed)
    #     elif direction == "left":
    #         self.position = (self.position[0] - self.speed, self.position[1])
    #     elif direction == "right":
    #         self.position = (self.position[0] + self.speed, self.position[1])

    # def draw(self, screen):
    #     # Placeholder for drawing the car on the screen
    #     pass

    """
    Top-down 2-D car with basic arcade physics.

    The car sprite is drawn procedurally (no image file needed):
      - a coloured body rectangle
      - darker windscreen
      - four small wheel rectangles
    Rotation is handled with pygame.transform.rotate on a pre-rendered
    surface so the rest of the code stays simple.
    """

    # Tuning constants
    ACCELERATION  = 0.15   # pixels/frame² when throttle is on
    BRAKE_FORCE   = 0.25   # deceleration when braking
    FRICTION      = 0.97   # speed multiplier each frame (drag)
    TURN_SPEED    = 3.0    # degrees per frame at full speed
    MAX_SPEED     = 5.0    # pixels per frame

    def __init__(self, x, y, angle=0, color=utils.RED):
        self.x      = float(x)
        self.y      = float(y)
        self.angle  = float(angle)   # degrees; 0 = pointing right
        self.speed  = 0.0
        self.color  = color

        # Size of the car body in its local (unrotated) frame
        self.width  = 40
        self.height = 20

        # Pre-render the car onto a small surface for rotation
        self._car_surf = self._build_car_surface()

    # ------------------------------------------------------------------
    def _build_car_surface(self):
        """
        Create the car image on a transparent surface.
        Origin is at the *centre* of the surface.
        """
        pad = 4   # padding so rotated corners aren't clipped
        w   = self.width  + pad * 2
        h   = self.height + pad * 2
        surf = pygame.Surface((w, h), pygame.SRCALPHA)

        # --- Body ---
        body_rect = pygame.Rect(pad, pad, self.width, self.height)
        pygame.draw.rect(surf, self.color, body_rect, border_radius=4)

        # --- Windscreen (front third, slightly darker) ---
        ws_w = self.width // 3
        ws_rect = pygame.Rect(
            pad + self.width - ws_w - 3,
            pad + 3,
            ws_w,
            self.height - 6
        )
        pygame.draw.rect(surf, (180, 220, 255, 200), ws_rect, border_radius=2)

        # --- Wheels (four corners) ---
        wheel_w, wheel_h = 6, 10
        wheel_color = (30, 30, 30)
        offsets = [
            (pad - wheel_w + 2,              pad + 1),          # front-left
            (pad - wheel_w + 2,              pad + self.height - wheel_h - 1),  # rear-left
            (pad + self.width - 2,           pad + 1),          # front-right
            (pad + self.width - 2,           pad + self.height - wheel_h - 1),  # rear-right
        ]
        for ox, oy in offsets:
            pygame.draw.rect(surf, wheel_color,
                             pygame.Rect(ox, oy, wheel_w, wheel_h),
                             border_radius=1)

        return surf

    # ------------------------------------------------------------------
    def handle_input(self):
        """Read keyboard state and update speed / angle."""
        keys = pygame.key.get_pressed()

        # Throttle / brake
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.speed = min(self.speed + self.ACCELERATION, self.MAX_SPEED)
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.speed = max(self.speed - self.BRAKE_FORCE, -self.MAX_SPEED / 2)

        # Steering (only meaningful when moving)
        if abs(self.speed) > 0.1:
            turn = self.TURN_SPEED * (self.speed / self.MAX_SPEED)
            if keys[pygame.K_LEFT]  or keys[pygame.K_a]:
                self.angle -= turn
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.angle += turn

    # ------------------------------------------------------------------
    def update(self):
        """Apply physics and move the car."""
        self.handle_input()

        # Friction
        self.speed *= self.FRICTION

        # Convert angle to velocity vector
        rad = math.radians(self.angle)
        self.x += math.cos(rad) * self.speed
        self.y += math.sin(rad) * self.speed

        # Keep within screen bounds
        self.x = max(0, min(utils.SCREEN_WIDTH,  self.x))
        self.y = max(0, min(utils.SCREEN_HEIGHT, self.y))

    # ------------------------------------------------------------------
    def draw(self, surface):
        """Rotate the pre-rendered car surface and blit it centred on (x, y)."""
        # pygame rotates counter-clockwise, our angle is clockwise → negate
        rotated = pygame.transform.rotate(self._car_surf, -self.angle)
        rect    = rotated.get_rect(center=(int(self.x), int(self.y)))
        surface.blit(rotated, rect)