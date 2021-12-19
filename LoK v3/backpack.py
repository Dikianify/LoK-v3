from interactable import Interactable
from imageProcessor import ImageProcessor
from textProcessor import TextProcessor
import config as cfg
import pygame as pg

class Backpack(Interactable):
    def __init__(self, coords, inventory):
        super().__init__(pg.Rect(coords), self.on_press)
        self.state = "closed"
        self.inventory = inventory
        self.bp_img = ImageProcessor("backpack", h=cfg.BP_HEIGHT, x=cfg.BP_X, y=cfg.BP_Y)
        self.ribbon = Ribbon(self)
        self.items = [RibbonItem(item, ImageProcessor(item)) for item in cfg.RIBBON_ITEM]

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
                if self.ribbon.pieces[0].piece.x >= cfg.RIBBON_START_X:
                    self.state = "closed"
                    return
                for ribbon_piece in self.ribbon.pieces:
                    ribbon_piece.piece.x += cfg.RIBBON_SPEED
                    if ribbon_piece.piece.x > cfg.RIBBON_START_X and ribbon_piece in self.ribbon.active_pieces:
                        self.ribbon.active_pieces.remove(ribbon_piece)  
            case "openned":
                if self.ribbon.pieces[0].piece.x > self.ribbon.min_x:
                    for ribbon_piece in self.ribbon.pieces:
                        ribbon_piece.piece.x -= cfg.RIBBON_SPEED
                        if ribbon_piece.piece.x > cfg.RIBBON_START_X and ribbon_piece not in self.ribbon.active_pieces:
                            self.ribbon.active_pieces.append(ribbon_piece)
                if self.ribbon.pieces[0].piece.x < self.ribbon.min_x:
                    for ribbon_piece in self.ribbon.pieces:
                        ribbon_piece.piece.x += cfg.RIBBON_SPEED
                        if ribbon_piece.piece.x > cfg.RIBBON_START_X and ribbon_piece in self.ribbon.active_pieces:
                            self.ribbon.active_pieces.remove(ribbon_piece)
            case "openning":
                if self.ribbon.pieces[0].piece.x <= self.ribbon.min_x:
                    self.state = "openned"
                    return
                for ribbon_piece in self.ribbon.pieces:
                    ribbon_piece.piece.x -= cfg.RIBBON_SPEED
                    if ribbon_piece.piece.x < cfg.RIBBON_START_X and ribbon_piece not in self.ribbon.active_pieces:
                        self.ribbon.active_pieces.append(ribbon_piece)

    def update_inventory(self):
        self.ribbon.unassign_pieces()
        self.ribbon.assign_pieces()

    def blit(self, target):
        for piece in self.ribbon.active_pieces:
            piece.blit(target)
        self.bp_img.blit(target)
        self.update_ribbon()

class Ribbon:
    def __init__(self, bp):
        self.bp = bp
        self.pieces = [RibbonPiece(ImageProcessor("ribbon1",h=cfg.RIBBON_HEIGHT,x=cfg.RIBBON_START_X,y=cfg.RIBBON_Y))]
        self.active_pieces = []
        for i in range(len(cfg.RIBBON_ITEM)):
            x = sum([ribbon.piece.w for ribbon in self.pieces]) + cfg.RIBBON_START_X
            if i % 2 == 0:
                self.pieces.append(RibbonPiece(ImageProcessor("ribbon3", h=cfg.RIBBON_HEIGHT, x=x, y=cfg.RIBBON_Y)))
            elif i % 2 == 1:
                self.pieces.append(RibbonPiece(ImageProcessor("ribbon2", h=cfg.RIBBON_HEIGHT, x=x, y=cfg.RIBBON_Y)))

    @property
    def min_x(self):
        # returns maximum x relative to the length of the inventory
        return cfg.RIBBON_START_X - sum([ribbon.piece.w for ribbon in self.pieces[:(len(self.bp.inventory)) + 1]])

    def assign_pieces(self):
        for index, item in enumerate(self.bp.inventory):
            self.pieces[index+1].assign_item(self.bp.items[item])

    def unassign_pieces(self):
        for i in range(len(self.pieces)):
            if i != len(self.pieces)-1:
                self.pieces[i+1].unassign_item()

class RibbonPiece:
    def __init__(self, piece):
        self.piece = piece
        self.item = None

    def assign_item(self, item):
        self.item = item
        self.center_item()

    def unassign_item(self):
        self.item = None

    def center_item(self):
        self.item.y = int(cfg.RIBBON_CENTER - self.item.item.h / 2)
        self.item.x = int(self.piece.x + (self.piece.w - self.item.item.w) / 2)

    def blit(self, source):
        self.piece.blit(source)
        if self.item != None:
            self.center_item()
            self.item.item_img.blit(source)

class RibbonItem(Interactable):
    def __init__(self, text, item):
        self.text = TextProcessor(text, "center", 100, 100, 0, 0, adjust=True, font_size=10, text_margin=0, box_color=cfg.BLACK, opacity = 100)
        self.item_img = item

    def __repr__(self):
        return self.text

    def event(self, event, observer):
        x, y = pg.mouse.get_pos()
        if self.item.rect.collidepoint((x,y)):
            self.text.rect.topleft = x, y
            observer.active_objs["temp"].append(self.text)