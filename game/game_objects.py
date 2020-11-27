"""
Game Object classes to
"""
import enum

import pygame

import collision_manager
import input_manager
from data_helper import limit_value, is_list_of_size, is_number
from file_manager import load_image


# creating enumerations using class
class Tag(enum.Enum):
    """
    Enumeration to identify fast and easily Game Objects
    """

    player = 1
    treasure = 2
    enemy = 3


class TileBase(pygame.sprite.DirtySprite):
    """
    Base class for any Sprite in the game
    """

    def __init__(self, image, size=None):
        super().__init__()

        if size is not None:
            self.image = load_image(image, size, size)
        else:
            self.image = image

        self.rect = self.image.get_rect()


class GameObject(TileBase):
    """
    Class that inherits from the Tile Base class for any Game Object in the game
    """

    def __init__(self, tile_base, x, y, tag=None):
        super().__init__(tile_base.image)
        self.rect.x = x
        self.rect.y = y
        self.tag = tag

    def collide(self, position, collider=None):
        """
        Function that manages the collision of the Game Object in a certain position with a collider

        :param position: Position (x-axis, y-axis) in which the collision occurred
        :param collider: Game Object with which collided
        """

        pass


class GameCharacter(GameObject):
    """
    Class that inherits from the Game Object class for any Character of the game
    """

    speed = 0.0
    direction_x = 0.0
    direction_y = 0.0

    def __init__(self, tile_base, x, y, tag=None):
        super().__init__(tile_base, x, y, tag)
        self.position_before_x = x
        self.position_before_y = y
        self.x_f = x
        self.y_f = y

    def move_to_x(self, x):
        """
        Move the Game Character to the desired x-axis position

        :param x: Position in the x-axis to move to
        """

        if is_number(x):
            self.position_before_x = self.x_f
            self.x_f = x
            self.rect.x = round(self.x_f)

    def move_to_y(self, y):
        """
        Move the Game Character to the desired y-axis position

        :param y: Position in the y-axis to move to
        """

        if is_number(y):
            self.position_before_y = self.y_f
            self.y_f = y
            self.rect.y = round(self.y_f)

    def move_to(self, point):
        """
        Move the Game Character to the desired point(x-axis, y-axis) position

        :param point: Position (x-axis, y-axis) to move to
        """

        if is_list_of_size(point, 2):
            self.move_to_x(point[0])
            self.move_to_y(point[1])


class PlayerCharacter(GameCharacter):
    """
    Class that inherits from the Game Character class for the Player of the game
    """

    speed = 0.5
    exit = False
    repeat = False
    won = None

    def __init__(self, tile_base, x, y, tag=None):
        super().__init__(tile_base, x, y, tag)

    def move_x(self, delta_time, width):
        """
        Move the character in the x-axis given a delta time, with a speed and a direction. Sticking to the limit
        if the position is lower than 0 or greater than the width of the __screen_manager minus the width of the character

        :param delta_time:
        :param width:
        :return:
        """

        # Before storing the value in the rect component, we use the float variables to make more precise calculations
        self.position_before_x = self.x_f

        self.x_f += self.direction_x * self.speed * delta_time
        self.x_f = limit_value(self.x_f, 0, width - self.rect.width)

        self.rect.x = round(self.x_f)

    def move_y(self, delta_time, height):
        """
        Move the character in the y-axis given a delta time, with a speed and a direction. Sticking to the limit
        if the position is lower than 0 or greater than the height of the __screen_manager minus the height of the character

        :param delta_time:
        :param height:
        :return:
        """

        # Before storing the value in the rect component, we use the float variables to make more precise calculations
        self.position_before_y = self.y_f

        self.y_f += self.direction_y * self.speed * delta_time
        self.y_f = limit_value(self.y_f, 0, height - self.rect.height)

        self.rect.y = round(self.y_f)

    def move(self, delta_time, display, colliders_group):
        """
        Move the character in the x-axis given a delta time, with a speed and a direction bouncing if the
        position is lower than 0 or greater than the width of the __screen_manager minus the width of the character


        :param delta_time:
        :param display:
        :param colliders_group:
        :return:
        """

        # We move in each axis and handle the possible collisions
        self.move_x(delta_time, display.width)
        collision_manager.handle_collisions_x(self, colliders_group)

        self.move_y(delta_time, display.height)
        collision_manager.handle_collisions_y(self, colliders_group)

    def update(self, *args, **kwargs):
        """
        Function that is called in each frame to execute the behaviour of character

        :param args: The expected arguments are the delta time, the __screen_manager, and the colliders group
        """

        # Get all the inputs of the __player
        self.direction_x, self.direction_y, self.exit = input_manager.get_inputs()
        self.exit += input_manager.handle_quit_event(pygame.event.get())

        # In each frame, we move and handle the possible collisions
        if args.__len__() > 2:
            delta_time, display, colliders_group = args

            self.move(delta_time, display, colliders_group)

    def collide(self, position, collider=None):

        # Check if we collided with an enemy or the treasure to exit the game loop
        if isinstance(collider, GameObject):
            if collider.tag == Tag.treasure:
                self.exit = True
                self.won = True

            elif collider.tag == Tag.enemy:
                self.exit = True
                self.repeat = True
                self.won = False

        # We move to the position of the collision
        self.move_to(position)


