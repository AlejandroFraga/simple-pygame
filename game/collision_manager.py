"""
Functions to handle and calculate the collisions of the game
"""

import pygame


def __collision_axis_x(game_object, collider):

    # Depending on the direction on the x-axis, we get the exact point, where the collision occurred
    if game_object.direction_x > 0:
        return collider.rect.x - game_object.rect.width

    else:
        return collider.rect.x + collider.rect.width


def __collision_axis_y(game_object, collider):

    # Depending on the direction on the y-axis, we get the exact point, where the collision occurred
    if game_object.direction_y > 0:
        return collider.rect.y - game_object.rect.height

    else:
        return collider.rect.y + collider.rect.height


def __collision_x(game_object, collider, first_collision=None, first_collider=None):

    # Get the x-axis position of the collision
    collision_axis_x = __collision_axis_x(game_object, collider)

    # If it's the firs position to be evaluated
    # Or by the direction, the collision is nearer to the player position before (so the collision was also before)
    if (first_collision is None
            or (game_object.direction_x > 0 and collision_axis_x < first_collision)
            or (game_object.direction_x <= 0 and collision_axis_x > first_collision)):

        # We update the first collision values
        first_collision = collision_axis_x
        first_collider = collider

    return first_collision, first_collider


def __collision_y(game_object, collider, first_collision=None, first_collider=None):

    # Get the y-axis position of the collision
    collision_axis_y = __collision_axis_y(game_object, collider)

    # If it's the firs position to be evaluated
    # Or by the direction, the collision is nearer to the player position before (so the collision was also before)
    if (first_collision is None
            or (game_object.direction_y > 0 and collision_axis_y < first_collision)
            or (game_object.direction_y <= 0 and collision_axis_y > first_collision)):

        # We update the first collision values
        first_collision = collision_axis_y
        first_collider = collider

    return first_collision, first_collider


def __first_collision_x(game_object, colliders):
    collision = None
    collider = None

    # We check which is the first collision by comparing the x-axis position of the colliders
    for collider_aux in colliders:
        collision, collider = __collision_x(game_object, collider_aux, collision, collider)

    return collision, collider


def __first_collision_y(game_object, colliders):
    collision = None
    collider = None

    # We check which is the first collision by comparing the y-axis position of the colliders
    for collider_aux in colliders:
        collision, collider = __collision_y(game_object, collider_aux, collision, collider)

    return collision, collider


def __get_colliders(game_character, colliders_group):

    # To avoid the game character to collide with himself, we check if he is inside the group
    is_in_group = game_character in colliders_group

    # In case that he is inside, before checking collisions, we remove him from the group, and add him later
    if is_in_group:
        colliders_group.remove(game_character)

    # Get all the sprites that are colliding with the game character from the given colliders group
    colliders = pygame.sprite.spritecollide(game_character, colliders_group, False)

    # In case that he was inside add him again
    if is_in_group:
        colliders_group.add(game_character)

    return colliders


def handle_collisions_x(game_character, colliders_group):
    """
    Function to handle the collisions in the x-axis by the movement of the game character

    :param game_character: Game character that has triggered the collision
    :param colliders_group: Sprite group in which the collision occurred
    """

    # Check if the game character collided
    colliders = __get_colliders(game_character, colliders_group)
    if colliders.__len__() > 0:

        # We store as new position, the current location, in which the game_character is triggering the collision
        new_pos_x = game_character.x_f

        # We calculate the exact position of the first collision so we can give it to the game character
        collision, collider = __first_collision_x(game_character, colliders)
        if collision is not None:
            new_pos_x = collision

        # Call the game character collide function, so he can react to this collision
        game_character.collide([new_pos_x, game_character.y_f], collider)


def handle_collisions_y(game_character, colliders_group):
    """
    Function to handle the collisions in the y-axis by the movement of the game character

    :param game_character: Game character that has triggered the collision
    :param colliders_group: Sprite group in which the collision occurred
    """

    # Check if the game character collided
    colliders = __get_colliders(game_character, colliders_group)
    if colliders.__len__() > 0:

        # We store as new position, the current location, in which the game_character is triggering the collision
        new_pos_y = game_character.y_f

        # We calculate the exact position of the first collision so we can give it to the game character
        collision, collider = __first_collision_y(game_character, colliders)
        if collision is not None:
            new_pos_y = collision

        # Call the game character collide function, so he can react to this collision
        game_character.collide([game_character.x_f, new_pos_y], collider)
