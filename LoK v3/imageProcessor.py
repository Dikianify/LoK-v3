import pygame as pg
import os
import config as cfg
from displayObject import DisplayObject

class ImageProcessor(DisplayObject):
    def __init__(self, name, h=None, x = 0, y = 0, base="assets",max_w=None):
        self.name = name
        self.path = os.path.join("data", base, name+".png")
        self.max_w = max_w
        self.img = self.image_setup(h).convert_alpha()
        super().__init__((x, y, self.img.get_width(), self.img.get_height()))

    def __repr__(self):
        return self.name
        
    @property
    def rect(self):
        return pg.Rect(self.x, self.y, self.w, self.h)

    def fit(self, image, w, h):
        return pg.transform.scale(image, (w, h))

    def image_setup(self, h):
        
        # image scaled to the height inputted. Width is determined 
        # by the ratio of the original image's dimensions. If the 
        # name is a ribbon item, it is fitted specially.
        # input:
        #   name - name of an image
        #   h - height of the image
        # output:
        #   img - transformed image

        image = pg.image.load(self.path).convert_alpha()
        h = image.get_height() if h == None else h
        img_w, img_h = pg.Surface.get_width(image), pg.Surface.get_height(image)
        w = int(h / img_h * img_w)
        if self.name in cfg.RIBBON_ITEM:
            w, h = self.get_ribbon_item_dim(h, img_h, img_w)
        if self.max_w != None:
            if w > int(self.max_w):
                scale = w / self.max_w
                h = h / scale
                w = self.max_w
        return self.fit(image, w, h)     

    def get_ribbon_item_dim(self, h, img_h, img_w):
        w = int(h / img_h * img_w)
        # if h + 10 < w:
        #     return h, int((h / img_w) * img_h)
        return w, h

    def blit(self, target):
        target.blit(self.img, self.rect)