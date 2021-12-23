import pygame as pg
import os

class MusicPlayer:
    def __init__(self, music_volume, effect_volume):
        self.set_music_volume(music_volume)
        self.effect_volume = effect_volume
        self.music = None

    def set_music_volume(self, val):
        self.music_volume = val
        pg.mixer.music.set_volume(val/100)

    def get_music_volume(self):
        return self.music_volume

    def set_effect_volume(self, val):
        self.effect_volume = val

    def get_effect_volume(self):
        return self.effect_volume

    def set_music(self, mus):
        if self.music != mus:
            mus_path = os.path.join("data", "sounds", "ost", mus + ".mp3")
            pg.mixer.music.fadeout(400)
            pg.mixer.music.load(mus_path)
            pg.mixer.music.play(30)
            self.music = mus    

    def play_sound(self, sound):
        sound_effect = pg.mixer.Sound(os.path.join("data", "sounds", "effects", sound + ".mp3"))
        sound_effect.set_volume(self.effect_volume/100)
        sound_effect.play()