import pygame
import config as cfg
from displayObject import DisplayObject

class TextProcessor(DisplayObject):
    def __init__(self, raw_text, alignment, max_width, max_height, min_width, min_height, box=cfg.DEFAULT_TEXT_BOX, adjust=False, scroll=False, font_size=20, text_margin=10, text_color=cfg.TEXT_COLOR, box_color=cfg.BOX_COLOR, opacity=255):
        self.raw_text=raw_text
        self.alignment=alignment
        self.obj_rect=pygame.Rect(box)
        self.adjust=adjust
        self.scroll=scroll
        self.scroll_count=0
        self.font_size=font_size
        self.text_margin=text_margin
        self.text_color=text_color
        self.box_color=box_color
        self.max_width, self.max_height, self.min_width, self.min_height = max_width, max_height, min_width, min_height

        self.text_list = self.text_fitter()
        surf = self.text_boxer()

        super().__init__(box, surf=surf, opacity=opacity)

    def text_fitter(self):
        # recursively fits text to a given height and width. Returns a list of the sliced text.
        sliced_text = []
        i, j = 0, 0
        while True:
            if self.font.size(self.raw_text[i:])[0] <= self.max_width:
                sliced_text.append(self.raw_text[i:])
                sliced_text_widths = [self.font.size(text)[0] for text in sliced_text]
                sliced_text_heights = [self.font.size(text)[1] for text in sliced_text]
                # reduced font size if text height overflows max height
                if sum(sliced_text_heights) > self.max_height:
                    self.font_size -= 2
                    sliced_text = self.text_fitter()
                # increased font size if beneath box margins
                if max(sliced_text_widths) < self.min_width and sum(sliced_text_heights) < self.min_height:
                    self.font_size += 1
                    sliced_text = self.text_fitter()
                return sliced_text
            elif self.font.size(self.raw_text[i:j])[0] > self.max_width:
                j = self.raw_text.rfind(" ", i, j) + 1
                if j == 0:
                    self.font_size -= 1
                else:
                    sliced_text.append(self.raw_text[i:j])
                    i = j
            j += 1
    
    def box_adjust(self, width, height):
        # if initialized box is larger than text box then this will resize
        self.coords = (0, 0, width, height)
        ui_rect = pygame.Rect(self.coords)
        ui_rect.midleft = (cfg.BUTTON_MARGIN, cfg.CONTINUE_BOX_CENTER[1])
        self.obj_rect = ui_rect

    def text_boxer(self):
        # assigns a text box for the text to be blitted onto
        line_widths = [self.font.size(item)[0] for item in self.text_list]
        width = max(line_widths)
        height = sum([self.font.size(text)[1] for text in self.text_list])
        if self.adjust==True:
            self.box_adjust(width + self.text_margin * 2, height + self.text_margin * 2)
        self.text_box = pygame.Rect(0, 0, width, height)

        # creates ui surface to blit text onto. Make sure you blit alpha before adding text!
        surf = pygame.Surface((self.obj_rect.size)).convert_alpha()
        surf.fill(self.box_color)

        return surf

    def get_text_objects(self):
        # get an updated list of text objects to blit onto the text box
        text_list = self.scroll_check()
        self.text_box.center = self.obj_rect.center

        text_obj_list = []              
        for index, lineText in enumerate(text_list):
            line = self.font.render(lineText, True, self.text_color)
            line_rect = line.get_rect()
            y = self.text_box.top
            if self.alignment=="center":
                x = self.text_box.center[0]
                line_rect.center = x, y + round((self.font.size("Tg")[1] * index) + self.font.size("Tg")[1] / 2.2)
            else:
                x = self.text_box.left
                line_rect.topleft = x, y + round(((self.font.size("Tg")[1] + 1) * index))
            text_obj_list.append((line, line_rect))
        return text_obj_list

    def scroll_check(self):
        # text list shortener for story box objects
        if self.scroll == True:
            self.scroll_count += cfg.SCROLL_SPEED
            if self.scroll_count >= sum([len(line) for line in self.text_list]):
                self.scroll = False
            else:
                new_text_list = []
                count = self.scroll_count
                for line in self.text_list:
                    if len(line) <= count:
                        new_text_list.append(line)
                        count -= len(line)
                    else:
                        new_text_list.append(line[:count])
                        return new_text_list
                return new_text_list
        return self.text_list

    def reset_scroll(self):
        self.scroll = True
        self.scroll_count = 0


    @property
    def font(self):
        return pygame.font.Font('freesansbold.ttf', self.font_size)


    @property
    def text_objs(self):
        return self.get_text_objects()

    def blit(self, target):
        self.blit_alpha(target, self.surf, self.obj_rect.topleft)
        for text in self.text_objs:
            target.blit(text[0], text[1])       