# Simple [Pygame](https://www.pygame.org/)

This is the base for a rpg game created in python with pygame: A cross-platform set of Python modules designed for writing video games.

Taking as starting point the final product of the project [Road Crossing Game](https://academy.zenva.com/product/python-programming-mini-degree/) from [Zenva](https://academy.zenva.com/)

## Table of contents

- [Description](#description)
  - [Gameplay and screeshots](#gameplay-and-screenshots)
  - [Level file xyntax](#level-file-syntax)
- [Posible future improvements](#posible-future-improvements)
- [Playing the game](#playing-the-game)

## Description

WIP

### Gameplay and screenshots

WIP

#### Final result from the Zenva course

![Crossy RPG Game](https://github.com/AlejandroFraga/simple-pygame/blob/main/images/Crossy_RPG_Game.gif?raw=true)

#### Zenva level with improvements

After the improvements made in this project, the original level looks like this:

![Simple pygame - Level 1](https://github.com/AlejandroFraga/simple-pygame/blob/main/images/Level_1.gif?raw=true)

#### Custom level with improvements

A second level was created to show what can be done with the project as it is now:

![Simple pygame - Level 2](https://github.com/AlejandroFraga/simple-pygame/blob/main/images/Level_2.gif?raw=true)

This level is read from a [plain txt file](https://github.com/AlejandroFraga/simple-pygame/tree/main/game/resources/levels/level_2.txt) which indicates how the level is constructed. This way, the level creation proccess is simple, fast, and as we'll see very visual.

### Level file syntax

#### -> Legend region

In this section, we introduce the folder in which the textures are located.
The size in pixel of the tiles to accommodate the display size of the level to our screen, so it wont overflow.
And set an [ASCII](https://theasciicode.com.ar) symbol to all the textures that we will be using in the level.

The syntax of this region lines will be:
```
ascii_symbol - route_to_image
```

For e.g.:

```
█ - wall_red_vertical.png
```

The route to the image will be concatenated to the last previous folder indicate, e.g.:

```
/ - resources/textures/
... - ...
Æ - enemy.png
```

The enemy png file will be searched in the *resources/textures/enemy.png* location.

But if there are multiple folder indicated, only the last one will be taken:

```
/ - resources/textures/enemies/
Æ - orc.png
/ - resources/textures/
... - ...
. - grass.png
```

The "orc" texture will be searched in the *resources/textures/enemies/orc.png* location.
But the "grass" texture will be searched in the *resources/textures/grass.png* location.

This way we can have the textures in different folders, organized and we don't have to indicate the complete path in each file.

We can see this region for the custom level I created:

![Simple pygame - Level 2 Legend](https://github.com/AlejandroFraga/simple-pygame/blob/main/images/Level_2_Legend.png?raw=true)

#### -> Background region

In this section, we include every tile that we want to be shown in the background.

The syntax of this region lines will be (without the spaces):

```
ascii_symbol ascii_symbol ascii_symbol ascii_symbol
```

For e.g.:

```
........═══════════........
```

Where we "paint" directly the map we want do be drawn.
Each symbol corresponds to his Legend line, or a space will correspond to an empty position.
So in the example before, we'll have 8 grass tiles, 11 blue floors and 8 grass tiles again (according to our Legend region).

Each line corresponds to a row of the background, so we can put many of them together to create the entire background.

As maybe we'll have some textures with transparencies, and we want to show something else underneath, we can have as many background layers as we need. Here the empty positions will come in handy as we won't have to repeat tiles.

To separate the different layers we'll put any number of consecuent dash "-" in a line between backgrounds:

```
------------
```

We can see this region for the custom level I created:

![Simple pygame - Level 2 Backgrounds](https://github.com/AlejandroFraga/simple-pygame/blob/main/images/Level_2_Backgrounds.png?raw=true)

#### -> Colliders region

In this section, we include every game object that we want to be collidable, as walls, trees.

The syntax of this region lines will be (without the spaces):

```
ascii_symbol ascii_symbol ascii_symbol ascii_symbol
```

For e.g.:

```
▓▓¥§¥§¥§█  £   £  █§§¥¥§¥▓▓
```

The same as in the backgrounds region, but there'll be only one layer of colliders.
We don't want multiple colliders in the same position, colliding with each other all the time.
In the end, this will just decide which tiles can we step on and which we don't.

We can see this region for the custom level I created:

![Simple pygame - Level 2 Colliders](https://github.com/AlejandroFraga/simple-pygame/blob/main/images/Level_2_Colliders.png?raw=true)

#### -> Elements region

In this section, we include the player, the enemies and everything that we want to be interactable, as the treasure.

The syntax of this region lines will be:

```
ascii_symbol - (coordinate_x, coordinate_y)
```

We give the symbol of the element we are setting on the map, and the coordinates in which we want it to appear.
The coordinates will start on (0,0) on the left top of the screen.
Moving n positions to the right and m positions to the bottom will give us the (n, m) coordinates.

We can see this region for the custom level I created:

![Simple pygame - Level 2 Elements](https://github.com/AlejandroFraga/simple-pygame/blob/main/images/Level_2_Elements.png?raw=true)

## Posible future improvements

 - - [X] Set the route of the images in the level file
 - - [X] Set the size of the tiles in px in the level file
 - - [ ] End cleaning and improving the code quality for version 2.0.0
 - - [ ] Enable/Disable the fps counter in the level file and dynamically
 - - [ ] Set the fps cap (0 to unlock) in the level file
 - - [ ] Change the text font, loading also by path
 - - [ ] Set the player and each enemy a speed in the level file
 - - [ ] Introduce animations in the game
 - - [ ] Screen/Level transition like in Zelda*
 - ...

![Zelda screen transition](https://habrastorage.org/getpro/habr/post_images/ae7/c29/539/ae7c295393f6706e17e788e0a1cc39e7.gif)

## Playing the game

To play the game, you have to execute the 'game/game.py' file with python.
The command to do this will be like:

```sh
$ python3 path_to/game.py path_to/level_file
$ python path_to/game.py path_to/level_file
```

Depending on the version of python that you have installed.
Try python3 first, and if the command is not recognised, try with python

You'll also need the [pygame package](https://github.com/pygame/pygame):
You can install it through pip with the command:

```sh
$ pip3 install pygame
$ pip install pygame
```

Depending on the version of pip that you have installed.
Try pip3 first, and if the command is not recognised, try with pip.
