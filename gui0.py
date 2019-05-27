# coding: utf-8

import time
import tkinter as tk
from fill_root import build_blocks
from fill_subject_info_block import build_parts_subject_info
from fill_connection_info_block import build_parts_connection_info
from fill_modeltrain_info_block import build_parts_modeltrain_info
from fill_experiment1_info_block import build_parts_experiment1_info
from fill_experiment2_info_block import build_parts_experiment2_info

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


def get_subject_info(parts):
    info = {}
    info['subject_name'] = parts['subject_info']['input_subject_name'].get()
    return info


for block in parts.items():
    print('-'*80)
    print(block[0], ':')
    for i, e in enumerate(block[1].items()):
        print('|--%d:' % i, e[0])


root.mainloop()
