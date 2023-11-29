import os
import pygame
from tkinter import Tk, filedialog, Label, Scale, Button, HORIZONTAL

class SimpleMP3Player:
    def __init__(self, master):
        self.master = master
        master.title("Simple MP3 Player")
        master.geometry("400x200")
        master.configure(bg="pink")

        self.current_file = None
        self.playing = False

        self.label = Label(master, text="Brak odtwarzanego pliku", bg="black", fg="white")
        self.label.grid(column=1, row=0)

        self.select_button = Button(master, text="Wybierz plik", command=self.select_file, bg="green", fg="black")
        self.select_button.grid(column=0, row=1)

        self.play_button = Button(master, text="Odtwarzaj", command=self.play, bg="green", fg="black")
        self.play_button.grid(column=2, row=1)

        self.pause_button = Button(master, text="Zatrzymaj", command=self.stop, bg="green", fg="black")
        self.pause_button.grid(column=0, row=2)

        self.resume_button = Button(master, text="Puść", command=self.resume, bg="green", fg="black")
        self.resume_button.grid(column=2, row=2)

        self.volume_label = Label(master, text="Głośność:", bg="pink", fg="Black")
        self.volume_label.grid(column=1, row= 3)

        self.volume_slider = Scale(master, from_=0, to=100, resolution=1, orient=HORIZONTAL, command=self.set_volume,
                                   bg="black", fg="white", troughcolor="black", highlightbackground="black")
        self.volume_slider.set(50)  # Domyślna głośność
        self.volume_slider.grid(column=1, row=4)

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
        if self.playing:
            pygame.mixer.music.pause()
            self.playing = False
        else:
            pygame.mixer.music.unpause()
            self.playing = True

    def set_volume(self, volume):
        pygame.mixer.music.set_volume(float(volume) / 100)

if __name__ == "__main__":
    window = Tk()
    window2 = Tk()
    widnow3 = Tk()
    window.configure(bg="Pink")
    mp3_player = SimpleMP3Player(window)
    window.mainloop()
