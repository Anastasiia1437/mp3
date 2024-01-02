import os
import pygame
from tkinter import Tk, filedialog, Label, Scale, Button, Frame, Listbox, END, HORIZONTAL, ttk
import time
from mutagen.mp3 import MP3

class SimpleMP3Player:
    def __init__(self, master):
        self.master = master
        master.title("Odtwarzacz MP3")
        master.geometry("779x500")
        master.configure(bg="black")
        master.resizable(False, False)

        self.current_file = None
        self.playing = False
        self.looping=False
        self.folder_path = filedialog.askdirectory(title="Wybierz folder")
        pygame.mixer.init()
        self.songindex = -1
        
        pygame.mixer.music.set_endevent(pygame.USEREVENT)
# Frames po lewej
        text_frame = Frame(master, bg="black",pady=5)
        text_frame.grid(row=0, column=0, columnspan=3, sticky="nsew")

        anim_frame = Frame(master, bg="black")
        anim_frame.grid(row=1, column=0, columnspan=3, sticky="nsew")

        tbar_frame = Frame(master, bg="black")
        tbar_frame.grid(row=2, column=0, columnspan=3, sticky="nsew")

        button_frame = Frame(master, bg="black", padx=107, pady=20)
        button_frame.grid(row=3, column=0, columnspan=3, sticky="s")

        volume_frame = Frame(master, bg="black")
        volume_frame.grid(row=4, column=0, columnspan=3, sticky="s")
# Frame po prawej
        List_frame = Frame(master, bg="black")
        List_frame.grid(row=0, column=3, rowspan=5, sticky="w")

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
                    self.nazwa_pliku = f"{self.mp3_files[self.current_index]}"
                    self.label1 = Label(text_frame, text="Altualny plik:", bg="black", fg="green")
                    self.label1.grid(row=0, column=0)

                    self.label2 = Label(text_frame, text=self.nazwa_pliku, bg="black", fg="green")
                    self.label2.grid(row=1, column=0)
                    
                    self.progress = Scale(tbar_frame, from_=0, to=100, orient=HORIZONTAL, length=420, sliderlength=20, showvalue=0, bg="#717291", highlightthickness=0, troughcolor="#525269")
                    self.progress.grid(column=0, row=1, columnspan=3, pady=10)
                    self.currenttime = Label(tbar_frame, text="00:00",bg="#717291")
                    self.currenttime.grid(column=0, row=2)
                    self.totaltime = Label(tbar_frame, text="00:00",bg="#717291")
                    self.totaltime.grid(column=2, row=2)

# Przyciski
                    self.prev_button = Button(button_frame, text="<", command=self.play_prev, padx=15, pady=15, bg="gray", fg="black",)
                    self.prev_button.grid(row=1, column=0, sticky="ew")

                    self.play_button = Button(button_frame, text = "II", command=self.play, padx=15, pady=15, bg="gray", fg="black",)
                    self.play_button.grid(row=1, column=1, sticky="ew")

                    self.next_button = Button(button_frame, text=">", command=self.play_next, padx=15, pady=15, bg="gray", fg="black",)
                    self.next_button.grid(row=1, column=2, sticky="ew")

                    self.volume_label = Label(volume_frame, text="Głośność:", bg="pink", fg="Black")
                    self.volume_label.grid(row=0, column=0)
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

                else:
                    print("Brak plików MP3 w folderze.")
            except OSError as e:
                print(f"Wystąpił błąd podczas odczytu zawartości folderu: {e}")
