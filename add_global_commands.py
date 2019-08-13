# coding: utf-8

import webbrowser
import os
import time
import pickle
import tkinter as tk

from fill_subject_info_block import get_subject_info
from fill_connection_info_block import get_connection_info
from fill_modeltrain_info_block import get_modeltrain_info
from fill_experiment1_info_block import get_experiment1_info
from fill_experiment2_info_block import get_experiment2_info
from perform_experiment import presentation, presentation_testing


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
    print_infos(infos)

    task_name = infos['experiment1_info']['task_name']
    table = {'Quzhou ': 'quzhou',
             'Shenchu': 'shenchu',
             'Taishou': 'taiqi',
             'Waizhan': 'waizhan'}
    task_name = table[task_name]

    num_trails = infos['experiment1_info']['counter1_value']
    num_runs = infos['experiment1_info']['counter2_value']

    task_map = presentation(task_name=task_name,
                            num_trails=num_trails, num_runs=num_runs)

    mk_html_report_experiment1(infos, task_map)

    return infos


def experiment2_go(parts):
    push_all_combobox_input(parts)
    infos = get_infos(parts)
    print_infos(infos)

    task_name = infos['experiment2_info']['task_name']
    table = {'Quzhou ': 'quzhou',
             'Shenchu': 'shenchu',
             'Taishou': 'taiqi',
             'Waizhan': 'waizhan'}
    task_name = table[task_name]

    num_trails = infos['experiment2_info']['counter1_value']
    num_runs = infos['experiment2_info']['counter2_value']

    model_name = infos['experiment2_info']['model_path']

    task_map, predict_map = presentation_testing(model=model_name,
                                                 task_name=task_name,
                                                 num_trails=num_trails,
                                                 num_runs=num_runs)

    mk_html_report_experiment2(infos, task_map, predict_map, model_name)

    return infos


def mk_html_report_experiment1(infos, task_map):
    html_tmp_path = os.path.join('resources', 'report_tmp.html')

    with open(html_tmp_path, 'rb') as f:
        lines = f.readlines()

    new_html_path = os.path.join(os.path.join('reports', 'a.html'))
    with open(new_html_path, 'w') as f:
        for line in lines:
            f.write(line.decode())

            if b'<!--tobefilled: subject information-->' in line:
                f.write('<td>%s</td>' % infos['subject_info']['subject_name'])
                f.write('<td>%s</td>' % infos['subject_info']['subject_age'])
                f.write('<td>%s</td>' % infos['subject_info']['subject_sex'])
                f.write('<td>%s</td>' % infos['subject_info']['date'])

            if b'<!--tobefilled: experiment information-->' in line:
                f.write('<td>%s</td>' % infos['experiment1_info']['task_name'])
                f.write('<td>%d</td>' %
                        infos['experiment1_info']['counter1_value'])
                f.write('<td>%d</td>' %
                        infos['experiment1_info']['counter2_value'])

            if b'<!--tobefilled: experiment detail-->' in line:
                num_trails = infos['experiment1_info']['counter1_value']
                num_runs = infos['experiment1_info']['counter2_value']
                f.write('<table>')

                f.write('<thead>')
                f.write('<tr>')
                for j in range(num_trails):
                    f.write('<th>%d</th>' % (j+1))
                f.write('</tr>')
                f.write('</thead>')

                for _run in range(num_runs):
                    f.write('<tr>')
                    for _trail in range(num_trails):
                        # 0 means no motion
                        # 1 means motion
                        f.write('<td>%d</td>' % task_map[(_run, _trail)])
                    f.write('</tr>')

                f.write('</table>')

    webbrowser.open(new_html_path)


def mk_html_report_experiment2(infos, task_map, predict_map, model_name):
    html_tmp_path = os.path.join('resources', 'report_tmp.html')

    with open(html_tmp_path, 'rb') as f:
        lines = f.readlines()

    new_html_path = os.path.join(os.path.join('reports', 'a.html'))
    with open(new_html_path, 'w') as f:
        for line in lines:
            f.write(line.decode())

            if b'<!--tobefilled: subject information-->' in line:
                f.write('<td>%s</td>' % infos['subject_info']['subject_name'])
                f.write('<td>%s</td>' % infos['subject_info']['subject_age'])
                f.write('<td>%s</td>' % infos['subject_info']['subject_sex'])
                f.write('<td>%s</td>' % infos['subject_info']['date'])

            if b'<!--tobefilled: experiment information-->' in line:
                f.write('<td>%s</td>' % infos['experiment1_info']['task_name'])
                f.write('<td>%d</td>' %
                        infos['experiment1_info']['counter1_value'])
                f.write('<td>%d</td>' %
                        infos['experiment1_info']['counter2_value'])

            if b'<!--tobefilled: experiment detail-->' in line:
                num_trails = infos['experiment2_info']['counter1_value']
                num_runs = infos['experiment2_info']['counter2_value']
                f.write('<table>')

                f.write('<thead>')
                f.write('<tr>')
                for j in range(num_trails):
                    f.write('<th>%d</th>' % (j+1))
                f.write('</tr>')
                f.write('</thead>')

                for _run in range(num_runs):
                    f.write('<tr>')
                    for _trail in range(num_trails):
                        # 0 means no motion
                        # 1 means motion
                        if task_map[(_run, _trail)] == predict_map[(_run, _trail)]:
                            f.write('<td>%d</td>' % task_map[(_run, _trail)])
                        else:
                            # '-' means the prediction is wrong.
                            f.write('<td>%d-</td>' % task_map[(_run, _trail)])
                    f.write('</tr>')

                f.write('</table>')

            if b'<!--tobefilled: model path-->' in line:
                f.write('<p>')
                f.write('model: %s' % model_name)
                f.write('</p>')

    webbrowser.open(new_html_path)


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
