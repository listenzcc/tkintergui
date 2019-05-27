# coding: utf-8

import time
import tkinter as tk
from fill_root import build_blocks
from fill_subject_info_block import build_parts_subject_info, get_subject_info
from fill_connection_info_block import build_parts_connection_info, get_connection_info
from fill_modeltrain_info_block import build_parts_modeltrain_info, get_modeltrain_info
from fill_experiment1_info_block import build_parts_experiment1_info, get_experiment1_info
from fill_experiment2_info_block import build_parts_experiment2_info, get_experiment2_info
from fill_profile_info_block import build_parts_profile_info

root = tk.Tk()
root.geometry('800x800+100+100')
root.resizable(False, False)

blocks = build_blocks(root)

label = tk.Label(root, text='Author: listenzcc@ia.ac.cn ')
label.place(relx=1, rely=1, anchor='se')

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


def print_infos():
    print('-'*80)
    print('subject_info:')
    print(get_subject_info(parts['subject_info']))
    print('connection_info:')
    print(get_connection_info(parts['connection_info']))
    print('modeltrain_info:')
    print(get_modeltrain_info(parts['modeltrain_info']))
    print('experiment1_info:')
    print(get_experiment1_info(parts['experiment1_info']))
    print('experiment1_info:')
    print(get_experiment2_info(parts['experiment2_info']))


parts['experiment1_info']['experiment1_task_gobutton']['command'] = print_infos
# print(get_subject_info(parts['subject_info']))

root.mainloop()
