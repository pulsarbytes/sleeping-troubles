# -*- coding: utf-8 -*-
"""
Sleeping Troubles v0.1.2

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
import pygbutton
import sys
import os
import sthelper
import random


class States(object):
    game_on = False
    music_on = True
    sound_on = True
    screen_copy = None

    def __init__(self):
        self.done = False
        self.quit = False
        self.target = None
        self.dirty_rects = []
        self.menuButtons = []
        self.soundButtons = []
        self.dice_locked = False

        # load sounds
        self.sound_button_hover = sthelper.load_sound('button-hover.wav')
        self.sound_button_hover.set_volume(0.2)
        self.sound_button_click = sthelper.load_sound('button-click.wav')
        self.sound_button_click.set_volume(0.5)

        # load sound icons
        self.icon_music_on, self.rect_icon_music_on = sthelper.load_image(
            'music-on.png', True)
        self.icon_music_off, self.rect_icon_music_off = sthelper.load_image(
            'music-off.png', True)
        self.icon_sound_on, self.rect_icon_sound_on = sthelper.load_image(
            'sound-on.png', True)
        self.icon_sound_off, self.rect_icon_sound_off = sthelper.load_image(
            'sound-off.png', True)

    def get_button_events(self, button_events):
        if 'enter' in button_events:
            if States.sound_on == True:
                sthelper.play_sound(self.sound_button_hover)

    def get_sound_button_events(self, event):
        for soundButton in self.soundButtons:
            sound_events = soundButton.handleEvent(event)
            if 'click' in sound_events:
                if soundButton._propGetId() == 'music_toggle':
                    if States.music_on == False:
                        States.music_on = True
                    else:
                        States.music_on = False
                if soundButton._propGetId() == 'sound_toggle':
                    if States.sound_on == False:
                        States.sound_on = True
                    else:
                        States.sound_on = False
                sthelper.play_sound(self.sound_button_click)
            if 'enter' in sound_events:
                if States.sound_on == True:
                    sthelper.play_sound(self.sound_button_hover)

    def update(self, screen):
        if States.music_on == True:
            pg.mixer.music.unpause()
        else:
            pg.mixer.music.pause()

    def draw(self, screen, background):
        """
        Blits persistent elements to background.
        Final blit of background happens in this function.
        """
        # draw sound icons buttons
        if States.music_on == True:
            music_icon = self.icon_music_on
        else:
            music_icon = self.icon_music_off
        if States.sound_on == True:
            sound_icon = self.icon_sound_on
        else:
            sound_icon = self.icon_sound_off

        musicToggleButton = pygbutton.PygButton((screen.get_width() - TOOLBAR_WIDTH/2 - 1.5*music_icon.get_width(
        ), TOPBAR_HEIGHT/2 - music_icon.get_height()/2, music_icon.get_width(), music_icon.get_height()), bid="music_toggle", normal=music_icon)
        soundToggleButton = pygbutton.PygButton((screen.get_width() - TOOLBAR_WIDTH/2 + 0.5*sound_icon.get_width(
        ), TOPBAR_HEIGHT/2 - sound_icon.get_height()/2, sound_icon.get_width(), sound_icon.get_height()), bid="sound_toggle", normal=sound_icon)

        sound_buttons = {
            "music_toggle": musicToggleButton,
            "sound_toggle": soundToggleButton,
        }
        for (button_id, button) in sound_buttons.items():
            button.draw(background)
            if len(self.soundButtons) < len(sound_buttons):
                self.soundButtons.append(button)

        screen.blit(background, (0, 0))


class Menu(States):
    def __init__(self):
        States.__init__(self)
        sthelper.play_music('game-music.mp3', 'stop')
        if States.music_on == True:
            sthelper.play_music('menu-music.wav')
            pg.mixer.music.pause()

    def get_event(self, event, screen):
        for menuButton in self.menuButtons:
            button_events = menuButton.handleEvent(event)
            if 'click' in button_events:
                if menuButton._propGetId() == 'continue':
                    self.done = True
                    self.target = 'game'
                if menuButton._propGetId() == 'game':
                    States.game_on = False
                    self.done = True
                    self.target = 'game'
                if menuButton._propGetId() == 'help':
                    self.done = True
                    self.target = 'help'
                if menuButton._propGetId() == 'credits':
                    self.done = True
                    self.target = 'credits'
                if menuButton._propGetId() == 'exit':
                    self.done = True
                    self.quit = True
                if States.sound_on == True:
                    sthelper.play_sound(self.sound_button_click)
            super(Menu, self).get_button_events(button_events)

        super(Menu, self).get_sound_button_events(event)

    def cleanup(self):
        pass

    def startup(self):
        pass

    def update(self, screen, dt):
        self.draw(screen)
        super(Menu, self).update(screen)

    def draw(self, screen):
        # fill a surface with a background color
        background = pg.Surface(screen.get_size())
        background = background.convert()
        background.fill(ST_PINK)

        # add logo image
        logo, rect_logo = sthelper.load_image('logo.png', True)
        background.blit(logo, (int(screen.get_width()/2) -
                        int(logo.get_width()/2), int(logo.get_height()/2)))

        # add Nick image
        nick_image, rect_nick_image = sthelper.load_image('nick.png', True)
        background.blit(nick_image, (int(screen.get_width(
        )/2) - (int(MENUBUTTON_WIDTH/2) + 110), 2*logo.get_height() + 2*MENUBUTTON_HEIGHT))

        # add Eugene image
        eugene_image, rect_eugene_image = sthelper.load_image(
            'eugene.png', True)
        background.blit(eugene_image, (int(screen.get_width()/2) + (int(MENUBUTTON_WIDTH/2) +
                        110) - eugene_image.get_width(), 2*logo.get_height() + 2*MENUBUTTON_HEIGHT))

        # add menu buttons
        if States.game_on == True:
            menu_buttons = {
                "continue": ["Continue game", ST_LIGHTGRAY, ST_BLACK],
                "game": ["New game", ST_LIGHTGRAY, ST_BLACK],
                "help": ["Help", ST_LIGHTGRAY, ST_BLACK],
                "credits": ["Credits", ST_LIGHTGRAY, ST_BLACK],
                "exit": ["Exit game", ST_LIGHTGRAY, ST_BLACK]
            }
        else:
            menu_buttons = {
                "game": ["New game", ST_LIGHTGRAY, ST_BLACK],
                "help": ["Help", ST_LIGHTGRAY, ST_BLACK],
                "credits": ["Credits", ST_LIGHTGRAY, ST_BLACK],
                "exit": ["Exit game", ST_LIGHTGRAY, ST_BLACK]
            }
        if len(self.menuButtons) != len(menu_buttons):
            self.menuButtons = []
        for i, (button_id, button) in enumerate(menu_buttons.items()):
            y_offset = 2*logo.get_height() + (i+1)*(MENUBUTTON_HEIGHT+MENUBUTTON_SPACE)
            menuButton = pygbutton.PygButton(((int(background.get_width()/2)) - int(MENUBUTTON_WIDTH/2), y_offset,
                                             MENUBUTTON_WIDTH, MENUBUTTON_HEIGHT), button[0], button_id, bgcolor=button[1], fgcolor=button[2])
            menuButton.draw(background)
            if len(self.menuButtons) < len(menu_buttons):
                self.menuButtons.append(menuButton)

        if pg.font:
            # add footer
            font = pg.font.Font(None, 16)
            footer = font.render('Sleeping Troubles v.' +
                                 ST_VERSION+' - '+ST_YEAR+'', 1, ST_BLACK40)
            footerpos = footer.get_rect(centerx=int(
                background.get_width()/2), y=screen.get_height() - 30)
            background.blit(footer, (footerpos.x, footerpos.y))

        super(Menu, self).draw(screen, background)


class Board(object):
    def __init__(self):
        x = (ST_SCREEN_WIDTH - TOOLBAR_WIDTH - SQUARES_SPACE)/9 - SQUARES_SPACE
        x = float("{0:.2f}".format(x))
        y = (ST_SCREEN_HEIGHT - TOPBAR_HEIGHT - SQUARES_SPACE)/8 - SQUARES_SPACE
        y = float("{0:.2f}".format(y))
        self.square_width = x
        self.square_height = y

        # icons
        self.icon_home, self.rect_icon_home = sthelper.load_image(
            'home.png', True)
        self.icon_hourglass, self.rect_icon_hourglass = sthelper.load_image(
            'hourglass.png', True)
        self.icon_telephone, self.rect_icon_telephone = sthelper.load_image(
            'telephone.png', True)
        self.icon_hourglass_white, self.rect_icon_hourglass_white = sthelper.load_image(
            'hourglass-white.png', True)
        self.icon_dreamcrystal, self.rect_icon_dreamcrystal = sthelper.load_image(
            'dream-crystal.png', True)
        self.icon_exclamation, self.rect_icon_exclamation = sthelper.load_image(
            'exclamation.png', True)
        self.icon_end, self.rect_icon_end = sthelper.load_image(
            'sleeping.png', True)

        # sounds
        self.sound_normal = sthelper.load_sound('button-click.wav')
        self.sound_lose_points = sthelper.load_sound('lose-points.wav')
        self.sound_telephone = sthelper.load_sound('telephone.wav')
        self.sound_gain_points = sthelper.load_sound('gain-points.wav')
        self.sound_gain_points.set_volume(0.5)
        self.sound_dream_crystal = sthelper.load_sound('dream-crystal.wav')
        self.sound_kitchen = sthelper.load_sound('kitchen.wav')
        self.sound_bathroom = sthelper.load_sound('bathroom.wav')
        self.sound_weird_noises = sthelper.load_sound('weird-noises.wav')
        self.sound_forgot_pill = sthelper.load_sound('forgot-pill.wav')
        self.sound_points_reduced = sthelper.load_sound('points-reduced.wav')

        self.squares = {
            1: {"type": 'start',        "bcolor": ST_ORANGE,      "coords": [1*SQUARES_SPACE,          1*SQUARES_SPACE],          "text": '',                  "fcolor": ST_DARKORANGE, "icon": self.icon_home, "sound": self.sound_normal},
            2: {"type": 'normal',       "bcolor": ST_LIGHTERGRAY, "coords": [2*SQUARES_SPACE + 1*x,    1*SQUARES_SPACE],          "text": '',                  "fcolor": ST_GRAY120, "icon": None, "sound": self.sound_normal},
            3: {"type": 'tpoints:-2',   "bcolor": ST_RED,         "coords": [3*SQUARES_SPACE + 2*x,    1*SQUARES_SPACE],          "text": '-2',                "fcolor": ST_BLACK, "icon": self.icon_hourglass, "sound": self.sound_lose_points},
            4: {"type": 'normal',       "bcolor": ST_LIGHTERGRAY, "coords": [4*SQUARES_SPACE + 3*x,    1*SQUARES_SPACE],          "text": '',                  "fcolor": ST_GRAY120, "icon": None, "sound": self.sound_normal},
            5: {"type": 'normal',       "bcolor": ST_LIGHTERGRAY, "coords": [5*SQUARES_SPACE + 4*x,    1*SQUARES_SPACE],          "text": '',                  "fcolor": ST_GRAY120, "icon": None, "sound": self.sound_normal},
            6: {"type": 'telephone',    "bcolor": ST_YELLOW,      "coords": [6*SQUARES_SPACE + 5*x,    1*SQUARES_SPACE],          "text": '',                  "fcolor": ST_GRAY120, "icon": self.icon_telephone, "sound": self.sound_telephone},
            7: {"type": 'tpoints:2',    "bcolor": ST_GREEN,       "coords": [7*SQUARES_SPACE + 6*x,    1*SQUARES_SPACE],          "text": '+2',                "fcolor": ST_WHITE, "icon": self.icon_hourglass_white, "sound": self.sound_gain_points},
            8: {"type": 'normal',       "bcolor": ST_LIGHTERGRAY, "coords": [8*SQUARES_SPACE + 7*x,    1*SQUARES_SPACE],          "text": '',                  "fcolor": ST_GRAY120, "icon": None, "sound": self.sound_normal},
            9: {"type": 'dcrystals:1',  "bcolor": ST_BLUE,        "coords": [9*SQUARES_SPACE + 8*x,    1*SQUARES_SPACE],          "text": '',                  "fcolor": ST_GRAY120, "icon": self.icon_dreamcrystal, "sound": self.sound_dream_crystal},
            10: {"type": 'normal',      "bcolor": ST_LIGHTERGRAY, "coords": [9*SQUARES_SPACE + 8*x,    2*SQUARES_SPACE + y],      "text": '',                  "fcolor": ST_GRAY120, "icon": None, "sound": self.sound_normal},
            11: {"type": 'tpoints:-4',  "bcolor": ST_RED,         "coords": [9*SQUARES_SPACE + 8*x,    3*SQUARES_SPACE + 2*y],    "text": '-4',                "fcolor": ST_BLACK, "icon": self.icon_hourglass, "sound": self.sound_lose_points},
            12: {"type": 'normal',      "bcolor": ST_LIGHTERGRAY, "coords": [9*SQUARES_SPACE + 8*x,    4*SQUARES_SPACE + 3*y],    "text": '',                  "fcolor": ST_GRAY120, "icon": None, "sound": self.sound_normal},
            13: {"type": 'normal',      "bcolor": ST_LIGHTERGRAY, "coords": [9*SQUARES_SPACE + 8*x,    5*SQUARES_SPACE + 4*y],    "text": '',                  "fcolor": ST_GRAY120, "icon": None, "sound": self.sound_normal},
            14: {"type": 'telephone',   "bcolor": ST_YELLOW,      "coords": [9*SQUARES_SPACE + 8*x,    6*SQUARES_SPACE + 5*y],    "text": '',                  "fcolor": ST_GRAY120, "icon": self.icon_telephone, "sound": self.sound_telephone},
            15: {"type": 'tpoints:-2',  "bcolor": ST_RED,         "coords": [9*SQUARES_SPACE + 8*x,    7*SQUARES_SPACE + 6*y],    "text": '-2',                "fcolor": ST_BLACK, "icon": self.icon_hourglass, "sound": self.sound_lose_points},
            16: {"type": 'kitchen',     "bcolor": ST_ORANGE,      "coords": [9*SQUARES_SPACE + 8*x,    8*SQUARES_SPACE + 7*y],    "text": 'KITCHEN',           "fcolor": ST_DARKORANGE, "icon": None, "sound": self.sound_kitchen},
            17: {"type": 'normal',      "bcolor": ST_LIGHTERGRAY, "coords": [8*SQUARES_SPACE + 7*x,    8*SQUARES_SPACE + 7*y],    "text": '',                  "fcolor": ST_GRAY120, "icon": None, "sound": self.sound_normal},
            18: {"type": 'normal',      "bcolor": ST_LIGHTERGRAY, "coords": [7*SQUARES_SPACE + 6*x,    8*SQUARES_SPACE + 7*y],    "text": '',                  "fcolor": ST_GRAY120, "icon": None, "sound": self.sound_normal},
            19: {"type": 'dcrystals:1', "bcolor": ST_BLUE,        "coords": [6*SQUARES_SPACE + 5*x,    8*SQUARES_SPACE + 7*y],    "text": '',                  "fcolor": ST_GRAY120, "icon": self.icon_dreamcrystal, "sound": self.sound_dream_crystal},
            20: {"type": 'normal',      "bcolor": ST_LIGHTERGRAY, "coords": [5*SQUARES_SPACE + 4*x,    8*SQUARES_SPACE + 7*y],    "text": '',                  "fcolor": ST_GRAY120, "icon": None, "sound": self.sound_normal},
            21: {"type": 'tpoints:1',   "bcolor": ST_GREEN,       "coords": [4*SQUARES_SPACE + 3*x,    8*SQUARES_SPACE + 7*y],    "text": '+1',                "fcolor": ST_WHITE, "icon": self.icon_hourglass_white, "sound": self.sound_gain_points},
            22: {"type": 'back:-7',     "bcolor": ST_BLACK,       "coords": [3*SQUARES_SPACE + 2*x,    8*SQUARES_SPACE + 7*y],    "text": '7 squares back',    "fcolor": ST_WHITE, "icon": self.icon_exclamation, "sound": self.sound_forgot_pill},
            23: {"type": 'normal',      "bcolor": ST_LIGHTERGRAY, "coords": [2*SQUARES_SPACE + 1*x,    8*SQUARES_SPACE + 7*y],    "text": '',                  "fcolor": ST_GRAY120, "icon": None, "sound": self.sound_normal},
            24: {"type": 'bathroom',    "bcolor": ST_ORANGE,      "coords": [1*SQUARES_SPACE,          8*SQUARES_SPACE + 7*y],    "text": 'BATHROOM',          "fcolor": ST_DARKORANGE, "icon": None, "sound": self.sound_bathroom},
            25: {"type": 'tpoints:-2',  "bcolor": ST_RED,         "coords": [1*SQUARES_SPACE,          7*SQUARES_SPACE + 6*y],    "text": '-2',                "fcolor": ST_BLACK, "icon": self.icon_hourglass, "sound": self.sound_lose_points},
            26: {"type": 'normal',      "bcolor": ST_LIGHTERGRAY, "coords": [1*SQUARES_SPACE,          6*SQUARES_SPACE + 5*y],    "text": '',                  "fcolor": ST_GRAY120, "icon": None, "sound": self.sound_normal},
            27: {"type": 'telephone',   "bcolor": ST_YELLOW,      "coords": [1*SQUARES_SPACE,          5*SQUARES_SPACE + 4*y],    "text": '',                  "fcolor": ST_GRAY120, "icon": self.icon_telephone, "sound": self.sound_telephone},
            28: {"type": 'normal',      "bcolor": ST_LIGHTERGRAY, "coords": [1*SQUARES_SPACE,          4*SQUARES_SPACE + 3*y],    "text": '',                  "fcolor": ST_GRAY120, "icon": None, "sound": self.sound_normal},
            29: {"type": 'back:-6',     "bcolor": ST_BLACK,       "coords": [1*SQUARES_SPACE,          3*SQUARES_SPACE + 2*y],    "text": '6 squares back',    "fcolor": ST_WHITE, "icon": self.icon_exclamation, "sound": self.sound_weird_noises},
            30: {"type": 'tpoints:1',   "bcolor": ST_GREEN,       "coords": [2*SQUARES_SPACE + 1*x,    3*SQUARES_SPACE + 2*y],    "text": '+1',                "fcolor": ST_WHITE, "icon": self.icon_hourglass_white, "sound": self.sound_gain_points},
            31: {"type": 'normal',      "bcolor": ST_LIGHTERGRAY, "coords": [3*SQUARES_SPACE + 2*x,    3*SQUARES_SPACE + 2*y],    "text": '',                  "fcolor": ST_GRAY120, "icon": None, "sound": self.sound_normal},
            32: {"type": 'dcrystals:1', "bcolor": ST_BLUE,        "coords": [4*SQUARES_SPACE + 3*x,    3*SQUARES_SPACE + 2*y],    "text": '',                  "fcolor": ST_GRAY120, "icon": self.icon_dreamcrystal, "sound": self.sound_dream_crystal},
            33: {"type": 'normal',      "bcolor": ST_LIGHTERGRAY, "coords": [5*SQUARES_SPACE + 4*x,    3*SQUARES_SPACE + 2*y],    "text": '',                  "fcolor": ST_GRAY120, "icon": None, "sound": self.sound_normal},
            34: {"type": 'tpoints:1',   "bcolor": ST_GREEN,       "coords": [6*SQUARES_SPACE + 5*x,    3*SQUARES_SPACE + 2*y],    "text": '+1',                "fcolor": ST_WHITE, "icon": self.icon_hourglass_white, "sound": self.sound_gain_points},
            35: {"type": 'risk',        "bcolor": ST_RED,         "coords": [7*SQUARES_SPACE + 6*x,    3*SQUARES_SPACE + 2*y],    "text": '',                  "fcolor": ST_WHITE, "icon": self.icon_hourglass_white, "sound": self.sound_points_reduced},
            36: {"type": 'normal',      "bcolor": ST_LIGHTERGRAY, "coords": [7*SQUARES_SPACE + 6*x,    4*SQUARES_SPACE + 3*y],    "text": '',                  "fcolor": ST_GRAY120, "icon": None, "sound": self.sound_normal},
            37: {"type": 'tpoints:-2',  "bcolor": ST_RED,         "coords": [7*SQUARES_SPACE + 6*x,    5*SQUARES_SPACE + 4*y],    "text": '-2',                "fcolor": ST_BLACK, "icon": self.icon_hourglass, "sound": self.sound_lose_points},
            38: {"type": 'normal',      "bcolor": ST_LIGHTERGRAY, "coords": [7*SQUARES_SPACE + 6*x,    6*SQUARES_SPACE + 5*y],    "text": '',                  "fcolor": ST_GRAY120, "icon": None, "sound": self.sound_normal},
            39: {"type": 'normal',      "bcolor": ST_LIGHTERGRAY, "coords": [6*SQUARES_SPACE + 5*x,    6*SQUARES_SPACE + 5*y],    "text": '',                  "fcolor": ST_GRAY120, "icon": None, "sound": self.sound_normal},
            40: {"type": 'tpoints:-4',  "bcolor": ST_RED,         "coords": [5*SQUARES_SPACE + 4*x,    6*SQUARES_SPACE + 5*y],    "text": '-4',                "fcolor": ST_BLACK, "icon": self.icon_hourglass, "sound": self.sound_lose_points},
            41: {"type": 'end',         "bcolor": ST_GREEN,       "coords": [4*SQUARES_SPACE + 3*x,    6*SQUARES_SPACE + 5*y],    "text": 'END',               "fcolor": ST_WHITE, "icon": self.icon_end, "sound": None},
        }

    def get_squares_count(self):
        return self.squares_count

    def get_squares(self):
        return self.squares

    def get_square_width(self):
        return self.square_width

    def get_square_height(self):
        return self.square_height

    def get_square_coords(self, position):
        squares = self.get_squares()
        coords = squares[position]['coords']
        return coords

    def get_square_sound(self, position):
        squares = self.get_squares()
        sound = squares[position]['sound']
        return sound


class Player(pg.sprite.Sprite):
    def __init__(self):
        self.position = 1
        self.image, self.rect_image = sthelper.load_image('player.png', True)

    def get_player_position(self):
        return self.position

    def set_player_position(self, position):
        self.position = position
        return self.position

    def get_player_image(self):
        return self.image


class Game(States):
    def __init__(self):
        States.__init__(self)
        self.end = False
        self.won_game = None

        # message
        self.message = 'Roll the dice!'

        # dice
        self.dice_images = [
            sthelper.load_image('dice_question.png', True),
            sthelper.load_image('dice_1.png', True),
            sthelper.load_image('dice_2.png', True),
            sthelper.load_image('dice_3.png', True),
            sthelper.load_image('dice_4.png', True),
            sthelper.load_image('dice_5.png', True),
            sthelper.load_image('dice_6.png', True)
        ]
        self.current_dice_roll = 0
        self.current_dice_image = self.dice_images[self.current_dice_roll][0]
        self.rollDiceButtons = []
        self.dice_locked = False
        self.sound_roll_dice = sthelper.load_sound('roll-dice.wav')
        self.sound_roll_dice_length = sthelper.get_sound_duration(
            'roll-dice.wav')
        self.sound_roll_dice_timer = None
        self.sound_roll_dice.set_volume(0.5)

        # inventory
        self.image_tpoint, self.rect_image_tpoint = sthelper.load_image(
            'hourglass.png', True)
        self.image_dcrystal, self.rect_image_dcrystal = sthelper.load_image(
            'dream-crystal.png', True)
        self.tpoints = STARTING_TPOINTS
        self.dcrystals = STARTING_DCRYSTALS

        # position
        self.position_type = None

        # images
        self.image_goodnight, self.rect_image_goodnight = sthelper.load_image(
            'goodnight.png', True)
        self.image_hannibal, self.rect_image_goodnight = sthelper.load_image(
            'hannibal.png', True)
        self.image_eugene, self.rect_image_eugene = sthelper.load_image(
            'eugene.png', True)

        # sounds
        self.sound_dream_crystal = sthelper.load_sound('dream-crystal.wav')

        # telephone
        self.telephone_call = False
        self.telephoneButtons = []

        # kitchen
        self.kitchen_stop = False
        self.kitchenButtons = []

        # move back squares
        self.move_back = False
        self.moveBackButtons = []

        # risk
        self.take_risk = False
        self.takeRiskButtons = []

    def get_event(self, event, screen):
        for menuButton in self.menuButtons:
            button_events = menuButton.handleEvent(event)
            if 'click' in button_events:
                if menuButton._propGetId() == 'menu':
                    self.done = True
                    self.target = 'menu'
                    sthelper.play_music('game-music.mp3', 'stop')
                    sthelper.play_music('menu-music.wav')
                    pg.mixer.music.pause()
                    pg.mixer.pause()
                if States.sound_on == True:
                    sthelper.play_sound(self.sound_button_click)
            super(Game, self).get_button_events(button_events)

        for rollDiceButton in self.rollDiceButtons:
            dice_events = rollDiceButton.handleEvent(event)
            if 'enter' in dice_events:
                if States.sound_on == True:
                    sthelper.play_sound(self.sound_button_hover)
            if 'click' in dice_events:
                if self.dice_locked == False:
                    if States.sound_on == True:
                        sthelper.play_sound(self.sound_roll_dice)
                    self.roll_dice()

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.done = True
                self.target = 'pause'
                # copy existing screen to States.screen_copy
                screen_rect = pg.Rect(
                    0, 0, screen.get_width(), screen.get_height())
                screen_copy = screen.subsurface(screen_rect)
                screen_copy = screen_copy.convert()
                States.screen_copy = screen_copy

        for kitchenButton in self.kitchenButtons:
            button_events = kitchenButton.handleEvent(event)
            if 'click' in button_events:
                if kitchenButton._propGetId() == 'forward':
                    self.update_player_position(4)
                    if States.sound_on == True:
                        sthelper.play_sound(self.sound_button_click)
                if kitchenButton._propGetId() == 'tpoints':
                    self.tpoints += 2
                    if States.sound_on == True:
                        sthelper.play_sound(self.sound_button_click)
                self.kitchen_stop = False
                self.dice_locked = False
                self.kitchenButtons = []
            super(Game, self).get_button_events(button_events)

        for moveBackButton in self.moveBackButtons:
            button_events = moveBackButton.handleEvent(event)
            if 'click' in button_events:
                button_id = moveBackButton._propGetId().rsplit(':', 1)
                if button_id[0] == 'back':
                    self.update_player_position(int(button_id[1]))
                if button_id[0] == 'dcrystals':
                    if self.dcrystals > 0:
                        self.dcrystals -= 1
                    if States.sound_on == True:
                        sthelper.play_sound(self.sound_dream_crystal)
                self.move_back = False
                self.dice_locked = False
                self.moveBackButtons = []
            super(Game, self).get_button_events(button_events)

        for takeRiskButton in self.takeRiskButtons:
            button_events = takeRiskButton.handleEvent(event)
            if 'click' in button_events:
                if takeRiskButton._propGetId() == 'bathroom':
                    self.update_player_position(-11)
                if takeRiskButton._propGetId() == 'risk':
                    sthelper.play_sound(self.sound_dream_crystal, 'stop')
                    if States.sound_on == True:
                        sthelper.play_sound(self.sound_button_click)
                self.take_risk = False
                self.dice_locked = False
                self.takeRiskButtons = []
            super(Game, self).get_button_events(button_events)

        for telephoneButton in self.telephoneButtons:
            button_events = telephoneButton.handleEvent(event)
            if 'click' in button_events:
                if telephoneButton._propGetId() == 'back':
                    self.update_player_position(-4)
                if telephoneButton._propGetId() == 'tpoints':
                    self.tpoints -= 2
                self.telephone_call = False
                self.dice_locked = False
                self.telephoneButtons = []
            super(Game, self).get_button_events(button_events)

        super(Game, self).get_sound_button_events(event)

    def cleanup(self):
        pass

    def startup(self):
        sthelper.play_music('menu-music.wav', 'stop')
        pg.mixer.unpause()

        if States.game_on == False:
            self.end = False
            self.tpoints = STARTING_TPOINTS
            self.dcrystals = STARTING_DCRYSTALS

            # create a bew board
            self.board = Board()
            self.squares = self.board.get_squares()
            self.square_width = self.board.get_square_width()
            self.square_height = self.board.get_square_height()

            # create a new player
            self.player = Player()
            self.player_image = self.player.get_player_image()
            self.current_position = self.player.get_player_position()
            self.current_position_coords = self.board.get_square_coords(
                self.current_position)
            self.next_position = self.current_position
            self.current_position_coords = self.board.get_square_coords(
                self.current_position)
            self.next_position_coords = self.current_position_coords

            # reset dice
            self.dice_locked = False
            self.sound_roll_dice_timer = None
            self.current_dice_roll = 0
            sthelper.play_sound(self.sound_roll_dice, 'stop')

            # reset message
            self.message = 'Roll the dice.'

        if self.end == True:
            sthelper.play_music('lullaby.wav')
        else:
            sthelper.play_music('game-music.mp3')

    def roll_dice(self):
        if States.game_on == False:
            States.game_on = True
        self.dice_locked = True
        self.sound_roll_dice_timer = 0
        self.current_dice_roll = random.randint(1, 6)

    def update_player_position(self, dice_roll):
        self.next_position = self.player.set_player_position(
            self.current_position + dice_roll)
        if self.next_position >= len(self.squares):
            self.end = True
            self.next_position = len(self.squares)
        self.current_position_coords = self.board.get_square_coords(
            self.current_position)
        self.next_position_coords = self.board.get_square_coords(
            self.next_position)
        self.current_position = self.next_position
        self.square_sound = self.board.get_square_sound(self.next_position)

        # unlock dice
        self.sound_roll_dice_timer = None
        self.dice_locked = False

        # play square sound
        if self.square_sound:
            sthelper.play_sound(self.square_sound)

        # get position feedback
        self.get_position_feedback()

        # decide if game is won or lost
        if self.end == True:
            States.music_on = True
            sthelper.play_music('lullaby.wav')
            if self.tpoints > 0:
                self.won_game = True
            else:
                self.won_game = False

    def get_position_feedback(self):
        self.position_type = self.squares[self.current_position]['type'].rsplit(
            ':', 1)

        # update message
        self.update_message()

        # update inventory
        self.update_inventory()

    def update_message(self):
        if self.position_type[0] == 'normal':
            self.message = 'Roll the dice again.'
        elif self.position_type[0] == 'tpoints':
            if int(self.position_type[1]) > 0:
                self.message = 'Yes! You gain ' + \
                    self.position_type[1] + \
                    ' Time Points. Roll the dice again.'
            else:
                self.message = 'Hannibal starts barking and you lose ' + \
                    self.position_type[1][1] + \
                    ' Time Points. Roll the dice again.'
        elif self.position_type[0] == 'dcrystals':
            self.message = 'You gain a Dream Crystal. Roll the dice again.'
        elif self.position_type[0] == 'bathroom':
            self.message = 'You stop at the bathroom and your Time Points are restored to 8. Roll the dice again.'
        elif self.position_type[0] == 'telephone':
            self.message = 'Eugene calls you and has a new task for you. You must either move 4 squares back or lose 2 Time Points.'
        elif self.position_type[0] == 'kitchen':
            self.message = 'You stop at the kitchen. You can move 4 squares forward or gain 2 Time Points.'
        elif self.position_type[0] == 'back':
            self.message = 'You have to move back ' + \
                str(abs(int(self.position_type[1]))) + \
                ' squares unless you have a Dream Crystal to use.'
        elif self.position_type[0] == 'risk':
            self.message = 'Your Time Points are reduced to 1. Will you risk to continue or go back to the bathroom to restore your Time Points?'

    def update_inventory(self):
        if self.position_type[0] == 'tpoints':
            self.tpoints += int(self.position_type[1])
        elif self.position_type[0] == 'dcrystals':
            self.dcrystals += int(self.position_type[1])
        elif self.position_type[0] == 'bathroom':
            self.tpoints = 8
        elif self.position_type[0] == 'telephone':
            self.telephone_call = True
            self.dice_locked = True
        elif self.position_type[0] == 'kitchen':
            self.kitchen_stop = True
            self.dice_locked = True
        elif self.position_type[0] == 'back':
            self.move_back = True
            self.dice_locked = True
        elif self.position_type[0] == 'risk':
            self.tpoints = 1
            self.take_risk = True
            self.dice_locked = True

        if self.tpoints <= 0:
            self.tpoints = 0
            self.end = True

    def update(self, screen, dt):
        self.draw(screen, dt)
        super(Game, self).update(screen)

    def draw(self, screen, dt):
        # fill a surface with a background color
        background = pg.Surface(screen.get_size())
        background = background.convert()
        background.fill(ST_WHITE)
        self.background = background

        # draw topbar box
        topbar = pg.Surface((screen.get_width()-TOOLBAR_WIDTH, TOPBAR_HEIGHT))
        topbar = topbar.convert()
        topbar.fill(ST_PINK)
        background.blit(topbar, (0, 0))

        # message box text
        if pg.font:
            font = pg.font.Font(None, 18)
            message_box_title = font.render('Message: ', 1, ST_BLACK100)
            background.blit(message_box_title, (20, int(
                TOPBAR_HEIGHT/2) - int(message_box_title.get_height()/2) + 2))

            if self.message:
                font = pg.font.Font(None, 24)
                self.message_text = font.render(self.message, 1, ST_DARKORANGE)
                background.blit(self.message_text, (100, int(
                    TOPBAR_HEIGHT/2) - int(message_box_title.get_height()/2)))

        # draw right toolbar box
        toolbar = pg.Surface((TOOLBAR_WIDTH, screen.get_height()))
        toolbar = toolbar.convert()
        toolbar.fill(ST_LIGHTERGRAY)
        background.blit(toolbar, (screen.get_width()-TOOLBAR_WIDTH, 0))

        # draw music controls background
        musicbox = pg.Surface((TOOLBAR_WIDTH, TOPBAR_HEIGHT))
        musicbox = musicbox.convert()
        musicbox.fill(ST_GRAY217)
        background.blit(musicbox, (screen.get_width()-TOOLBAR_WIDTH, 0))

        # add menu buttons in right toolbar
        menu_buttons = {
            "menu": "Main menu"
        }
        for i, (button_id, button_text) in enumerate(menu_buttons.items()):
            y_offset = (TOPBAR_HEIGHT+25) + i*(TOOLBAR_MENUBUTTON_HEIGHT+10)
            menuButton = pygbutton.PygButton((screen.get_width() - TOOLBAR_WIDTH/2 - TOOLBAR_MENUBUTTON_WIDTH/2, y_offset,
                                             TOOLBAR_MENUBUTTON_WIDTH, TOOLBAR_MENUBUTTON_HEIGHT), button_text, button_id, bgcolor=ST_LIGHTGRAY)
            menuButton.draw(background)
            if len(self.menuButtons) < len(menu_buttons):
                self.menuButtons.append(menuButton)

        # draw dice background
        dicebox = pg.Surface((TOOLBAR_WIDTH - 2*10, DICEBOX_HEIGHT))
        dicebox = dicebox.convert()
        dicebox.fill(ST_GRAY217)
        background.blit(dicebox, (screen.get_width()-(TOOLBAR_WIDTH-10),
                        TOPBAR_HEIGHT + 2*25 + TOOLBAR_MENUBUTTON_HEIGHT))

        # wait for dice roll to finish
        if self.dice_locked == True:
            if self.sound_roll_dice_timer != None:
                self.sound_roll_dice_timer += dt
                if self.sound_roll_dice_timer > self.sound_roll_dice_length:
                    # update current position
                    self.update_player_position(self.current_dice_roll)
            if self.kitchen_stop == True or self.move_back == True or self.take_risk == True or self.telephone_call == True:
                self.current_dice_image = self.dice_images[self.current_dice_roll][0]
            else:
                # blit random dice image
                random_dice_image = random.randint(1, 6)
                self.current_dice_image = self.dice_images[random_dice_image][0]
                current_image = self.current_dice_image
                self.current_dice_image = pg.transform.rotate(
                    current_image, 45)
        else:
            # blit current dice roll
            self.current_dice_image = self.dice_images[self.current_dice_roll][0]

        # draw dice image
        background.blit(self.current_dice_image, (screen.get_width() - int(TOOLBAR_WIDTH/2) - int(
            self.current_dice_image.get_width()/2), 230 - int(self.current_dice_image.get_height()/2)))

        # draw dice roll button
        if self.end == False:
            if self.dice_locked == False:
                rollDiceButton = pygbutton.PygButton((screen.get_width() - TOOLBAR_WIDTH/2 - ROLLBUTTON_WIDTH/2, 280, ROLLBUTTON_WIDTH,
                                                     ROLLBUTTON_HEIGHT), "ROLL DICE", 'roll-dice', bgcolor=ST_ORANGE, font=pg.font.Font(None, 24))
                rollDiceButton.draw(background)
                if len(self.rollDiceButtons) < 1:
                    self.rollDiceButtons.append(rollDiceButton)
            else:
                rollDiceButton = pygbutton.PygButton((screen.get_width() - TOOLBAR_WIDTH/2 - ROLLBUTTON_WIDTH/2, 280, ROLLBUTTON_WIDTH,
                                                     ROLLBUTTON_HEIGHT), "ROLLING...", 'rolling-dice', bgcolor=ST_LIGHTGRAY, font=pg.font.Font(None, 24))
                rollDiceButton.draw(background)
                self.rollDiceButtons = []
        else:
            rollDiceButton = pygbutton.PygButton((screen.get_width() - TOOLBAR_WIDTH/2 - ROLLBUTTON_WIDTH/2, 280, ROLLBUTTON_WIDTH,
                                                 ROLLBUTTON_HEIGHT), "GAME OVER", 'game-over', bgcolor=ST_LIGHTGRAY, font=pg.font.Font(None, 24))
            rollDiceButton.draw(background)
            self.rollDiceButtons = []

        # draw inventory
        if pg.font:
            # Title
            font = pg.font.Font(None, 22)
            inventorytitle = font.render('INVENTORY', 1, ST_BLACK60)
            inventorytitlepos = inventorytitle.get_rect(x=background.get_width(
            ) - int(TOOLBAR_WIDTH/2) - int(inventorytitle.get_width()/2), y=410)
            background.blit(
                inventorytitle, (inventorytitlepos.x, inventorytitlepos.y))

            # Time points
            tpointsbox = pg.Surface((int(TOOLBAR_WIDTH/2) - 15, 170))
            tpointsbox = tpointsbox.convert()
            tpointsbox.fill(ST_GRAY217)
            background.blit(
                tpointsbox, (screen.get_width() - (TOOLBAR_WIDTH - 10), 440))

            font = pg.font.Font(None, 18)
            tpointstitle = font.render('Time Points', 1, ST_BLACK100)
            tpointstitlepos = tpointstitle.get_rect(x=background.get_width(
            ) - int(TOOLBAR_WIDTH/2) - int(TOOLBAR_WIDTH/4) - int(tpointstitle.get_width()/2), y=455)
            background.blit(
                tpointstitle, (tpointstitlepos.x, tpointstitlepos.y))
            background.blit(self.image_tpoint, (background.get_width(
            ) - int(TOOLBAR_WIDTH/2) - int(TOOLBAR_WIDTH/4) - int(self.image_tpoint.get_width()/2), 490))

            font = pg.font.Font(None, 54)
            tpointscount = font.render(str(self.tpoints), 1, ST_BLACK60)
            tpointscountpos = tpointscount.get_rect(x=background.get_width(
            ) - int(TOOLBAR_WIDTH/2) - int(TOOLBAR_WIDTH/4) - int(tpointscount.get_width()/2), y=560)
            background.blit(
                tpointscount, (tpointscountpos.x, tpointscountpos.y))

            # Dream crystals
            dcrystalsbox = pg.Surface((int(TOOLBAR_WIDTH/2) - 15, 170))
            dcrystalsbox = dcrystalsbox.convert()
            dcrystalsbox.fill(ST_GRAY217)
            background.blit(dcrystalsbox, (screen.get_width() -
                            (int(TOOLBAR_WIDTH/2) - 5), 440))

            font = pg.font.Font(None, 18)
            dcrystalstitle = font.render('Dream Crystals', 1, ST_BLACK100)
            dcrystalstitlepos = dcrystalstitle.get_rect(x=background.get_width(
            ) - int(TOOLBAR_WIDTH/2) + int(TOOLBAR_WIDTH/4) - int(dcrystalstitle.get_width()/2), y=455)
            background.blit(
                dcrystalstitle, (dcrystalstitlepos.x, dcrystalstitlepos.y))
            background.blit(self.image_dcrystal, (background.get_width(
            ) - int(TOOLBAR_WIDTH/2) + int(TOOLBAR_WIDTH/4) - int(self.image_dcrystal.get_width()/2), 490))

            font = pg.font.Font(None, 54)
            dcrystalscount = font.render(str(self.dcrystals), 1, ST_BLACK60)
            dcrystalscountpos = dcrystalscount.get_rect(x=background.get_width(
            ) - int(TOOLBAR_WIDTH/2) + int(TOOLBAR_WIDTH/4) - int(dcrystalscount.get_width()/2), y=560)
            background.blit(
                dcrystalscount, (dcrystalscountpos.x, dcrystalscountpos.y))

        # add footer
        if pg.font:
            font = pg.font.Font(None, 16)
            footer = font.render('Sleeping Troubles v.' +
                                 ST_VERSION+' - '+ST_YEAR+'', 1, ST_BLACK40)
            footerpos = footer.get_rect(x=background.get_width(
            ) - int(TOOLBAR_WIDTH/2) - int(footer.get_width()/2), y=screen.get_height() - 30)
            background.blit(footer, (footerpos.x, footerpos.y))

        # draw board
        for key in self.squares:
            if self.squares[key]['coords'] and self.squares[key]['coords'] != []:
                square = pg.Surface(
                    (int(self.square_width), int(self.square_height)))
                square = square.convert()
                square.fill(self.squares[key]['bcolor'])
                # draw border
                pg.draw.rect(square, ST_GRAY120, (0, 0, int(
                    self.square_width), int(self.square_height)), 1)

                if pg.font and self.squares[key]['text'] != '' and not self.squares[key]['icon']:
                    font = pg.font.Font(None, 22)
                    description = font.render(
                        self.squares[key]['text'], 1, self.squares[key]['fcolor'])
                    square.blit(description, (int(square.get_width()/2) - int(description.get_width(
                    )/2), int(square.get_height()/2) - int(description.get_height()/2)))

                if self.squares[key]['icon']:
                    if self.squares[key]['text'] == '':
                        y_offset = square.get_height()/2 - \
                            self.squares[key]['icon'].get_height()/2
                    else:
                        y_offset = 10
                        if pg.font:
                            font = pg.font.Font(None, 18)
                            text = font.render(
                                self.squares[key]['text'], 1, self.squares[key]['fcolor'])
                            square.blit(
                                text, (int(square.get_width()/2) - int(text.get_width()/2), 55))
                    square.blit(self.squares[key]['icon'], (int(square.get_width(
                    )/2) - int(self.squares[key]['icon'].get_width()/2), int(y_offset)))

                background.blit(square, (int(self.squares[key]['coords'][0]), int(
                    TOPBAR_HEIGHT) + int(self.squares[key]['coords'][1])))

        # draw player
        background.blit(self.player_image, (int(self.next_position_coords[0]) + int(self.square_width/2) - int(self.player_image.get_width(
        )/2), TOPBAR_HEIGHT + int(self.next_position_coords[1]) + int(self.square_height/2) - int(self.player_image.get_height()/2)))

        # draw telephone popup
        if self.telephone_call == True:
            telephone_popup_bg = pg.Surface((POPUP_WIDTH, POPUP_HEIGHT))
            telephone_popup_bg = telephone_popup_bg.convert()
            telephone_popup_bg.fill(ST_YELLOW)
            pg.draw.rect(telephone_popup_bg, ST_BLACK,
                         (0, 0, POPUP_WIDTH - 1, POPUP_HEIGHT - 1), 2)
            background.blit(telephone_popup_bg, (int(screen.get_width()/2) - int(telephone_popup_bg.get_width()/2),
                            int(screen.get_height()/2) - int(telephone_popup_bg.get_height()/2)))
            telephone_popup = pg.Surface(
                (POPUP_WIDTH - 2*POPUP_PADDING, POPUP_HEIGHT - 2*POPUP_PADDING)).convert()
            telephone_popup.fill(ST_WHITE)
            background.blit(telephone_popup, (int(screen.get_width()/2) - int(telephone_popup.get_width()/2),
                            int(screen.get_height()/2) - int(telephone_popup.get_height()/2)))
            font = pg.font.Font(None, 38)
            telephone_title = font.render(
                'YOU HAVE A TELEPHONE CALL', 1, ST_PURPLE)
            background.blit(telephone_title, (screen.get_width(
            )/2 - telephone_title.get_width()/2, screen.get_height()/2 - 100))
            font = pg.font.Font(None, 24)
            telephone_text = font.render(
                'Eugene calls you and has a new task for you.', 1, ST_PURPLE)
            background.blit(telephone_text, (screen.get_width(
            )/2 - telephone_text.get_width()/2, screen.get_height()/2 - 50))

            telephone_buttons = {
                "back": "Move 4 squares back",
                "tpoints": "Lose 2 Time Points"
            }
            for i, (button_id, button_text) in enumerate(telephone_buttons.items()):
                x_offset = screen.get_width()/2 - telephone_popup.get_width() / \
                    2 + 30 + i*POPUP_BUTTON_WIDTH + i*30
                telephoneButton = pygbutton.PygButton((x_offset, screen.get_height(
                )/2, POPUP_BUTTON_WIDTH, POPUP_BUTTON_HEIGHT), button_text, button_id, bgcolor=ST_PURPLE, fgcolor=ST_YELLOW)
                telephoneButton.draw(background)
                if len(self.telephoneButtons) < len(telephone_buttons):
                    self.telephoneButtons.append(telephoneButton)

        # draw kitchen popup
        if self.kitchen_stop == True:
            kitchen_popup_bg = pg.Surface((POPUP_WIDTH, POPUP_HEIGHT))
            kitchen_popup_bg = kitchen_popup_bg.convert()
            kitchen_popup_bg.fill(ST_ORANGE)
            pg.draw.rect(kitchen_popup_bg, ST_BLACK,
                         (0, 0, POPUP_WIDTH - 1, POPUP_HEIGHT - 1), 2)
            background.blit(kitchen_popup_bg, (screen.get_width(
            )/2 - kitchen_popup_bg.get_width()/2, screen.get_height()/2 - kitchen_popup_bg.get_height()/2))
            kitchen_popup = pg.Surface(
                (POPUP_WIDTH - 2*POPUP_PADDING, POPUP_HEIGHT - 2*POPUP_PADDING)).convert()
            kitchen_popup.fill(ST_WHITE)
            background.blit(kitchen_popup, (screen.get_width(
            )/2 - kitchen_popup.get_width()/2, screen.get_height()/2 - kitchen_popup.get_height()/2))
            font = pg.font.Font(None, 44)
            kitchen_title = font.render('KITCHEN STOP', 1, ST_DARKORANGE)
            background.blit(kitchen_title, (screen.get_width(
            )/2 - kitchen_title.get_width()/2, screen.get_height()/2 - 100))
            font = pg.font.Font(None, 24)
            kitchen_text = font.render('Select a Bonus', 1, ST_DARKORANGE)
            background.blit(kitchen_text, (screen.get_width(
            )/2 - kitchen_text.get_width()/2, screen.get_height()/2 - 50))

            kitchen_buttons = {
                "forward": "Move 4 squares forward",
                "tpoints": "Gain 2 Time Points"
            }
            for i, (button_id, button_text) in enumerate(kitchen_buttons.items()):
                x_offset = screen.get_width()/2 - kitchen_popup.get_width() / \
                    2 + 30 + i*POPUP_BUTTON_WIDTH + i*30
                kitchenButton = pygbutton.PygButton((x_offset, screen.get_height(
                )/2, POPUP_BUTTON_WIDTH, POPUP_BUTTON_HEIGHT), button_text, button_id, bgcolor=ST_ORANGE)
                kitchenButton.draw(background)
                if len(self.kitchenButtons) < len(kitchen_buttons):
                    self.kitchenButtons.append(kitchenButton)

        # draw move-back popup
        if self.move_back == True:
            move_back_popup_bg = pg.Surface((POPUP_WIDTH, POPUP_HEIGHT))
            move_back_popup_bg = move_back_popup_bg.convert()
            move_back_popup_bg.fill(ST_RED)
            pg.draw.rect(move_back_popup_bg, ST_BLACK,
                         (0, 0, POPUP_WIDTH - 1, POPUP_HEIGHT - 1), 2)
            background.blit(move_back_popup_bg, (screen.get_width(
            )/2 - move_back_popup_bg.get_width()/2, screen.get_height()/2 - move_back_popup_bg.get_height()/2))
            move_back_popup = pg.Surface(
                (POPUP_WIDTH - 2*POPUP_PADDING, POPUP_HEIGHT - 2*POPUP_PADDING)).convert()
            move_back_popup.fill(ST_BLACK)
            background.blit(move_back_popup, (screen.get_width(
            )/2 - move_back_popup.get_width()/2, screen.get_height()/2 - move_back_popup.get_height()/2))
            font = pg.font.Font(None, 30)
            if self.position_type[1] == '-6':
                move_back_title = font.render(
                    'WEIRD NOISES COMING FROM THE ATTIC', 1, ST_DARKORANGE)
            elif self.position_type[1] == '-7':
                move_back_title = font.render(
                    'YOU FORGOT TO TAKE YOUR VALERIAN PILL', 1, ST_DARKORANGE)
            background.blit(move_back_title, (screen.get_width(
            )/2 - move_back_title.get_width()/2, screen.get_height()/2 - 100))
            font = pg.font.Font(None, 22)

            if self.dcrystals > 0:
                move_back_text = font.render(
                    'If you have a Dream Crystal you can avoid going back', 1, ST_WHITE)

                move_back_buttons = {
                    "back:"+self.position_type[1]: "Move " + str(abs(int(self.position_type[1]))) + " squares back",
                    "dcrystals": "Use a Dream Crystal"
                }
            else:
                move_back_text = font.render(
                    "You don't have a Dream Crystal. You must go back", 1, ST_WHITE)

                move_back_buttons = {
                    "back:"+self.position_type[1]: "Move " + str(abs(int(self.position_type[1]))) + " squares back"
                }

            background.blit(move_back_text, (screen.get_width(
            )/2 - move_back_text.get_width()/2, screen.get_height()/2 - 50))

            for i, (button_id, button_text) in enumerate(move_back_buttons.items()):
                x_offset = screen.get_width()/2 - move_back_popup.get_width() / \
                    2 + 30 + i*POPUP_BUTTON_WIDTH + i*30
                moveBackButton = pygbutton.PygButton((x_offset, screen.get_height(
                )/2, POPUP_BUTTON_WIDTH, POPUP_BUTTON_HEIGHT), button_text, button_id, bgcolor=ST_LIGHTGRAY, fgcolor=ST_BLACK)
                moveBackButton.draw(background)
                if len(self.moveBackButtons) < len(move_back_buttons):
                    self.moveBackButtons.append(moveBackButton)

        # draw risk popup
        if self.take_risk == True:
            take_risk_popup_bg = pg.Surface((POPUP_WIDTH, POPUP_HEIGHT))
            take_risk_popup_bg = take_risk_popup_bg.convert()
            take_risk_popup_bg.fill(ST_YELLOW)
            pg.draw.rect(take_risk_popup_bg, ST_BLACK,
                         (0, 0, POPUP_WIDTH - 1, POPUP_HEIGHT - 1), 2)
            background.blit(take_risk_popup_bg, (screen.get_width(
            )/2 - take_risk_popup_bg.get_width()/2, screen.get_height()/2 - take_risk_popup_bg.get_height()/2))
            take_risk_popup = pg.Surface(
                (POPUP_WIDTH - 2*POPUP_PADDING, POPUP_HEIGHT - 2*POPUP_PADDING)).convert()
            take_risk_popup.fill(ST_RED)
            background.blit(take_risk_popup, (screen.get_width(
            )/2 - take_risk_popup.get_width()/2, screen.get_height()/2 - take_risk_popup.get_height()/2))
            font = pg.font.Font(None, 32)
            take_risk_title = font.render(
                'YOUR TIME POINTS ARE REDUCED TO 1', 1, ST_YELLOW)
            background.blit(take_risk_title, (screen.get_width(
            )/2 - take_risk_title.get_width()/2, screen.get_height()/2 - 100))
            font = pg.font.Font(None, 24)
            take_risk_text = font.render(
                'Will you risk to continue or go back?', 1, ST_YELLOW)
            background.blit(take_risk_text, (screen.get_width(
            )/2 - take_risk_text.get_width()/2, screen.get_height()/2 - 50))

            take_risk_buttons = {
                "bathroom": "Go back to the Bathroom",
                            "risk": "Take the risk"
            }
            for i, (button_id, button_text) in enumerate(take_risk_buttons.items()):
                x_offset = screen.get_width()/2 - take_risk_popup.get_width() / \
                    2 + 30 + i*POPUP_BUTTON_WIDTH + i*30
                takeRiskButton = pygbutton.PygButton((x_offset, screen.get_height(
                )/2, POPUP_BUTTON_WIDTH, POPUP_BUTTON_HEIGHT), button_text, button_id, bgcolor=ST_BLACK, fgcolor=ST_YELLOW)
                takeRiskButton.draw(background)
                if len(self.takeRiskButtons) < len(take_risk_buttons):
                    self.takeRiskButtons.append(takeRiskButton)

        # draw end popup
        if self.end == True:
            end_popup_bg = pg.Surface((POPUP_WIDTH, POPUP_HEIGHT))
            end_popup_bg = end_popup_bg.convert()
            if self.won_game == True:
                end_popup_bg.fill(ST_GREEN)
                pg.draw.rect(end_popup_bg, ST_BLACK,
                             (0, 0, POPUP_WIDTH - 1, POPUP_HEIGHT - 1), 2)
                background.blit(end_popup_bg, (screen.get_width(
                )/2 - end_popup_bg.get_width()/2, screen.get_height()/2 - end_popup_bg.get_height()/2))
                end_popup = pg.Surface(
                    (POPUP_WIDTH - 2*POPUP_PADDING, POPUP_HEIGHT - 2*POPUP_PADDING)).convert()
                end_popup.fill(ST_WHITE)
                background.blit(end_popup, (screen.get_width(
                )/2 - end_popup.get_width()/2, screen.get_height()/2 - end_popup.get_height()/2))
                background.blit(self.image_goodnight, (screen.get_width(
                )/2 - self.image_goodnight.get_width()/2, screen.get_height()/2 - self.image_goodnight.get_height()/2))
            elif self.won_game == False:
                end_popup_bg.fill(ST_RED)
                pg.draw.rect(end_popup_bg, ST_BLACK,
                             (0, 0, POPUP_WIDTH - 1, POPUP_HEIGHT - 1), 2)
                background.blit(end_popup_bg, (screen.get_width(
                )/2 - end_popup_bg.get_width()/2, screen.get_height()/2 - end_popup_bg.get_height()/2))
                end_popup = pg.Surface(
                    (POPUP_WIDTH - 2*POPUP_PADDING, POPUP_HEIGHT - 2*POPUP_PADDING)).convert()
                end_popup.fill(ST_WHITE)
                background.blit(end_popup, (screen.get_width(
                )/2 - end_popup.get_width()/2, screen.get_height()/2 - end_popup.get_height()/2))
                background.blit(self.image_hannibal, (screen.get_width(
                )/2 - self.image_hannibal.get_width()/2, screen.get_height()/2 + 30))
                font = pg.font.Font(None, 44)
                end_title = font.render('GAME OVER', 1, ST_RED)
                background.blit(end_title, (screen.get_width(
                )/2 - end_title.get_width()/2, screen.get_height()/2 - 100))
                font = pg.font.Font(None, 24)
                end_text = font.render(
                    'You lost all your Time Points.', 1, ST_RED)
                end_text_2 = font.render(
                    'Eugene and Hannibal kept you up all night.', 1, ST_RED)
                background.blit(end_text, (screen.get_width(
                )/2 - end_text.get_width()/2, screen.get_height()/2 - 50))
                background.blit(end_text_2, (screen.get_width(
                )/2 - end_text_2.get_width()/2, screen.get_height()/2 - 22))

        super(Game, self).draw(screen, background)


class Pause(States):
    def __init__(self):
        States.__init__(self)

    def get_event(self, event, screen):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.done = True
                self.target = 'game'

    def cleanup(self):
        States.screen_copy = None

    def startup(self):
        pg.mixer.music.pause()
        pg.mixer.pause()

    def update(self, screen, dt):
        self.draw(screen)

    def draw(self, screen):
        # draw a transparent surface over the current screen
        current_screen = States.screen_copy
        mask = pg.Surface(screen.get_size())
        mask.fill(ST_GRAY120)
        mask.set_alpha(220)
        screen.blit(current_screen, (0, 0))
        screen.blit(mask, (0, 0))

        if pg.font:
            font = pg.font.Font(None, 36)
            pausetext = font.render('GAME IS PAUSED', 1, ST_WHITE)
            pausetextpos = pausetext.get_rect(centerx=screen.get_width(
            )/2, y=screen.get_height()/2 - 2 * pausetext.get_height())
            screen.blit(pausetext, (pausetextpos.x, pausetextpos.y))

            font = pg.font.Font(None, 26)
            pausesubtext = font.render(
                "Press 'Esc' key to resume game", 1, ST_WHITE)
            pausesubtextpos = pausesubtext.get_rect(
                centerx=screen.get_width()/2, y=screen.get_height()/2)
            screen.blit(pausesubtext, (pausesubtextpos.x, pausesubtextpos.y))


class Help(States):
    def __init__(self):
        States.__init__(self)
        self.hannibal_image, self.rect_hannibal_image = sthelper.load_image(
            'hannibal.png', True)

    def get_event(self, event, screen):
        for menuButton in self.menuButtons:
            button_events = menuButton.handleEvent(event)
            if 'click' in button_events:
                if menuButton._propGetId() == 'menu':
                    self.done = True
                    self.target = 'menu'
                if States.sound_on == True:
                    sthelper.play_sound(self.sound_button_click)
            super(Help, self).get_button_events(button_events)

        super(Help, self).get_sound_button_events(event)

    def cleanup(self):
        pass

    def startup(self):
        pass

    def update(self, screen, dt):
        self.draw(screen)

        super(Help, self).update(screen)

    def draw(self, screen):
        # fill a surface with a background color
        background = pg.Surface(screen.get_size())
        background = background.convert()
        background.fill(ST_WHITE)

        # draw topbar box
        topbar = pg.Surface((screen.get_width()-TOOLBAR_WIDTH, TOPBAR_HEIGHT))
        topbar = topbar.convert()
        topbar.fill(ST_PINK)
        background.blit(topbar, (0, 0))

        # draw right toolbar box
        toolbar = pg.Surface((TOOLBAR_WIDTH, screen.get_height()))
        toolbar = toolbar.convert()
        toolbar.fill(ST_LIGHTERGRAY)
        background.blit(toolbar, (screen.get_width()-TOOLBAR_WIDTH, 0))

        # draw music controls background
        musicbox = pg.Surface((TOOLBAR_WIDTH, TOPBAR_HEIGHT))
        musicbox = musicbox.convert()
        musicbox.fill(ST_GRAY217)
        background.blit(musicbox, (screen.get_width()-TOOLBAR_WIDTH, 0))

        # add menu buttons
        menu_buttons = {
            "menu": "Main menu",
        }
        for i, (button_id, button_text) in enumerate(menu_buttons.items()):
            y_offset = (TOPBAR_HEIGHT+25) + i*(TOOLBAR_MENUBUTTON_HEIGHT+10)
            menuButton = pygbutton.PygButton((screen.get_width() - TOOLBAR_WIDTH/2 - TOOLBAR_MENUBUTTON_WIDTH/2, y_offset,
                                             TOOLBAR_MENUBUTTON_WIDTH, TOOLBAR_MENUBUTTON_HEIGHT), button_text, button_id, bgcolor=ST_LIGHTGRAY)
            menuButton.draw(background)
            if len(self.menuButtons) < len(menu_buttons):
                self.menuButtons.append(menuButton)

        # draw Hannibal image
        background.blit(self.hannibal_image, (screen.get_width(
        ) - TOOLBAR_WIDTH/2 - self.hannibal_image.get_width()/2, screen.get_height() - 180))

        if pg.font:
            # add title
            font = pg.font.Font(None, 36)
            title = font.render("Help", 1, ST_BLACK)
            background.blit(
                title, (50, TOPBAR_HEIGHT/2 - title.get_height()/2))

            # add help text
            help_list = [
                "Nick experiences a short adventure of sleeping trouble and your goal is to help him reach his bed",
                "so that he can finally sleep peacefully.",
                "",
                "The game is played with 1 dice and Nick starts with 8 Time Points and 1 Dream Crystal at his disposal.",
                "Nick has to reach his bed before losing all his Time Points.",
                ""
            ]
            for i, line in enumerate(help_list):
                font = pg.font.Font(None, 24)
                y_offset = 110 + i*37
                text = font.render(line, 1, ST_BLACK)
                textpos = text.get_rect(x=50, y=y_offset)
                background.blit(text, (textpos.x, textpos.y))

            # draw color squares
            color_squares = {
                "red": ["Red squares", ST_RED, "Nick loses Time Points.", ST_WHITE],
                "green": ["Green squares", ST_GREEN, "Nick gains Time Points.", ST_BLACK],
                "blue": ["Blue squares", ST_BLUE, "Nick gains 1 Dream Crystal that he can use on a Black Square to avoid going backwards.", ST_BLACK],
                "black": ["Black squares", ST_BLACK, "Nick has to go backwards, unless he has a Dream Crystal.", ST_WHITE],
                "yellow": ["Yellow squares", ST_YELLOW, "Eugene calls Nick and has a new task for him. Nick must either move 4 squares back or lose 2 Time Points.", ST_BLACK],
                "kitchen": ["Kitchen stop", ST_ORANGE, "Nick moves 4 Squares forward or gains 2 Time Points.", ST_BLACK],
                "bathroom": ["Bathroom stop", ST_ORANGE, "Nick's Time Points are restored to 8.", ST_BLACK]
            }
            for i, square in enumerate(color_squares):
                colorSquare = pygbutton.PygButton(
                    (50, 330+i*42, 140, 32), color_squares[square][0], bgcolor=color_squares[square][1], fgcolor=color_squares[square][3])
                colorSquare.draw(background)
                font = pg.font.Font(None, 24)
                y_offset = 339+i*42
                text = font.render(color_squares[square][2], 1, ST_BLACK)
                textpos = text.get_rect(x=200, y=y_offset)
                background.blit(text, (textpos.x, textpos.y))

            # add footer
            font = pg.font.Font(None, 16)
            footer = font.render('Sleeping Troubles v.' +
                                 ST_VERSION+' - '+ST_YEAR+'', 1, ST_BLACK40)
            footerpos = footer.get_rect(x=background.get_width(
            ) - TOOLBAR_WIDTH/2 - footer.get_width()/2, y=screen.get_height() - 30)
            background.blit(footer, (footerpos.x, footerpos.y))

        super(Help, self).draw(screen, background)


class Credits(States):
    def __init__(self):
        States.__init__(self)
        self.rascal_image, self.rect_rascal_image = sthelper.load_image(
            'rascal.png', True)

    def get_event(self, event, screen):
        for menuButton in self.menuButtons:
            button_events = menuButton.handleEvent(event)
            if 'click' in button_events:
                if menuButton._propGetId() == 'menu':
                    self.done = True
                    self.target = 'menu'
                if States.sound_on == True:
                    sthelper.play_sound(self.sound_button_click)
            super(Credits, self).get_button_events(button_events)

        super(Credits, self).get_sound_button_events(event)

    def cleanup(self):
        pass

    def startup(self):
        pass

    def update(self, screen, dt):
        self.draw(screen)

        super(Credits, self).update(screen)

    def draw(self, screen):
        # fill a surface with a background color
        background = pg.Surface(screen.get_size())
        background = background.convert()
        background.fill(ST_WHITE)

        # draw topbar box
        topbar = pg.Surface((screen.get_width()-TOOLBAR_WIDTH, TOPBAR_HEIGHT))
        topbar = topbar.convert()
        topbar.fill(ST_PINK)
        background.blit(topbar, (0, 0))

        # draw right toolbar box
        toolbar = pg.Surface((TOOLBAR_WIDTH, screen.get_height()))
        toolbar = toolbar.convert()
        toolbar.fill(ST_LIGHTERGRAY)
        background.blit(toolbar, (screen.get_width()-TOOLBAR_WIDTH, 0))

        # draw music controls background
        musicbox = pg.Surface((TOOLBAR_WIDTH, TOPBAR_HEIGHT))
        musicbox = musicbox.convert()
        musicbox.fill(ST_GRAY217)
        background.blit(musicbox, (screen.get_width()-TOOLBAR_WIDTH, 0))

        # draw Rascal image
        background.blit(self.rascal_image, (screen.get_width(
        ) - TOOLBAR_WIDTH/2 - self.rascal_image.get_width()/2, screen.get_height() - 180))

        # add menu buttons
        menu_buttons = {
            "menu": "Main menu",
        }
        for i, (button_id, button_text) in enumerate(menu_buttons.items()):
            y_offset = (TOPBAR_HEIGHT+25) + i*(TOOLBAR_MENUBUTTON_HEIGHT+10)
            menuButton = pygbutton.PygButton((screen.get_width() - TOOLBAR_WIDTH/2 - TOOLBAR_MENUBUTTON_WIDTH/2, y_offset,
                                             TOOLBAR_MENUBUTTON_WIDTH, TOOLBAR_MENUBUTTON_HEIGHT), button_text, button_id, bgcolor=ST_LIGHTGRAY)
            menuButton.draw(background)
            if len(self.menuButtons) < len(menu_buttons):
                self.menuButtons.append(menuButton)

        if pg.font:
            # add title
            font = pg.font.Font(None, 36)
            title = font.render("Credits", 1, ST_BLACK)
            background.blit(
                title, (50, TOPBAR_HEIGHT/2 - title.get_height()/2))

            # add text
            credits_list = [
                "Sleeping Troubles by Pulsar Bytes",
                "Game concept and design by Evi Filakouri",
                "Developed by Yannis Maragos",
                "Developed with Python and Pygame",
                "Released under the terms of the GNU General Public License"
            ]
            for i, line in enumerate(credits_list):
                font = pg.font.Font(None, 24)
                y_offset = 110 + i*37
                text = font.render(line, 1, ST_BLACK)
                textpos = text.get_rect(x=50, y=y_offset)
                background.blit(text, (textpos.x, textpos.y))

            # add footer
            font = pg.font.Font(None, 16)
            footer = font.render('Sleeping Troubles v.' +
                                 ST_VERSION+' - '+ST_YEAR+'', 1, ST_BLACK40)
            footerpos = footer.get_rect(x=background.get_width(
            ) - TOOLBAR_WIDTH/2 - footer.get_width()/2, y=screen.get_height() - 30)
            background.blit(footer, (footerpos.x, footerpos.y))

        super(Credits, self).draw(screen, background)


class Control:
    """
    Controls the entire program.
    Switches between states.
    Contains:
        - current state
        - main game loop
        - main event loop
        - main update
        - main change state
    """

    def __init__(self, **settings):
        self.__dict__.update(settings)
        self.done = False
        # set window icon
        self.window_icon = sthelper.load_window_icon('window_icon.png', -1)
        pg.display.set_icon(self.window_icon)
        # create display surface
        self.screen = pg.display.set_mode(self.size)
        # set window title
        pg.display.set_caption('Sleeping Troubles')
        self.clock = pg.time.Clock()

    def setup_states(self, state_dict, start_state):
        self.state_dict = state_dict
        self.state_name = start_state
        self.state = self.state_dict[self.state_name]

    def change_state(self):
        self.state.done = False  # reset current state otherwise it remains done forever
        self.state_name = self.state.target
        self.state.cleanup()
        self.state = self.state_dict[self.state_name]  # set new state
        self.state.startup()

    def update(self, dt):
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.change_state()
        self.state.update(self.screen, dt)

    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            self.state.get_event(event, self.screen)

    def main_game_loop(self):
        while not self.done:
            delta_time = self.clock.tick(
                self.fps)/1000.0  # time between frames
            self.event_loop()
            self.update(delta_time)
            dirty_rects = self.state.dirty_rects
            if dirty_rects != []:
                pg.display.update(dirty_rects)
            else:
                pg.display.update()


def run_game():

    # create dictionary of control settings
    settings = {
        'size': (ST_SCREEN_WIDTH, ST_SCREEN_HEIGHT),
        'fps': ST_FPS
    }

    # start control
    app = Control(**settings)

    # setup dictionary of states, so that we can reference objects when setting states
    state_dict = {
        'menu': Menu(),
        'credits': Credits(),
        'game': Game(),
        'help': Help(),
        'pause': Pause()
    }
    # set initial state (menu)
    app.setup_states(state_dict, 'menu')

    # start main game loop
    app.main_game_loop()

    # exit
    pg.quit()
    sys.exit()


if __name__ == '__main__':

    pg.mixer.pre_init(44100, 16, 2, 512)
    pg.mixer.init()
    pg.init()

    # center pygame window on screen
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    # get path for data folder
    if getattr(sys, 'frozen', False):
        # frozen
        main_dir = os.path.split(os.path.abspath(sys.executable))[0]
    else:
        # unfrozen
        main_dir = os.path.split(os.path.abspath(__file__))[0]
    data_dir = os.path.join(main_dir, 'data')

    # constants
    ST_SCREEN_WIDTH = 1300
    ST_SCREEN_HEIGHT = 740
    ST_FPS = 20
    ST_VERSION = '0.1.2'
    ST_YEAR = '2018'

    # dimensions and sizes
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

    # game
    STARTING_TPOINTS = 8
    STARTING_DCRYSTALS = 1

    # colors
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

    run_game()

# Dirty Rects
    """
    - Blit a piece of the background over the sprite's current location, erasing it.
        # Example 1
        area_to_copy = original_surface.get_rect(x=0,y=0,width=100,height=100)
        destination_area = (0,500, 1300, 100)
        target_surface.blit(original_surface, destination_area, area_to_copy)
        # Example 2
        area_to_copy = original_surface.subsurface((1200,0,100,100)).convert()
        destination_area = (0,300)
        target_surface.blit(area_to_copy, destination_area)
    - Append the sprite's current location rectangle ((top,left,width,height)) to a list called dirty_rects.
    - Move the sprite and Draw it at it's new location.
    - Append the sprite's new location ((top,left,width,height)) to the dirty_rects list.
    - Call display.update(dirty_rects)
    """
