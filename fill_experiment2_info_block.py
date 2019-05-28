# coding: utf-8

import tkinter as tk
from components import add_components_experiment_task, add_components_counter, add_components_model_selection


def build_parts_experiment2_info(master):
    parts = {}

    radiobuttons, var, button = add_components_experiment_task(master=master)
    parts['experiment2_task_var'] = var
    parts['experiment2_task_radiobuttons'] = radiobuttons
    parts['experiment2_task_viewbutton'] = button

    label_note, label_count, button_s1, button_a1 = add_components_counter(
        master=master)
    label_note['text'] = 'Counter I'
    parts['experiment2_counter1_label'] = label_note
    parts['experiment2_counter1_value'] = label_count
    parts['experiment2_counter1_button_s1'] = button_s1
    parts['experiment2_counter1_button_a1'] = button_a1

    label_note, label_count, button_s1, button_a1 = add_components_counter(
        master=master)
    label_note['text'] = 'Counter II'
    parts['experiment2_counter2_label'] = label_note
    parts['experiment2_counter2_value'] = label_count
    parts['experiment2_counter2_button_s1'] = button_s1
    parts['experiment2_counter2_button_a1'] = button_a1

    button = tk.Button(master=master, text='Go!!!',
                       command=lambda: print('Experiment II starts.'))
    parts['experiment2_task_gobutton'] = button

    label_model_select, text_file_name, button_select = add_components_model_selection(
        master=master)
    parts['experiment2_label_selectdata'] = label_model_select
    parts['experiment2_button_selectdata'] = button_select
    parts['experiment2_text_file_path'] = text_file_name

    grid_info = dict(experiment2_counter1_label=dict(row=4, column=0),
                     experiment2_counter1_button_s1=dict(row=4, column=1),
                     experiment2_counter1_value=dict(row=4, column=2),
                     experiment2_counter1_button_a1=dict(row=4, column=3),
                     experiment2_counter2_label=dict(row=5, column=0),
                     experiment2_counter2_button_s1=dict(row=5, column=1),
                     experiment2_counter2_value=dict(row=5, column=2),
                     experiment2_counter2_button_a1=dict(row=5, column=3))

    for e in grid_info.keys():
        parts[e].grid(row=grid_info[e]['row'], column=grid_info[e]['column'],
                      sticky=tk.NSEW, padx=5, pady=5)

    for i, e in enumerate(parts['experiment2_task_radiobuttons']):
        e.grid(row=i, column=0, sticky=tk.NSEW, padx=5, pady=5, columnspan=3)
    parts['experiment2_task_viewbutton'].grid(
        row=0, column=3, sticky=tk.NSEW, padx=5, pady=5, rowspan=4)

    parts['experiment2_label_selectdata'].grid(
        row=6, column=0, sticky=tk.NSEW, padx=5, pady=5, columnspan=4)
    parts['experiment2_button_selectdata'].grid(
        row=7, column=0, sticky=tk.NSEW, padx=5, pady=5, columnspan=4)
    parts['experiment2_text_file_path'].grid(
        row=8, column=0, sticky=tk.NSEW, padx=5, pady=5, columnspan=4)

    parts['experiment2_task_gobutton'].grid(
        row=9, column=0, sticky=tk.NSEW, padx=5, pady=5, columnspan=4)

    return parts


def get_experiment2_info(parts):
    info = {}
    info['task'] = parts['experiment2_task_var'].get()
    info['counter1_value'] = int(parts['experiment2_counter1_value']['text'])
    info['counter2_value'] = int(parts['experiment2_counter2_value']['text'])
    info['model_path'] = parts['experiment2_text_file_name'].get(
        1.0, tk.END)[:-1]
    return info
