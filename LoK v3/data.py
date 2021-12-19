import pickle
import os
import config as cfg

class Data:
    def __init__(self):
        self.data_dict = self.load()
        if self.data_dict == None:
            self.data_dict = {
                
                "text_box_color":cfg.TEXT_BOX_COLOR,"text_color":cfg.TEXT_COLOR,"button_color":cfg.BUTTON_COLOR,
                "inventory":[],"traversed_rows":[],"endings":[],"option":"0"
                
                }
            self.save()

    def save(self):
        with open("savegame", "wb") as f:
            inv = []
            for I in self.data_dict["inventory"]:
                inv.append(I.__repr__())
            self.data_dict["inventory"] = inv
            pickle.dump([self.data_dict], f)

    def load(self):
        try:
            with open("savegame", "rb") as f:
                self.data_dict = pickle.load(f)
        except:
            return None