"""
Air Hockey

Run with: python3 main.py

Controls: Arrow keys move your paddle (left side, blue).
"""

import pygame

from game.game_engine import GameEngine
from game.renderer import WINDOW_SIZE, WIDTH


MATCH_DURATION = 30_000  # 30 seconds in milliseconds


def main():
    pygame.init()

    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Air Hockey")

    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 24)

    engine = GameEngine()

    running = True
    match_over = False

    # Record the exact time at which the match starts.
    match_start_time = pygame.time.get_ticks()

    while running:

        # -------------------------
        # Handle events
        # -------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # -------------------------
        # Calculate remaining time
        # -------------------------
        elapsed_time = pygame.time.get_ticks() - match_start_time

        remaining_time = max(0, MATCH_DURATION - elapsed_time)

        # Convert milliseconds to seconds for display.
        remaining_seconds = (remaining_time + 999) // 1000

        # -------------------------
        # Match still running
        # -------------------------
        if not match_over:

            keys = pygame.key.get_pressed()
            engine.handle_input(keys)
            engine.update()

            # Match ends when 30 seconds have elapsed.
            if remaining_time <= 0:
                match_over = True

        # -------------------------
        # Draw game
        # -------------------------
        engine.draw(screen, font)

        # Display remaining time.
        timer_text = f"Time: {remaining_seconds}"

        timer_surface = font.render(
            timer_text,
            True,
            (255, 255, 255)
        )

        timer_rect = timer_surface.get_rect(
            center=(WIDTH // 2, 25)
        )

        screen.blit(timer_surface, timer_rect)

        # -------------------------
        # Display result when match ends
        # -------------------------
        if match_over:
            winner = engine.get_winner()

            if winner == "Player":
                result_text = "Player Wins!"
            elif winner == "Computer":
                result_text = "Computer Wins!"
            else:
                result_text = "Draw!"

            from game import renderer

            renderer.draw_banner(
                screen,
                font,
                result_text
            )

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()