# coding: utf-8

import time
import tkinter as tk
from components import Block
from components import add_components_subject_age, add_components_subject_name, add_components_subject_sex, add_components_experiment_task, add_components_counter, add_components_connection_info, add_components_model_training, add_components_model_selection, add_components_date

root = tk.Tk()
root.geometry('800x800+100+100')
root.resizable(False, False)

blocks = {}
parts = {}

'''
# Building blocks
'''
block = Block(root, name='Subject Info')
block.place(
    relx=1/40, rely=1/40, relwidth=12/40, relheight=24/40, anchor='nw')
blocks['subject_info'] = block

block = Block(root, name='Connection Info')
block.place(
    relx=1/40, rely=26/40, relwidth=12/40, relheight=12/40, anchor='nw')
blocks['connection_info'] = block

block = Block(root, name='Experiment I Info')
block.place(
    relx=14/40, rely=1/40, relwidth=12/40, relheight=24/40, anchor='nw')
blocks['experiment1_info'] = block

block = Block(root, name='Model Training Info')
block.place(
    relx=14/40, rely=26/40, relwidth=12/40, relheight=12/40, anchor='nw')
blocks['modeltrain_info'] = block

block = Block(root, name='Experiment II Info')
block.place(
    relx=27/40, rely=1/40, relwidth=12/40, relheight=37/40, anchor='nw')
blocks['experiment2_info'] = block

label = tk.Label(root, text='Author: listenzcc@ia.ac.cn ')
label.place(relx=1, rely=1, anchor='se')

'''
# Filling Subject Info Block
'''
master = blocks['subject_info'].panel

combobox, label = add_components_subject_name(master=master)
parts['input_subject_name'] = combobox
parts['label_subject_name'] = label

combobox, label = add_components_subject_age(master=master)
parts['input_subject_age'] = combobox
parts['label_subject_age'] = label

combobox, label = add_components_subject_sex(master=master)
parts['input_subject_sex'] = combobox
parts['label_subject_sex'] = label

label_date_label, label_date = add_components_date(master=master)
parts['label_date_label'] = label_date_label
parts['label_date'] = label_date

grid_info = dict(label_subject_name=dict(row=0, column=0),
                 input_subject_name=dict(row=0, column=1),
                 label_subject_age=dict(row=1, column=0),
                 input_subject_age=dict(row=1, column=1),
                 label_subject_sex=dict(row=2, column=0),
                 input_subject_sex=dict(row=2, column=1),
                 label_date_label=dict(row=3, column=0),
                 label_date=dict(row=3, column=1))

for e in grid_info.keys():
    parts[e].grid(row=grid_info[e]['row'], column=grid_info[e]['column'],
                  sticky=tk.NSEW, padx=5, pady=5)


def get_subject_info(parts):
    info = {}
    info['subject_name'] = parts['input_subject_name'].get()
    return info


'''
# Filling Connection Info Block
'''
master = blocks['connection_info'].panel

combobox_IP, combobox_port, label_IP, label_port = add_components_connection_info(
    master=master)
parts['input_IP'] = combobox_IP
parts['input_port'] = combobox_port
parts['label_IP'] = label_IP
parts['label_port'] = label_port

grid_info = dict(label_IP=dict(row=0, column=0),
                 input_IP=dict(row=0, column=1),
                 label_port=dict(row=1, column=0),
                 input_port=dict(row=1, column=1))

for e in grid_info.keys():
    parts[e].grid(row=grid_info[e]['row'], column=grid_info[e]['column'],
                  sticky=tk.NSEW, padx=5, pady=5)

'''
# Filling Model Training Info Block
'''
master = blocks['modeltrain_info'].panel
label_data_select, button_select, text_file_name, button_train, label_score, label_score_output = add_components_model_training(
    master=master)
parts['modeltrain_label_selectdata'] = label_data_select
parts['modeltrain_button_selectdata'] = button_select
parts['modeltrain_text_file_name'] = text_file_name
parts['modeltrain_button_train'] = button_train
parts['modeltrain_label_score'] = label_score
parts['modeltrain_label_score_output'] = label_score_output

