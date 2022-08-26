import os
import platform
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import customtkinter as ctk
from stat import S_IREAD, S_IRGRP, S_IROTH, S_IWUSR
import json

# tester_file = "tester.txt"

# read only
# os.chmod(tester_file, S_IREAD)

# write only
# os.chmod(tester_file, S_IWUSR)

# read & write
# os.chmod(tester_file, S_IWUSR|S_IREAD)



class App:

    def __init__(self, root):
        self.root = root
        self.root.geometry('410x310')
        self.root.title('BL2 R.O.S')
        ctk.set_default_color_theme(current_path + 'theme.json')
        self.image = tk.PhotoImage(file=current_path + 'vault.png')
        self.state = tk.StringVar()
        self.build()

    def build(self):
        title_lbl = ctk.CTkLabel(self.root, text="BL2 Read Only Setter", text_font='Arial 30 bold')
        self.lbox = tk.Listbox(self.root, height=len(self.files), width=12)
        read_only_btn = ctk.CTkButton(self.root, text='Read Only',height=2, width=120, command=self.set_read_only)
        read_write_btn = ctk.CTkButton(self.root, text='Read & Write',height=2, width=120, command=self.set_read_and_write)
        all_read_write_btn = ctk.CTkButton(self.root, text='All Read & Write',height=2, width=120, command=self.set_all_read_and_write)
        img_lbl = ctk.CTkLabel(self.root, image=self.image)
        state_lbl = ctk.CTkLabel(self.root, textvariable=self.state)

        title_lbl.grid(row=0,column=0, padx=8, pady=0.5, columnspan=2)
        self.lbox.grid(row=1, column=0, padx=8, pady=0.5)
        read_only_btn.grid(row=2, column=0, padx=8, pady=0.5)
        read_write_btn.grid(row=3, column=0, padx=8, pady=0.5)
        all_read_write_btn.grid(row=4, column=0, padx=8, pady=0.5)
        img_lbl.grid(row=1, column=1, rowspan=6, sticky='s')
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
        webbrowser.open("")

    def report_issue(self):
        webbrowser.open("")

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
        files = [f for f in files if f[-1] == 'v'] # add path to each file
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

def launch_screen(root):
    lbl = ctk.CTkLabel(root, text='tester')
    set_save_folder_btn = ctk.CTkButton(root, text='set save fodler', command=lambda: set_save_folder(root))
    end_btn = ctk.CTkButton(root, text='Continue', command=launch_main_program)

    lbl.pack()
    set_save_folder_btn.pack()
    end_btn.pack()

def main():
    global current_path
    global img
    global path_to_saves

    slash = '/' if 'macOS' in platform.platform() else '\\'

    current_path = os.path.dirname(os.path.abspath(__file__)) + slash
    img = Image.open(current_path + 'vault.png')

    with open(current_path + 'saves.txt', 'r') as f:
        path_to_saves = f.read().strip() + slash

    if path_to_saves == '':
        first_run_root = ctk.CTk()
        launch_screen(first_run_root)
        first_run_root.mainloop()
    root = ctk.CTk()
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()
