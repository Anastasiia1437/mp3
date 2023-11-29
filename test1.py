import tkinter as tk

def zmien_nazwe_przycisku():
    aktualna_nazwa = przycisk.cget("text")
    
    # Zamień nazwę przycisku na inną
    nowa_nazwa = "Nowa Nazwa" if aktualna_nazwa != "Nowa Nazwa" else "Stara Nazwa"
    przycisk.config(text=nowa_nazwa)

root = tk.Tk()

# Tworzenie przycisku
przycisk = tk.Button(root, text="Stara Nazwa", command=zmien_nazwe_przycisku)
przycisk.pack(pady=20)

root.mainloop()
