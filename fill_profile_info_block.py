# coding: utf-8


import tkinter as tk
from components import add_components_profile_selection


def build_parts_profile_info(master):
    parts = {}

    label_profile, input_profile_name, button_save_profile, button_load_profile = add_components_profile_selection(
        master)
    parts['profile_label_profile'] = label_profile
    parts['profile_input_profile_name'] = input_profile_name
    parts['profile_button_save_profile'] = button_save_profile
    parts['profile_button_load_profile'] = button_load_profile

    grid_info = dict(profile_label_profile=dict(row=0, column=0),
                     profile_input_profile_name=dict(row=1, column=0),
                     profile_button_save_profile=dict(row=2, column=0),
                     profile_button_load_profile=dict(row=3, column=0))

    for e in grid_info.keys():
        parts[e].grid(row=grid_info[e]['row'], column=grid_info[e]['column'],
                      sticky=tk.NSEW, padx=5, pady=5)

    return parts
