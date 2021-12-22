from interactable import Interactable, Button, TextBox
from textProcessor import TextProcessor
from imageProcessor import ImageProcessor
import pygame as pg
import config as cfg

class GameNode(Interactable):
    def __init__(self, row_id=None, option_id=None, data=None):
        self.row_id = row_id
        self.option_id = option_id
        self.data = data
        self.children = []
        self.text_box = None
        self.continue_button = None
        self.button = None
        self.last_text_box = None
        self.box_dimension = None
        self.button_dimension = None
        self.last_text_box_bool = False

    def get_text_box(self, next_nodes, color):
        if self.text_box == None:
            self.reset_text_box(next_nodes, color)
        else:
            self.text_box.text_obj.reset_scroll()

    def reset_text_box(self, next_nodes, color):
        continue_button = Button(TextProcessor("Continue", "center", cfg.CONTINUE_WIDTH * 0.9, cfg.CONTINUE_HEIGHT * 0.85, cfg.CONTINUE_WIDTH * 0.72, cfg.CONTINUE_HEIGHT * 0.425, box= cfg.CONTINUE_BOX_RECT, opacity = 200, box_color = color), next_nodes, args=self, trigger=[pg.MOUSEBUTTONDOWN, pg.K_SPACE, pg.K_RETURN])
        self.text_box = TextBox(TextProcessor(self.data.text, "left", cfg.DEFAULT_TEXT_BOX[2] / 1.015, cfg.DEFAULT_TEXT_BOX[3] / 1.02, cfg.DEFAULT_TEXT_BOX[2] * 0.7, cfg.DEFAULT_TEXT_BOX[3] * 0.7, adjust=True, scroll=True, opacity = 100, box_color=color), continue_button)
    
    def get_button(self, next_nodes, color):
        self.button = Button(TextProcessor(self.data.text, "center", self.button_dimension[0], self.button_dimension[1], self.button_dimension[2], self.button_dimension[3], box=self.box_dimension, opacity = 200, box_color = color), next_nodes, args=self, trigger=self.trigger)

    
    def get_last_text_box(self, color):
        return TextProcessor(self.data.text, "center", cfg.LAST_TEXT_BOX[2] / 1.025, cfg.LAST_TEXT_BOX[3] / 1.05, cfg.LAST_TEXT_BOX[2] * 0.7, cfg.LAST_TEXT_BOX[3] * 0.7, box = cfg.LAST_TEXT_BOX, opacity = 100, box_color = color)

    def add_child(self, child_node):
        self.children.append(child_node)

    def add_parent(self, parent_node):
        if self not in parent_node.children:
            parent_node.add_child(self)

    def remove_child(self, node):
        if node in self.children:
            self.children.remove(node)

    def get_children(self):
        return self.children

    def render_background(self):
        return ImageProcessor(self.data.bg, h=cfg.WINDOW_HEIGHT)

    def blit(self, target):
        if self.text_box != None:
            self.text_box.blit(target)
        if self.button != None:
            self.button.blit(target)
        if self.last_text_box != None:
            self.last_text_box.blit(target)

    def event(self, event, observer):
        if self.button != None:
            self.button.event(event, observer)
        if self.text_box != None:
            self.text_box.event(event, observer)





class CellData:
    def __init__(self, conditional=None, destination=None, text = None, incoming = None, leaving = None, ending = None, noise = "None", bg = None, music = None):
        if conditional == None:
            conditional = []
        else:
            conditional = conditional.replace("(", "").replace(")", "").split()
            for index, condition in enumerate(conditional):
                conditional[index] = condition.split(",")
        self.conditionals = conditional
        self.destination = destination
        self.text = text
        self.incoming = incoming
        self.leaving = leaving
        self.ending = ending
        self.noise = noise
        self.bg = bg
        self.music = music




