import os
import pygame
from tkinter import Tk, filedialog, Label, Scale, Button, Frame, Listbox, END, HORIZONTAL

while True:
    class SimpleMP3Player:
        def __init__(self, master):
            self.master = master
            master.title("Odtwarzacz MP3")
            master.geometry("400x200")
            master.configure(bg="pink")

            self.current_file = None
            self.playing = False

            self.folder_path = filedialog.askdirectory(title="Wybierz folder")
            if self.folder_path:
                os.system(f"start {self.folder_path}")
                print(f"\nZawartość folderu {self.folder_path}:")
                try:
                    self.files = os.listdir(self.folder_path)
                    for file in self.files:
                        print(file)
                    self.mp3_files = [f for f in self.files if f.lower().endswith(".mp3")]
                    if self.mp3_files:
                        self.current_index = 0
                        self.current_mp3_file = os.path.join(self.folder_path, self.mp3_files[self.current_index])
                        pygame.mixer.init()
                        pygame.mixer.music.load(self.current_mp3_file)
                        pygame.mixer.music.play()
                        self.playing = True
                        self.label = Label(master, text=f"Aktualny plik: {self.mp3_files[self.current_index]}", bg="black", fg="white")
                        self.label.grid(column=1, row=0)

                        self.listbox = Listbox(master, selectmode="SINGLE", exportselection=0)
                        self.listbox.grid(row=4)

                        for mp3_file in self.mp3_files:
                            self.listbox.insert(END, mp3_file)

                        self.listbox.bind("<Double-Button-1>", self.play_selected)

                        self.prev_button = Button(master, text="Poprzedni", command=self.play_prev)
                        self.prev_button.grid(column=0, row=1)

                        self.play_button = Button(master, text = "II", command=self.play, bg="green", fg="black")
                        self.play_button.grid(column=1, row=1)

                        self.volume_label = Label(master, text="Głośność:", bg="pink", fg="Black")
                        self.volume_label.grid(column=1, row= 2)

                        self.next_button = Button(master, text="Następny", command=self.play_next)
                        self.next_button.grid(column=2, row=1)

                        self.volume_slider = Scale(master, from_=0, to=100, resolution=1, orient=HORIZONTAL, command=self.set_volume,
                                                   bg="black", fg="white", troughcolor="black", highlightbackground="black")
                        self.volume_slider.set(20)  # Domyślna głośność
                        self.volume_slider.grid(column=1, row=3)
                    else:
                        print("Brak plików MP3 w folderze.")
                except OSError as e:
                    print(f"Wystąpił błąd podczas odczytu zawartości folderu: {e}")

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
            self.label.config(text=f"Aktualny plik: {self.mp3_files[self.current_index]}")

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

    if __name__ == "__main__":
        window = Tk()
        window.configure(bg="Pink")
        mp3_player = SimpleMP3Player(window)
        window.mainloop()
    