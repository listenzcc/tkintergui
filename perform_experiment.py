# coding:utf-8

import os
import time
import random
import pickle
import numpy as np
from myClientNew import ScanClient
from psychopy import visual, core, event


def presentation(task_name, task_innername, num_trails=5, num_runs=1,
                 infos=[], my_buffer=[]):
    # num_rest means there will be num_rest none-MI trails performed
    num_rest = num_trails

    my_buffer.on(infos['connection_info']['IP'],
                 int(infos['connection_info']['port']))

    time_task = 4  # seconds
    time_rest = 2  # seconds
    time_after = 2 # seconds

    task_map = {}
    for r in range(num_runs):
        n0 = random.sample(range(num_rest+num_trails), k=num_trails)
        for t in range(num_rest+num_trails):
            if t in n0:
                task_map[(r, t)] = 1
            else:
                task_map[(r, t)] = 0

    win = visual.Window(size=(1920, 1080), pos=(0, 0), color=(-1, -1, -1))
    # win = visual.Window(color=(0, 0, 0), fullsrc=True)

    pics_dir = os.path.join('movie_4D', 'pics')
    num_pics = len([s for s in os.listdir(pics_dir) if s.startswith(task_innername)])
    divide_pics = time_task / (num_pics-1)

    imgs = [visual.ImageStim(win, image=os.path.join(
        pics_dir, '%s_%d.png' % (task_innername, j))) for j in range(num_pics)]

    note_imgs = {}
    for name in ['206_start.png',
                 '206_red1.png',
                 '206_red2.png',
                 '206_green.png',
                 '206_end.png']:
        note_imgs[name] = visual.ImageStim(win, image=os.path.join(
            pics_dir, '..', name))

    all_data = []
    for _run in range(num_runs):
        ###############################################################
        # Run start
        note_imgs['206_start.png'].draw()
        win.flip()
        key = event.waitKeys()
        if key == ['escape']:
            break

        for _trail in range(num_rest+num_trails):
            #############################################################
            # Trail start
            # Pre task stimuli
            my_buffer.start()

            if task_map[(_run, _trail)] == 0:
                # If not motion imagery
                note_imgs['206_red2.png'].draw()
                win.flip()
                core.wait(time_rest)

                imgs[0].draw()
                win.flip()
                core.wait(time_task)

            if task_map[(_run, _trail)] == 1:
                # If motion imagery
                note_imgs['206_red1.png'].draw()
                win.flip()
                core.wait(time_rest)

                t = time.time()
                for j, img in enumerate(imgs):
                    img.draw()
                    win.flip()
                    while (time.time()-t) < divide_pics*j:
                        pass

            # Save data for last 4 seconds
            my_buffer.stop()
            all_data.append([my_buffer.output(), task_map[(_run, _trail)]])

            # Trail ends after time_after
            note_imgs['206_green.png'].draw()
            win.flip()
            core.wait(time_after)

    win.close()

    with open(os.path.join('last_data', 'last.pkl'), 'wb') as f:
        pickle.dump(all_data, f)

    report_pre = '-'.join([infos['subject_info']['subject_name'],
                                     task_name,
                                     time.strftime('%Y%m%d-%H-%M-%S')])

    with open(os.path.join('last_data',
                           '-'.join([report_pre, 'data.pkl'])), 'wb') as f:
        pickle.dump(all_data, f)

    return task_map, report_pre


def predict(model, data):
    '''
    input: model_file_path, data of shape (None, 62, 4000)
    output: pred_label
    '''
    ##############
    # Predict whether imaging motion is performed, based on data and model
    # label= 0, 1: 0 means no motion, 1 means motion.
    # label = random.choice([0, 1])
    with open(model, 'rb') as f:
        cla = pickle.load(f)

    data = data.reshape((1, ) + data.shape)
    print(data.shape)

    label = cla.predict(data)

    return label


def presentation_testing(model, task_name, task_innername,
                         num_trails=5, num_runs=1,
                         infos=[], my_buffer=[]):

    # num_rest means there will be num_rest none-MI trails performed
    num_rest = int(num_trails/2)

    print(infos)
    print(my_buffer)
    my_buffer.on(infos['connection_info']['IP'],
                 int(infos['connection_info']['port']))

    if model is None:
        print('Warning: no model selected.')
    print('Model:', model)

    time_task = 4  # seconds
    time_rest = 2  # seconds
    time_after = 2 # seconds

    task_map = {}
    predict_map = {}
    for r in range(num_runs):
        n0 = random.sample(range(num_rest+num_trails), k=num_trails)
        for t in range(num_rest+num_trails):
            if t in n0:
                task_map[(r, t)] = 1
            else:
                task_map[(r, t)] = 0
            predict_map[(r, t)] = 0

    win = visual.Window(size=(1000, 1000))

    pics_dir = os.path.join('movie_4D', 'pics')
    num_pics = len([s for s in os.listdir(
        pics_dir) if s.startswith(task_innername)])
    divide_pics = time_task / (num_pics-1)

    imgs = [visual.ImageStim(win, image=os.path.join(
        pics_dir, '%s_%d.png' % (task_innername, j))) for j in range(num_pics)]

    note_imgs = {}
    for name in ['206_start.png',
                 '206_red1.png',
                 '206_red2.png',
                 '206_green.png',
                 '206_end.png']:
        note_imgs[name] = visual.ImageStim(win, image=os.path.join(
            pics_dir, '..', name))

    string_welcome = u'\u00A1Prepare run %d|%d,\n press any key to continue!'
    for _run in range(num_runs):
        ###############################################################
        # Run start
        note_imgs['206_start.png'].draw()
        win.flip()
        key = event.waitKeys()
        if key == ['escape']:
            break

        for _trail in range(num_rest+num_trails):
            #############################################################
            # Trail start
            # Pre task stimuli
            my_buffer.start()

            if task_map[(_run, _trail)] == 0:
                # If not motion imagery
                note_imgs['206_red2.png'].draw()
                win.flip()
                core.wait(time_rest)

                imgs[0].draw()
                win.flip()
                core.wait(time_task)

            if task_map[(_run, _trail)] == 1:
                # If motion imagery
                note_imgs['206_red1.png'].draw()
                win.flip()
                core.wait(time_rest)

                t = time.time()
                for j, img in enumerate(imgs):
                    img.draw()
                    win.flip()
                    while (time.time()-t) < divide_pics*j:
                        pass

            ########################
            # Predict whether imaging motion is performed,
            # Based on model and data.
            # I have invited model in.
            # Todo: read data from somewhere.
            # data = read_lastest_data(): read data from last several seconds.
            my_buffer.stop()
            x = my_buffer.output()
            if x == 'offline':
                label = 1
            else:
                label = predict(model=infos['experiment2_info']['model_path'],
                                data=my_buffer.output())
            predict_map[(_run, _trail)] = label
            if label == task_map[(_run, _trail)]:
                msg = visual.TextStim(win, text='Correct.')
            else:
                msg = visual.TextStim(win, text='Wrong.')
            msg.draw()
            win.flip()
            core.wait(time_after)

    win.close()

    return task_map, predict_map
