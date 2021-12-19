import pygame

class DisplayObject:
    def __init__(self, coords, color=None, surf=None, opacity=255):
        # assembling surface that stuff will be blitted onto the surface
        self.color = color
        self.x,self.y,self.w,self.h = coords
        self.opacity=opacity
        if surf == None:
            self.obj_rect = pygame.Rect(self.x,self.y,self.w,self.h)
            self.surf = pygame.Surface((self.obj_rect.size)).convert_alpha()
            if color != None:
                self.surf.fill(color)
        else:
            self.surf = surf

    def blit_alpha(self, target, source, location):
        x = location[0]
        y = location[1]
        temp = pygame.Surface((source.get_width(), source.get_height())).convert()
        temp.blit(target, (-x, -y))
        temp.blit(source, (0, 0))
        temp.set_alpha(self.opacity)
        target.blit(temp, location)

    def blit(self, target):
        self.blit_alpha(target, self.surf, self.obj_rect.topleft)