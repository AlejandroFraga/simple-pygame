from enum import Enum

import pygame

from data_helper import safe_cast, split_in_chars_and_remove, clean_end_line_str, process_coordinates


def load_image(file_path, width, height):
    """
    Function to load and scale an image in the given path with the given proportions

    :param file_path: Path of the image file
    :param width: Width to scale the image to
    :param height:Height to scale the image to
    :return: Loaded image
    """

    image = None

    try:
        # Load the image and scale it to the desired size
        image = pygame.image.load(file_path)
        image = pygame.transform.scale(image, (width, height))

    except FileNotFoundError:
        print("\nERROR: Couldn't load the image: " + file_path)

    finally:
        return image


def open_file(file_path):
    """
    Function that safely opens a file checking before that the path it's a file

    :param file_path: Path of the file to open
    :return: The file opened in readonly mode
    """

    file = None

    try:
        # Open the file in readonly mode in utf-8 encoding to avoid ascii reading problems
        file = open(file_path, "r", encoding='utf-8')

    except IOError:
        print("\nERROR: Couldn't open the file: " + file_path)

    finally:
        return file


def close_file(file):
    """
    Function that safely closes an opened file

    :param file: File to close
    """

    try:
        file.close()

    except IOError:
        print("\nERROR: Couldn't close the file!")


class Reading(Enum):
    """
    Enumeration to indicate what part of the file is currently being read
    """

    Other = 1
    Legend = 2
    Background = 3
    Colliders = 4
    Elements = 5


class FileReader:
    """
    Class that opens (and closes) and reads all lines from the given file, separating them into lists and dictionaries
    """

    # Variables to indicate and store the path of the images
    path_symbol = "/"
    path = ""

    # Variables to indicate and store the tiles size
    tiles_size_symbol = "("
    tiles_size = 64

    # Indicator symbols in the level file
    region_line_symbol = "->"
    separator_symbol = " - "
    background_end_symbol = "-"
    break_line_symbol = "\n"
    comment_symbol = "#"

    def __init__(self):
        # Init the dictionary, lists and region reading
        self.legend = {}
        self.backgrounds = []
        self.background = []
        self.backgrounds.append(self.background)
        self.colliders = []
        self.elements = []
        self.reading = Reading.Other

    def __region_line(self, line):
        # Set the region reading according to the line
        if line.__contains__("Legend"):
            self.reading = Reading.Legend

        elif line.__contains__("Background"):
            self.reading = Reading.Background

        elif line.__contains__("Colliders"):
            self.reading = Reading.Colliders

        elif line.__contains__("Elements"):
            self.reading = Reading.Elements

        # If it doesn't match any of the regions before, set the default value
        else:
            self.reading = Reading.Other

    def __legend_line(self, line):
        # Split by the separator and check that there are more than 1 element
        duple = line.split(self.separator_symbol)
        if duple.__sizeof__() > 1:

            # If it's the path value, store it in its global variable
            if duple[0].startswith(self.path_symbol):
                self.path = clean_end_line_str(duple[1])

            # If it's the tiles size value, store it in its global variable
            elif duple[0].startswith(self.tiles_size_symbol):
                self.tiles_size = safe_cast(clean_end_line_str(duple[1]), int, self.tiles_size)

            # Otherwise, process the legend and store it in the dictionary
            else:
                self.legend[duple[0]] = self.path + clean_end_line_str(duple[1])

    def __background_line(self, line):
        # The line indicates the end of the background current list
        if line.startswith(self.background_end_symbol):

            # Create a new background list, store it in the backgrounds and ignore the rest of this line
            self.background = []
            self.backgrounds.append(self.background)
            return

        # Separate all chars in the line and exclude the line break if it's inside
        row = split_in_chars_and_remove(line, self.break_line_symbol)

        self.background.append(row)

    def __collider_line(self, line):
        # Separate all chars in the line and exclude the line break if it's inside
        row = split_in_chars_and_remove(line, self.break_line_symbol)

        self.colliders.append(row)

    def __element_line(self, line):
        duple = line.split(self.separator_symbol)

        # Correctly process the coordinates in the second part of the line
        duple = process_coordinates(duple)

        self.elements.append(duple)

    def __analyze_lines(self, lines):

        for line in lines:

            # For each line, check if it's only a break line or a comment
            if line.startswith(self.comment_symbol) or line == self.break_line_symbol:
                continue

            # Check if it's a region line, indicating the start of this region
            elif line.startswith(self.region_line_symbol):
                self.__region_line(line)

            # Or being already in a region, it's a line from it
            elif self.reading == Reading.Legend:
                self.__legend_line(line)

            elif self.reading == Reading.Background:
                self.__background_line(line)

            elif self.reading == Reading.Colliders:
                self.__collider_line(line)

            elif self.reading == Reading.Elements:
                self.__element_line(line)

        return self.legend, self.backgrounds, self.colliders, self.elements, self.tiles_size

    def read_level_file(self, level_file_path):
        """
        Function that opens, reads and analyzes all the lines of the level file given

        :param level_file_path: Path of the level file to read
        :return: The result of the reading and analysis of the level file
        """

        level_file = open_file(level_file_path)
        if level_file is None:
            return None

        lines = level_file.readlines()
        result = self.__analyze_lines(lines)
        close_file(level_file)

        return result
