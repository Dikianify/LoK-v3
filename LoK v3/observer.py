from game import Game
from backpack import Backpack
import config as cfg
from data import Data
from gameNode import EndNode, StartNode, HellEndNode
from interactable import Button
from random import randint

class Observer(Game):
    def __init__(self):
        self.data = Data()
        super().__init__(cfg.GAMEFILE)
        self.traversed_rows = self.data.data_dict["traversed_rows"]
        self.endings = self.data.data_dict["endings"]
        self.backpack_obj = Backpack(cfg.BP_COORDS, self.data.data_dict["inventory"])
        self.settings_obj = None
        self.active_objs = {"backpack":[], "settings":[]}
        self.start_node = StartNode(self.get_option_objs, self.update_active_objs, self.data)
        self.end_node = EndNode(self.get_option_objs, self.update_active_objs, self.start_node)
        self.hell_end_node = HellEndNode(self.get_option_objs, self.update_active_objs, self.start_node)
        self.update_active_objs("nodes", [self.start_node])

    def update_active_objs(self, key, value):
        self.active_objs[key] = value

    def remove_active_obj(self, key):
        del self.active_objs[key]

    def conditional_check(self, conditionals, default_destination):
        # takes in a an end node that we are moving on from.
        for cond in conditionals:
            condition = cond[0][0]
            match condition:
                case "b":
                    self.active_objs["backpack"].append(self.backpack_obj)
                case "r":
                    if cond[0][1:] in self.traversed_rows:
                        return cond[1]
                case "i":
                    if cond[0][1:] in self.backpack_obj.inventory:
                        return cond[1]
                case "e":
                    if cond[0][1:] in self.endings:
                        return cond[1]
                case "h":
                    if 1 == randint(1,2):
                        return cond[0][1:]
                    else:
                        return cond[1]
                case "f":
                    for row in self.traversed_rows:
                        if row >= 142:
                            self.traversed_rows.remove(row)
                        if self.backpack_obj.items["bone"] in self.backpack_obj.inventory:
                            self.backpack_obj.inventory.remove(self.backpack_obj.items["bone"])
        return default_destination

    def inventory_check(self, node):
        if node.data.incoming != None:
            self.backpack_obj.inventory.append(self.backpack_obj.items[node.data.incoming])
        if node.data.leaving != None:
            self.backpack_obj.inventory.remove(self.backpack_obj.items[node.data.leaving])
        self.backpack_obj.update_inventory()

    def end_check(self, node):
        if node.data.ending != None:
            self.endings.append(node.data.ending)
            if "2" in node.data.ending or "3" in node.data.ending or "4" in node.data.ending:
                end_node = self.hell_end_node
            else:
                end_node = self.end_node
            end_node.get_end_text_box(node.data.ending)
            self.update_active_objs("nodes", [end_node])
            return True
        return False

    def next_nodes(self, node):
        node.button = None
        self.traversed_rows.append(node.row_id)
        if len(node.get_children()) == 1:
            next_node = node.get_children()[0]
            next_node.get_text_box()
            self.update_active_objs("nodes", [next_node])
        else:
            if not self.end_check(node):
                self.inventory_check(node)
                next_id = self.conditional_check(node.data.conditionals, node.data.destination)
                next_nodes = self.get_option_objs(next_id)
                if len(next_nodes) > 1:
                    next_nodes[0].last_text_box = node.get_last_text_box()
                self.update_active_objs("nodes", next_nodes)
        self.data.save()

    def get_option_objs(self, key):
        option_nodes = self.options[str(key)]
        if len(option_nodes) == 1:
            for index, node in enumerate(option_nodes):
                node.get_text_box()
                option_nodes[index] = node
        else:
            for index, node in enumerate(option_nodes):
                node.get_button(self.next_nodes)
                option_nodes[index] = node
        return option_nodes

    def switch_game(self):
        self.game = not self.game




