import os
import pygame
from tkinter import *

class SimpleMP3Player:
    def __init__(self, master):
        self.master = master
        master.title("MP3 Player")
        master.geometry("400x200")
        master.configure(bg="black")

        self.current_file = None
        self.playing = False

        self.label = Label(master, text="Brak odtwarzanego pliku", bg="black", fg="green")
        self.label.pack()

        self.select_button = Button(master, text="Wybierz plik", command=self.select_file, bg="green", fg="black")
        self.select_button.pack(fill='x')

        self.play_button = Button(master, text="Odtwarzaj", command=self.play, bg="green", fg="black")
        self.play_button.pack(fill='x')

        self.pause_button = Button(master, text="Zatrzymaj", command=self.stop, bg="green", fg="black")
        self.pause_button.pack(fill='x')

        self.resume_button = Button(master, text="Puść", command=self.resume, bg="green", fg="black")
        self.resume_button.pack(fill='x')

        self.volume_label = Label(master, text="Głośność:", bg="black", fg="green")
        self.volume_label.pack()

        self.volume_slider = Scale(master, from_=0, to=100, resolution=1, orient=HORIZONTAL, command=self.set_volume,
                                   bg="gray", fg="green", troughcolor="green", highlightbackground="green",
                                   activebackground="green", sliderrelief="flat")
        self.volume_slider.set(50)  # Domyślna głośność
        self.volume_slider.pack(fill='x')

    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("MP3 files", "*.mp3")])
        if file_path:
            self.current_file = file_path
            self.label.config(text=os.path.basename(file_path))

    def play(self):
        if self.current_file:
            pygame.mixer.init()
            pygame.mixer.music.load(self.current_file)
            pygame.mixer.music.play()
            self.playing = True

    def stop(self):
        pygame.mixer.music.stop()
        self.playing = False

    def resume(self):
        pygame.mixer.music.unpause()
        self.playing = True

    def set_volume(self, volume):
        pygame.mixer.music.set_volume(float(volume) / 100)

if __name__ == "__main__":
    root = Tk()
    root.configure(bg="black")
    mp3_player = SimpleMP3Player(root)
    root.mainloop()
