from openpyxl import load_workbook
import config as cfg
from textProcessor import TextProcessor
from interactable import Button
from gameNode import GameNode, CellData

class Game:
    def __init__(self, gamefile):
        self.file_wb = load_workbook(gamefile)
        self.file_text_ws = self.file_wb['text']

        # building every node in a row and then hooking them up to eachother
        self.options = self.build_nodes()
        

    def build_nodes(self):
        end_nodes = []
        options = {}
        cell = self.file_text_ws.cell
        continue_obj = TextProcessor("Continue", "center", cfg.CONTINUE_WIDTH * 0.9, cfg.CONTINUE_HEIGHT * 0.85, cfg.CONTINUE_WIDTH * 0.72, cfg.CONTINUE_HEIGHT * 0.425, box= cfg.CONTINUE_BOX_RECT, opacity = 100)
        for i in range(2,self.file_text_ws.max_row):
            # acquiring option data
            option_node = GameNode(row_id=i,option_id=cell(i, 1).value,data=CellData(conditional=cell(i, 3).value,destination=cell(i, 4).value,incoming=cell(i, 17).value,leaving=cell(i, 18).value,ending=cell(i, 19).value,text = self.file_text_ws.cell(i, 2).value, noise = self.file_wb['sounds'].cell(i, 2).value, bg = self.file_wb['bgs'].cell(i, 2).value, music = self.file_wb['music'].cell(i, 2).value))
            if str(cell(i,1).value) not in options:
                options[str(cell(i,1).value)] = [option_node]
            else:
                options[str(cell(i,1).value)].append(option_node) 
            prev_option = option_node

            for c in range(5, 17):
                print("row: {}, column : {}, text: {}".format(i, c, self.file_text_ws.cell(i, c).value))

            # acquiring story text data. Regular story nodes will point to the next story node, so they can point to the next node
            for j in range(5,17):
                if self.file_text_ws.cell(i, j).value != None:
                    text_node = GameNode(data=CellData(conditional=cell(i, 3).value, destination=cell(i, 4).value, incoming=cell(i, 17).value, leaving=cell(i, 18).value, ending=cell(i, 19).value, text = self.file_text_ws.cell(i, j).value, noise = self.file_wb['sounds'].cell(i, 2).value, bg = self.file_wb['bgs'].cell(i, 2).value, music = self.file_wb['music'].cell(i, 2).value))
                    text_node.continue_button = Button(continue_obj, self.next_nodes, args=text_node)
                    prev_option.add_child(text_node)
                    prev_option = text_node
                if self.file_text_ws.cell(i, j).value == None or j == 17:
                    prev_option.last_text_box_bool = True
                    end_nodes.append(prev_option)
                    break

        # building buttons for options dicitionary
        for key, value_list in options.items():
            if len(value_list) == 1:
                value_list = value_list[0].get_children()
                value_list[0].button = Button(continue_obj, self.next_nodes, args=value_list[0]) if len(value_list) == 1 else None
            else:
                BUTTON_WIDTH = round(cfg.WINDOW_WIDTH / (len(value_list) + 1))
                BUTTON_MARGIN = round((cfg.WINDOW_WIDTH - BUTTON_WIDTH * len(value_list)) / (len(value_list) + 1))
                for index, option in enumerate(value_list):
                    if option.data.text == None:
                        option = option.get_children()[0]
                    else:
                        option.box_dimension = (BUTTON_WIDTH * index + BUTTON_MARGIN * (index + 1), cfg.BUTTON_Y, BUTTON_WIDTH, cfg.BUTTON_BASE_HEIGHT)
                        option.button_dimension = BUTTON_WIDTH * 0.9, cfg.BUTTON_BASE_HEIGHT * 0.85, BUTTON_WIDTH * 0.72, cfg.BUTTON_BASE_HEIGHT * 0.425
                    value_list[index] = option
            options[key] = value_list
            
        return options