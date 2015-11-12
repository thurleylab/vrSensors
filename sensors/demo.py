import ctypes
import Tkinter

from multiprocessing import Process
from multiprocessing.sharedctypes import Value
from mouse import Mouse
from shared import Point


class DemoApp:

    def __init__(self):
        self.master = Tkinter.Tk()

        self.x = Tkinter.StringVar()
        self.x.set("0.0")
        self.y = Tkinter.StringVar()
        self.y.set("0.0")

        Tkinter.Label(self.master, textvariable=self.x).pack()
        Tkinter.Label(self.master, textvariable=self.y).pack()


def launch_app(frequency, coordinates, stop_trigger):
    def on_destroy():
        stop_trigger.value = True
        app.master.destroy()

    def on_key(event):
        if event.keycode == 9:  # escape event
            on_destroy()

    def coords_update():
        app.x.set(coordinates.x)
        app.y.set(coordinates.y)

        app.master.after(delay, coords_update)

    delay = int(100/frequency)

    app = DemoApp()
    app.master.bind("<Key>", on_key)
    app.master.protocol("WM_DELETE_WINDOW", on_destroy)

    coords_update()
    app.master.mainloop()


if __name__ == "__main__":
    m1 = Mouse.list_connected()[0]
    coordinates = Value(Point, 0., 0., lock=False)
    stop_trigger = Value(ctypes.c_bool, False, lock=False)

    mouse_process = Process(target=m1.stream, args=(200, coordinates, stop_trigger))
    app_process = Process(target=launch_app, args=(50, coordinates, stop_trigger))

    mouse_process.start()
    app_process.start()

    mouse_process.join()
    app_process.join()
