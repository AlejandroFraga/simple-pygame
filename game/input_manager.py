"""
The input manager is used to process all the inputs received from the __player
"""
import pygame

# Keys to exit the game loop and end execution
exit_keys = [pygame.K_ESCAPE]

# Keys to control the movement of the __player
move_left_keys = [pygame.K_LEFT, pygame.K_a]
move_right_keys = [pygame.K_RIGHT, pygame.K_d]
move_up_keys = [pygame.K_UP, pygame.K_w]
move_down_keys = [pygame.K_DOWN, pygame.K_s]


def is_pressed(pressed_keys, keys):
    """
    Function that given an sequence of booleans that correspond to the pressed keys
    indicates if any of the indicated keys are pressed
    """

    # For each key check if the key is pressed as its value in the sequence is true
    for key in keys:
        if pressed_keys[key]:
            return True
    # If none of the keys is pressed, return false
    return False


def get_movement_inputs(pressed_keys):
    """
    Function that checks and stores the direction of movement in both axis given the
    sequence of booleans that correspond to the pressed keys
    """

    # Initiate the variables with the default values
    direction_x, direction_y = 0.0, 0.0

    # Check for every direction individually so multiple keys can be pressed at the
    # same time, having all of them into account
    if is_pressed(pressed_keys, move_left_keys):
        direction_x -= 1.0

    if is_pressed(pressed_keys, move_right_keys):
        direction_x += 1.0

    if is_pressed(pressed_keys, move_up_keys):
        direction_y -= 1.0

    if is_pressed(pressed_keys, move_down_keys):
        direction_y += 1.0

    return direction_x, direction_y


def get_inputs():
    """
    Function that returns the values of the inputs of the __player
    """

    # Get all the pressed keys
    pressed_keys = pygame.key.get_pressed()

    # If any of the exit keys are pressed, set to exit the game loop
    is_game_over = is_pressed(pressed_keys, exit_keys)

    # Get the movement inputs
    direction_x, direction_y = get_movement_inputs(pressed_keys)

    return direction_x, direction_y, is_game_over


def handle_quit_event(events):
    """
    Function that checks all the events looking for a QUIT event, it returns
    True if it's found, and False otherwise
    """

    # If we have a QUIT event, exit out of the game loop
    for event in events:
        if event.type == pygame.QUIT:
            return True
    # If none of the events is QUIT, return false
    return False
