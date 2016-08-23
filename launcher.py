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
        self.app.geometry('200x200')

        tkinter.Label(self.app, text='width (max {}): '.format(self.app.winfo_screenwidth())).pack()
        self.width_entry = tkinter.Entry(self.app)
        self.width_entry.pack()
        tkinter.Label(self.app, text='height (max {}): '.format(self.app.winfo_screenheight())).pack()
        self.height_entry = tkinter.Entry(self.app)
        self.height_entry.pack()
        self.config = {}

        # button
        self.isfullscreen = tkinter.BooleanVar()
        fullscreen = tkinter.Checkbutton(self.app, variable=self.isfullscreen, text='Fullscreen')
        fullscreen.pack()
        start_button = tkinter.Button(self.app, text='Start', command=self.start)
        start_button.pack(side='bottom')
        score_button = tkinter.Button(self.app, text='Score', command=self.score)
        score_button.pack(side='bottom')

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

    def score(self):
        self.app.destroy()
        Score()


class Score:
    def __init__(self):
        # window
        self.app = tkinter.Tk()
        self.app.title('Scores')
        self.app.geometry('200x200')

        for player, score in DB('game.db').get_scores():
            line = player + ' - ' + str(score)
            tkinter.Label(self.app, text=line).pack()

        tkinter.Button(self.app, text='Launcher', command=self.launcher).pack(side='bottom')
        self.app.mainloop()

    def launcher(self):
        self.app.destroy()
        Launcher()


if __name__ == '__main__':
    Launcher()
