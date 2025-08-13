import customtkinter as ctk
from customtkinter import filedialog
from tkinter import messagebox
import manager
import cfgManager
import re
app = ctk.CTk()
app.geometry("800x500")
app.title("Smart File Organizer")

#----commands -----
def open_file():
    filepath = filedialog.askopenfilename(
        title="Select a file",
        filetypes=[("All files", "*.*")]
    )
    if filepath:
        rerult = manager.SortSingleFile(filepath)

def open_directory():
    dirpath = filedialog.askdirectory(title="Select a directory")
    if dirpath:
        result = manager.SortDir(dirpath)



def add_condition():
    window = ctk.CTkToplevel()
    window.geometry("400x300")
    window.title("Add Condition")

    selected_path = ctk.StringVar()
    selected_option = ctk.StringVar()
    param_value = ctk.StringVar()

    optionMenu = ctk.CTkOptionMenu( window, values=["date", "size", "type"], variable=selected_option)
    optionMenu.set("Choose a condition type to organize by.")   
    optionMenu.pack(pady=10, padx=20)

    param_entry = ctk.CTkEntry(window, placeholder_text="Enter value for selected condition", textvariable=param_value)
    param_entry.pack(pady=10, padx=20)

    path_label = ctk.CTkLabel(window, text="No directory selected", text_color="gray")
    path_label.pack(pady=5)

    def open_directory():
        path = filedialog.askdirectory(title="Select a directory")
        if path:
            selected_path.set(path)
            path_label.configure(text=f"Selected: {path}", text_color="green")

    opendirectory = ctk.CTkButton(window, text="Select Directory", command=open_directory)
    opendirectory.pack(pady=10)

    def confirm():
        condition = selected_option.get()
        param = param_value.get()
        path = selected_path.get()

        if not path:
            messagebox.showwarning("Missing Info", "Please select a directory.")
            return
        if not param:
            messagebox.showwarning("Missing Info", "Please enter a value for the condition.")
            return
        if condition == "date" and len(re.findall("[0-9]{4}-[0-9]{2}-[0-9]{2}", param)) == 0:
            messagebox.showwarning("Invalid Format", "Please enter a value in format for YYYY-MM-DD.")
            return
        cfgManager.AddCfg(condition, param, path)
        messagebox.showinfo("Success", f"Condition '{condition}' with value '{param}' added for:\n{path}")
        window.destroy()

    confirm_button = ctk.CTkButton(window, text="Confirm", command=confirm)
    confirm_button.pack(pady=15)

def settings():
    window = ctk.CTkToplevel()
    window.geometry("400x300")
    window.title("Settings")

    selected_path = ctk.StringVar()
    selected_option_first = ctk.StringVar()
    selected_option_second = ctk.StringVar()
    selected_option_third = ctk.StringVar()
    param_value = ctk.StringVar()

    options = ["date", "size", "type"]

    first = ctk.CTkOptionMenu(window, values=options, variable=selected_option_first)
    first.set("Choose the first condition")
    first.pack(pady=10, padx=20)

    def update_second_options(*args):
        new_options = [opt for opt in options if opt != selected_option_first.get()]
        second.configure(values=new_options)
        if selected_option_second.get() not in new_options:
            selected_option_second.set("")

    def update_third_options(*args):
        new_options = [opt for opt in options if opt != selected_option_first.get() and opt != selected_option_second.get()]
        third.configure(values=new_options)
        if selected_option_third.get() not in new_options:
            selected_option_third.set("")

    second = ctk.CTkOptionMenu(window, values=[opt for opt in options if opt != selected_option_first.get()], variable=selected_option_second)
    second.set("Choose the second condition")
    second.pack(pady=15, padx=20)

    third = ctk.CTkOptionMenu(window, values=[opt for opt in options if opt != selected_option_first.get() and opt != selected_option_second.get()], variable=selected_option_third)
    third.set("Choose the third condition")
    third.pack(pady=15, padx=20)

    selected_option_first.trace_add('write', update_second_options)
    selected_option_second.trace_add('write', update_third_options)

    def confirm():
        if not selected_option_first.get() or not selected_option_second.get() or not selected_option_third.get():
            messagebox.showwarning("Missing Info", "Please select all three conditions.")
            return
        messagebox.showinfo("Success", "Successfully customized.")
        window.destroy()

    confirm_button = ctk.CTkButton(window, text="Confirm", command=confirm)
    confirm_button.pack(pady=15)

# ------- design -------

openfile = ctk.CTkButton(app, text="Organize File", command=open_file)
openfile.pack(pady=15)

opendirectory = ctk.CTkButton(app, text="Organize Directory", command=open_directory)
opendirectory.pack(pady=20)

add = ctk.CTkButton(app, text="Add Condition", command=add_condition)
add.pack(pady=25)

settings = ctk.CTkButton(app, text="settings", command=settings)
settings.pack(pady=23)

app.mainloop()