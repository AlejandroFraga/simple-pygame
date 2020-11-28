# Simple [Pygame][pygame]

This is the base for a rpg game created in python with pygame: A cross-platform set of Python modules designed for writing video games.

## Table of contents

- [Description](#description)
  - [Gameplay and screeshots](#gameplay-and-screenshots)
  - [Level file syntax](#level-file-syntax)
- [Posible future improvements](#posible-future-improvements)
- [Playing the game](#playing-the-game)

## Description

After completing the Zenva course [Learn Python Programming by Making a Game][course], the final version of the project is a very basic crossy "rpg" game in which you control the player with the up and down arrow key. You can only move in this two directions.

Your objective is to reach the treasure avoiding the enemies which bounce from side to side in the screen.

This course shows a lot about python and how to use it. But there are some problems in this [version](#final-result-from-the-zenva-course):
 - Everything is hard-coded, from sizes to collision detection
 - The background, in reality is just a picture drawn below everything else
 - When reescaling the player and enemies, as we can see the textures are streched as their aspect ratio doesn't correspond to the new sizes
 - The collision detection ignores completely all the background objects, as it is only a picture (you can see the enemies going through trees)
 - All the coding was done in a single file, with huge functions all in a big spaghetti code
 - The speed of everything is pixel dependent, so, making the display smaller will make eveything move faster
 - ...

The final code looks like this:

![Crossy RPG Game Code](https://github.com/AlejandroFraga/simple-pygame/blob/main/images/Crossy_RPG_Game_Code.gif?raw=true)

So I decide to fix a lot of the problems and improve this project. My objective is not to create a perfect game, with a thousand levels and completely polished. Is to end up with a improved version of this game, with the basis for anyone to create his own levels and the hability to create and test them fastly.

This can be splitted into subobjectives, which are:
 - - [X] The spaghetti code will be reorganized and improved
 - - [X] All the levels should be stored and read from simple text files, so multiple can be easily stored and modified
 - - [X] The background won't be a simple picture but a collection of tiles that will be drawn and managed individually
 - - [X] The collision in the tiles should be easily and visually indicated in the file
 - - [X] The collision system will really work and manage all the collisions in the game in both axis
 - - [X] The player will be able to move in both axis, not just up and down
 - - [X] All the tiles will have the same size

First of all, the spaghetti code had to be cleaned. So I created a simple diagram showing the different files that I would create and how they would interact: 

![File Interaction](https://github.com/AlejandroFraga/simple-pygame/blob/main/images/File_Interaction.jpg?raw=true)

The only file that wasn't represented was the Data Helper, as it would be a file with functions to help the other classes process data. For example safely casting a variable to a type, or checking if a variable is a list of a exact size... So this file would interact with all the others when needed.

After splitting all the code into its respective files, creating new functions and cleaning all the spaghetti code, I began to improve the background and tile system of the game.

I trimmed all the tiles in the background image, separating it into [the different textures](https://github.com/AlejandroFraga/simple-pygame/tree/main/game/resources/textures) of the game in tiles of 16x16 pixels. And began to write the file from which I would load the level, initially just replicating the background image.

Then I started working in the collision system, making the enemies bounce the colliders of the desired game objects in the game and making the player unable to step on them but sticking to the limits before colliding, so we can go sticked to the walls or the limits of the screen.

Instead of calculating if player will collide, and leaving him in the same position, if he can get closer to the collider we'll move him. This way we'll be able to enter 1 tile size corridors.

The player was improved to be able to move in both axis.

And in general, another improvements were made to improve the overall quality and 

### Gameplay and screenshots

Here we can see a gifs showing the different points of development, starting from the final result of the course.
After all the improvement of the game, the original level reworked.
And finally, a custom map.

#### Final result from the Zenva course

![Crossy RPG Game Level](https://github.com/AlejandroFraga/simple-pygame/blob/main/images/Crossy_RPG_Game_Level.gif?raw=true)

#### Zenva level with improvements

After the improvements made in this project, the original level looks like this:

![Simple pygame - Level 1](https://github.com/AlejandroFraga/simple-pygame/blob/main/images/Level_1.gif?raw=true)

#### Custom level with improvements

A second level was created to show what can be done with the project as it is now:

![Simple pygame - Level 2](https://github.com/AlejandroFraga/simple-pygame/blob/main/images/Level_2.gif?raw=true)

These last two levels are read from a [plain txt files](https://github.com/AlejandroFraga/simple-pygame/tree/main/game/resources/levels) which indicates how the level is constructed. This way, the level creation proccess is simple, fast, and as we'll see very visual.

In just a few minutes, anyone, just with a simple txt editor as WordPad, can create a simple map.

### Level file syntax

There are some reserved ascii symbols that shouldn't be used to avoid problems:
 - "/" Reserved to indicate the routes in the Legend region
 - "(" Reserved to indicate the sizes of the tiles in the Legend section, but also should be used to indicate coordinates
 - "\-" Reserved to separate symbols from textures/coordinates, and to separate background layers
 - ">" Combinated with the slash "->" indicates the start of a region
 - " " The space is reserved to indicate that that tile should be empty
 - "#" The lines that start with this symbol, are treated as comments, and so, ignored by the game
 - And also, empty lines are ignored

With that in mind, we can begin to see the syntax of all the regions of the level file. Each region will start with the line:

```
-> name_of_the_region
```

This way, we indicate the file reader, that the next lines, until a change, are from that region.

The order of the regions is not important, you can put them as you want, even "pause" one and go back to it later again.

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
ascii_symbol ascii_symbol ascii_symbol ascii_symbol ...
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
ascii_symbol ascii_symbol ascii_symbol ascii_symbol ...
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

With this syntax, anyone can easily create his own custom level and load it in the game to play.

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
 - - [ ] Set the caption/title of the screen in the level file
 - - [ ] Change the text font, loading also by path
 - - [ ] Better error handling when loading the level (no player, no treasure, ...)
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

   [zenva]: <https://academy.zenva.com>
   [pygame]: <https://www.pygame.org>
   [course]: <https://academy.zenva.com/product/learn-python-programming-by-making-a-game/>
