# coding: utf-8

import tkinter as tk
from components import add_components_model_training


def build_parts_modeltrain_info(master):
    parts = {}

    label_data_select, button_select, text_file_path, button_train, label_score, label_score_output = add_components_model_training(
        master=master)
    parts['modeltrain_label_selectdata'] = label_data_select
    parts['modeltrain_button_selectdata'] = button_select
    parts['modeltrain_text_file_path'] = text_file_path
    parts['modeltrain_button_train'] = button_train
    parts['modeltrain_label_score'] = label_score
    parts['modeltrain_label_score_output'] = label_score_output

    grid_info = dict(modeltrain_label_selectdata=dict(row=0, column=0),
                     modeltrain_button_selectdata=dict(row=1, column=0),
                     modeltrain_text_file_path=dict(row=2, column=0),
                     modeltrain_button_train=dict(row=3, column=0),
                     modeltrain_label_score=dict(row=4, column=0),
                     modeltrain_label_score_output=dict(row=4, column=1))

    for e in grid_info.keys():
        parts[e].grid(row=grid_info[e]['row'], column=grid_info[e]['column'],
                      sticky=tk.NSEW, padx=5, pady=5)

    return parts


def get_modeltrain_info(parts):
    info = {}
    info['file_path'] = parts['modeltrain_text_file_path'].get(
        1.0, tk.END)[:-1]
    return info
