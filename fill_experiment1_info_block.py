# coding: utf-8

import tkinter as tk
from components import add_components_experiment_task, add_components_counter


def build_parts_experiment1_info(master):
    parts = {}

    radiobuttons, var, button = add_components_experiment_task(master=master)
    parts['experiment1_task_var'] = var
    parts['experiment1_task_radiobuttons'] = radiobuttons
    parts['experiment1_task_viewbutton'] = button

    # Counter 1
    label_note, label_count, button_s1, button_a1 = add_components_counter(
        master=master, text='5')
    label_note['text'] = '想象次数'
    parts['experiment1_counter1_label'] = label_note
    parts['experiment1_counter1_value'] = label_count
    parts['experiment1_counter1_button_s1'] = button_s1
    parts['experiment1_counter1_button_a1'] = button_a1

    # Counter 2
    # label_note, label_count, button_s1, button_a1 = add_components_counter(
    #     master=master, text='1')
    # label_note['text'] = '训练轮次'
    # parts['experiment1_counter2_label'] = label_note
    # parts['experiment1_counter2_value'] = label_count
    # parts['experiment1_counter2_button_s1'] = button_s1
    # parts['experiment1_counter2_button_a1'] = button_a1

    # Start button
    button = tk.Button(master=master, text='训练阶段实验开始')
    parts['experiment1_task_gobutton'] = button

    grid_info = dict(experiment1_counter1_label=dict(row=4, column=0),
                     experiment1_counter1_button_s1=dict(row=4, column=1),
                     experiment1_counter1_value=dict(row=4, column=2),
                     experiment1_counter1_button_a1=dict(row=4, column=3),
                     # experiment1_counter2_label=dict(row=5, column=0),
                     # experiment1_counter2_button_s1=dict(row=5, column=1),
                     # experiment1_counter2_value=dict(row=5, column=2),
                     # experiment1_counter2_button_a1=dict(row=5, column=3),
                     )

    for e in grid_info.keys():
        parts[e].grid(row=grid_info[e]['row'], column=grid_info[e]['column'],
                      sticky=tk.NSEW, padx=5, pady=5)

    for i, e in enumerate(parts['experiment1_task_radiobuttons']):
        e.grid(row=i, column=0, sticky=tk.NSEW, padx=5, pady=5, columnspan=3)
    parts['experiment1_task_viewbutton'].grid(
        row=0, column=3, sticky=tk.NSEW, padx=5, pady=5, rowspan=4)
    parts['experiment1_task_gobutton'].grid(
        row=6, column=0, sticky=tk.NSEW, padx=5, pady=5, columnspan=4)

    return parts


def get_experiment1_info(parts):
    info = {}
    info['task_name'] = parts['experiment1_task_var'].get()
    info['counter1_value'] = int(parts['experiment1_counter1_value']['text'])
    # info['counter2_value'] = int(parts['experiment1_counter2_value']['text'])
    return info
