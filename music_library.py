import os
import webbrowser
from tkinter import *
from tkinter import messagebox
from tkinter.font import Font

import pandas as pd
from fuzzywuzzy import fuzz

from index_music_library import index_music_library

if os.path.exists("songs.csv"):
    start_refresh = False
else:
    start_refresh = True
    index_music_library()
    exit(0)


class MusicLibrary(object):
    def __init__(self, master):
        self.paths = []
        self.songs = pd.read_csv("songs.csv")
        master.bind("<Return>", self.open_folder)
        master.geometry('950x500')
        master.resizable(True, True)
        self.menu_init(master)
        self.entry_init(master)
        self.popup_init(master)
        self.list_init(master)

    def entry_init(self, master):
        my_font = Font(size=19)
        self.text = Entry(master, width=100, bg='gray25', font=my_font, fg='gray93', highlightthickness=0, bd=0)
        self.text.bind('<Key>', self.callback)
        self.text.pack()
        self.text.focus()

    def list_init(self, master):
        my_font = Font(size=15)
        self.list = Listbox(master, selectmode=SINGLE, bg='gray19', fg='gray93', highlightthickness=0, bd=0, height=60,
                            width=70, font=my_font)
        self.list.pack()
        self.list.bind("<Double-Button-1>", self.open_folder)
        self.list.bind("<Button-3>", self.popup)  # Button-2 on Aqua
        self.list.bind("<Button-1>", self.popupFocusOut)

    def popup_init(self, master):
        self.popup_menu = Menu(master, tearoff=0, bg='gray25', fg='gray93', )
        self.popup_menu.add_command(label="Show in files",
                                    command=self.open_folder)
        self.popup_menu.add_command(label="Add to vlc",
                                    command=self.add_to_vlc)
        self.popup_menu.add_command(label="Add to audacious",
                                    command=self.add_to_audacious)

    def menu_init(self, master):
        self.menubar = Menu(master, bg='gray10', fg='gray93', bd=0)

        # create a pulldown menu, and add it to the menu bar
        self.filemenu = Menu(self.menubar, tearoff=0, bg='gray13', fg='gray93')
        self.filemenu.add_command(label="Refresh Library", command=self.refresh_library)
        self.filemenu.add_command(label="Help", command=self.open_help)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=master.quit)
        self.menubar.add_cascade(label="Settings", menu=self.filemenu)
        master.config(menu=self.menubar)

    def open_help(self):
        webbrowser.open('https://github.com/panos-stavrianos/music_library')

    def refresh_library(self):
        MsgBox = messagebox.askquestion('Refresh Library', 'This may take a while\nAre you sure you want to continue',
                                        icon='warning')
        if MsgBox == 'yes':
            global start_refresh
            start_refresh = True
            root.destroy()
        else:
            messagebox.showinfo('Return', 'You will now return to the application screen')

    def popupFocusOut(self, event=None):
        self.popup_menu.unpost()

    def popup(self, event):
        try:
            self.paths[self.list.curselection()[0]]
            self.list.select_clear(0, 'end')
            self.list.select_set(self.list.index("@%s,%s" % (event.x, event.y)))
            self.popup_menu.tk_popup(event.x_root, event.y_root + 25, 0)
        except:
            pass
        finally:
            self.popup_menu.grab_release()

    def callback(self, event):

        self.list.event_generate("<<ListboxSelect>>")
        text = (self.text.get() + event.char).replace("\n", "").replace("\r", "")
        songs = self.songs
        songs['score'] = songs.apply(lambda x: fuzz.ratio(x['full_text'], text), axis=1)
        songs = songs.sort_values(by=['score'], ascending=False).head(200)
        self.list.delete(0, 'end')
        self.paths = []

        for i, song in songs.iterrows():
            self.paths.insert(i, song['path'])
            self.list.insert(i,
                             '{} - {} - {}'.format(song['artist'], song['album'], song['title']))

        self.list.select_clear(0, 'end')
        self.list.select_set(0)
        return True

    def open_folder(self, event=None):
        try:
            song_path = self.paths[self.list.curselection()[0]]
            song_folder_path = os.path.abspath(os.path.join(song_path, os.pardir))
            os.system('xdg-open "{}"'.format(song_folder_path))
        except:
            pass

    def add_to_vlc(self, event=None):
        try:
            song_path = self.paths[self.list.curselection()[0]]
            os.system('vlc --one-instance --playlist-enqueue --no-playlist-autostart "{}" &'.format(song_path))
        except:
            pass

    def add_to_audacious(self, event=None):
        try:
            song_path = self.paths[self.list.curselection()[0]]
            os.system('audacious --enqueue "{}" &'.format(song_path))
        except:
            pass


root = Tk()
root.title("Music Library")
root.configure(background='gray19')

app = MusicLibrary(root)

root.mainloop()

if start_refresh:
    index_music_library()
