import os
import platform
import json
from stat import S_IREAD, S_IRGRP, S_IROTH, S_IWUSR
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import customtkinter as ctk
import webbrowser

# tester_file = "tester.txt"

# read only
# os.chmod(tester_file, S_IREAD)

# write only
# os.chmod(tester_file, S_IWUSR)

# read & write
# os.chmod(tester_file, S_IWUSR|S_IREAD)

if 'macOS' in platform.platform():
    PADX, PADY = 8, 0.5
    WIDTH, HEIGHT = 0, 0
    TITLE_FONT = 'Arial 30 bold'
    GEO = '410x310'
else:
    PADX, PADY = 10, 5
    WIDTH, HEIGHT = 0, 0
    TITLE_FONT = 'Arial 24 bold'
    GEO = '360x310'

IMAGE_SIZE = int(260*1.5), int(281*1.5)

class App:

    def __init__(self, root):
        self.root = root
        self.root.geometry(GEO)
        self.root.title('BL2 R.O.S')
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme(current_path + 'theme.json')
        img = Image.open(current_path + 'vault.png')
        resize_img = img.resize(IMAGE_SIZE)
        self.image = ImageTk.PhotoImage(resize_img)
        self.state = tk.StringVar()
        self.root.iconphoto(False, self.image)
        self.build()

    def build(self):
        title_lbl = ctk.CTkLabel(self.root, text="BL2 Read Only Setter", text_font=TITLE_FONT)
        self.lbox = tk.Listbox(self.root, height=len(self.files), width=12)
        read_only_btn = ctk.CTkButton(self.root, text='Read Only',height=2, width=120, command=self.set_read_only)
        read_write_btn = ctk.CTkButton(self.root, text='Read & Write',height=2, width=120, command=self.set_read_and_write)
        all_read_write_btn = ctk.CTkButton(self.root, text='All Read & Write',height=2, width=120, command=self.set_all_read_and_write)
        img_lbl = ctk.CTkLabel(self.root, image=self.image, width=4, height=4)
        state_lbl = ctk.CTkLabel(self.root, textvariable=self.state)

        title_lbl.grid(row=0,column=0, padx=PADX, pady=PADY, columnspan=2)
        self.lbox.grid(row=1, column=0, padx=PADX, pady=PADY)
        read_only_btn.grid(row=2, column=0, padx=PADX, pady=PADY)
        read_write_btn.grid(row=3, column=0, padx=PADX, pady=PADY)
        all_read_write_btn.grid(row=4, column=0, padx=PADX, pady=PADY)
        img_lbl.grid(row=1, column=1, rowspan=6)
        state_lbl.grid(row=5, column=0, padx=8, pady=0.5)

        self.lbox.bind("<<ListboxSelect>>", self.on_select)

        for i in self.files:
            self.lbox.insert('end', i)

        self.create_menu_bar()

    def create_menu_bar(self):
        menubar = tk.Menu(self.root)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Set Saves Folder", command=lambda: set_save_folder(self.root))
        menubar.add_cascade(label="File", menu=filemenu)

        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="About", command=self.about)
        helpmenu.add_command(label="Report Issue", command=self.report_issue)
        menubar.add_cascade(label="Help", menu=helpmenu)

        self.root.config(menu=menubar)

    def about(self):
        webbrowser.open("https://github.com/NyanBlak/BL2ReadOnlyApp")

    def report_issue(self):
        webbrowser.open("https://github.com/NyanBlak/BL2ReadOnlyApp/issues")

    def set_read_only(self):
        active = self.lbox.get(tk.ACTIVE)
        os.chmod(path_to_saves + active, S_IREAD|S_IRGRP|S_IROTH)
        self.state.set('Read Only')

    def set_read_and_write(self):
        active = self.lbox.get(tk.ACTIVE)
        os.chmod(path_to_saves + active, S_IWUSR|S_IREAD)
        self.state.set('Read & Write')

    def set_all_read_and_write(self):
        for i in self.files:
            os.chmod(path_to_saves +  i, S_IWUSR|S_IREAD)
        self.state.set('Read & Write')

    def on_select(self, event=None):
        active = event.widget.get(event.widget.curselection())
        try:
            with open(path_to_saves +  active, 'w') as s:
                self.state.set('Read & Write')
        except PermissionError:
            self.state.set('Read Only')

    @property
    def files(self):
        os.chdir(path_to_saves)
        files = filter(os.path.isfile, os.listdir(path_to_saves))
        files = [f for f in files if f[-1] == 'v' and f[0] != '.'] # add path to each file
        files.sort(key=os.path.getmtime)
        files.reverse()
        files = files[0:7]
        return files

def set_save_folder(root):
    folder = filedialog.askdirectory()
    with open(current_path + 'saves.txt', 'w') as f:
        f.write(folder)
    root.destroy()
    main()

def launch_main_program():
    with open('saves.txt', 'r') as f:
        content = f.read()
        if content == '':
            messagebox.showerror(title='ERROR!', message='No Saves folder selected')
        else:
            print(content)

def main():
    global current_path
    global img
    global path_to_saves

    slash = '/' if 'macOS' in platform.platform() else '\\'

    current_path = os.path.dirname(os.path.abspath(__file__)) + slash
    img = Image.open(current_path + 'vault.png')

    with open(current_path + 'saves.txt', 'r') as f:
        path_to_saves = f.read().strip() + slash

    root = ctk.CTk()
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()
