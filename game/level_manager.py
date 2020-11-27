from pygame.sprite import Group

from data_helper import is_list_of_size
from file_manager import FileReader
from game_objects import TileBase, GameObject, PlayerCharacter, EnemyCharacter, Tag


class LevelLoader:
    """
    Class that gives all the information from the file reader to the game controller
    Processing ascii symbols into Game Objects, Groups...
    """

    def __init__(self):
        # Size of the tiles
        self.tiles_size = 64

        # Variables to return to the game
        self.background_group = Group()
        self.colliders_group = Group()
        self.interactive_group = Group()
        self.player = None
        self.max_x = 0
        self.max_y = 0

        # Variables to store the information from the file reader
        self.__legend = {}
        self.__backgrounds = []
        self.__colliders = []
        self.__elements = []

        # Symbols to identify player, treasure and enemy
        self.__player_symbol = ""
        self.__treasure_symbol = ""
        self.__enemy_symbol = ""

    def __read_level_file(self, level_file_path):
        result = FileReader().read_level_file(level_file_path)
        if result is None:
            return False

        self.__legend, self.__backgrounds, self.__colliders, self.__elements, self.tiles_size = result
        return True

    def __process_legend(self):

        # For each legend element check if it's the player, treasure or enemy symbol, to difference it later on
        for element in self.__legend:
            if "player" in self.__legend[element]:
                self.__player_symbol = element

            elif "treasure" in self.__legend[element]:
                self.__treasure_symbol = element

            elif "enemy" in self.__legend[element]:
                self.__enemy_symbol = element

            # Create the TileBase from which the GameObjects will be created
            self.__legend[element] = TileBase(self.__legend[element], self.tiles_size)

    def __process_background(self, background):
        x, y, max_x_aux = 0, 0, 0

        # For every tile in every row of the background, we create the Game Object from the Tile Base stored in legend
        for row in background:
            for tile in row:

                # Check that the tile is not empty and the Tile Base is in the legend
                if tile != " " and tile in self.__legend:
                    game_object = GameObject(self.__legend[tile], self.tiles_size * x, self.tiles_size * y)
                    self.background_group.add(game_object)
                x += 1
            y += 1
            max_x_aux = max(max_x_aux, x)
            x = 0
        return max_x_aux, y

    def __process_backgrounds(self):

        for background in self.__backgrounds:
            max_x_aux, max_y_aux = self.__process_background(background)

            # Calculate the max x-axis and y-axis position of the background
            # So the display we create has the necessary proportions to show everything
            self.max_x = max(max_x_aux, self.max_x)
            self.max_y = max(max_y_aux, self.max_y)

    def __process_colliders(self):
        x, y = 0, 0

        for row in self.__colliders:
            for tile in row:

                # Check that the tile is not empty and the Tile Base is in the legend
                if tile != " " and tile in self.__legend:

                    # Create the game object and add it to the colliders group
                    game_object = GameObject(self.__legend[tile], self.tiles_size * x, self.tiles_size * y)
                    self.colliders_group.add(game_object)
                x += 1
            y += 1
            x = 0

    def __process_element_player(self, legend, x, y):
        # Create the player character and add it to the interactive group
        self.player = PlayerCharacter(legend, x, y, Tag.player)
        self.interactive_group.add(self.player)

    def __process_element_treasure(self, legend, x, y):
        # Create the treasure object and add it to the colliders and interactive group
        treasure = GameObject(legend, x, y, Tag.treasure)
        self.colliders_group.add(treasure)
        self.interactive_group.add(treasure)

    def __process_element_enemy(self, legend, x, y):
        # Create the enemy character and add it to the colliders and interactive group
        enemy = EnemyCharacter(legend, x, y, Tag.enemy)
        self.colliders_group.add(enemy)
        self.interactive_group.add(enemy)

    def __process_element(self, element):

        # Check that the element has the type and size expected, and the element symbol is in the legend list
        if is_list_of_size(element, 2) and is_list_of_size(element[1], 2) and element[0] in self.__legend:

            # Calculate the position of the Game Object by the coordinates
            x = self.tiles_size * int(element[1][0])
            y = self.tiles_size * int(element[1][1])

            # For each legend element check if it's the player, treasure or enemy
            if element[0] == self.__player_symbol:
                self.__process_element_player(self.__legend[element[0]], x, y)

            elif element[0] == self.__treasure_symbol:
                self.__process_element_treasure(self.__legend[element[0]], x, y)

            elif element[0] == self.__enemy_symbol:
                self.__process_element_enemy(self.__legend[element[0]], x, y)

            else:
                # Otherwise, create the game object and add it to the interactive group
                game_object = GameObject(self.__legend[element[0]], x, y)
                self.interactive_group.add(game_object)

    def __process_elements(self):

        for element in self.__elements:
            self.__process_element(element)

    def load_level(self, level_file_path):
        """
        Function that loads a level from a given file path

        :param level_file_path: Path of the level file
        :return: True if the level file was read, False otherwise
        """

        if not self.__read_level_file(level_file_path):
            return False

        self.__process_legend()
        self.__process_backgrounds()
        self.__process_colliders()
        self.__process_elements()

        return True
