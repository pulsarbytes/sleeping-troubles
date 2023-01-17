# -*- coding: utf-8 -*-
"""
Sleeping Troubles v.0.1.2

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
import pygame as pg
from pygame.locals import *
import os
import sys

if getattr(sys, 'frozen', False):
    # frozen
    main_dir = os.path.split(os.path.abspath(sys.executable))[0]
else:
    # unfrozen
    main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'data')


def load_window_icon(name, colorkey=None):
    """
    Loads window icon.
    """
    fullname = os.path.join(data_dir, name)
    try:
        icon = pg.image.load(fullname)
    except pg.error as message:
        print("Couldn't load image:", name)
        raise SystemExit(message)
    if colorkey is not None:
        if colorkey == -1:
            colorkey = icon.get_at((0, 0))
        icon.set_colorkey(colorkey, pg.RLEACCEL)
    return icon


def load_image(name, transparent=False, colorkey=None):
    """
    Platform independent function that loads an image file located in 'data' folder.
    name: file name
    colorkey: RGB value (tuple)
    Returns: tuple of image object, image rect
    """

    fullname = os.path.join(data_dir, name)
    try:
        image = pg.image.load(fullname)
    except pg.error as message:
        print("Couldn't load image:", name)
        raise SystemExit(message)
    if transparent == True:
        image = image.convert_alpha()
    else:
        image = image.convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pg.RLEACCEL)
    return image, image.get_rect()


def load_sound(name):
    """
    Platform independent function that loads a sound file located in 'data' folder.
    name: file name
    Returns: sound object
    """
    class NoneSound:
        def play(self): pass
    if not pg.mixer:
        return NoneSound()
    fullname = os.path.join(data_dir, name)
    try:
        sound = pg.mixer.Sound(fullname)
    except pg.error as message:
        print("Couldn't load sound:", name)
        raise SystemExit(message)
    return sound


def play_sound(sound, action='play'):
    """
    Platform independent function that plays a pygame sound.
    name: sound object name
    Returns: None
    """
    class NoneSound:
        def play(self): pass
    if not pg.mixer:
        return NoneSound()
    try:
        if action == 'play':
            pg.mixer.Sound.play(sound)
        else:
            pg.mixer.Sound.stop(sound)
    except pg.error as message:
        print("Couldn't play sound:", sound)
        raise SystemExit(message)
    return


def play_music(name, action='play', repeat=-1):
    """
    Platform independent function that plays a musical track located in 'data' folder.
    name: file name
    Returns: None
    """
    class NoneSound:
        def play(self): pass
    if not pg.mixer:
        return NoneSound()
    fullname = os.path.join(data_dir, name)
    try:
        pg.mixer.music.load(fullname)
        pg.mixer.music.set_volume(0.4)
        if action == 'play':
            pg.mixer.music.play(repeat)
        elif action == 'stop':
            pg.mixer.music.stop()
    except pg.error as message:
        print("Couldn't load music:", name)
        raise SystemExit(message)
    return


def get_sound_duration(name):
    import wave
    import contextlib
    fullname = os.path.join(data_dir, name)
    with contextlib.closing(wave.open(fullname, 'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
        duration = float("{0:.2f}".format(duration))
        return duration
