# coding:utf-8

import os
import time
import random
from psychopy import visual, core, event


def presentation(task_name='quzhou', num_trails=5, num_runs=5):
    time_task = 4  # seconds
    time_rest = 2  # seconds

    task_map = {}
    for r in range(num_runs):
        n0 = random.sample(range(num_trails), k=int(num_trails/2))
        for t in range(num_trails):
            if t in n0:
                task_map[(r, t)] = 0
            else:
                task_map[(r, t)] = 1

    win = visual.Window(size=(1000, 1000))

    pics_dir = os.path.join('movie_4D', 'pics')
    num_pics = len([s for s in os.listdir(
        pics_dir) if s.startswith(task_name)])
    divide_pics = time_task / (num_pics-1)

    imgs = [visual.ImageStim(win, image=os.path.join(
        pics_dir, '%s_%d.png' % (task_name, j))) for j in range(num_pics)]

    string_welcome = u'\u00A1Prepare run %d|%d,\n press any key to continue!'
    for _run in range(num_runs):
        msg = visual.TextStim(win, text=string_welcome % (_run+1, num_runs))
        msg.draw()
        win.flip()
        key = event.waitKeys()
        if key == ['escape']:
            break

        for _trail in range(num_trails):
            t = time.time()
            while True:
                circle = visual.Circle(win, radius=0.05, edges=32)
                circle.setColor(random.choices(range(255), k=3), 'rgb255')
                circle.draw()
                win.flip()
                if time_rest-(time.time()-t) < 0.1:
                    core.wait(time_rest-(time.time()-t))
                    break
                core.wait(min(random.random(), time_rest-(time.time()-t)))
            print('Passed: %f seconds.' % (time.time()-t))

            t = time.time()
            if task_map[(_run, _trail)] == 0:
                imgs[0].draw()
                win.flip()
                core.wait(time_task-(time.time()-t))
            else:
                for j, img in enumerate(imgs):
                    img.draw()
                    win.flip()
                    while (time.time()-t) < divide_pics*j:
                        pass
            print('Passed: %f seconds.' % (time.time()-t))

    win.close()

    return task_map


def predict(model=None, data=None):
    label = random.choice([0, 1])
    return label


def presentation_testing(model=None, task_name='quzhou', num_trails=5, num_runs=5):
    if model is None:
        print('Warning: no model selected.')
    print('Model:', model)

    time_task = 4  # seconds
    time_rest = 2  # seconds

    task_map = {}
    predict_map = {}
    for r in range(num_runs):
        n0 = random.sample(range(num_trails), k=int(num_trails/2))
        for t in range(num_trails):
            if t in n0:
                task_map[(r, t)] = 0
            else:
                task_map[(r, t)] = 1
            predict_map[(r, t)] = 0

    win = visual.Window(size=(1000, 1000))

    pics_dir = os.path.join('movie_4D', 'pics')
    num_pics = len([s for s in os.listdir(
        pics_dir) if s.startswith(task_name)])
    divide_pics = time_task / (num_pics-1)

    imgs = [visual.ImageStim(win, image=os.path.join(
        pics_dir, '%s_%d.png' % (task_name, j))) for j in range(num_pics)]

    string_welcome = u'\u00A1Prepare run %d|%d,\n press any key to continue!'
    for _run in range(num_runs):
        msg = visual.TextStim(win, text=string_welcome % (_run+1, num_runs))
        msg.draw()
        win.flip()
        key = event.waitKeys()
        if key == ['escape']:
            break

        for _trail in range(num_trails):
            t = time.time()
            while True:
                circle = visual.Circle(win, radius=0.05, edges=32)
                circle.setColor(random.choices(range(255), k=3), 'rgb255')
                circle.draw()
                win.flip()
                if time_rest-(time.time()-t) < 0.1:
                    core.wait(time_rest-(time.time()-t))
                    break
                core.wait(min(random.random(), time_rest-(time.time()-t)))
            print('Passed: %f seconds.' % (time.time()-t))

            t = time.time()
            if task_map[(_run, _trail)] == 0:
                imgs[0].draw()
                win.flip()
                core.wait(time_task-(time.time()-t))
            else:
                for j, img in enumerate(imgs):
                    img.draw()
                    win.flip()
                    while (time.time()-t) < divide_pics*j:
                        pass
            print('Passed: %f seconds.' % (time.time()-t))

            label = predict()
            predict_map[(_run, _trail)] = label
            if label == task_map[(_run, _trail)]:
                msg = visual.TextStim(win, text='Correct.')
            else:
                msg = visual.TextStim(win, text='Wrong.')
            msg.draw()
            win.flip()
            core.wait(1)

    win.close()

    return task_map, predict_map
