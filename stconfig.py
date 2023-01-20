"""
Sleeping Troubles v0.1.3

Sleeping Troubles is a simple board game, developed with Python and Pygame, implementing a State machine.
Sleeping Troubles requires Pygame to be installed. Pygame can be downloaded from http://pygame.org.
Developed by Yannis Maragos. Concept and design by Evi Filakouri.

Copyright (C) 2018  Pulsar Bytes.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License version 2 only,
as published by the Free Software Foundation.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

ST_VERSION = '0.1.3'
ST_FPS = 20
ST_YEAR = '2023'

# Audio
SOUND_ON = True
MUSIC_ON = True

MIXER_FREQUENCY = 44100
MIXER_SIZE = -16
MIXER_CHANNELS = 2
MIXER_BUFFER = 4096

# Dimensions and sizes
ST_SCREEN_WIDTH = 1300
ST_SCREEN_HEIGHT = 740

TOPBAR_HEIGHT = 70
TOOLBAR_WIDTH = 260
MENUBUTTON_WIDTH = 250
MENUBUTTON_HEIGHT = 36
MENUBUTTON_SPACE = 14
SQUARES_SPACE = 6
TOOLBAR_MENUBUTTON_WIDTH = 160
TOOLBAR_MENUBUTTON_HEIGHT = 30
DICEBOX_HEIGHT = 220
ROLLBUTTON_WIDTH = 160
ROLLBUTTON_HEIGHT = 40
POPUP_WIDTH = 520
POPUP_HEIGHT = 340
POPUP_PADDING = 20
POPUP_BUTTON_WIDTH = 195
POPUP_BUTTON_HEIGHT = 40

# Game
STARTING_TPOINTS = 8
STARTING_DCRYSTALS = 1

# Colors
ST_PINK = (255, 230, 230)
ST_BLACK40 = (40, 40, 40)
ST_BLACK60 = (60, 60, 60)
ST_BLACK100 = (100, 100, 100)
ST_RED = (255, 51, 51)
ST_GREEN = (113, 209, 113)
ST_BLUE = (65, 194, 194)
ST_BLACK = (0, 0, 0)
ST_YELLOW = (255, 255, 102)
ST_ORANGE = (239, 185, 65)
ST_DARKORANGE = (240, 90, 40)
ST_WHITE = (255, 255, 255)
ST_LIGHTGRAY = (212, 208, 200)
ST_GRAY120 = (120, 120, 120)
ST_GRAY217 = (217, 217, 217)
ST_LIGHTERGRAY = (230, 230, 255)
ST_PURPLE = (191, 0, 191)
