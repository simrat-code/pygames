import imp
import pygame
import sys
from game.car import Car
from game.obstacle import Obstacle
from game.course import Course
from game import utils

# Initialize Pygame
pygame.init()

# Set up the game window
screen = pygame.display.set_mode((utils.SCREEN_WIDTH, utils.SCREEN_HEIGHT))
pygame.display.set_caption("2D Car Game")

# Create game objects
# car = Car()
# course = Course()

# # Main game loop
# def main2():
#     clock = pygame.time.Clock()
#     # WASD keys for movement
#     direction = "up"  # Default direction
#     while True:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()

#         keys = pygame.key.get_pressed()
#         if keys[pygame.K_w]:
#             direction = "up"
#         if keys[pygame.K_s]:
#             direction = "down"
#         if keys[pygame.K_a]:
#             direction = "left"
#         if keys[pygame.K_d]:
#             direction = "right"

#         # Update game state
#         car.move(direction)

#         # Draw everything
#         screen.fill((255, 255, 255))  # Clear screen with white
#         course.draw(screen)
#         car.draw(screen)
        
#         pygame.display.flip()  # Update the display
#         clock.tick(60)  # Limit to 60 frames per second

def main():
    pygame.init()
    screen  = pygame.display.set_mode((utils.SCREEN_WIDTH, utils.SCREEN_HEIGHT))
    pygame.display.set_caption("2-D Car Game")
    clock   = pygame.time.Clock()
    font    = pygame.font.SysFont("monospace", 16)

    course  = Course()
    car     = Car(x=400, y=120, angle=0, color=utils.RED)

    running = True
    while running:
        # ── Events ──────────────────────────────
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        # ── Update ──────────────────────────────
        car.update()

        on_track = course.is_on_track(car.x, car.y)
        if not on_track:
            car.speed *= 0.85   # slow down when on grass

        # ── Draw ────────────────────────────────
        course.draw(screen)
        car.draw(screen)

        # HUD
        status = "ON TRACK" if on_track else "OFF TRACK"
        hud = font.render(
            f"Speed: {car.speed:+.2f}  Angle: {car.angle % 360:.0f}°  {status}",
            True, utils.WHITE
        )
        screen.blit(hud, (10, 10))

        pygame.display.flip()
        clock.tick(utils.FPS)

    pygame.quit()

if __name__ == "__main__":
    main()