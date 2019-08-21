# coding: utf-8

import tkinter as tk
from components import add_components_connection_info


def build_parts_connection_info(master):
    parts = {}

    combobox_IP, combobox_port, label_IP, label_port, button_disconnect = add_components_connection_info(
        master=master)

    parts['input_IP'] = combobox_IP
    parts['input_port'] = combobox_port
    parts['label_IP'] = label_IP
    parts['label_port'] = label_port
    parts['button_disconnect'] = button_disconnect

    grid_info = dict(label_IP=dict(row=0, column=0),
                     input_IP=dict(row=0, column=1),
                     label_port=dict(row=1, column=0),
                     input_port=dict(row=1, column=1),
                     button_disconnect=dict(row=2, column=1))

    for e in grid_info.keys():
        parts[e].grid(row=grid_info[e]['row'], column=grid_info[e]['column'],
                      sticky=tk.NSEW, padx=5, pady=5)

    return parts


def get_connection_info(parts):
    info = {}
    info['IP'] = parts['input_IP'].get()
    info['port'] = parts['input_port'].get()
    return info
