"""
Main file in the game that calls the level loader to load the lever from the given file
Controls the display though the screen manager
"""

import sys

import pygame

from level_manager import LevelLoader
from screen import ScreenManager
from data_helper import is_list_of_size


class GameController:
    # Groups of sprites loaded
    __background = None
    __colliders = None
    __interactive = None

    # Player reference
    __player = None

    # Some managers and loaders
    __screen_manager = None
    __game_screen = None
    __level_loader = None

    # Variables to calculate the time by pixel size, so it doesn't matter the tile size that is chosen,
    # the game will execute at the same speed
    __px_to_s = None
    __default_tile_size = 64

    # Clock used to update game events and frames
    __clock = pygame.time.Clock()

    def __set_level_values(self):
        # Get the three groups of sprites loaded
        self.__background = self.__level_loader.background_group
        self.__colliders = self.__level_loader.colliders_group
        self.__interactive = self.__level_loader.interactive_group

        # Get the player reference
        self.__player = self.__level_loader.player

        # Return the tile size and max number of tiles in both axis
        return self.__level_loader.tiles_size, self.__level_loader.max_x, self.__level_loader.max_y

    def __init_game_loop(self, level):
        # Create the level loader and load the level
        self.__level_loader = LevelLoader()
        if not self.__level_loader.load_level(level):
            return False

        # Get the variables values of the level loader and retrieve the tile size and max number of tiles in both axis
        tiles_size, max_x, max_y = self.__set_level_values()

        # Create the screen manager, set the caption and calculate the time relative to the tile size
        # So it doesn't matter the tile_size that is chosen, the game will execute at the same speed
        self.__screen_manager = ScreenManager(tiles_size, max_x * tiles_size, max_y * tiles_size, self.__clock)
        self.__screen_manager.set_caption("Simple PyGame - " + level)
        self.__px_to_s = tiles_size / self.__default_tile_size

        return True

    def __get_delta_time(self):
        # Get the time between game loops ignoring the first loop to always start in the same point of execution
        # And avoid problems reloading the level or charging new levels
        if self.first_loop:
            self.first_loop = False
            return 0
        else:
            return self.__clock.get_time() * self.__px_to_s

    def __show_game_result(self):
        # Show the win or loose screen in its respective case
        if self.__player.won is not None:
            if self.__player.won:
                self.__screen_manager.win_screen()
            else:
                self.__screen_manager.loose_screen()

    def __game_loop(self):
        self.first_loop = True

        # Main game loop, used to updated all gameplay such as movement, checks, and graphics
        # Runs until exit = True
        while not self.__player.exit:
            # Get the delta time
            delta_time = self.__get_delta_time()

            # Call all update functions of the interactive group
            self.__interactive.update(delta_time, self.__screen_manager, self.__colliders)

            # Draw by groups
            all_groups = [self.__background, self.__colliders, self.__interactive]
            self.__screen_manager.draw_groups(all_groups)

            # Update and tick the __clock
            self.__screen_manager.update_and_tick()

        # We show the result of the game
        self.__show_game_result()

        return self.__player.repeat

    @staticmethod
    def __quit_all():
        # Quit pygame and the program
        pygame.quit()
        quit()

    def play(self, level):
        """
        Function that loads the level and starts the game loop

        :param level: Level file to load
        """

        # Init the game loop by loading all the level info
        if self.__init_game_loop(level):

            # If the game loop returns that should repeat, we play again
            if self.__game_loop():
                self.play(level)
            else:
                self.__quit_all()

        else:
            self.__quit_all()


def print_help():
    print("\n\nERROR EXECUTING THE GAME")
    print("------------------------\n")

    print("To play the game, you have to execute the 'game/game.py' file with python.")
    print("The command to do this will be like:\n")

    print("$> python3 path_to/game.py path_to/level_file")
    print("$> python path_to/game.py path_to/level_file\n")

    print("Depending on the version of python that you have installed.")
    print("Try python3 first, and if the command is not recognised, try with python.\n")

    print("You'll also need the pygame package: https://www.pygame.org/ https://github.com/pygame/pygame")
    print("You can install it through pip with the command:\n")

    print("$> pip3 install pygame")
    print("$> pip install pygame\n")

    print("Depending on the version of pip that you have installed.")
    print("Try pip3 first, and if the command is not recognised, try with pip.")


def main(args):
    if is_list_of_size(args, 2):
        GameController().play(args[1])
    else:
        print_help()


if __name__ == "__main__":
    main(sys.argv)
