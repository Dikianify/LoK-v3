import pip
import pygame
import os

def install(package):
    if hasattr(pip, 'main'):
        pip.main(['install', package])
    else:
        pip._internal.main(['install', package])


GAMEFILE = "LoK text.xlsx"

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
FPS = 30

# R G B
BLACK = ( 0, 0, 0)
LIGHT_BLACK = (0, 0, 0, 100)
WHITE = (255, 255, 255)
PURPLE = (129, 73, 171)
LIGHT_PURPLE = (183, 136, 219, 100)

BG_COLOR = BLACK
BASIC_FONT_SIZE = 20

BOX_COLOR = PURPLE
TEXT_BOX_COLOR = LIGHT_PURPLE
TEXT_COLOR = WHITE
BASIC_FONT_SIZE = 20
SCROLL_SPEED = 1

BUTTON_COLOR = WHITE


# Item Parameters

# backpack
BP_WIDTH = round(WINDOW_WIDTH / 12)
BP_HEIGHT= round(round(BP_WIDTH) * 1.5)
BP_MARGIN = int(WINDOW_HEIGHT/ 24)
BP_X = WINDOW_WIDTH - BP_WIDTH - BP_MARGIN
BP_Y = BP_MARGIN
BP_COORDS = (BP_X, BP_Y, BP_WIDTH, BP_HEIGHT)
BPSTATE = "closed"

# ribbon
RIBBON_HEIGHT = int(BP_HEIGHT - BP_HEIGHT / 3)
RIBBON_SPEED = 3
RIBBON_START_X = int(BP_X + BP_WIDTH * 0.3)
RIBBON_CENTER = int(BP_Y + BP_HEIGHT / 2)
RIBBON_Y = int(RIBBON_CENTER - RIBBON_HEIGHT / 2)


# items on ribbon

RIBBON_ITEM = ['mask', 'skateboard', 'curse', 'blessing', 'juice', 'bone', 'check']
ITEM_HEIGHT = int(RIBBON_HEIGHT - RIBBON_HEIGHT / 3)

# settings
SETTINGS_GEAR_DIMENSION = int(WINDOW_WIDTH / 24)
SETTINGS_GEAR_X = int(WINDOW_WIDTH / 24)
SETTINGS_GEAR_Y = int(WINDOW_WIDTH / 24)

SETTINGS_MENU_HEIGHT = int(WINDOW_HEIGHT * .8)

# Continue Button Parameters

CONTINUE_WIDTH = BP_HEIGHT
CONTINUE_HEIGHT = int(BP_WIDTH/ 2)
CONTINUE_BOX = (0, 0, CONTINUE_WIDTH, CONTINUE_HEIGHT)
CONTINUE_BOX_RECT = pygame.Rect(CONTINUE_BOX)
CONTINUE_BOX_CENTER = (round(WINDOW_WIDTH - (WINDOW_WIDTH / 8)), round(WINDOW_HEIGHT - (WINDOW_HEIGHT / 5)))
CONTINUE_BOX_RECT.center = CONTINUE_BOX_CENTER
CONTINUE_BOX_X, CONTINUE_BOX_Y = CONTINUE_BOX_RECT.topleft
CONTINUE_BOX = (CONTINUE_BOX_X, CONTINUE_BOX_Y, CONTINUE_WIDTH, CONTINUE_HEIGHT)
BUTTON_MARGIN = WINDOW_WIDTH - CONTINUE_BOX_RECT.right

LEFT_MARGIN = WINDOW_WIDTH - (CONTINUE_BOX_RECT.width + BUTTON_MARGIN * 3)
DEFAULT_TEXT_BOX = (0, 0, WINDOW_WIDTH - (CONTINUE_BOX_RECT.width + BUTTON_MARGIN * 3), int(WINDOW_HEIGHT / 3))

DEFAULT_TEXT_BOX_TEXT_MARGINS = (DEFAULT_TEXT_BOX[2] / 1.015, DEFAULT_TEXT_BOX[3] / 1.02, DEFAULT_TEXT_BOX[2] / 1.01, DEFAULT_TEXT_BOX[3] / 1.015)

# Buttons

BUTTON_BASE_HEIGHT = round(WINDOW_HEIGHT / 6)
BUTTON_Y = round(WINDOW_HEIGHT - ((WINDOW_HEIGHT / 12) + BUTTON_BASE_HEIGHT))

LAST_TEXT_BOX = (round((WINDOW_WIDTH - round(WINDOW_WIDTH / 1.5)) / 2), round(BUTTON_Y - (WINDOW_HEIGHT - BUTTON_Y)), round(WINDOW_WIDTH / 1.5), BUTTON_BASE_HEIGHT)