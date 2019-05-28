# coding: utf-8

import os
import time
from psychopy import visual, core, event


win = visual.Window()

msg = visual.TextStim(win, text=u"\u00A1Hola mundo!")

msg.draw()
win.flip()
core.wait(1)

n = 117
s = 4/(n-1)
imgs = [visual.ImageStim(win, image=os.path.join(
    'movie_4D', 'pics', '%s_%d.png' % ('quzhou', j))) for j in range(n)]

t = time.time()
for j, img in enumerate(imgs):
    img.draw()
    win.flip()
    while (time.time()-t) < s*j:
        pass

print(time.time()-t)

event.waitKeys()

'''
msg = visual.TextStim(win, text='waitKeys begins.')
msg.draw()
win.flip()
while True:
    key = event.waitKeys()
    msg = visual.TextStim(win, text='%s pressed.' % key)
    msg.draw()
    win.flip()
    if key == ['escape']:
        break

for j in range(3, 0, -1):
    msg = visual.TextStim(win, text='Close in %d seconds.' % j)
    msg.draw()
    win.flip()
    core.wait(1)
    keys = event.getKeys(timeStamped=True)
    print(keys)
'''
win.close()
