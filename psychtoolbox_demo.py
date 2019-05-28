from psychopy import visual, core, event

win = visual.Window()
msg = visual.TextStim(win, text=u"\u00A1Hola mundo!")

msg.draw()
win.flip()
core.wait(1)

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

core.wait(3)
msg = visual.TextStim(win, text='getKeys begins.')
keys = event.getKeys(timeStamped=True)
print(keys)

win.close()
