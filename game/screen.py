"""
File that manages all the screen functions, like painting sprites or text, or updating every frame
"""
import pygame


class ScreenManager:
    # Frames per second maximum value, set to 0 to unlock
    fps_cap = 0

    # Color of the fps counter, in this case, white
    fps_color = (255, 255, 255)

    # Font family to use in all screen text
    __font = "arial"

    # Color of the fps counter, in this case, white
    text_color = (0, 0, 0)

    def __init__(self, tiles_size, width, height, clock):
        self.width = width
        self.height = height
        self.clock = clock

        # Initiate the font system and create the font with the font family and size desired
        pygame.font.init()
        self.font = pygame.font.SysFont(self.__font, round(tiles_size * 1.5))

        # Create the window of specified size in white to __screen_manager the game
        self.game_screen = pygame.display.set_mode((width, height))

    @staticmethod
    def set_caption(caption):
        """
        Function to set the caption/title of the window in which the game will be executed

        :param caption: Text to set as caption
        """

        pygame.display.set_caption(caption)

    def draw_group(self, group):
        """
        Draw all sprites inside of the group

        :param group: Group of sprites to be drawn
        """

        group.draw(self.game_screen)

    def draw_groups(self, groups):
        """
        Draw all sprites inside of every group

        :param groups: Groups of sprites to be drawn
        """

        for group in groups:
            self.draw_group(group)

    def paint_text_centered(self, text):
        """
        Paint a given text in the center of the screen

        :param text: Text to be painted in the center of the screen
        """

        text_render = self.font.render(text, True, self.text_color)

        # Calculate the center of the screen minus the center of the text, to center the text on the screen
        text_center_x = self.width / 2 - text_render.get_rect().width / 2
        text_center_y = self.height / 2 - text_render.get_rect().height / 2

        self.game_screen.blit(text_render, (text_center_x, text_center_y))

    def __update_fps(self):
        # Get the current frames per second value and paint it on the screen
        fps = round(self.clock.get_fps()).__str__()
        fps_text = self.font.render(fps, True, self.fps_color)

        self.game_screen.blit(fps_text, (0, 0))

    def update_and_tick(self):
        """
        Function to update the display and tick the clock
        """

        # Update the frames per second counter
        self.__update_fps()

        # Update all the graphics
        pygame.display.update()

        # Tick the clock to update everything within the game
        self.clock.tick(self.fps_cap)

    def win_screen(self):
        """
        Screen to be shown when the player wins
        """

        # Update all the graphics
        self.paint_text_centered("You win!")

        # Update all the graphics
        pygame.display.update()

        # Hold the win screen
        self.clock.tick(1)

    def loose_screen(self):
        """
        Screen to be shown when the player looses
        """

        # Update all the graphics
        self.paint_text_centered("You loose!")

        # Update all the graphics
        pygame.display.update()

        # Hold the loose screen
        self.clock.tick(1)
