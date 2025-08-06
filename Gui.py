import customtkinter as ctk
import tkinter as tk
from customtkinter import filedialog
import manager
app = ctk.CTk()
app.geometry("800x500")
app.title("Smart File Organizer")

#----commands -----
def open_file():
    filepath = filedialog.askopenfilename(
        title="Select a file",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )
    if filepath:
        rerult = manager.SortSingleFile(filepath)

def open_directory():
    dirpath = filedialog.askdirectory(title="Select a directory")
    if dirpath:
        result = manager.SortDir(dirpath)
# ------- design -------

openfile = ctk.CTkButton(app, text="Open File", command=open_file)
openfile.pack(pady=15)

opendirectory = ctk.CTkButton(app, text="Open Directory", command=open_directory)
opendirectory.pack(pady=20)

add = ctk.CTkButton(app, text="Add Condition")
add.pack(pady=25)

settings = ctk.CTkButton(app, text="settings")
settings.pack(pady=23)

app.mainloop()