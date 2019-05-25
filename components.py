# coding: utf-8

import random
import time
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog


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
        self.set_panel()

    def set_panel(self):
        self.panel = tk.Frame(self)
        self.panel.place(relx=0.5, rely=0.5, relwidth=0.8,
                         relheigh=0.8, anchor='c')

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


def add_components_date(master):
    label_date_label = tk.Label(master, text='Date:')
    label_date = tk.Label(master, text=time.strftime('%Y-%m-%d-%H-%M-%S'))

    def update_date(event):
        label_date['text'] = time.strftime('%Y-%m-%d-%H-%M-%S')

    label_date.bind('<Button-1>', update_date)

    return label_date_label, label_date


def add_components_subject_sex(master):
    combobox = ttk.Combobox(master, textvariable=tk.StringVar(), width=15)
    combobox.bind('<Key>', combobox_enter_pressed)
    history_subjects = ['Female', 'Male', 'Chaos']
    history_subjects.sort()
    combobox['values'] = history_subjects
    combobox.current(0)

    label = tk.Label(master, text='Name:')

    return combobox, label


def add_components_subject_name(master):
    combobox = ttk.Combobox(master, textvariable=tk.StringVar(), width=15)
    combobox.bind('<Key>', combobox_enter_pressed)
    history_subjects = ['Subject I', 'Subject II', 'Subject III']
    history_subjects.sort()
    combobox['values'] = history_subjects
    combobox.current(0)

    label = tk.Label(master, text='Name:')

    return combobox, label


def add_components_subject_age(master):
    combobox = ttk.Combobox(master, width=15)
    combobox.bind('<Key>', combobox_enter_pressed)
    ages = ['27']
    combobox['values'] = ages
    combobox.current(0)

    label = tk.Label(master, text='Age:')

    return combobox, label


def add_components_experiment_task(master):
    task_name = ['Quzhou ',
                 'Shenchu',
                 'Taishou',
                 'Waizhan']
    radiobuttons = task_name.copy()
    var = tk.StringVar()
    for i, e in enumerate(task_name):
        radiobuttons[i] = tk.Radiobutton(master, variable=var, text=e, value=e)
    var.set(task_name[0])

    button = tk.Button(master=master, text='>',
                       command=lambda: print(var.get()))

    return radiobuttons, var, button


def add_components_counter(master):
    label_count = tk.Label(master, text='5')

    def _add():
        x = int(label_count['text'])
        if x < 10:
            label_count['text'] = '%d' % (x+1)

    def _sub():
        x = int(label_count['text'])
        if x > 0:
            label_count['text'] = '%d' % (x-1)

    button_s1 = tk.Button(master, text='-1', command=_sub)
    button_a1 = tk.Button(master, text='+1', command=_add)

    label_note = tk.Label(master, text='Counter')

    return label_note, label_count, button_s1, button_a1


def add_components_connection_info(master):
    combobox_IP = ttk.Combobox(master, textvariable=tk.StringVar(), width=15)
    combobox_IP.bind('<Key>', combobox_enter_pressed)
    IPs = ['192.168.1.1']
    combobox_IP['values'] = IPs
    combobox_IP.current(0)

    combobox_port = ttk.Combobox(master, textvariable=tk.StringVar(), width=15)
    combobox_port.bind('<Key>', combobox_enter_pressed)
    ports = ['2000']
    combobox_port['values'] = ports
    combobox_port.current(0)

    label_IP = tk.Label(master, text='IP:')
    label_port = tk.Label(master, text='port:')

    return combobox_IP, combobox_port, label_IP, label_port


def add_components_model_training(master):
    label_data_select = tk.Label(master, text='Select Data')

    text_file_name = tk.Text(master, height=3, width=20)

    def select_file():
        fname = filedialog.askopenfilename()
        print('Model training: %s selected.' % fname)
        text_file_name.delete(1.0, tk.END)
        text_file_name.insert(tk.INSERT, fname)

    button_select = tk.Button(master, text='Select', command=select_file)

    button_train = tk.Button(master, text='Train')

    label_score = tk.Label(master, text='Score')

    label_score_output = tk.Label(master, text='--')

    return label_data_select, button_select, text_file_name, button_train, label_score, label_score_output


def add_components_model_selection(master):
    label_model_select = tk.Label(master, text='Select Model')

    text_file_name = tk.Text(master, height=3, width=20)

    def select_file():
        fname = filedialog.askopenfilename()
        print('Model selecting: %s selected.' % fname)
        text_file_name.delete(1.0, tk.END)
        text_file_name.insert(tk.INSERT, fname)

    button_select = tk.Button(master, text='Select', command=select_file)

    return label_model_select, text_file_name, button_select
