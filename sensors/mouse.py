import usb
import time
import ctypes


class Mouse(object):
    """
    Represents an optical mouse connected via USB.
    Provides methods to stream mouse position coordinates (x, y)
    to the shared memory location (Point).
    """
    report_timeout = 2  # ms

    class _MouseFilter(object):

        def __call__(self, device):
            for cfg in device:
                itf = usb.util.find_descriptor(cfg, bInterfaceClass=3, bInterfaceProtocol=2)
                if itf is not None:
                    return True

            return False

    def __init__(self, usb_device):
        self.usb_device = usb_device

        try:
            if self.usb_device.is_kernel_driver_active(0):
                self.usb_device.detach_kernel_driver(0)
        except NotImplementedError:  # not implemented on Win
            pass

        cfg = self.usb_device[0]
        itf = usb.util.find_descriptor(cfg, bInterfaceClass=3, bInterfaceProtocol=2)
        self._endpoint_in = itf.endpoints()[0]

    def _read_report(self, size=None, timeout=None):
        size_f = size or self._endpoint_in.wMaxPacketSize
        timeout_f = timeout or self.report_timeout
        try:
            return self._endpoint_in.read(size_f, timeout_f)
        except usb.USBError:
            return None

    def get_position_change(self):
        report = self._read_report()
        if report:
            x = float(ctypes.c_int8(report[1]).value)
            y = float(ctypes.c_int8(report[2]).value)
            return x, y
        return 0., 0.

    @staticmethod
    def list_connected(**kwargs):
        mice = [Mouse(x) for x in usb.core.find(find_all=True, custom_match=Mouse._MouseFilter())]

        for key, value in kwargs.items():
            if value is not None:
                mice = filter(lambda x: getattr(x.usb_device, key, None) == value, mice)

        return mice


def stream(bus, address, frequency, x, y, stop_trigger):
    """
    Updates x, y (memory-shared) coordinates with actual mouse
    position with a given frequency.

    :param bus:             bus of the mouse
    :param address:         address of the mouse
    :param frequency:       update frequency in Hz
    :param x:               var to update x (multiprocessing.sharedctypes.Value)
    :param y:               var to update y (multiprocessing.sharedctypes.Value)
    :param stop_trigger:    shared Value of ctypes.c_bool (multiprocessing.sharedctypes.Value)
    """
    mouse = Mouse.list_connected(bus=bus, address=address)[0]
    delay = 1./frequency

    while not stop_trigger:
        x1, y1 = mouse.get_position_change()
        x.value += x1
        y.value += y1

        time.sleep(delay)
