"""
GameEngine: owns the puck, both paddles, and the computer AI, and runs
one frame's worth of game logic.

Tasks implemented:
1. Fixed puck-paddle collision handling.
2. Added match scoring.
3. Added 30-second match timer handling through main.py.
4. Added proper puck reset and relaunch after scoring.
"""

import random

from game.puck import Puck
from game.paddle import Paddle
from game.ai import ComputerAI
from game.collisions import handle_paddle_collision
from game.renderer import WIDTH, HEIGHT, MARGIN, GOAL_TOP, GOAL_BOTTOM

PLAYER_SPEED = 6
PUCK_RADIUS = 12
PADDLE_RADIUS = 28
INITIAL_PUCK_SPEED = 4.5


class GameEngine:
    def __init__(self):
        # Match scores
        self.player_score = 0
        self.computer_score = 0

        # Create puck and launch it
        self.puck = Puck(WIDTH / 2, HEIGHT / 2, PUCK_RADIUS)
        self._launch_puck()

        # Player paddle
        self.player = Paddle(
            x=WIDTH * 0.15,
            y=HEIGHT / 2,
            radius=PADDLE_RADIUS,
            min_x=MARGIN + PADDLE_RADIUS,
            max_x=WIDTH / 2 - PADDLE_RADIUS,
            min_y=MARGIN + PADDLE_RADIUS,
            max_y=HEIGHT - MARGIN - PADDLE_RADIUS,
        )

        # Computer paddle
        self.computer = Paddle(
            x=WIDTH * 0.85,
            y=HEIGHT / 2,
            radius=PADDLE_RADIUS,
            min_x=WIDTH / 2 + PADDLE_RADIUS,
            max_x=WIDTH - MARGIN - PADDLE_RADIUS,
            min_y=MARGIN + PADDLE_RADIUS,
            max_y=HEIGHT - MARGIN - PADDLE_RADIUS,
        )

        self.ai = ComputerAI()

    def _launch_puck(self):
        """
        Give the puck a new starting velocity and direction.
        """
        angle_choices = [0.3, 0.6, -0.3, -0.6]

        direction = random.choice([-1, 1])
        vy_factor = random.choice(angle_choices)

        self.puck.vx = INITIAL_PUCK_SPEED * direction
        self.puck.vy = INITIAL_PUCK_SPEED * vy_factor

    def handle_input(self, keys_pressed):
        """
        Handle keyboard input for the player's paddle.
        """
        import pygame

        dx = dy = 0

        if keys_pressed[pygame.K_UP]:
            dy -= PLAYER_SPEED

        if keys_pressed[pygame.K_DOWN]:
            dy += PLAYER_SPEED

        if keys_pressed[pygame.K_LEFT]:
            dx -= PLAYER_SPEED

        if keys_pressed[pygame.K_RIGHT]:
            dx += PLAYER_SPEED

        self.player.move_by(dx, dy)

    def update(self):
        """
        Update the game state for one frame.
        """
        # Update computer paddle
        self.ai.update(self.computer, self.puck)

        # Move puck
        self.puck.move()

        # Bounce off top and bottom walls
        self.puck.bounce_off_walls(HEIGHT, MARGIN)

        # Handle paddle collisions
        handle_paddle_collision(self.puck, self.player)
        handle_paddle_collision(self.puck, self.computer)

        # Check for goals
        self._handle_goals()

    def _handle_goals(self):
        """
        Detect goals and update the appropriate score.

        Left goal:
            Computer scores.

        Right goal:
            Player scores.

        If the puck hits the wall outside the goal opening,
        it simply bounces back.
        """

        # Left side
        if self.puck.x - self.puck.radius < MARGIN:

            if GOAL_TOP < self.puck.y < GOAL_BOTTOM:
                # Computer scored
                self.computer_score += 1

                # Reset puck for the next point
                self._reset_puck()

            else:
                # Hit wall outside the goal
                self.puck.x = MARGIN + self.puck.radius
                self.puck.vx = -self.puck.vx

        # Right side
        elif self.puck.x + self.puck.radius > WIDTH - MARGIN:

            if GOAL_TOP < self.puck.y < GOAL_BOTTOM:
                # Player scored
                self.player_score += 1

                # Reset puck for the next point
                self._reset_puck()

            else:
                # Hit wall outside the goal
                self.puck.x = WIDTH - MARGIN - self.puck.radius
                self.puck.vx = -self.puck.vx

    def _reset_puck(self):
        """
        Reset the puck to the center of the table and immediately
        launch it again for the next point.
        """

        self.puck.x = WIDTH / 2
        self.puck.y = HEIGHT / 2

        # Give the puck a fresh velocity and direction.
        self._launch_puck()

    def get_winner(self):
        """
        Determine the winner based on the current scores.
        """

        if self.player_score > self.computer_score:
            return "Player"

        elif self.computer_score > self.player_score:
            return "Computer"

        else:
            return "Draw"

    def draw(self, surface, font):
        """
        Draw the table, paddles, puck, and scores.
        """
        from game import renderer

        # Draw table
        renderer.draw_table(surface)

        # Draw player paddle
        renderer.draw_paddle(
            surface,
            self.player,
            renderer.COLOR_PLAYER
        )

        # Draw computer paddle
        renderer.draw_paddle(
            surface,
            self.computer,
            renderer.COLOR_COMPUTER
        )

        # Draw puck
        renderer.draw_puck(surface, self.puck)

        # Draw player score
        renderer.draw_text(
            surface,
            font,
            f"Player: {self.player_score}",
            (30, 25)
        )

        # Draw computer score
        renderer.draw_text(
            surface,
            font,
            f"Computer: {self.computer_score}",
            (WIDTH - 180, 25)
        )