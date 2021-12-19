import pygame
import config as cfg
from displayObject import DisplayObject

class Interactable:
    def __init__(self, rect, func, trigger=[pygame.MOUSEBUTTONDOWN], args=None):
        self.obj_rect = rect
        self.func = func
        self.trigger = trigger
        self.args = args

    def event(self, event, observer):
        if event.type in self.trigger:
            try:
                if self.obj_rect.collidepoint(event.pos):
                    self.func(self.args)
            except:
                self.func(self.args)


class Button(Interactable):
    def __init__(self, text_obj, func, args=None):
        super().__init__(text_obj.obj_rect, func, args=args)
        self.text_obj = text_obj
        self.text_objs = text_obj.get_text_objects()

    def blit(self, target):
        self.text_obj.blit(target)


class TextBox(Interactable):
    def __init__(self, text_obj):
        self.text_obj = text_obj
        super().__init__(pygame.Rect(0, 0, cfg.WINDOW_WIDTH, cfg.WINDOW_HEIGHT), self.end_scroll, trigger=[pygame.MOUSEBUTTONDOWN, pygame.KEYUP])

    def blit(self, target):
        self.text_obj.blit(target)

    def end_scroll(self, arg):
        self.text_obj.scroll = False   