grid_info = dict(modeltrain_button_selectdata=dict(row=1, column=0),
                 modeltrain_button_train=dict(row=1, column=1),
                 modeltrain_label_score=dict(row=3, column=0),
                 modeltrain_label_score_output=dict(row=3, column=1))

for e in grid_info.keys():
    parts[e].grid(row=grid_info[e]['row'], column=grid_info[e]['column'],
                  sticky=tk.NSEW, padx=5, pady=5)

parts['modeltrain_label_selectdata'].grid(
    row=0, column=0, sticky=tk.NSEW, padx=5, pady=5, columnspan=2)
parts['modeltrain_text_file_name'].grid(
    row=2, column=0, sticky=tk.NSEW, padx=5, pady=5, columnspan=2)


for e in grid_info.keys():
    parts[e].grid(row=grid_info[e]['row'], column=grid_info[e]['column'],
                  sticky=tk.NSEW, padx=5, pady=5)

'''
# Filling Experiment I Info Block
'''
master = blocks['experiment1_info'].panel

radiobuttons, var, button = add_components_experiment_task(master=master)
parts['experiment1_task_var'] = var
parts['experiment1_task_radiobuttons'] = radiobuttons
parts['experiment1_task_viewbutton'] = button

label_note, label_count, button_s1, button_a1 = add_components_counter(
    master=master)
label_note['text'] = 'Counter I'
parts['experiment1_counter1_label'] = label_note
parts['experiment1_counter1_value'] = label_count
parts['experiment1_counter1_button_s1'] = button_s1
parts['experiment1_counter1_button_a1'] = button_a1

label_note, label_count, button_s1, button_a1 = add_components_counter(
    master=master)
label_note['text'] = 'Counter II'
parts['experiment1_counter2_label'] = label_note
parts['experiment1_counter2_value'] = label_count
parts['experiment1_counter2_button_s1'] = button_s1
parts['experiment1_counter2_button_a1'] = button_a1

button = tk.Button(master=master, text='Go!!!',
                   command=lambda: print('Experiment I starts.', get_subject_info(parts)))
parts['experiment1_task_gobutton'] = button

grid_info = dict(experiment1_counter1_label=dict(row=4, column=0),
                 experiment1_counter1_button_s1=dict(row=4, column=1),
                 experiment1_counter1_value=dict(row=4, column=2),
                 experiment1_counter1_button_a1=dict(row=4, column=3),
                 experiment1_counter2_label=dict(row=5, column=0),
                 experiment1_counter2_button_s1=dict(row=5, column=1),
                 experiment1_counter2_value=dict(row=5, column=2),
                 experiment1_counter2_button_a1=dict(row=5, column=3))

for e in grid_info.keys():
    parts[e].grid(row=grid_info[e]['row'], column=grid_info[e]['column'],
                  sticky=tk.NSEW, padx=5, pady=5)

for i, e in enumerate(parts['experiment1_task_radiobuttons']):
    e.grid(row=i, column=0, sticky=tk.NSEW, padx=5, pady=5, columnspan=3)
parts['experiment1_task_viewbutton'].grid(
    row=0, column=3, sticky=tk.NSEW, padx=5, pady=5, rowspan=4)
parts['experiment1_task_gobutton'].grid(
    row=6, column=0, sticky=tk.NSEW, padx=5, pady=5, columnspan=4)

'''
# Filling Experiment II Info Block
'''
master = blocks['experiment2_info'].panel

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
parts['experiment2_text_file_name'] = text_file_name

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
parts['experiment2_text_file_name'].grid(
    row=8, column=0, sticky=tk.NSEW, padx=5, pady=5, columnspan=4)

parts['experiment2_task_gobutton'].grid(
    row=9, column=0, sticky=tk.NSEW, padx=5, pady=5, columnspan=4)


for e in parts.items():
    print(e)

root.mainloop()
