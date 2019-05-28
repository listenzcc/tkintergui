# coding: utf-8

import os
import pickle
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


def save_profile():
    saved = {}
    for info_name, part in parts.items():
        saved[info_name] = {}
        for widget_name, widget in part.items():
            s = {}
            p = parts[info_name][widget_name]

            if widget_name in ['input_subject_name',
                               'input_subject_age',
                               'input_subject_sex',
                               'input_IP',
                               'input_port']:
                s['values'] = p['values']
                s['current'] = p.current()

            if widget_name in ['experiment1_counter1_value',
                               'experiment1_counter2_value',
                               'experiment2_counter1_value',
                               'experiment2_counter2_value']:
                s['text'] = p['text']

            if widget_name in ['experiment1_task_var',
                               'experiment2_task_var']:
                s['task_var'] = p.get()

            if widget_name in ['modeltrain_text_file_path',
                               'experiment2_text_file_path']:
                s['file_path'] = p.get(1.0, tk.END)[:-1]

            if s:
                saved[info_name][widget_name] = s

    profile_name = parts['profile_info']['profile_input_profile_name'].get()
    if len(profile_name) == 0:
        profile_name = 'AutoProfile_' + time.strftime('%H-%M-%S')

    with open(os.path.join('profiles', profile_name), 'wb') as f:
        pickle.dump([saved], f)

    combobox = parts['profile_info']['profile_input_profile_name']
    if combobox.current() == -1:
        names = [e for e in combobox['values']]
        names.append(profile_name)
        names.sort()
        combobox['values'] = names

    print('save profile')


def load_profile():
    combobox = parts['profile_info']['profile_input_profile_name']
    if combobox.current() == -1:
        print('Profile %s not exists.' % combobox.get())
        return

    f = open(os.path.join('profiles', combobox.get()), 'rb')
    saved = pickle.load(f)[0]
    f.close()

    print('-'*80)
    for e in saved.items():
        print(e[0], ':', e[1])

    for info_name, part in saved.items():
        for widget_name, atts in part.items():
            s = saved[info_name][widget_name]
            p = parts[info_name][widget_name]

            if widget_name in ['input_subject_name',
                               'input_subject_age',
                               'input_subject_sex',
                               'input_IP',
                               'input_port']:
                p['values'] = s['values']
                if not s['current'] == -1:
                    p.current(s['current'])

            if widget_name in ['experiment1_counter1_value',
                               'experiment1_counter2_value',
                               'experiment2_counter1_value',
                               'experiment2_counter2_value']:
                p['text'] = s['text']

            if widget_name in ['experiment1_task_var',
                               'experiment2_task_var']:
                p.set(s['task_var'])

            if widget_name in ['modeltrain_text_file_path',
                               'experiment2_text_file_path']:
                p.delete(1.0, tk.END)
                p.insert(tk.INSERT, s['file_path'])


parts['profile_info']['profile_button_save_profile']['command'] = save_profile
parts['profile_info']['profile_button_load_profile']['command'] = load_profile

root.mainloop()
