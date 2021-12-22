from imageProcessor import ImageProcessor
from interactable import Interactable, Button
from textProcessor import TextProcessor
from copy import copy
import pygame as pg
import config as cfg

class Settings_Gear(Interactable):
    def __init__(self, music_player, update_active_objs, get_active_objs, next_nodes, data):
        self.gear_obj = ImageProcessor("gear", cfg.SETTINGS_GEAR_DIMENSION, x = cfg.SETTINGS_GEAR_X, y = cfg.SETTINGS_GEAR_Y)
        self.settings = Settings(music_player, update_active_objs, get_active_objs, next_nodes, data)
        super().__init__(self.gear_obj.rect, self.add_settings, trigger=[pg.MOUSEBUTTONUP, pg.K_s],args=[update_active_objs])

    def add_settings(self, args):
        args[0]("settings", [self.settings, self.settings.diamond1_obj, self.settings.diamond2_obj, self.settings.checkmark_obj, self.settings.change_color_button])

    def blit(self, target):
        self.gear_obj.blit(target)


class Settings(Interactable):
    def __init__(self, music_player, update_active_objs, get_active_objs, next_nodes, data):
        self.settings_obj = ImageProcessor("settings", cfg.SETTINGS_MENU_HEIGHT, y=cfg.SETTINGS_MENU_Y)
        self.settings_obj.x = int((cfg.WINDOW_WIDTH / 2) - (self.settings_obj.w / 2))
        self.diamond1_obj = Diamond(int(cfg.SETTINGS_MENU_HEIGHT * 0.75 - cfg.DIAMOND_HEIGHT / 2 + cfg.SETTINGS_MENU_Y), self.settings_obj, music_player.set_music_volume, music_player.get_music_volume)
        self.diamond2_obj = Diamond(int(cfg.SETTINGS_MENU_HEIGHT * 0.87 - cfg.DIAMOND_HEIGHT / 2 + cfg.SETTINGS_MENU_Y), self.settings_obj, music_player.set_effect_volume, music_player.get_effect_volume)
        self.checkmark_obj = CheckBox(self.settings_obj, music_player)
        self.change_color_rect = pg.Rect(int(self.settings_obj.w * 0.56) + self.settings_obj.x, int(self.settings_obj.h * 0.78125) + self.settings_obj.y, int(self.settings_obj.w / 3), int(self.settings_obj.h / 16))
        self.change_color_button = Button(TextProcessor("Change Color", "center", self.change_color_rect.w *0.9, self.change_color_rect.h *0.9, self.change_color_rect.w * 0.6, self.change_color_rect.h * 0.6, box=self.change_color_rect, box_color=data.data_dict["box_color"], opacity = 350), self.change_color, trigger=[pg.MOUSEBUTTONUP])
        self.update_active_objs = update_active_objs
        self.get_active_objs = get_active_objs
        self.next_nodes = next_nodes
        self.data = data

    def update_button(self):
        self.change_color_button = Button(TextProcessor("Change Color", "center", self.change_color_rect.w *0.9, self.change_color_rect.h *0.9, self.change_color_rect.w * 0.6, self.change_color_rect.h * 0.6, box=self.change_color_rect, box_color=self.data.data_dict["box_color"], opacity = 350), self.change_color, trigger=[pg.MOUSEBUTTONUP])
        new_active_objs = self.get_active_objs()
        new_settings = new_active_objs["settings"]
        new_settings[4] = self.change_color_button
        new_nodes = new_active_objs["nodes"]
        if len(new_nodes) == 1:
            for index, node in enumerate(new_nodes):
                node.reset_text_box(self.next_nodes, self.data.data_dict["box_color"])
                new_nodes[index] = node
        else:
            for index, node in enumerate(new_nodes):
                if index == 0:
                    node.last_text_box = TextProcessor(self.data.data_dict["last_text"], "center", cfg.LAST_TEXT_BOX[2] / 1.025, cfg.LAST_TEXT_BOX[3] / 1.05, cfg.LAST_TEXT_BOX[2] * 0.7, cfg.LAST_TEXT_BOX[3] * 0.7, box = cfg.LAST_TEXT_BOX, opacity = 100, box_color = self.data.data_dict["box_color"])
                node.get_button(self.next_nodes, self.data.data_dict["box_color"])
                new_nodes[index] = node
        for key, value in new_active_objs.items():
            self.update_active_objs(key, value)
        self.data.save()

    def event(self, event, observer):
        if event.type == pg.MOUSEBUTTONDOWN:
            if not self.settings_obj.rect.collidepoint(pg.mouse.get_pos()):
                self.update_active_objs("settings", [])
        if event.type == pg.KEYDOWN:
            if event.key in [pg.K_ESCAPE]:
                self.update_active_objs("settings", [])

    def change_color(self, args):
        self.color_palette = ColorPalette(self.data, copy(self.get_active_objs()), self.update_active_objs, self.update_button)
        for key, value in self.get_active_objs().items():
            self.update_active_objs(key, [])
        self.update_active_objs("splash", [self.color_palette])

    def blit(self, target):
        self.settings_obj.blit(target)


