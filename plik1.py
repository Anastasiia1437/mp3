import os
import pygame
from tkinter import Tk, filedialog, Label, Scale, Button, Frame, Listbox, END, HORIZONTAL, ttk
import time

class SimpleMP3Player:
    def __init__(self, master):
        self.master = master
        master.title("Odtwarzacz MP3")
        master.geometry("800x500")
        master.configure(bg="black")
        master.resizable(False, False)

        # ... (Inne inicjalizacje)

        # Frame z timebarem
        self.timebar_frame = Frame(master, bg="purple")
        self.timebar_frame.grid(row=2, column=0, columnspan=3, sticky="nsew")

        # Label do wyświetlania czasu trwania piosenki
        self.duration_label = Label(self.timebar_frame, text="Czas trwania: 0:00", bg="black", fg="white")
        self.duration_label.grid(row=0, column=0, padx=10)

        # Label do wyświetlania aktualnego czasu
        self.current_time_label = Label(self.timebar_frame, text="Aktualny czas: 0:00", bg="black", fg="white")
        self.current_time_label.grid(row=0, column=1, padx=10)

        # Pasek czasu
        self.timebar = ttk.Progressbar(self.timebar_frame, orient=HORIZONTAL, length=500, mode="determinate")
        self.timebar.grid(row=1, column=0, columnspan=2, pady=5)

        # ... (Pozostałe inicjalizacje)

    # ... (Pozostałe metody)

    def play_current(self):
        # ... (Pozostała logika)

        # Ustawienie czasu trwania piosenki
        self.song_length = pygame.mixer.Sound(self.current_mp3_file).get_length()
        self.duration_label.config(text=f"Czas trwania: {int(self.song_length//60)}:{int(self.song_length%60):02}")

    def mainloop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.USEREVENT:
                    self.play_next()

            # Aktualizacja paska czasu
            if pygame.mixer.music.get_busy() and self.playing:
                self.current_time = pygame.mixer.music.get_pos() / 1000  # w sekundach
                self.current_time_label.config(text=f"Aktualny czas: {int(self.current_time//60)}:{int(self.current_time%60):02}")
                self.timebar["value"] = (self.current_time / self.song_length) * 100

            self.master.update()
            time.sleep(0.01)

# ... (Pozostała część kodu)

if __name__ == "__main__":
    window = Tk()
    window.configure(bg="Pink")
    mp3_player = SimpleMP3Player(window)
    window.mainloop()