class EnemyCharacter(GameCharacter):
    """
    Class that inherits from the Game Character class for the Enemies in the game
    """

    speed = 0.2
    direction_x = 1.0

    def __init__(self, tile_base, x, y, tag=None):
        super().__init__(tile_base, x, y, tag)

    def move_x(self, delta_time, width):
        """
        Move the character in the x-axis given a delta time, with a speed and a direction. Bouncing if the
        position is lower than 0 or greater than the width of the __screen_manager minus the width of the character

        :param delta_time: Time between game loops
        :param width: Width of the __screen_manager
        """

        # Before storing the value in the rect component, we use the float variables to make more precise calculations
        self.x_f += self.direction_x * self.speed * delta_time

        # If the new position in the x-axis is lower than 0 or greater than the width of the __screen_manager minus the
        # width of the character, collide
        if self.x_f < 0:
            self.__collide_x(0)

        elif self.x_f > width - self.rect.width:
            self.__collide_x(width - self.rect.width)

        self.rect.x = round(self.x_f)

    def __collide_x(self, collision_point_x):
        """
        Manage the x-axis collision by bouncing and inverting the direction of the character

        :param collision_point_x: Y-axis position in which the collision occurred
        """

        self.direction_x = -self.direction_x
        self.move_to(collision_point_x * 2 - self.x_f)

    def __collide_y(self, collision_point_y):
        """
        Manage the y-axis collision by bouncing and inverting the direction of the character

        :param collision_point_y: Y-axis position in which the collision occurred
        """

        self.direction_y = -self.direction_y
        self.move_to(collision_point_y * 2 - self.y_f)

    def update(self, *args, **kwargs):
        """
        Function that is called in each frame to execute the behaviour of character

        :param args: The expected arguments are the delta time, the __screen_manager, and the colliders group
        """

        # In each frame, we move in the x-axis and handle the possible collisions
        if args.__len__() > 2:
            delta_time, display, colliders_group = args

            self.move_x(delta_time, display.width)
            collision_manager.handle_collisions_x(self, colliders_group)

    def collide(self, position, collider=None):

        # Check that the collider is not the __player so he is the one that manages this collision
        if type(collider) is not PlayerCharacter:
            if is_list_of_size(position, 2):

                # Split the collision in x-axis and y-axis so both directions can be easily managed
                if position[0] is not None:
                    self.__collide_x(position[0])

                if position[1] is not None:
                    self.__collide_y(position[1])
