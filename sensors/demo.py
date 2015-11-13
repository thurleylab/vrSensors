import ctypes
import Tkinter

from multiprocessing import Process
from multiprocessing.sharedctypes import Value
from mouse import Mouse, stream


class DemoApp:

    def __init__(self):
        self.master = Tkinter.Tk()

        self.x = Tkinter.StringVar()
        self.x.set("0.0")
        self.y = Tkinter.StringVar()
        self.y.set("0.0")

        Tkinter.Label(self.master, textvariable=self.x).pack()
        Tkinter.Label(self.master, textvariable=self.y).pack()


def launch_app(frequency, x, y, stop_trigger):
    def on_destroy():
        stop_trigger.value = True
        app.master.destroy()

    def on_key(event):
        if event.keycode == 9 or event.keycode == 27:  # escape event Linux/Win
            on_destroy()

    def coords_update():
        app.x.set(x.value)
        app.y.set(y.value)

        app.master.after(delay, coords_update)

    delay = int(100/frequency)

    app = DemoApp()
    app.master.bind("<Key>", on_key)
    app.master.protocol("WM_DELETE_WINDOW", on_destroy)

    coords_update()
    app.master.mainloop()


if __name__ == "__main__":
    m1 = Mouse.list_connected()[0]

    x = Value('d', 0.0, lock=False)
    y = Value('d', 0.0, lock=False)
    stop_trigger = Value(ctypes.c_bool, False, lock=False)

    mouse_process = Process(target=stream, args=(m1.usb_device.bus, m1.usb_device.address, 200, x, y, stop_trigger))
    app_process = Process(target=launch_app, args=(50, x, y, stop_trigger))

    mouse_process.start()
    app_process.start()

    mouse_process.join()
    app_process.join()
