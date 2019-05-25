# coding: utf-8

import time
import tkinter as tk
from tkinter import ttk
from components import Block


def combobox_enter_pressed(event):
    # Add new entry if <Enter Key> is pressed
    if event.keycode != 13:
        return

    cb = event.widget
    if not isinstance(cb, ttk.Combobox):
        print('Warning:', 'wrong widget called.')
        print('Got:', type(cb), 'instead of', 'tkinter.ttk.Combobox.')
        return

    if cb.current() == -1:
        values = [e for e in cb['values']]
        values.append(cb.get())
        values.sort()
        cb['values'] = values


root = tk.Tk()
root.geometry('800x600+100+200')
root.resizable(False, False)

blocks = {}

block = Block(root, name='Block 1')
block.place(relx=0.2, rely=0.3, width=300, height=400)
blocks['subject_info'] = block

inputs = {}
notes = {}


def add_components_subject_sex(master, inputs, notes):
    # v = tk.IntVar()
    # radiobutton0 = tk.Radiobutton(master, variable=v, text='Female', value=0)
    # radiobutton1 = tk.Radiobutton(master, variable=v, text='Male', value=1)
    # radiobutton2 = tk.Radiobutton(master, variable=v, text='Chaos', value=2)
    # radiobutton0.place(relx=0, rely=0.7, width=70, height=20)
    # radiobutton1.place(relx=0.5, rely=0.7, width=70, height=20)
    # radiobutton2.place(relx=0.7, rely=0.7, width=70, height=20)
    # label = tk.Label(master, text='Sex:')
    # label.place(relx=0, rely=0.7, width=100, height=20, anchor='w')

    combobox = ttk.Combobox(master, textvariable=tk.StringVar())
    combobox.bind('<Key>', combobox_enter_pressed)
    history_subjects = ['Female', 'Male', 'Chaos']
    history_subjects.sort()
    combobox['values'] = history_subjects
    combobox.current(0)
    combobox.grid(row=2, column=1, sticky=tk.NSEW, padx=5, pady=5)

    label = tk.Label(master, text='Name:')
    label.grid(row=2, column=0, sticky=tk.NSEW, padx=5, pady=5)

    inputs['subject_sex'] = combobox
    notes['subject_sex'] = label


add_components_subject_sex(
    master=blocks['subject_info'], inputs=inputs, notes=notes)


def add_components_subject_name(master, inputs, notes):
    combobox = ttk.Combobox(master, textvariable=tk.StringVar())
    combobox.bind('<Key>', combobox_enter_pressed)
    history_subjects = ['Subject I', 'Subject II', 'Subject III']
    history_subjects.sort()
    combobox['values'] = history_subjects
    combobox.current(0)
    combobox.grid(row=0, column=1, sticky=tk.NSEW, padx=5, pady=5)

    label = tk.Label(master, text='Name:')
    label.grid(row=0, column=0, sticky=tk.NSEW, padx=5, pady=5)

    inputs['subject_name'] = combobox
    notes['subject_name'] = label


add_components_subject_name(
    master=blocks['subject_info'], inputs=inputs, notes=notes)


def add_components_subject_age(master, inputs, notes):
    combobox = ttk.Combobox(master)
    combobox.bind('<Key>', combobox_enter_pressed)
    combobox.grid(row=1, column=1, sticky=tk.NSEW, padx=5, pady=5)

    label = tk.Label(master, text='Age:')
    label.grid(row=1, column=0, sticky=tk.NSEW, padx=5, pady=5)

    inputs['subject_age'] = combobox
    notes['subject_age'] = label


add_components_subject_age(
    master=blocks['subject_info'], inputs=inputs, notes=notes)


root.mainloop()
