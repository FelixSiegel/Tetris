# Tetris

## Installation

What you need:  

- Python3  
- PyGame-Libary (install it via `pip install pygame` from the terminal)  
- The both datas `Tetris.py` and `Settings.txt`, last isn´t necessary but it allows you to change the Window-Settings

Then run `Tetris.py` and have fun :)

## Features

![Bildschirmfoto_2022-03-12_20-07-05](https://user-images.githubusercontent.com/98593245/158031498-ca1a6a07-a166-47f1-8f3f-c2f9c8e9b5e2.png)

- all shapes (I,J,L,O,S,T,Z) included and also with different colors
- collides with Border and other Tetrominos will dectected
- filled rows are detected and deleted + rows above will fallen
- the falltime becoms faster every 10 completed Rows
- Controlling:
    * you can **Rotate** (`Arrow-Up`-Key) and **move** the Tetromino to **left** (`Left-Arrow`-Key) and **right** (`Right-Arrow`-Key) Side and also **down** with the `Down-Arrow`-Key
    * with `Space`-Key you can **drop** the falling Tetromino to the bottom
    * you can **pause** the Game with `p`-Key and **resume** by pressing **any key**
    * if the game is over you can **restart** the Game after 1 second by pressing **any key**
    * with the shortcut `Strg + Q` can you **close** the window (recommended for Splash-Screen-Mode)

A other usefull Features is, that you can set some Window-Properties. To do so you need to create a textfile named `settings.txt` which needs to be in the same directory as the programm.

```python
{
    "dimensions": "auto",
    "tilesize": "auto",
    "fps": 60,
    "windowframe": "noframe"
}
```

As you can see in the text above, you can change currently 4 Values (dimension, tilesize, fps, windowframe):  

- **dimensions:**
    * Defaults to "auto", which means that the program tries to adjust the window size to your screen size. (It also depends on the set tilesize)
    * Otherwise it must be a list with two entries - first the width and then the height of the window (for example: [600, 1000])
- **FPS:**
    * Default set to the integer 60 (mean 60 Frames per seconds)
- **tilesize:**
    * Default set to "auto", which means that the program tries to adjust the Size of the bricks from the Tetrominos to the best that fits into the Window (It also depends on the set tilesize)
    * Otherwise it must be an integer that defines the Size in pixels
- **windowframe:**
    * Standart set to "standart" that means that a normal Window will created
    * Otherwise you can set it to "noframe", where a ![splash-screen Window](https://en.wikipedia.org/wiki/Splash_screen) will created

All 4 values must be contained in the file, otherwise the default values are used automatically. The same is true if the file does not exist or the values do not follow the requirements.
