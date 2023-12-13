import os
import pygame
from tkinter import Tk, filedialog, Label, Scale, Button, Frame, Listbox, END, HORIZONTAL, VERTICAL
from definicje import play, play_next, play_prev, play_selected, set_volume, change_folder

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
#Frame po prawej
        List_frame = Frame(master, bg="black")
        List_frame.grid(row=0, column=3, rowspan=4, sticky="w")
#wybieranie folderu
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
                    label1 = Label(text_frame, text="Altualny plik:", bg="black", fg="green")
                    label1.grid(row=0, column=0)
                    label2 = Label(text_frame, text=f"{mp3_files[current_index]}", bg="black", fg="green")
                    label2.grid(row=1, column=0)

                    prev_button = Button(button_frame, text="<", command=play_prev, bg="gray", fg="black", padx="20", pady="20")
                    prev_button.grid(row=1, column=0, sticky="ew")

                    play_button = Button(button_frame, text="II", command=play, bg="gray", fg="black", padx="20", pady="20")
                    play_button.grid(row=1, column=1, sticky="ew")

                    next_button = Button(button_frame, text=">", command=play_next, bg="gray", fg="black", padx="20", pady="20")
                    next_button.grid(row=1, column=2, sticky="ew")

                    volume_label = Label(volume_frame, text="Głośność:", bg="black", fg="green")
                    volume_label.grid(row=0, column=0)

                    volume_slider = Scale(volume_frame, from_=0, to=100, resolution=1, orient=HORIZONTAL,
                                               command=set_volume, bg="black", fg="green", troughcolor="black",
                                               highlightbackground="black", width="15", length="326")
                    volume_slider.set(50)  # Domyślna głośność
                    volume_slider.grid(row=1, column=0, sticky="nsew")

                    listbox = Listbox(List_frame, selectmode="SINGLE", exportselection=0, bg="black", foreground="green", width="56", height="28")
                    listbox.pack()

                    for mp3_file in mp3_files:
                        listbox.insert(END, mp3_file)

                    listbox.bind("<Double-Button-1>", play_selected)

                    library = Button(List_frame, text="Zmień folder", command=change_folder, bg="gray", fg="black", padx="10", pady="5")
                    library.pack()

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