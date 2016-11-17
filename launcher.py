# Python packages
import tkinter

# Modules from this project
from db import DB
from game import Game


class Launcher:
    def __init__(self):
        # window
        self.app = tkinter.Tk()
        self.app.title('DevInVale2015')

        self.config_frame = tkinter.Frame()
        self.score_frame = tkinter.Frame()

        tkinter.Label(self.config_frame, text='width (max {}): '
                      .format(self.app.winfo_screenwidth())).pack()
        self.width_entry = tkinter.Entry(self.config_frame)
        self.width_entry.pack()
        tkinter.Label(self.config_frame, text='height (max {}): '
                      .format(self.app.winfo_screenheight())).pack()
        self.height_entry = tkinter.Entry(self.config_frame)
        self.height_entry.pack()
        self.config = {}

        # buttons
        self.isfullscreen = tkinter.BooleanVar()
        tkinter.Checkbutton(self.config_frame, variable=self.isfullscreen, text='Fullscreen').pack()
        tkinter.Button(self.config_frame, text='Start', command=self.start).pack(side='bottom')

        # scores
        tkinter.Label(self.score_frame, text='Score\n').pack()
        for player, score in DB('game.db').scores():
            line = player + ' - ' + str(score)
            tkinter.Label(self.score_frame, text=line).pack()

        self.config_frame.grid(row=0, column=0, padx=10, pady=10)
        self.score_frame.grid(row=0, column=1, padx=20, pady=10)

        self.app.mainloop()

    def read_entry(self):
        self.config['resolution'] = None
        try:
            width = int(self.width_entry.get())
            height = int(self.height_entry.get())
            if width <= int(self.app.winfo_screenwidth()) and height <= int(self.app.winfo_screenheight()):
                self.config['resolution'] = (width, height)
        except ValueError:
            pass

    def start(self):
        self.read_entry()
        self.app.destroy()
        if self.config['resolution']:
            game = Game(width=self.config['resolution'][0],
                        height=self.config['resolution'][1],
                        fullscreen=self.isfullscreen.get())
        else:
            game = Game(fullscreen=self.isfullscreen.get())
        game.run()


if __name__ == '__main__':
    Launcher()
