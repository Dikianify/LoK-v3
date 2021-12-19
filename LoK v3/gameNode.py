from interactable import Interactable, Button, TextBox
from textProcessor import TextProcessor
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

    def get_text_box(self):
        self.text_box = TextBox(TextProcessor(self.data.text, "left", cfg.DEFAULT_TEXT_BOX[2] / 1.015, cfg.DEFAULT_TEXT_BOX[3] / 1.02, cfg.DEFAULT_TEXT_BOX[2] * 0.7, cfg.DEFAULT_TEXT_BOX[3] * 0.7, adjust=True, scroll=True, opacity = 100))

    def get_button(self, next_nodes):
        self.button = Button(TextProcessor(self.data.text, "center", self.button_dimension[0], self.button_dimension[1], self.button_dimension[2], self.button_dimension[3], box=self.box_dimension), next_nodes, args=self)

    def get_last_text_box(self):
        self.last_text_box = TextProcessor(self.data.text, "center", cfg.LAST_TEXT_BOX[2] / 1.015, cfg.LAST_TEXT_BOX[3] / 1.02, cfg.LAST_TEXT_BOX[2] * 0.7, cfg.LAST_TEXT_BOX[3] * 0.7, box = cfg.LAST_TEXT_BOX, opacity = 100)

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

    def blit(self, target):
        if self.text_box != None:
            self.text_box.blit(target)
            if self.text_box.text_obj.scroll == False:
                self.button = self.continue_button
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
    def __init__(self, conditional=None, destination=None, text = None, incoming = None, leaving = None, ending = None, noise = None, bg = None, music = None):
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