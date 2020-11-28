"""
Some functions to help rest of the game process and treat data easily
"""


def safe_cast(val, to_type, default=None):
    """
    Safe cast to the desired type, returning the default value if the
    cast can't be successfully done

    :param val: value to be casted
    :param to_type: type to be casted
    :param default: default value to return in case of can't cast the value to the type
    :return: The value casted to the type, default value if can't be done
    """

    try:
        return to_type(val)
    except (ValueError, TypeError):
        return default


def safe_add(x, y=None):
    """
    Safe addition of two numbers, in case that any of them is not a number, the first
    one is returned

    :param x: First number to be added
    :param y: Second number to be added, None by default
    :return: The sum of both numbers, the value of the first if any of them is not a number
    """

    if is_number(x) and is_number(y):
        return x + y
    else:
        return x


def is_number(number):
    """
    Check if the given number is an int or a float

    :param number: Number to check
    :return: The result of the check
    """
    return type(number) is int or type(number) is float


def is_str(string):
    """
    Check if the given string is an str

    :param string: String to check
    :return: The result of the check
    """
    return type(string) is str


def is_list(var):
    """
    Check if the given variable is a list

    :param var: Variable to check
    :return: The result of the check
    """
    return type(var) is list


def is_list_of_size(var, size):
    """
    Check if the given variable is a list with the given size

    :param var: Variable to check
    :param size: Size of the list
    :return: The result of the check
    """
    return is_list(var) and is_number(size) and var.__len__() == size


def limit_value(value, minimum, maximum):
    """
    Function that limits a given value by a minimum and a maximum value

    :param value: Value to be limited
    :param minimum: Minimum value
    :param maximum: Maximum value
    :return: The value limited by the minimum and a maximum
    """

    if is_number(minimum) and value < minimum:
        return minimum

    elif is_number(maximum) and value > maximum:
        return maximum

    return value


def split_in_chars_and_remove(line, remove):
    """
    Function that splits the line in a row of chars and removes the given char if included

    :param line: Line to split
    :param remove: Char to remove
    :return: The line split and without the char to remove
    """

    row = ""

    if is_str(line):

        # Separate all chars in the line
        row = [char for char in line]

        # Exclude the line break if it's inside
        if is_str(remove) and row.__contains__(remove):
            row.remove(remove)

    return row


def clean_end_line_str(string):
    """
    Clean the str string from break line and special characters

    :param string: String to clean
    :return:
    """

    # Replace \r or \n space with nothing, so they are removed from the string
    if is_str(string):
        return string.replace('\r', '').replace('\n', '')
    else:
        return string


def clean_parentheses_and_space_str(string):
    """
    Clean the str string from break line and special characters

    :param string: String to clean
    :return:
    """

    # In case that string is a str, replace (, ) or a space with nothing, so they are removed from the string
    if is_str(string):
        return string.replace('(', '').replace(')', '').replace(' ', '')
    else:
        return string


def process_coordinates(coordinates):
    """
    Function that process the coordinates of a duple, cleaning and splitting them into 2 numbers

    :param coordinates: str of the coordinates to process
    :return: The coordinates processed
    """

    if is_str(coordinates):

        # Split the element by the "," in the middle
        coordinates = coordinates.split(",")

        if is_list_of_size(coordinates, 2):
            # Clean the spaces, parenthesis and end of line of the elements, so only the numbers remain
            coordinates[0] = clean_parentheses_and_space_str(coordinates[0])
            coordinates[1] = clean_end_line_str(clean_parentheses_and_space_str(coordinates[1]))

    return coordinates


def check_slash_at_end(string):
    """
    Function that adds a slash at the end of a string, if it doesn't have it already

    :param string: Str to check the slash at the end
    :return: The string with the slash at the end
    """

    if is_str(string) and not string.endswith("/"):
        string += "/"

    return string
