import tkinter as tk
import time


class Application(tk.Frame):
    def say_hi(self):
        print("hi there, everyone!")

    def createWidgets(self):
        self.QUIT = tk.Button(self)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"] = "red"
        self.QUIT["command"] = self.quit

        self.QUIT.pack(side='top')

        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Hello",
        self.hi_there["command"] = self.say_hi

        self.hi_there.pack(side='bottom')

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack()
        self.createWidgets()


root = tk.Tk()
root.geometry('800x600+100+200')
root.resizable(False, False)

frame = tk.Frame(root)
frame['bg'] = 'cyan'
frame.place(relx=0.5, y=400, width=100, height=50)
# frame.pack()


def tc(s=None):
    if s:
        print(s)
    else:
        print(time.ctime())


def cc(b=None):
    if b is None:
        return
    print(b.pi)
    if b.visible:
        b.place_forget()
        b.visible = False
    else:
        b.place(b.pi)
        b.visible = True


button = tk.Button(frame, text='aaa', fg='red', command=lambda s='x': tc(s))
button.place(relx=0.5, rely=0.5, width=50, height=20)
button.visible = True
button.pi = button.place_info()


button1 = tk.Button(frame, text='bbb', fg='blue',
                    command=lambda x=button: cc(x))
button1.place(relx=0, rely=0, width=50, height=20)

frame.mainloop()

# app = Application(master=root)
# app.mainloop()
# root.destroy()
