#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 16 09:54:05 2022

contributors: Infinity Coding

A Tetris imitation written in Python and using the Python-libary PyGame.

For more infos go to the documention at the GitHub-Repository (https://github.com/FelixSiegel/Tetris)
"""

import pygame
from sys import exit as close_program
from random import choice

pygame.init()

# =============================================================================
# try to read settings file
# =============================================================================

try:
    with open("settings.txt") as f_in:
        settings = eval(f_in.read())
    
    if settings["dimensions"] != "auto" and settings["tilesize"] != "auto":
        # checking if rules heeded
        if settings["dimensions"][0] % settings["tilesize"] != 0 or \
            settings["dimensions"][1] % settings["tilesize"] != 0:
            raise ValueError
except: # if file not found or not correct
    settings = { 
                "dimensions": "auto",
                "tilesize": "auto",
                "fps": 60,
                "windowframe": "default"
                }
finally: # finally if some values set to auto -> automatically set them
    if settings["dimensions"] == "auto": # if the dimensions set to auto
        m_width, m_height = pygame.display.list_modes()[0] # get max display height and width
        if settings["tilesize"] == "auto":
            # if auto tilesizing on: set it so that 20 rows can created
            settings["tilesize"] = (m_height - m_height%20) // 20 
            
        # set window height to max possible with one row place
        m_height -= m_height%settings["tilesize"] + settings["tilesize"]
        m_width = int((m_height/10)*6) # set window width to 6/10 of the height
        # make sure that (width % tilesize) equals zero:
        m_width += settings["tilesize"] - m_width%settings["tilesize"] 
        settings["dimensions"] = (m_width, m_height) # confirm new dimensions
    
    elif settings["tilesize"] == "auto": # if dimensions given but tilesize set to auto
        settings["dimensions"][1] -= settings["dimensions"][1]%20 # set height so that 20 rows fit into it
        tilesize = settings["dimensions"][1] // 20 # set tilesize so, that 20 rows can fit into the height
        settings["dimensions"][0] -= settings["dimensions"][0]%tilesize # tailor width
        settings["tilesize"] = tilesize # confirm tilesize
        del tilesize # del temp variable
    
# =============================================================================
# set initial variables
# =============================================================================

WIDTH = settings["dimensions"][0]
HEIGHT = settings["dimensions"][1]
TILESIZE = settings["tilesize"]
FPS = settings["fps"]
POINTS = 0

# =============================================================================
# Setup Pygame
# =============================================================================

if settings["windowframe"] == "noframe":
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)
else: screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption('Tetris')
clock = pygame.time.Clock()

# =============================================================================
# Define the Shapes and there rotations
# =============================================================================

I = [['0100',
      '0100',
      '0100',
      '0100'],
     ['0000',
      '1111',
      '0000',
      '0000']]
J = [['1000',
      '1110',
      '0000',
      '0000'],
     ['0110',
      '0100',
      '0100',
      '0000'],
     ['0000',
      '1110',
      '0010',
      '0000'],
     ['0100',
      '0100',
      '1100',
      '0000']]
L = [['0010',
      '1110',
      '0000',
      '0000'],
     ['0100',
      '0100',
      '0110',
      '0000'],
     ['1110',
      '1000',
      '0000',
      '0000'],
     ['1100',
      '0100',
      '0100',
      '0000']]
O = [['0000',
      '0110',
      '0110',
      '0000']]
S = [['0000',
      '0011',
      '0110',
      '0000'],
     ['0100',
      '0110',
      '0010',
      '0000']]
T = [['0100',
      '1110',
      '0000',
      '0000'],
     ['1000',
      '1100',
      '1000',
      '0000'],
     ['1110',
      '0100',
      '0000',
      '0000'],
     ['0100',
      '1100',
      '0100',
      '0000']]
Z = [['0000',
      '1100',
      '0110',
      '0000'],
     ['0100',
      '1100',
      '1000',
      '0000']]

shapes = [I, J, L, O, S, T, Z]
shape_colors = [(13, 105, 105), (31, 25, 90), (100, 62, 14),
                (110, 99, 13), (23, 75, 0), (46, 20, 40), (92, 0, 0)] # define color to the shapes

tetrominos = {} # dict for saving the tetrominos, that will drawn

# =============================================================================
# Function for render Textes and Infos
# =============================================================================

def debug(info, pos=(10, 10), text_size=10, centered=False, offset=0):
    font = pygame.font.SysFont("liberationserif", text_size)
    text = font.render(str(info), True, (255, 255, 255))
    if centered:
        center = [WIDTH//2-text.get_width()//2, HEIGHT//2-text.get_height()//2]
        center[1] += text.get_height()*offset
        pos = center
    screen.blit(text, pos)
    pygame.display.update()

# =============================================================================
# Function for selecting new Shape from Shapes
# =============================================================================

def getNewShape():
    """Function that returns a random Tetromino-Shape and the color of it"""
    shape = choice(shapes)
    color = shape_colors[shapes.index(shape)]
    return (shape, color)

# =============================================================================
# Function that add the current instance of Tetromino to the other falled tetro-
# minos in the tetrominos-dict 
# =============================================================================

def cur_shapeToTetros(shape):
    """Function which combine the current Tetromino and the falled Tetrominos and 
        return this configuartion in form of an Dictionary"""
    adding_tetrominos = {}
    for y_offset, row in enumerate(shape[0]):
        for x_offset, col in enumerate(row):
            if col == '1':
                x, y = shape[1]+(x_offset*TILESIZE), shape[2] + \
                    (y_offset*TILESIZE)
                adding_tetrominos.update({(x, y): shape[3]})
    adding_tetrominos.update(tetrominos)
    return adding_tetrominos

# =============================================================================
# Function for add a falling Tetromino to the other falled Tetrominos 
# =============================================================================

def addFalled(shape):
    """Function which add the current falling Tetromino (Instance of the class 
        Tetromino) to the falled Tetromino-Dictionary"""
    for y_offset, row in enumerate(shape[0]):
        for x_offset, col in enumerate(row):
            if col == '1':
                x, y = shape[1] + x_offset * \
                    TILESIZE, shape[2] + y_offset*TILESIZE
                tetrominos.update({(x, y): shape[3]})

# =============================================================================
# Function for check, if some rows are competed and let fall the rows over them
# =============================================================================

def checkRow(tetros):
    """Function, which check for completed rows and, if necessary, delete them 
        and let fall the rows over them (Returning the new Configuartion in a Dictionary"""
    global POINTS, fall_time
    # Dictionary where to each row the number of bricks is noted
    rows = {}
    for key in tetros.keys():
        if key[1] in rows:
            rows[key[1]] += 1
        else:
            rows.update({key[1]: 1})

    print(rows)
    # for each full row -> delete row +  fall rows over the full row
    for row in sorted(rows.keys()):
        if rows[row] == WIDTH//TILESIZE: # if full row
            falled = {} 
            POINTS += 1 
            if POINTS % 10 == 0: # ever 10 points
                fall_time -= FPS//60 # increase falltime of Tetromino
            for t in sorted(tetros.keys(), key=lambda xy: xy[1]):
                if t[1] < row:
                    falled.update({(t[0], t[1]+TILESIZE): tetros[t]})
                elif t[1] > row:
                    falled.update({(t): tetros[t]})
            tetros = falled.copy()
    return tetros

# =============================================================================
# Class for the currently falling Tetromino
# =============================================================================

class Tetromino():
    def __init__(self, shape, color):
        self.shape = shape
        self.color = color
        self.x = (WIDTH//TILESIZE//2) * TILESIZE - TILESIZE*2 # entspricht der mitte
        self.y = 0
        self.rotation = 0
        self.c_element = shape[self.rotation]  # derzeitiges Shape

    def fall(self, x=0, y=TILESIZE):
        """Function for moving/falling the Tetromino"""
        if self.collide(self.c_element, self.x+x, self.y+y) == False:
            self.y += y
            self.x += x
            return True
        return False

    def rotate(self):
        """Function for rotating the Tetromino"""
        self.rotation += 1
        if len(self.shape) == self.rotation:
            self.rotation = 0
        if self.collide(self.shape[self.rotation], self.x, self.y) == False:
            self.c_element = self.shape[self.rotation]
        else: # if colliding -> set rotation back
            self.rotation -= 1
            if 0 > self.rotation:
                self.rotation = len(self.shape)-1

    def collide(self, shape, x, y):
        """Checking, if Tetromino collide with a border or an other Tetromino"""
        for y_offset in range(len(shape)):
            for x_offset in range(len(shape[y_offset])):
                if shape[y_offset][x_offset] == '1':
                    if x + x_offset*TILESIZE < 0 or x + x_offset*TILESIZE >= WIDTH:
                        return True  # x
                    if y + y_offset*TILESIZE >= HEIGHT:
                        return True  # y
                    if (x + x_offset*TILESIZE, y + y_offset*TILESIZE) in tetrominos:
                        return True  # collide with a other Tetromino
        return False

    def get_shape(self):  # return current Shape with position and color
        return (self.c_element, self.x, self.y, self.color)

# =============================================================================
# Function for draw all Tetrominos to the screen
# =============================================================================

def drawTetrominos(tetros):
    """Function, which draw all tetrominos to the screen"""
    for tetro in tetros.keys():
        pygame.draw.rect(
            screen, tetros[tetro], (tetro[0], tetro[1], TILESIZE, TILESIZE), border_radius=5)

# =============================================================================
# Function for draw the GameOver-Screen
# =============================================================================

def gameOver():
    global tetrominos, count, fall_time, move_count, falled, userMoved, FPS, POINTS
    count = 0
    """Function which called, if the game is over"""
    debug("Points: " + str(POINTS))
    debug("Game Over!", text_size=TILESIZE, centered=True)
    while True:
        count += 1
        for event in pygame.event.get():  # cheking for events
            if event.type == pygame.QUIT:  # if the user close the Window
                pygame.quit()
                close_program()
            if event.type == pygame.KEYUP:
                if count >= FPS: # cou can restart only after 1 second
                    # reset variables (without c_tetromino, cause it doesn't fall yet)
                    tetrominos = {}
                    POINTS, count = 0, 0
                    fall_time = FPS//2
                    move_count = [0, 0]
                    falled, userMoved = False, False
                    return
        pressedKeys = pygame.key.get_pressed()
        if pressedKeys[pygame.K_LCTRL] and pressedKeys[pygame.K_q]:
            pygame.quit()
            close_program()
        clock.tick(30)

# =============================================================================
# Function for draw the Pause-Screen
# =============================================================================

def pause():
    """Function which called if the game is paused"""
    screen.fill("black")
    debug("Paused!", text_size=TILESIZE, centered=True, offset=-0.5)
    debug("Press any key to continue",
          text_size=TILESIZE, centered=True, offset=0.5)
    while True:
        for event in pygame.event.get([pygame.QUIT, pygame.KEYDOWN]):  # cheking for events
            if event.type == pygame.QUIT:  # if the user close the Window
                pygame.quit()
                close_program()
            if event.type == pygame.KEYDOWN:
                return
        clock.tick(30)

# =============================================================================
# Init basic Variables
# =============================================================================

newshape = getNewShape() # getting a random shape
c_tetromino = Tetromino(newshape[0], newshape[1]) # make a Instance of Tetromino

falled = False 
count = 0 # past time
fall_time = FPS//2 # time, when to update the screen
move_count = [0, 0] # need, that the moving isn't to speedy

# =============================================================================
# Main Game-Loop:
# =============================================================================

while True:
    count += 1
    move_count[0] -= 1 if move_count[0] >= 0 else 0
    move_count[1] -= 1 if move_count[1] >= 0 else 0
    userMoved = False
    
    #checking for events
    for event in pygame.event.get([pygame.QUIT, pygame.KEYDOWN]):
        if event.type == pygame.QUIT:  # if user close the Window
            pygame.quit()
            close_program()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:  # rotate
                c_tetromino.rotate()
                falled = False
                userMoved = True
            if event.key == pygame.K_SPACE:  # let fall it to the bottom
                while True:
                    if not(c_tetromino.fall()):
                        break
                userMoved = True
            if event.key == pygame.K_DOWN:  # one down
                if not(c_tetromino.fall()): # if it can't move down, cause it's at bottom
                    falled = True # set falled to True
                userMoved = True
            if event.key == pygame.K_p: # if P pressed:
                pause()
    
    #following is for the moving to the right or left side
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT]:
        if move_count[0] <= 0:
            c_tetromino.fall(x=-TILESIZE, y=0)
            falled, userMoved = False, True
            move_count[0] = FPS//7.5 # if FPS = 30 its 4
    else: move_count[0] = 0
    
    if keys[pygame.K_RIGHT]:
        if move_count[1] <= 0:
            c_tetromino.fall(x=TILESIZE, y=0)
            falled, userMoved = False, True
            move_count[1] = FPS//7.5 # if FPS = 30 its 4
    else: move_count[1] = 0
        
    if keys[pygame.K_LCTRL] and keys[pygame.K_q]: # short cut for closing Window(Strg+Q)
        pygame.quit()
        close_program()

    # if Tetromino falled but user Moved, check if it can fall further or not
    if userMoved == True: 
        if c_tetromino.fall() == False: # if not
            falled = True # set Falled finally to True
        else: c_tetromino.fall(y=-TILESIZE) # falled = True + previous Position

    # following is for the falling and drawing
    if count % fall_time == 0 or userMoved == True:
        if falled == True:  # if Tetromino has reached the bottom
            addFalled(c_tetromino.get_shape()) # add it to other falled Tetrominos
            tetrominos = checkRow(tetrominos) # checking for completed rows
            
            newshape = getNewShape()  # get new Shape
            c_tetromino = Tetromino(newshape[0], newshape[1]) # creating new Instance to Tetromino
            falled = False  # set falled back to False

            if c_tetromino.fall() == False: # if the new Tetromino can't move the game is over
                screen.fill('black')
                drawTetrominos(cur_shapeToTetros(
                    c_tetromino.get_shape()))  # draw Tetrominos
                pygame.display.update() # updating Display
                gameOver() # and call the gameover function
            else: c_tetromino.fall(y=-TILESIZE) # if it can fall > set it to startposition

        screen.fill('black')

        drawTetrominos(cur_shapeToTetros(
            c_tetromino.get_shape()))  # draw Tetrominos

        debug(str(round(clock.get_fps())) + " fps")   # show FPS
        debug("Points: " + str(POINTS), pos=(10, 25)) # show Points

        if count % fall_time == 0:
            falled = not(c_tetromino.fall())
            
        pygame.display.update()
    clock.tick(FPS)