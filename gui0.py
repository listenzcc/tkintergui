# coding: utf-8

import random
import time
import tkinter as tk


class Block(tk.Frame):
    def __init__(self, master, name='Block', bg=None):
        tk.Frame.__init__(self, master)

        if bg is None:
            self['bg'] = random_color()
        else:
            self['bg'] = bg
        self.fg = good_fg(self['bg'])
        self.name = name
        self.set_labels()

    def set_labels(self):
        self.labels = dict()
        self.labels['head'] = tk.Label(
            self, text=self.name, bg=self['bg'], fg=self.fg)
        self.labels['head'].place(relx=0, rely=0)
        self.labels['foot'] = tk.Label(
            self, text=time.ctime(), bg=self['bg'], fg=self.fg)
        self.labels['foot'].place(relx=1, rely=1, anchor='se')
        for label in self.labels.values():
            label.pi = label.place_info()


def random_color():
    return '#' + ''.join([random.choice('0123456789ABCDEF') for j in range(6)])


def good_fg(bg):
    if sum([int(bg[i:i+2], 16) for i in [1, 3, 5]]) < 200:
        return 'white'
    else:
        return 'black'


root = tk.Tk()
root.geometry('800x600+100+200')
root.resizable(False, False)

block = Block(root, name='Block 1')
block.place(relx=0.2, rely=0.3, width=200, height=100)

root.mainloop()
