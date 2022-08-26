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
    WIDTH, HEIGHT = 120, 10 
    TITLE_FONT = 'Arial 30 bold'
    GEO = '390x320'
    IMAGE_SIZE = int(260*0.8), int(281*0.8)
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
        self.root.iconphoto(False, self.image)

        self.state = tk.StringVar()
        self.build()

    def build(self):
        title_lbl = ctk.CTkLabel(self.root, text="BL2 Read Only Setter", text_font=TITLE_FONT)
        main_frame = ctk.CTkFrame(self.root, width=155, height=220, corner_radius=10)

        self.lbox = tk.Listbox(main_frame, height=len(self.files), width=13)
        read_only_btn = ctk.CTkButton(main_frame, text='Read Only', height=HEIGHT, width=WIDTH, command=self.set_read_only)
        read_write_btn = ctk.CTkButton(main_frame, text='Read & Write', height=HEIGHT, width=WIDTH, command=self.set_read_and_write)
        all_read_write_btn = ctk.CTkButton(main_frame, text='All Read & Write', height=HEIGHT, width=WIDTH, command=self.set_all_read_and_write)

        state_lbl = ctk.CTkLabel(self.root, textvariable=self.state)
        img_lbl = ctk.CTkLabel(self.root, image=self.image, width=4, height=4)

        title_lbl.place(relx=0.1)
        main_frame.place(relx=0.03, rely=0.15)
        self.lbox.place(relx=0.1, rely=0.05)
        read_only_btn.place(relx=0.1, rely=0.55)
        read_write_btn.place(relx=0.1, rely=0.70)
        all_read_write_btn.place(relx=0.1, rely=0.85)

        state_lbl.place(relx=0.03, rely=0.85)
        img_lbl.place(relx=0.45, rely=0.15)

        self.lbox.bind("<<ListboxSelect>>", self.on_select)

        for file in self.files:
            if file in characters.keys():
                self.lbox.insert('end', characters[file])
            else:
                self.lbox.insert('end', file)

        self.create_menu_bar()

    def create_menu_bar(self):
        menubar = tk.Menu(self.root)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Set Saves Folder", command=self.set_save_folder)
        filemenu.add_separator()
        filemenu.add_command(label="Set Save Alias", command=self.set_save_alias)
        filemenu.add_command(label="Remove Save Alias", command=self.remove_save_alias)
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
        file = active if ".sav" in active else inv_characters[active]
        os.chmod(path_to_saves + file, S_IREAD|S_IRGRP|S_IROTH)
        self.state.set('Read Only')

    def set_read_and_write(self):
        active = self.lbox.get(tk.ACTIVE)
        file = active if ".sav" in active else inv_characters[active]
        os.chmod(path_to_saves + file, S_IWUSR|S_IREAD)
        self.state.set('Read & Write')

    def set_all_read_and_write(self):
        for i in self.files:
            os.chmod(path_to_saves +  i, S_IWUSR|S_IREAD)
        self.state.set('Read & Write')

    def on_select(self, event=None):
        active = event.widget.get(event.widget.curselection())
        file = active if ".sav" in active else inv_characters[active]
        try:
            with open(path_to_saves +  file, 'w') as s:
                self.state.set('Read & Write')
        except PermissionError:
            self.state.set('Read Only')

    def set_save_folder(self):
        folder = filedialog.askdirectory()
        with open(current_path + 'saves.txt', 'w') as f:
            f.write(folder)
        restart(self.root)

    def set_save_alias(self):
        def apply():
            alias = alias_ent.get()
            characters[os.path.basename(file)] = alias
            with open(current_path + 'characters.json', 'w') as f:
                f.write(json.dumps(characters, indent=4))
            restart(self.root)
        file = filedialog.askopenfilename(initialdir=path_to_saves)
        file = os.path.basename(file)

        top = ctk.CTkToplevel(self.root)
        top.geometry("150x100")

        file_lbl = ctk.CTkLabel(top, text=file)
        alias_ent = ctk.CTkEntry(top, width=200)
        apply_btn = ctk.CTkButton(top, text='Apply', command=apply)

        file_lbl.pack()
        alias_ent.pack()
        apply_btn.pack()

    def remove_save_alias(self):
        def remove():
            active = lbox.get(tk.ACTIVE)
            split = active.split(" : ")
            file = split[0]
            print(split)
            del characters[file]
            with open(current_path + 'characters.json', 'w') as f:
                f.write(json.dumps(characters))
            restart(self.root)

        top = ctk.CTkToplevel(self.root)

        lbox = tk.Listbox(top, height=12)
        remove_btn = ctk.CTkButton(top, text='Remove', command=remove)

        lbox.pack()
        remove_btn.pack()

        for file, char in characters.items():
            lbox.insert('end', f"{file} : {char}")

    @property
    def files(self):
        os.chdir(path_to_saves)
        files = filter(os.path.isfile, os.listdir(path_to_saves))
        files = [f for f in files if f[-1] == 'v' and f[0] != '.'] # add path to each file
        files.sort(key=os.path.getmtime)
        files.reverse()
        files = files[0:7]
        return files

def restart(root):
    root.destroy()
    main()

def main():
    global current_path
    global img
    global path_to_saves
    global characters
    global inv_characters

    slash = '/' if 'macOS' in platform.platform() else '\\'

    current_path = os.path.dirname(os.path.abspath(__file__)) + slash
    img = Image.open(current_path + 'vault.png')

    with open(current_path + 'saves.txt', 'r') as f:
        path_to_saves = f.read().strip() + slash

    with open(current_path + "characters.json", "r") as f:
        characters = json.load(f)
        inv_characters = {v: k for k, v in characters.items()}

    root = ctk.CTk()
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()
