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

import tkinter.font as tkFont
from PIL import ImageTk, Image

for fname in ['last_data', 'last_model']:
    if not os.path.exists(fname):
        os.mkdir(fname)

root = tk.Tk()
root.geometry('800x800+100+100')
root.resizable(False, False)

########################
# Row 1
# Logo
img0 = Image.open(os.path.join('movie_4D', 'Logo_CASIC.jpg'))
img0 = img0.resize((100, 100), Image.ANTIALIAS)
img0 = ImageTk.PhotoImage(img0)
logo0 = tk.Label(root, image=img0)
logo0.place(relx=5/40, rely=0/40, relwidth=5/40, relheight=5/40, anchor='nw')

img1 = Image.open(os.path.join('movie_4D', 'Logo_RCHPMT.jpg'))
img1 = img1.resize((100, 100), Image.ANTIALIAS)
img1 = ImageTk.PhotoImage(img1)
logo1 = tk.Label(root, image=img1)
logo1.place(relx=30/40, rely=0/40, relwidth=5/40, relheight=5/40, anchor='nw')

logo2 = tk.Label(root, text='上肢脑机康复系统',
                 font=tkFont.Font(family='Fixdsys', size=24, weight=tkFont.BOLD))
logo2.place(relx=10/40, rely=0/40, relwidth=20/40, relheight=5/40, anchor='nw')

########################
# Build blocks
blocks = build_blocks(root)

# label = tk.Label(root, text='Author: listenzcc@ia.ac.cn ')
# label.place(relx=1, rely=1, anchor='se')

########################
# Fill blocks
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

########################
# Hook command functions
set_command(parts['experiment1_info']['experiment1_task_gobutton'],
            lambda p=parts: experiment1_go(p))
set_command(parts['experiment2_info']['experiment2_task_gobutton'],
            lambda p=parts: experiment2_go(p))
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
