# coding: utf-8

from psychopy import visual, core, event
import os
import random
import time
import numpy as np
import tkinter as tk
import pickle
from tkinter import ttk
from tkinter import filedialog
from myClassifiers import CSP_classifier, FBCSP_classifier


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
        # self.labels['foot'].place(relx=1, rely=1, anchor='se')
        for label in self.labels.values():
            label.pi = label.place_info()


def random_color():
    rand_string = 'ABCDEF'  # '0123456789ABCDEF'
    return '#' + ''.join([random.choice(rand_string) for j in range(6)])


def good_fg(bg):
    if sum([int(bg[i:i+2], 16) for i in [1, 3, 5]]) < 200:
        return 'white'
    else:
        return 'black'


def combobox_enter_pressed(_event):
    # Add new entry if <Enter Key> is pressed
    if _event.keycode != 13:
        return

    cb = _event.widget
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

    def update_date(_event):
        widget = _event.widget
        widget['text'] = time.strftime('%Y-%m-%d-%H-%M-%S')

    label_date.bind('<Button-1>', update_date)

    return label_date_label, label_date


def add_components_subject_sex(master):
    combobox = ttk.Combobox(master, textvariable=tk.StringVar(), width=15)
    combobox.bind('<Key>', combobox_enter_pressed)
    history_subjects = ['Female', 'Male']  # , 'Chaos']
    history_subjects.sort()
    combobox['values'] = history_subjects
    combobox.current(0)

    label = tk.Label(master, text='Sex:')

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


def perform_task(task_name):
    win = visual.Window()
    msg = visual.TextStim(win, text=task_name)
    msg.draw()
    win.flip()

    table = {'屈 肘': 'quzhou',
             '伸 臂': 'shenchu',
             '前 屈': 'taiqi',
             '侧 展': 'waizhan'}
    task_name = table[task_name]

    pics_dir = os.path.join('movie_4D', 'pics')
    n = len([s for s in os.listdir(pics_dir) if s.startswith(task_name)])
    s = 4 / (n-1)

    imgs = [visual.ImageStim(win, image=os.path.join(
        pics_dir, '%s_%d.png' % (task_name, j))) for j in range(n)]

    # event.waitKeys()

    t = time.time()
    for j, img in enumerate(imgs):
        img.draw()
        win.flip()
        while (time.time()-t) < s*j:
            pass
    print(time.time()-t)

    win.close()


def add_components_experiment_task(master):
    task_name = ['屈 肘',
                 '伸 臂',
                 '前 屈',
                 '侧 展']
    radiobuttons = task_name.copy()
    var = tk.StringVar()
    for i, e in enumerate(task_name):
        radiobuttons[i] = tk.Radiobutton(master, variable=var, text=e, value=e)
    var.set(task_name[0])

#     button = tk.Button(master=master, text='>',
#                        command=lambda: print(var.get()))

    button = tk.Button(master=master, text='>',
                       command=lambda: perform_task(var.get()))

    return radiobuttons, var, button


def add_components_counter(master, text='5'):
    label_count = tk.Label(master, text=text)

    def _add():
        x = int(label_count['text'])
        if x < 100:
            label_count['text'] = '%d' % (x+1)

    def _sub():
        x = int(label_count['text'])
        if x > 1:
            label_count['text'] = '%d' % (x-1)

    button_s1 = tk.Button(master, text='-1', command=_sub)
    button_a1 = tk.Button(master, text='+1', command=_add)

    label_note = tk.Label(master, text='Counter')

    return label_note, label_count, button_s1, button_a1


def add_components_connection_info(master):
    combobox_IP = ttk.Combobox(master, textvariable=tk.StringVar(), width=15)
    combobox_IP.bind('<Key>', combobox_enter_pressed)
    IPs = ['192.168.1.103']
    combobox_IP['values'] = IPs
    combobox_IP.current(0)

    combobox_port = ttk.Combobox(master, textvariable=tk.StringVar(), width=15)
    combobox_port.bind('<Key>', combobox_enter_pressed)
    ports = ['4000']
    combobox_port['values'] = ports
    combobox_port.current(0)

    label_IP = tk.Label(master, text='IP:')
    label_port = tk.Label(master, text='port:')

    button_disconnect = tk.Button(master, text='Disconnect')

    return combobox_IP, combobox_port, label_IP, label_port, button_disconnect


def add_components_model_training(master):
    label_data_select = tk.Label(master, text='实验文件')

    text_file_name = tk.Text(master, height=3, width=20)
    text_file_name.insert(tk.INSERT, os.path.join('last_data', 'last.pkl'))

    def select_file():
        fname = filedialog.askopenfilename()
        print('Model training: %s selected.' % fname)
        text_file_name.delete(1.0, tk.END)
        text_file_name.insert(tk.INSERT, fname)

    button_select = tk.Button(master, text='选择实验文件', command=select_file)

    def model_train():
        ##############
        # This function is to TRAINING a model using experiment data
        # Todo: A function training model,
        #       return training accuracy and model file

        # Fetch experiment_file_path from textbox: text_file_name
        experiment_file_path = text_file_name.get(1.0, tk.END)[:-1]


        with open(experiment_file_path, 'rb') as f:
            d = pickle.load(f)

        num_sample = len(d)
        shape = d[0][0].shape
        train_x = np.empty([num_sample, shape[0], shape[1]])
        train_y = np.empty([num_sample, 1])
        for j, e in enumerate(d):
            train_x[j] = e[0]
            train_y[j] = e[1]

        print(train_x.shape, train_y.shape)

        # Defence code: experiment_file_path should exist
        # assert(os.path.exists(experiment_file_name))

        # Train a model
        # I suggest saving the model_file in 'models' folder
        # [acc, model_file] = model_train_on_data(experiment_file_name)
        cla = CSP_classifier()
        # train_x:(None, 62, 4000), train_y:(None, 1)
        acc = cla.fit(train_x, train_y)  
        
        # acc = random.choice(range(70, 100))
        # save the fitted model
        model_file_path = os.path.join('last_model',
                                       os.path.basename(experiment_file_path)+'_fitted_model.pkl')
        with open(model_file_path, 'wb') as f:
            pickle.dump(cla, f)

        # Report
        print('Experiment file is %s, model is %s, accuracy is %f' % (
            experiment_file_path, model_file_path, acc))
        label_score_output['text'] = '%d%%' % (acc * 100)

    button_train = tk.Button(master, text='开始模型训练', command=model_train)

    label_score = tk.Label(master, text='得分')

    label_score_output = tk.Label(master, text='--')

    return label_data_select, button_select, text_file_name, button_train, label_score, label_score_output


def add_components_model_selection(master):
    label_model_select = tk.Label(master, text='模型文件')

    text_file_name = tk.Text(master, height=3, width=20)
    text_file_name.insert(tk.INSERT, os.path.join('last_model', 'last.pkl_fitted_model.pkl'))

    def select_file():
        fname = filedialog.askopenfilename()
        print('Model selecting: %s selected.' % fname)
        text_file_name.delete(1.0, tk.END)
        text_file_name.insert(tk.INSERT, fname)

    button_select = tk.Button(master, text='选择模型文件', command=select_file)

    return label_model_select, text_file_name, button_select


def add_components_profile_selection(master):
    button_save = tk.Button(master, text='保存设置')
    button_load = tk.Button(master, text='载入设置')

    label = tk.Label(master, text='设置名称')

    combobox = ttk.Combobox(master, textvariable=tk.StringVar(), width=15)
    names = os.listdir('profiles')
    combobox['values'] = names
    if names:
        combobox.current(0)

    return label, combobox, button_save, button_load
