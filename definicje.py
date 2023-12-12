from tkinter import *
import pygame
import os
def play_prev(self):
    self.current_index = (self.current_index - 1) % len(self.mp3_files)
    self.play_current()
def play_next(self):
    self.current_index = (self.current_index + 1) % len(self.mp3_files)
    self.play_current()
def play_current(self):
    self.current_mp3_file = os.path.join(self.folder_path, self.mp3_files[self.current_index])
    pygame.mixer.music.load(self.current_mp3_file)
    pygame.mixer.music.play()
    self.label2.config(text=f"{self.mp3_files[self.current_index]}")
def play_selected(self, event):
    selected_index = self.listbox.curselection()
    if selected_index:
        self.current_index = selected_index[0]
        self.play_current()
def play(self):
    if self.playing:
        pygame.mixer.music.pause()
        self.playing = False
    else:
        pygame.mixer.music.unpause()
        self.playing = True
    aktualna_nazwa = self.play_button.cget("text")
    nowa_nazwa = "▷" if aktualna_nazwa != "▷" else "II"
    self.play_button.config(text=nowa_nazwa)
def set_volume(self, volume):
    pygame.mixer.music.set_volume(float(volume) / 100)