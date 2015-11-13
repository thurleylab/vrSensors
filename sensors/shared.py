import ctypes


class Point(ctypes.Structure):
    """
    C-like structure to hold and share actual
    coordinates of the mouse between processes.
    """
    _fields_ = [('x', ctypes.c_double), ('y', ctypes.c_double)]

    def __getstate__(self):
        return {'x': self.x, 'y': self.y}

    def __setstate__(self, state):
        self.x = state['x']
        self.y = state['y']