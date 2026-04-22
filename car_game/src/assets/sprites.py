def load_sprite(image_path):
    """Load a single sprite image from the given path."""
    import pygame
    return pygame.image.load(image_path)

def load_sprites(image_paths):
    """Load multiple sprite images from a list of paths."""
    return [load_sprite(path) for path in image_paths]

def scale_sprite(sprite, width, height):
    """Scale a sprite to the specified width and height."""
    return pygame.transform.scale(sprite, (width, height))

def load_animations(animation_paths):
    """Load a series of sprite images for animations."""
    return [load_sprite(path) for path in animation_paths]