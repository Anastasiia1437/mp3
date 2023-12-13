import os
import pygame
from tkinter import Tk, filedialog, Label, Scale, Button, Frame, Listbox, END, HORIZONTAL, VERTICAL

class SimpleMP3Player:
    def __init__(self, master):
        self.master = master
        master.title("Odtwarzacz MP3")
        master.geometry("679x500")
        master.configure(bg="black")
        master.resizable(False, False)

        self.current_file = None
        self.playing = False
#Frames po lewej
        text_frame = Frame(master, bg="pink",pady=5)
        text_frame.grid(row=0, column=0, columnspan=3, sticky="nsew")

        anim_frame = Frame(master, bg="red",pady=5)
        anim_frame.grid(row=1, column=0, columnspan=3, sticky="nsew")

        button_frame = Frame(master, bg="blue")
        button_frame.grid(row=2, column=0, columnspan=3, sticky="s")

        volume_frame = Frame(master, bg="red")
        volume_frame.grid(row=3, column=0, columnspan=3, sticky="s")
#Frame po lewej
        List_frame = Frame(master, bg="black")
        List_frame.grid(row=0, column=3, rowspan=4, sticky="w")
#wybieranie folderu
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

                    self.prev_button = Button(button_frame, text="<", command=self.play_prev, bg="gray", fg="black", padx="20", pady="20")
                    self.prev_button.grid(row=1, column=0, sticky="ew")

                    self.play_button = Button(button_frame, text="II", command=self.play, bg="gray", fg="black", padx="20", pady="20")
                    self.play_button.grid(row=1, column=1, sticky="ew")

                    self.next_button = Button(button_frame, text=">", command=self.play_next, bg="gray", fg="black", padx="20", pady="20")
                    self.next_button.grid(row=1, column=2, sticky="ew")

                    self.volume_label = Label(volume_frame, text="Głośność:", bg="black", fg="green")
                    self.volume_label.grid(row=0, column=0)

                    self.volume_slider = Scale(volume_frame, from_=0, to=100, resolution=1, orient=HORIZONTAL,
                                               command=self.set_volume, bg="black", fg="green", troughcolor="black",
                                               highlightbackground="black", width="15", length="326")
                    self.volume_slider.set(50)  # Domyślna głośność
                    self.volume_slider.grid(row=1, column=0, sticky="nsew")

                    self.listbox = Listbox(List_frame, selectmode="SINGLE", exportselection=0, bg="black", foreground="green", width="56", height="31")
                    self.listbox.pack()

                    for mp3_file in self.mp3_files:
                        self.listbox.insert(END, mp3_file)

                    self.listbox.bind("<Double-Button-1>", self.play_selected)

                    

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