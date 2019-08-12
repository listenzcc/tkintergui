# coding: utf-8

import tkinter as tk
import random


class Component_number(tk.Frame):
    def __init__(self, master,
                 name='name:', num=13, limit=[1, 1e9], small=1, large=5):
        tk.Frame.__init__(self, master)
        self['bg'] = "#" + \
            ''.join([random.choice('0123456789ABCDEF') for j in range(6)])

        self.name = name
        self.num = num
        self.limit = limit
        self.small = small
        self.large = large
        self.init_parts()

        self.update_parts()

        self.place_parts()

    def event_button_click(self, command):
        num = self.num
        if command == 'sub_small':
            self.num -= self.small
        if command == 'sub_large':
            self.num -= self.large
        if command == 'add_small':
            self.num += self.small
        if command == 'add_large':
            self.num += self.large
        if self.num < self.limit[0] or self.num > self.limit[1]:
            self.num = num
        self.update_parts()

    def init_parts(self):
        self.labels = {}
        self.labels['title'] = tk.Label(self, text=self.name)
        self.labels['num'] = tk.Label(self)
        self.buttons = {}
        for command in ['sub_small', 'sub_large', 'add_small', 'add_large']:
            self.buttons[command] = tk.Button(
                self, command=lambda c=command: self.event_button_click(c))

    def update_parts(self):
        self.labels['num']['text'] = '%d' % self.num
        self.buttons['sub_small']['text'] = '-%d' % self.small
        self.buttons['sub_large']['text'] = '-%d' % self.large
        self.buttons['add_small']['text'] = '+%d' % self.small
        self.buttons['add_large']['text'] = '+%d' % self.large

    def place_parts(self):
        self.labels['title'].place(relx=0.5, rely=0.1, anchor='n')
        self.buttons['sub_large'].place(relx=0.1, rely=0.5, anchor='c')
        self.buttons['sub_small'].place(relx=0.3, rely=0.5, anchor='c')
        self.labels['num'].place(relx=0.5, rely=0.5, anchor='c')
        self.buttons['add_small'].place(relx=0.7, rely=0.5, anchor='c')
        self.buttons['add_large'].place(relx=0.9, rely=0.5, anchor='c')

        def set_pi(e):
            e.pi = e.place_info()

        [set_pi(e) for e in self.buttons.values()]

    def hide_buttons(self):
        [e.place_forget() for e in self.buttons.values()]

    def show_buttons(self):
        [e.place(e.pi) for e in self.buttons.values()]


root = tk.Tk()
root.geometry('800x600+100+200')
root.resizable(False, False)


f1 = tk.Frame(root, width=200, height=100)
comp_num1 = Component_number(f1)
comp_num1.place(width=200, height=100)
f2 = tk.Frame(root, width=200, height=100)
comp_num2 = Component_number(f2, name='zzzz')
comp_num2.place(width=200, height=100)

f1.pack()
f2.pack()


# comp_num.place(dict(relx=0.2, rely=0.3, width=200, height=100))

# comp_num.place(dict(relx=0.2, rely=0.3, width=200, height=100))

b1 = tk.Button(root, text='hide', command=comp_num1.hide_buttons)
b1.pack()
b2 = tk.Button(root, text='show', command=comp_num1.show_buttons)
b2.pack()

root.mainloop()