class ColorPalette(Interactable):
    def __init__(self, data, active_objs_copy, update_active_objs, update_button):
        self.img_obj = ImageProcessor("color2", h=cfg.WINDOW_HEIGHT)
        self.img_obj.x = int(cfg.WINDOW_WIDTH / 2 - self.img_obj.w / 2)
        self.data = data
        self.update_button = update_button
        self.active_objs_copy = active_objs_copy
        self.update_active_objs = update_active_objs
        super().__init__(self.img_obj.rect, self.change_color, trigger=[pg.MOUSEBUTTONDOWN])

    def change_color(self, args):
        x, y = pg.mouse.get_pos()
        self.data.data_dict["box_color"] = self.img_obj.img.get_at((x-self.img_obj.x,y))
        for key, value in self.active_objs_copy.items():
            self.update_active_objs(key, value)
        self.update_button()

    def blit(self, target):
        self.img_obj.blit(target)


class Diamond(Interactable):
    def __init__(self, y, settings_obj, set_func, volume):
        self.diamond_obj = ImageProcessor("diamond", h=cfg.DIAMOND_HEIGHT)
        self.diamond_obj.y = y
        self.minx = int((settings_obj.w * 0.15 - self.diamond_obj.w / 2) + settings_obj.x)
        self.maxx = int((settings_obj.w * 0.385 - self.diamond_obj.w / 2) + settings_obj.x)
        self.set_func = set_func
        self.volume = volume
        self.drag = False

    def set_diamond_x(self):
        self.diamond_obj.x = int(((self.volume()/100) * (self.maxx - self.minx)) + self.minx)

    def event(self, event, observer):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.diamond_obj.rect.collidepoint(pg.mouse.get_pos()):
                self.drag = True
        if event.type == pg.MOUSEMOTION and self.drag == True:
            mouse_x = pg.mouse.get_pos()[0]
            if self.minx <= mouse_x <= self.maxx:
                self.set_func(int((mouse_x - self.minx) / (self.maxx - self.minx) * 100))
            elif self.maxx <= mouse_x:
                self.set_func(100)
            elif self.minx >= mouse_x:
                self.set_func(0)
        if event.type == pg.MOUSEBUTTONUP:
            self.drag = False

    def blit(self, target):
        self.set_diamond_x()
        self.diamond_obj.blit(target)



class CheckBox(Interactable):
    def __init__(self, settings_obj, music_player):
        self.checkbox = pg.Rect(int(settings_obj.w * 0.25) + settings_obj.x, int(settings_obj.h * 0.625) + settings_obj.y, int(settings_obj.w * 0.05), int(settings_obj.h * 0.04678))
        self.check = ImageProcessor("check", int(settings_obj.h * 0.05))
        self.check.x = int(settings_obj.w * 0.25) + settings_obj.x
        self.check.y = int(settings_obj.h * 0.62) + settings_obj.y
        self.music_player = music_player
        self.previous_volumes = []
        super().__init__(self.checkbox, self.toggle_mute, trigger=[pg.MOUSEBUTTONDOWN, pg.K_m])

    def toggle_mute(self, args):
        if self.music_player.music_volume != 0 and self.music_player.effect_volume != 0:
            self.previous_volumes = [self.music_player.music_volume, self.music_player.effect_volume]
            self.music_player.set_music_volume(0)
            self.music_player.set_effect_volume(0)
        else:
            self.music_player.set_music_volume(self.previous_volumes[0])
            self.music_player.set_effect_volume(self.previous_volumes[1])           

    def blit(self, target):
        if self.music_player.music_volume == 0 and self.music_player.effect_volume == 0:
            self.check.blit(target)