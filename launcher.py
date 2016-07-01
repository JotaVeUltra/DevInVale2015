# Python packages
import tkinter

# Modules from this project
from game import Game


class Launcher:
    def __init__(self):
        # window
        self.app = tkinter.Tk()
        self.app.title('DevInVale2015')
        self.app.geometry('200x200')

        tkinter.Label(self.app, text='width: ').pack()
        self.width_entry = tkinter.Entry(self.app)
        self.width_entry.pack()
        tkinter.Label(self.app, text='height: ').pack()
        self.height_entry = tkinter.Entry(self.app)
        self.height_entry.pack()

        # button
        self.start_button = tkinter.Button(self.app, text='Start', command=self.start)
        self.start_button.pack(side='bottom')

        self.app.mainloop()

    def read_entry(self):
        try:
            width = int(self.width_entry.get())
            height = int(self.height_entry.get())
            return {'width': width, 'height': height}
        except ValueError:
            return

    def start(self):
        resolution = self.read_entry()
        self.app.destroy()
        if resolution:
            game = Game(width=resolution['width'], height=resolution['height'])
        else:
            game = Game()
        game.run()


if __name__ == '__main__':
    Launcher()
