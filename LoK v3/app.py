import pygame
from pygame.locals import *
import config as cfg
import sys
from interactable import Interactable
from observer import Observer

class App():

    # main app

    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Legend of Kira')

        self.DISPLAY_SURF = pygame.display.set_mode((cfg.WINDOW_WIDTH, cfg.WINDOW_HEIGHT))
        self.BASIC_FONT = pygame.font.Font('freesansbold.ttf', cfg.BASIC_FONT_SIZE)
        self.FPS_CLOCK = pygame.time.Clock()
        self.observer = Observer()

    def update(self):
        self.DISPLAY_SURF.fill(cfg.BG_COLOR)
        event_list = []
        for event in pygame.event.get():
            print(event)
            event_list.append(event)
        for obj_list in self.observer.active_objs.values():
            for obj in obj_list:
                obj.blit(self.DISPLAY_SURF)
                if issubclass(type(obj), Interactable):
                    for event in event_list:
                        self.terminate_check(event)
                        obj.event(event, self.observer)
        self.observer.active_objs["temp"] = []
        pygame.display.update()
        self.FPS_CLOCK.tick(cfg.FPS)


    def terminate_check(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()