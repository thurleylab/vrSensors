import ctypes


class Point(ctypes.Structure):
    """
    C-like structure to hold and share actual
    coordinates of the mouse between processes.
    """
    _fields_ = [('x', ctypes.c_double), ('y', ctypes.c_double)]