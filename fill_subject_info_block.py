# coding: utf-8

import tkinter as tk
from components import add_components_subject_age, add_components_subject_name, add_components_subject_sex, add_components_date


def build_parts_subject_info(master):
    parts = {}

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

    return parts


def get_subject_info(parts):
    info = {}
    info['subject_name'] = parts['input_subject_name'].get()
    info['subject_age'] = parts['input_subject_age'].get()
    info['subject_sex'] = parts['input_subject_sex'].get()
    info['date'] = parts['label_date']['text']
    return info
