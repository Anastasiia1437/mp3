import os
import pygame
from tkinter import Tk, filedialog, Label, Scale, Button, Frame, Listbox, END, HORIZONTAL, ttk
import time

class SimpleMP3Player:
    def __init__(self, master):
        self.master = master
        master.title("Odtwarzacz MP3")
        master.geometry("679x500")
        master.configure(bg="black")
        master.resizable(False, False)

        self.current_file = None
        self.playing = False
        
        pygame.mixer.music.set_endevent(pygame.USEREVENT)
# Frames po lewej
        text_frame = Frame(master, bg="pink",pady=5)
        text_frame.grid(row=0, column=0, columnspan=3, sticky="nsew")

        anim_frame = Frame(master, bg="red")
        anim_frame.grid(row=1, column=0, columnspan=3, sticky="nsew")

        tbar_frame = Frame(master, bg="yellow")
        tbar_frame.grid(row=2, column=0, columnspan=3, sticky="nsew")

        button_frame = Frame(master, bg="blue", padx=107, pady=20)
        button_frame.grid(row=3, column=0, columnspan=3, sticky="s")

        volume_frame = Frame(master, bg="brown")
        volume_frame.grid(row=4, column=0, columnspan=3, sticky="s")
# Frame po prawej
        List_frame = Frame(master, bg="black")
        List_frame.grid(row=0, column=3, rowspan=5, sticky="w")
# Wybieranie folderu
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

# Przyciski
                    self.prev_button = Button(button_frame, text="<", command=self.play_prev, padx=15, pady=15, bg="gray", fg="black",)
                    self.prev_button.grid(row=1, column=0, sticky="ew")

                    self.play_button = Button(button_frame, text = "II", command=self.play, padx=15, pady=15, bg="gray", fg="black",)
                    self.play_button.grid(row=1, column=1, sticky="ew")

                    self.next_button = Button(button_frame, text=">", command=self.play_next, padx=15, pady=15, bg="gray", fg="black",)
                    self.next_button.grid(row=1, column=2, sticky="ew")

                    self.volume_label = Label(volume_frame, text="Głośność:", bg="pink", fg="Black")
                    self.volume_label.grid(row=0, column=0)

# Label do wyświetlania czasu trwania piosenki
                    self.duration_label = Label(tbar_frame, text="Czas trwania: 0:00", bg="black", fg="white")
                    self.duration_label.grid(row=0, column=0, padx=10)
                   
# Label do wyświetlania aktualnego czasu
                    self.current_time_label = Label(tbar_frame, text="Aktualny czas: 0:00", bg="black", fg="white")
                    self.current_time_label.grid(row=0, column=1, padx=10)

# Pasek czasu
                    self.timebar = Scale(tbar_frame, from_=0, to=100, orient=HORIZONTAL, length=420, bg="purple", highlightthicknes=0)
                    self.timebar.grid(row=1, column=0, columnspan=2, pady=5)

# Dźwięk
                    volume_slider = Scale(volume_frame, from_=0, to=100, resolution=1, orient=HORIZONTAL,
                                               command=self.set_volume, bg="black", fg="green", troughcolor="black",
                                               highlightbackground="black", width="15", length="326")
                    volume_slider.set(50)  # Domyślna głośność
                    volume_slider.grid(row=1, column=0, sticky="nsew")

                    self.listbox = Listbox(List_frame, selectmode="SINGLE", exportselection=0, bg="black", foreground="green", width="56", height="28")
                    self.listbox.pack()

                    for mp3_file in self.mp3_files:
                        self.listbox.insert(END, mp3_file)

                    self.listbox.bind("<Double-Button-1>", self.play_selected)

                    library = Button(List_frame, text="Zmień folder", command=self.change_folder, bg="gray", fg="black", padx="10", pady="5")
                    library.pack()

                else:
                    print("Brak plików MP3 w folderze.")
            except OSError as e:
                print(f"Wystąpił błąd podczas odczytu zawartości folderu: {e}")
# Definicje

    
    
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
# Ustawienie czasu trwania piosenki
        self.song_length = pygame.mixer.Sound(self.current_mp3_file).get_length()
        self.duration_label.config(text=f"Czas trwania: {int(self.song_length//60)}:{int(self.song_length%60):02}")

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


    def set_volume(self, volume):
        pygame.mixer.music.set_volume(float(volume) / 100)

    def change_folder(self):
        folder_path = filedialog.askdirectory(title="Wybierz folder")
        if folder_path:
                print(f"\nZawartość folderu {folder_path}:")
                try:
                    files = os.listdir(folder_path)
                    for file in files:
                        print(file)
                    mp3_files = [f for f in files if f.lower().endswith(".mp3")]
                    if mp3_files:
                        current_index = 0
                        current_mp3_file = os.path.join(folder_path, mp3_files[current_index])
                        pygame.mixer.init()
                        pygame.mixer.music.load(current_mp3_file)
                        pygame.mixer.music.play()
                        self.playing = True
                    else:
                        print("Brak plików MP3 w folderze.")
                except OSError as e:
                    print(f"Wystąpił błąd podczas odczytu zawartości folderu: {e}")

    #if self.playing == False:
    #    play_next()


if __name__ == "__main__":
    window = Tk()
    window.configure(bg="Pink")
    mp3_player = SimpleMP3Player(window)
    window.mainloop()