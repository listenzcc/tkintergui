# coding: utf-8

import os
import time
import pickle
import tkinter as tk

from fill_subject_info_block import get_subject_info
from fill_connection_info_block import get_connection_info
from fill_modeltrain_info_block import get_modeltrain_info
from fill_experiment1_info_block import get_experiment1_info
from fill_experiment2_info_block import get_experiment2_info


def set_command(button, command):
    button['command'] = command


def get_infos(parts):
    return dict(subject_info=get_subject_info(parts['subject_info']),
                connection_info=get_connection_info(parts['connection_info']),
                modeltrain_info=get_modeltrain_info(parts['modeltrain_info']),
                experiment1_info=get_experiment1_info(
                    parts['experiment1_info']),
                experiment2_info=get_experiment2_info(parts['experiment2_info']))


def print_infos(infos):
    print('-' * 80)
    for info_name, part in infos.items():
        print('%s:' % info_name)
        for info in part.items():
            print(info)


def push_combobox_input(combobox):
    if len(combobox.get()) == 0:
        return

    if not combobox.current() == -1:
        return

    values = [e for e in combobox['values']]
    values.append(combobox.get())
    values.sort()

    combobox['values'] = values


def push_all_combobox_input(parts):
    [push_combobox_input(c) for c in [
        parts['subject_info']['input_subject_name'],
        parts['subject_info']['input_subject_age'],
        parts['subject_info']['input_subject_sex'],
        parts['connection_info']['input_IP'],
        parts['connection_info']['input_port']]]


def experiment1_go(parts):
    push_all_combobox_input(parts)
    infos = get_infos(parts)
    # print_infos(infos)

    with open(os.path.join('resources', 'infos.pkl'), 'wb') as f:
        pickle.dump(infos, f)

    os.system('python perform_experiment1.py')

    return 0


def experiment2_go(parts):
    push_all_combobox_input(parts)
    infos = get_infos(parts)
    # print_infos(infos)

    with open(os.path.join('resources', 'infos.pkl'), 'wb') as f:
        pickle.dump(infos, f)

    os.system('python perform_experiment2.py')

    return 0


def save_profile(parts):
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


def load_profile(parts):
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
