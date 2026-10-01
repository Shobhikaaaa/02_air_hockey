"""
collisions: puck-vs-paddle collision handling.
"""


def handle_paddle_collision(puck, paddle):
    """
    If the puck overlaps the paddle, bounce it off using the collision
    normal and push it outside the paddle so it cannot get stuck.

    Returns True if a collision was handled this frame.
    """
    dx = puck.x - paddle.x
    dy = puck.y - paddle.y

    distance_squared = dx ** 2 + dy ** 2
    min_distance = puck.radius + paddle.radius

    if distance_squared >= min_distance ** 2:
        return False

    # Handle the extremely unlikely case where puck and paddle centers
    # are exactly on top of each other.
    if distance_squared == 0:
        nx, ny = 1.0, 0.0
        distance = 0.0
    else:
        distance = distance_squared ** 0.5
        nx = dx / distance
        ny = dy / distance

    # Move the puck outside the paddle to prevent it from getting stuck.
    overlap = min_distance - distance
    puck.x += nx * overlap
    puck.y += ny * overlap

    # Reflect the puck velocity around the collision normal.
    velocity_along_normal = puck.vx * nx + puck.vy * ny

    # If the puck is already moving away from the paddle, don't reflect it again.
    if velocity_along_normal >= 0:
        return True

    puck.vx -= 2 * velocity_along_normal * nx
    puck.vy -= 2 * velocity_along_normal * ny

    return True