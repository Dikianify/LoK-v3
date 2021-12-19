from interactable import Interactable
from imageProcessor import ImageProcessor
from textProcessor import TextProcessor
import config as cfg
import pygame as pg

class Backpack(Interactable):
    def __init__(self, coords, inventory):
        super().__init__(pg.Rect(coords), self.on_press, trigger = [pg.MOUSEBUTTONDOWN, pg.K_b])
        self.state = "closed"
        self.bp_img = ImageProcessor("backpack", h=cfg.BP_HEIGHT, x=cfg.BP_X, y=cfg.BP_Y)
        self.ribbon = Ribbon(self)
        self.items = {item:RibbonItem(item, ImageProcessor(item, h=cfg.ITEM_HEIGHT)) for item in cfg.RIBBON_ITEM}
        self.inventory = inventory

    def on_press(self, arg):
        if self.state == "closed" or self.state == "closing":
            self.state = "openning"
        else:
            self.state = "closing"

    def update_ribbon(self):
        match self.state:
            case "closed":
                return
            case "closing":
                if self.ribbon.ribbon_img.x >= cfg.RIBBON_START_X:
                    self.state = "closed"
                    return
                self.ribbon.ribbon_img.x += cfg.RIBBON_SPEED
                for item in self.inventory:
                    item.item_img.x += cfg.RIBBON_SPEED
            case "openned":
                if self.ribbon.ribbon_img.x > self.ribbon.min_x:
                    self.ribbon.ribbon_img.x -= cfg.RIBBON_SPEED
                    for item in self.inventory:
                        item.item_img.x -= cfg.RIBBON_SPEED             
                if self.ribbon.ribbon_img.x < self.ribbon.min_x:
                    self.ribbon.ribbon_img.x += cfg.RIBBON_SPEED
                    for item in self.inventory:
                        item.item_img.x += cfg.RIBBON_SPEED
            case "openning":
                if self.ribbon.ribbon_img.x <= self.ribbon.min_x:
                    self.state = "openned"
                    return
                self.ribbon.ribbon_img.x -= cfg.RIBBON_SPEED
                for item in self.inventory:
                    item.item_img.x -= cfg.RIBBON_SPEED

    def update_inventory(self):
        self.ribbon.assign_pieces()

    def blit(self, target):
        if self.ribbon.ribbon_img.x <= cfg.RIBBON_START_X:
            self.ribbon.blit(target)
        active_items = []
        for item in self.inventory:
            if item.item_img.x < cfg.RIBBON_START_X:
                backpack_end_x = int((cfg.RIBBON_START_X + (self.bp_img.w-(cfg.RIBBON_START_X-self.bp_img.x))) * 0.95)
                if (item.item_img.x + item.item_img.w) > backpack_end_x:
                    width = backpack_end_x-item.item_img.x
                    subsurf = item.item_img.img.subsurface((0,0,width,item.item_img.h))
                    subsurf_rect = subsurf.get_rect()
                    subsurf_rect.x, subsurf_rect.y, = item.item_img.x, item.item_img.y
                    target.blit(subsurf, subsurf_rect)
                else:
                    item.item_img.blit(target)
                    active_items.append(item)
        self.bp_img.blit(target)
        [item.mouse_check(target) for item in active_items]
        self.update_ribbon()


class Ribbon:
    def __init__(self, bp):
        self.bp = bp
        self.ribbon_img = ImageProcessor("bigribbon",h=cfg.RIBBON_HEIGHT,x=cfg.RIBBON_START_X,y=cfg.RIBBON_Y)
        self.parts = self.ribbon_img.w / 10

    @property
    def min_x(self):
        # returns maximum x relative to the length of the inventory
        return cfg.RIBBON_START_X - (len(self.bp.inventory)+1) * self.parts
    
    def assign_pieces(self):
        for index, item in enumerate(self.bp.inventory):
            item.item_img.x = self.ribbon_img.x + (index) * self.parts + self.parts/2

    def blit(self, target):
        width = cfg.RIBBON_START_X - self.ribbon_img.x
        subsurf = self.ribbon_img.img.subsurface((0, 0, width, self.ribbon_img.h))
        subsurf_rect = pg.Rect(self.ribbon_img.x, self.ribbon_img.y, width, self.ribbon_img.h)
        target.blit(subsurf, subsurf_rect)


class RibbonItem:
    def __init__(self, text, item):
        self.raw_text = text
        self.text = TextProcessor(text, "center", 100, 100, 0, 0, adjust=True, font_size=12, text_margin=0, box_color=cfg.BLACK, opacity = 100)
        self.item_img = item
        self.item_img.y = int(cfg.RIBBON_CENTER - self.item_img.h / 2)

    def __repr__(self):
        return self.raw_text

    def mouse_check(self, target):
        x, y = pg.mouse.get_pos()
        if self.item_img.rect.collidepoint((x, y)):
            self.text.obj_rect.topleft = (x, y)
            self.text.blit(target)