# Definicje

    
    
    def play_prev(self):
        self.current_index = (self.current_index - 1) % len(self.mp3_files)
        self.songindex -= 1
        if self.songindex < -len(self.mp3_files):
            self.songindex = len(self.mp3_files) - 1
        self.audio = os.path.join(self.folder_path, self.mp3_files[self.songindex])
        pygame.mixer.music.load(self.current_mp3_file)
        self.info = MP3(self.current_mp3_file)
        self.minutes, self.seconds = self.convert(self.info.info.length)
        self.minutes = round(self.minutes)
        self.seconds = round(self.seconds)
        self.totaltime.config(text=str(self.minutes) + ":" + str(self.seconds))
        self.timer = 0
        self.currenttime.config(text="0:00")
        self.playing = False
        self.played = False
        self.progress.set(0)
        self.progress.config(to=self.info.info.length)
        self.play_current()

    def play_next(self):
        self.current_index = (self.current_index + 1) % len(self.mp3_files)
        if not self.looping:
            self.songindex += 1
        try:
            self.audio = os.path.join(self.folder_path, self.mp3_files[self.songindex])
        except IndexError:
            self.songindex = 0
            self.audio = os.path.join(self.folder_path, self.mp3_files[self.songindex])
        pygame.mixer.music.load(self.current_mp3_file)
        self.info = MP3(self.current_mp3_file)
        self.minutes, self.seconds = self.convert(self.info.info.length)
        self.minutes = round(self.minutes)
        self.seconds = round(self.seconds)
        self.totaltime.config(text=str(self.minutes) + ":" + str(self.seconds))
        self.timer = 0
        self.currenttime.config(text="0:00")
        self.playing = False
        self.played = False
        self.progress.set(0)
        self.progress.config(to=self.info.info.length)
        self.play_current()

    def play_current(self):
        self.current_index = (self.current_index) % len(self.mp3_files)
        self.current_mp3_file = os.path.join(self.folder_path, self.mp3_files[self.current_index])
        pygame.mixer.music.load(self.current_mp3_file)
        pygame.mixer.music.play()
        self.label2.config(text=f"{self.mp3_files[self.current_index]}")
        self.playing = True
        self.played = False
        self.progress.set(0)
        self.progress.config(to=self.info.info.length)
        self.update_timebar()
    
    def convert(self,seconds):
        seconds %= 3600
        mins = seconds // 60
        seconds %= 60
        return(mins, seconds)
    
    def loop(self):
        if not self.looping:
            self.looping = True
        else:
            self.looping = False
        self.loopStatus.config(text="looping: "+str(self.looping))
    
    def update_timebar(self):
        if pygame.mixer.music.get_busy() and self.playing:
            current_time_ms = pygame.mixer.music.get_pos()
            current_time_sec = current_time_ms / 1000

            minutes, seconds = divmod(current_time_sec, 60)
            total_length = self.info.info.length
            total_minutes, total_seconds = divmod(total_length, 60)

            self.currenttime.config(text=f"{int(minutes):02}:{int(seconds):02}")
            self.totaltime.config(text=f"{int(total_minutes):02}:{int(total_seconds):02}")
            self.progress.set(current_time_sec)

            if not self.played:
                self.progress.after(1000, self.update_timebar)



    def play_selected(self, event):
        selected_index = self.listbox.curselection()
        if selected_index:
            self.current_index = selected_index[0]
            self.current_mp3_file = os.path.join(self.folder_path, self.mp3_files[self.current_index])
            pygame.mixer.music.load(self.current_mp3_file)
            self.info = MP3(self.current_mp3_file)
            self.minutes, self.seconds = self.convert(self.info.info.length)
            self.minutes = round(self.minutes)
            self.seconds = round(self.seconds)
            self.totaltime.config(text=str(self.minutes) + ":" + str(self.seconds))
            self.timer = 0
            self.currenttime.config(text="0:00")
            self.playing = False
            self.played = False
            self.progress.set(0)
            self.progress.config(to=self.info.info.length)
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
        
    def set_position(self, value):
        if self.playing:
            pygame.mixer.music.pause()
            pygame.mixer.music.set_pos(value)
            pygame.mixer.music.unpause()
            self.playing = True
            self.played = False
            self.update_timebar()
        
    def mainloop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.USEREVENT:
                    self.play_next()

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