import os
import pygame
from tkinter import Tk, filedialog, Label, Scale, Button, Frame, Listbox, END, HORIZONTAL, VERTICAL

class SimpleMP3Player:
    def __init__(self, master):
        self.master = master
        master.title("Odtwarzacz MP3")
        master.geometry("660x300")
        master.configure(bg="black")

        self.current_file = None
        self.playing = False

        text_frame = Frame(master, bg="black", pady=5)
        text_frame.grid(row=0, column=0, columnspan=3, sticky="nsew")

        button_frame = Frame(master, bg="black")
        button_frame.grid(row=1, column=0, columnspan=3, sticky="nsew")

        volume_frame = Frame(master, bg="black")
        volume_frame.grid(row=2, column=0, columnspan=3, sticky="nsew")

        Main_frame2 = Frame(master, bg="black", padx="100", pady="70")
        Main_frame2.grid(row=0, column=3, rowspan=3, sticky="w")

        self.folder_path = filedialog.askdirectory(title="Wybierz folder")
        if self.folder_path:
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
                    self.label1 = Label(text_frame, text="Altualny plik:", bg="black", fg="green")
                    self.label1.grid(row=0, column=0)
                    self.label2 = Label(text_frame, text=f"{self.mp3_files[self.current_index]}", bg="black", fg="green")
                    self.label2.grid(row=1, column=0)

                    self.prev_button = Button(button_frame, text="<", command=self.play_prev, bg="gray", fg="green")
                    self.prev_button.grid(row=1, column=0)

                    self.play_button = Button(button_frame, text="II", command=self.play, bg="gray", fg="green")
                    self.play_button.grid(row=1, column=1)

                    self.next_button = Button(button_frame, text=">", command=self.play_next, bg="gray", fg="green")
                    self.next_button.grid(row=1, column=2)

                    self.volume_label = Label(volume_frame, text="Głośność:", bg="pink", fg="Black")
                    self.volume_label.grid(row=0, column=0)

                    self.volume_slider = Scale(volume_frame, from_=0, to=100, resolution=1, orient=HORIZONTAL,
                                               command=self.set_volume, bg="black", fg="white", troughcolor="black",
                                               highlightbackground="black")
                    self.volume_slider.set(50)  # Domyślna głośność
                    self.volume_slider.grid(row=0, column=1)

                    self.listbox = Listbox(Main_frame2, selectmode="SINGLE", exportselection=0, bg="black", foreground="green")
                    self.listbox.pack()

                    for mp3_file in self.mp3_files:
                        self.listbox.insert(END, mp3_file)

                    self.listbox.bind("<Double-Button-1>", self.play_selected)

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


if __name__ == "__main__":
    window = Tk()
    window.configure(bg="Pink")
    mp3_player = SimpleMP3Player(window)
    window.mainloop()