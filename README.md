# Tetris

## Installation

What you need:
- Python3
- PyGame-Libary (install it via `pip install pygame` from the terminal
- The both datas `Tetris.py` and `Settings.txt`, last isn´t necessary but it allows you to change the Window-Settings

Then run `Tetris.py` and have fun :)

## Features

![Bildschirmfoto_2022-03-12_20-07-05](https://user-images.githubusercontent.com/98593245/158031498-ca1a6a07-a166-47f1-8f3f-c2f9c8e9b5e2.png)

- all shapes (I,J,L,O,S,T,Z) included and have also different colors
- you can **Rotate** (`Arrow-Up`-Key) and **move** the Tetromino to **left** (`Left-Arrow`-Key) and **right** (`Right-Arrow`-Key) Side and also **down** with the `Down-Arrow`-Key
- collides with Border and other Tetrominos will dectected
- filled rows are detected and deleted + rows above will fallen
- you can Pause the Game with `p`-Key and resume by pressing any key
- if the game is over you can restart the Game after 1 second by pressing any key
- the falltime becoms faster every 10 completed Rows

A other usefull Features is, that you can set some Window-Properties. To do so you need to create a textfile named `settings.txt` which needs to be in the same directory as the programm.

![Bildschirmfoto_2022-03-12_19-48-21](https://user-images.githubusercontent.com/98593245/158030907-0868a3ae-637f-44eb-92f7-66550bd88027.png)

As you can see in the Screenshot, you can change currently 3 Values (dimension, fps, tilesize):  
**dimensions:** here you need a tupel with 2 Values -> 1st is the width of the window and the 2nd is the height of the window  
**FPS:** here you need an integer that define the Frames per seconds  
**tilesize:** This value define the size of the bricks of the Tetrominos, the value must be divisible without remainder by the width and height of the window  

You need to have all 3 Values in the file, otherwise the standard values are used. The same is true if the file does not exist or the values do not follow the requirements.


## Conclusion

Currently there are no known bugs, if you notice any or if you have any other ideas to make the game better, please feel free to report or suggest them.
