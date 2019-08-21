# coding: utf-8

import os
import pickle
import time
import tkinter as tk
from fill_root import build_blocks
from fill_subject_info_block import build_parts_subject_info
from fill_connection_info_block import build_parts_connection_info
from fill_modeltrain_info_block import build_parts_modeltrain_info
from fill_experiment1_info_block import build_parts_experiment1_info
from fill_experiment2_info_block import build_parts_experiment2_info
from fill_profile_info_block import build_parts_profile_info
from add_global_commands import set_command, save_profile, load_profile, experiment1_go, experiment2_go

from myBuffer import Buffer

for fname in ['last_data', 'last_model']:
    if not os.path.exists(fname):
        os.mkdir(fname)

root = tk.Tk()
root.geometry('800x800+100+100')
root.resizable(False, False)

my_buffer = Buffer()

blocks = build_blocks(root)

def disconnect():
    my_buffer.off()

button = tk.Button(root, text='Disconnect', command=disconnect)
button.place(relx=1, rely=1, anchor='se')
# label = tk.Label(root, text='Author: listenzcc@ia.ac.cn ')
# label.place(relx=1, rely=1, anchor='se')

parts = {}

parts['subject_info'] = build_parts_subject_info(
    blocks['subject_info'].panel)

parts['connection_info'] = build_parts_connection_info(
    blocks['connection_info'].panel)

parts['modeltrain_info'] = build_parts_modeltrain_info(
    blocks['modeltrain_info'].panel)

parts['experiment1_info'] = build_parts_experiment1_info(
    blocks['experiment1_info'].panel)

parts['experiment2_info'] = build_parts_experiment2_info(
    blocks['experiment2_info'].panel)

parts['profile_info'] = build_parts_profile_info(
    blocks['profile_info'].panel)

for block in parts.items():
    print('-'*80)
    print(block[0], ':')
    for i, e in enumerate(block[1].items()):
        print('|--%d:' % i, e[0])

set_command(parts['experiment1_info']['experiment1_task_gobutton'],
            lambda p=parts, b=my_buffer: experiment1_go(p, b))
set_command(parts['experiment2_info']['experiment2_task_gobutton'],
            lambda p=parts, b=my_buffer: experiment2_go(p, b))
set_command(parts['profile_info']['profile_button_save_profile'],
            lambda p=parts: save_profile(p))
set_command(parts['profile_info']['profile_button_load_profile'],
            lambda p=parts: load_profile(p))

root.mainloop()

########################
# Todo: Train model and predict imaging motion
# Train model:
# components.py (228): finish function model_train()
# components.py (241): add function model_train_on_data()
# Predict imaging motion:
# perform_experiment.py (72): finish function predict()
# perform_experiment.py (139): add function read_lastest_data()

########################
# By the way,
# Parameters of experiment design is hard coded in perform_experiment.py
# If require longer gap between two stimuli in testing experiment,
# larger time_rest in line 86 in perform_experiment.py.