class EndNode(Interactable):
    BUTTON_WIDTH = round(cfg.WINDOW_WIDTH / 3)
    BUTTON_MARGIN = round((cfg.WINDOW_WIDTH - BUTTON_WIDTH * 2) / 3)
    BUTTON_DIMENSION = BUTTON_WIDTH * 0.9, cfg.BUTTON_BASE_HEIGHT * 0.85, BUTTON_WIDTH * 0.72, cfg.BUTTON_BASE_HEIGHT * 0.425
    button1_box_dimension = (BUTTON_MARGIN, cfg.BUTTON_Y, BUTTON_WIDTH, cfg.BUTTON_BASE_HEIGHT)
    button2_box_dimension = (BUTTON_WIDTH + BUTTON_MARGIN * 2, cfg.BUTTON_Y, BUTTON_WIDTH, cfg.BUTTON_BASE_HEIGHT)
    button3_box_dimension = (cfg.WINDOW_WIDTH/2 - BUTTON_WIDTH/2, cfg.BUTTON_Y, BUTTON_WIDTH, cfg.BUTTON_BASE_HEIGHT)

    def __init__(self, get_option_objs, update_active_objs, update_sounds, main_menu_node, data, win_node = ""):
        self.get_option_objs, self.update_active_objs, self.update_sounds = get_option_objs, update_active_objs, update_sounds
        self.main_menu_node = main_menu_node
        self.win_node = win_node
        self.game_data = data
        self.data=CellData(music="end")
        self.buttons = [
        Button(TextProcessor("Restart", "center", self.BUTTON_WIDTH * 0.9, cfg.BUTTON_BASE_HEIGHT * 0.85, self.BUTTON_WIDTH * 0.72, cfg.BUTTON_BASE_HEIGHT * 0.425, box=self.button1_box_dimension,opacity=200), self.restart, trigger = [pg.MOUSEBUTTONDOWN, pg.K_1]),
        Button(TextProcessor("Main Menu", "center", self.BUTTON_WIDTH * 0.9, cfg.BUTTON_BASE_HEIGHT * 0.85, self.BUTTON_WIDTH * 0.72, cfg.BUTTON_BASE_HEIGHT * 0.425, box=self.button2_box_dimension,opacity=200), self.main_menu, trigger = [pg.MOUSEBUTTONDOWN, pg.K_2]),
        ]
        self.win_button = Button(TextProcessor("Continue", "center", self.BUTTON_WIDTH * 0.9, cfg.BUTTON_BASE_HEIGHT * 0.85, self.BUTTON_WIDTH * 0.72, cfg.BUTTON_BASE_HEIGHT * 0.425, box=self.button3_box_dimension,opacity=200), self.assign_win_node, trigger = [pg.MOUSEBUTTONDOWN, pg.K_1])

    def reset_buttons(self):
        self.buttons = [
        Button(TextProcessor("Restart", "center", self.BUTTON_WIDTH * 0.9, cfg.BUTTON_BASE_HEIGHT * 0.85, self.BUTTON_WIDTH * 0.72, cfg.BUTTON_BASE_HEIGHT * 0.425, box=self.button1_box_dimension,opacity=200), self.restart, trigger = [pg.MOUSEBUTTONDOWN, pg.K_1]),
        Button(TextProcessor("Main Menu", "center", self.BUTTON_WIDTH * 0.9, cfg.BUTTON_BASE_HEIGHT * 0.85, self.BUTTON_WIDTH * 0.72, cfg.BUTTON_BASE_HEIGHT * 0.425, box=self.button2_box_dimension,opacity=200), self.main_menu, trigger = [pg.MOUSEBUTTONDOWN, pg.K_2]),
        ]      

    def event(self, event, observer):
        if len(self.game_data.data_dict["endings"]) != 8:
            for button in self.buttons:
                button.event(event, observer)

    def blit(self, target):
        self.end_text_box.blit(target)
        if len(self.game_data.data_dict["endings"]) != 8:
            for button in self.buttons:
                button.blit(target)
        else:
            self.win_button.blit(target)

    def restart(self, arg):
        next_nodes = self.get_option_objs("0")
        self.update_sounds(next_nodes[0].data.music, next_nodes[0].data.noise)
        self.update_active_objs("nodes", next_nodes)
        self.game_data.data_dict["backpack"] = False
        self.game_data.data_dict["traversed_rows"] = []

    def main_menu(self, arg):
        self.game_data.data_dict["option"] = "0"
        self.game_data.data_dict["backpack"] = False
        self.main_menu_node.reset_buttons()
        self.update_active_objs("nodes", [self.main_menu_node])

    def render_background(self):
        return ImageProcessor(self.game_data.data_dict["endings"][-1][7], h=cfg.WINDOW_HEIGHT)

    def assign_win_node(self, arg):
        self.update_active_objs("nodes", [self.win_node])

    def get_end_text_box(self, end):
        self.end_text_box =TextProcessor(end, "center", cfg.LAST_TEXT_BOX[2] / 1.2, cfg.LAST_TEXT_BOX[3] / 1.2, cfg.LAST_TEXT_BOX[2] * 0.6, cfg.LAST_TEXT_BOX[3] * 0.6, box = cfg.LAST_TEXT_BOX, opacity = 100, font_size = 10)

class HellEndNode(EndNode):
    def __init__(self, get_option_objs, update_active_objs, update_sounds, main_menu_node, data, win_node = ""):
        super().__init__(get_option_objs, update_active_objs, update_sounds, main_menu_node, data, win_node = win_node)
        self.buttons[0] = Button(TextProcessor("Try Again", "center", self.BUTTON_WIDTH * 0.9, cfg.BUTTON_BASE_HEIGHT * 0.85, self.BUTTON_WIDTH * 0.72, cfg.BUTTON_BASE_HEIGHT * 0.425, box=self.button1_box_dimension,opacity=200), self.try_again, trigger = [pg.MOUSEBUTTONDOWN, pg.K_1])

    def try_again(self, arg):
        next_nodes = self.get_option_objs("706")
        self.update_sounds(next_nodes[0].data.music, next_nodes[0].data.noise)
        self.update_active_objs("nodes", next_nodes)

