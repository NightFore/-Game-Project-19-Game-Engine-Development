import pygame

def align_rect(source_rect, target_position, align):
    """
    Aligns the source rectangle based on the specified alignment relative to the target position.

    Args:
        source_rect (pygame.Rect): The source rectangle to be aligned.
        target_position (tuple): The target position (x, y) to align the source rectangle to.
        align (str): The alignment specifier (e.g., 'center', 'nw', 'n', 'ne', 'w', 'e', 'sw', 's', 'se').

    Returns:
        pygame.Rect: The aligned rectangle.
    """
    if align == 'center':
        source_rect.center = target_position
    elif align == 'nw':
        source_rect.topleft = target_position
    elif align == 'n':
        source_rect.midtop = target_position
    elif align == 'ne':
        source_rect.topright = target_position
    elif align == 'w':
        source_rect.midleft = target_position
    elif align == 'e':
        source_rect.midright = target_position
    elif align == 'sw':
        source_rect.bottomleft = target_position
    elif align == 's':
        source_rect.midbottom = target_position
    elif align == 'se':
        source_rect.bottomright = target_position

    return source_rect
