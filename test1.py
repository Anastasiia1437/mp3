import tkinter as tk

root = tk.Tk()

frame1 = tk.Frame(root, width=200, height=200, bg='red')
frame2 = tk.Frame(root, width=200, height=200, bg='green')
frame3 = tk.Frame(root, width=200, height=200, bg='blue')

# Ustawienie orientacji na HORIZONTAL
paned_window = tk.PanedWindow(root, orient=tk.HORIZONTAL)

paned_window.add(frame1)
paned_window.add(frame2)
paned_window.add(frame3)

paned_window.pack(fill=tk.BOTH, expand=True)

root.mainloop()