class StartNode(Interactable):
    BUTTON_WIDTH = round(cfg.WINDOW_WIDTH / 3)
    BUTTON_MARGIN = round((cfg.WINDOW_WIDTH - BUTTON_WIDTH * 2) / 3)
    BUTTON_DIMENSION = BUTTON_WIDTH * 0.9, cfg.BUTTON_BASE_HEIGHT * 0.85, BUTTON_WIDTH * 0.72, cfg.BUTTON_BASE_HEIGHT * 0.425
    button1_box_dimension = (BUTTON_MARGIN, cfg.BUTTON_Y, BUTTON_WIDTH, cfg.BUTTON_BASE_HEIGHT)
    button2_box_dimension = (BUTTON_WIDTH + BUTTON_MARGIN * 2, cfg.BUTTON_Y, BUTTON_WIDTH, cfg.BUTTON_BASE_HEIGHT)
   
   
    def __init__(self, get_option_objs, update_active_objs, update_sounds, data, backpack, gear):
        self.get_option_objs, self.update_active_objs, self.update_sounds = get_option_objs, update_active_objs, update_sounds
        self.game_data = data
        self.backpack = backpack
        self.gear = gear
        self.last_text_box = TextProcessor(self.game_data.data_dict["last_text"], "center", cfg.LAST_TEXT_BOX[2] / 1.025, cfg.LAST_TEXT_BOX[3] / 1.05, cfg.LAST_TEXT_BOX[2] * 0.7, cfg.LAST_TEXT_BOX[3] * 0.7, box = cfg.LAST_TEXT_BOX, opacity = 100)
        self.buttons = [
        Button(TextProcessor("Continue", "center", self.BUTTON_WIDTH * 0.9, cfg.BUTTON_BASE_HEIGHT * 0.85, self.BUTTON_WIDTH * 0.72, cfg.BUTTON_BASE_HEIGHT * 0.425, box=self.button1_box_dimension, opacity=200, box_color = self.game_data.data_dict["box_color"]), self.continue_game, trigger = [pg.MOUSEBUTTONDOWN, pg.K_1]),
        Button(TextProcessor("New Game", "center", self.BUTTON_WIDTH * 0.9, cfg.BUTTON_BASE_HEIGHT * 0.85, self.BUTTON_WIDTH * 0.72, cfg.BUTTON_BASE_HEIGHT * 0.425, box=self.button2_box_dimension, opacity=200, box_color = self.game_data.data_dict["box_color"]), self.new_game, trigger = [pg.MOUSEBUTTONDOWN, pg.K_2]),
        ]

    def reset_buttons(self):
        self.buttons = [
        Button(TextProcessor("Continue", "center", self.BUTTON_WIDTH * 0.9, cfg.BUTTON_BASE_HEIGHT * 0.85, self.BUTTON_WIDTH * 0.72, cfg.BUTTON_BASE_HEIGHT * 0.425, box=self.button1_box_dimension, opacity=200, box_color = self.game_data.data_dict["box_color"]), self.continue_game, trigger = [pg.MOUSEBUTTONDOWN, pg.K_1]),
        Button(TextProcessor("New Game", "center", self.BUTTON_WIDTH * 0.9, cfg.BUTTON_BASE_HEIGHT * 0.85, self.BUTTON_WIDTH * 0.72, cfg.BUTTON_BASE_HEIGHT * 0.425, box=self.button2_box_dimension, opacity=200, box_color = self.game_data.data_dict["box_color"]), self.new_game, trigger = [pg.MOUSEBUTTONDOWN, pg.K_2]),
        ]       

    def event(self, event, observer):
        for button in self.buttons:
            button.event(event, observer)

    def blit(self, target):
        self.update_sounds("intro", "None")
        for button in self.buttons:
            button.blit(target)   

    def continue_game(self, arg):
        next_nodes = self.get_option_objs(self.game_data.data_dict["option"])
        if len(next_nodes) != 1:
            next_nodes[0].last_text_box = self.last_text_box
        self.update_sounds(next_nodes[0].data.music, next_nodes[0].data.noise)
        self.update_active_objs("nodes", next_nodes)
        self.update_active_objs("background", [next_nodes[0].render_background()])
        self.update_active_objs("gear", [self.gear])
        if self.game_data.data_dict["backpack"] == True:
            self.update_active_objs("backpack", [self.backpack])

    def new_game(self, arg):
        self.game_data.data_dict["option"] = "0"
        self.game_data.data_dict["traversed_rows"] = []
        self.game_data.data_dict["inventory"] = []
        next_nodes = self.get_option_objs(self.game_data.data_dict["option"])
        self.update_sounds(next_nodes[0].data.music, "None")
        self.update_active_objs("background", [next_nodes[0].render_background()])
        self.update_active_objs("gear", [self.gear])
        self.update_active_objs("nodes", next_nodes)


class WinNode(EndNode):
    def __init__(self, get_option_objs, update_active_objs, update_sounds, main_menu_node, data):
        super().__init__(get_option_objs, update_active_objs, update_sounds, main_menu_node, data)
        self.get_end_text_box("Congratulations, you found all the endings!")