# Python packages
import tkinter
from configparser import ConfigParser
from os.path import isfile

# Modules from this project
from constants import TITLE, SETTINGS, DEFAULT_SETTINGS
from db import scores
from game import Game


class Launcher:
    def __init__(self):
        # window
        self.app = tkinter.Tk()
        self.app.title(TITLE)

        config_frame = tkinter.Frame()
        score_frame = tkinter.Frame()

        self.config = ConfigParser()
        if isfile(SETTINGS):
            self.config.read(SETTINGS)
        else:
            self.config.read(DEFAULT_SETTINGS)
            with open(SETTINGS, 'w') as configfile:
                self.config.write(configfile)

        tkinter.Label(config_frame, text='player name').pack()
        self.name_entry = tkinter.Entry(config_frame)
        self.name_entry.insert(tkinter.END, self.config['USER']['player'])
        self.name_entry.pack()

        # buttons
        self.isfullscreen = tkinter.BooleanVar()
        self.isfullscreen.set(self.config['VIDEO']['fullscreen'] == 'yes')
        tkinter.Checkbutton(config_frame, variable=self.isfullscreen, text='Fullscreen').pack(pady=10)
        tkinter.Button(config_frame, text='Start', command=self.start).pack(side='bottom')

        # scores
        tkinter.Label(score_frame, text='Score\n').pack()
        for player, score in scores():
            line = '{} - {}'.format(player, score)
            tkinter.Label(score_frame, text=line).pack()

        config_frame.grid(row=0, column=0, padx=10, pady=10)
        score_frame.grid(row=0, column=1, padx=20, pady=10)

        self.app.mainloop()

    def read_entry(self):
        self.config['VIDEO']['fullscreen'] = 'yes' if self.isfullscreen.get() else 'no'
        self.config['USER']['player'] = self.name_entry.get()
        with open(SETTINGS, 'w') as configfile:
            self.config.write(configfile)

    def start(self):
        self.read_entry()
        self.app.destroy()
        game = Game()
        game.run()


if __name__ == '__main__':
    Launcher()
