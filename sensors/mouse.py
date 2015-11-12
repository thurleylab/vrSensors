import usb
import time
import ctypes


class Mouse(object):
    """
    Represents an optical mouse connected via USB.
    Provides methods to stream mouse position coordinates (x, y)
    to the shared memory location (Point).
    """

    _inch_to_meter = 0.0254
    x_resolution = 400.
    y_resolution = 400.
    report_timeout = 100  # ms

    def __init__(self, usb_device):
        self.usb_device = usb_device

        if self.usb_device.is_kernel_driver_active(0):
            self.usb_device.detach_kernel_driver(0)

        cfg = self.usb_device[0]
        itf = usb.util.find_descriptor(cfg, bInterfaceClass=3, bInterfaceProtocol=2)
        self.endpoint_in = itf.endpoints()[0]

    def _read_report(self, size=None, timeout=None):
        size_f = size or self.endpoint_in.wMaxPacketSize
        timeout_f = timeout or self.report_timeout
        try:
            return self.endpoint_in.read(size_f, timeout_f)
        except usb.USBError:
            return None

    def _get_position_change(self):
        report = self._read_report()
        if report:
            x = float(ctypes.c_int8(report[1]).value) / self.x_resolution
            y = float(ctypes.c_int8(report[2]).value) / self.x_resolution
            return x, y
        return 0, 0

    def stream(self, frequency, coordinates, stop_trigger):
        """
        Updates given (memory-shared) coordinates with actual mouse
        position with a given frequency.

        :param frequency:       update frequency in Hz
        :param coordinates:     shared Value of mouse.Point (multiprocessing.sharedctypes.Value)
        :param stop_trigger:    shared Value of ctypes.c_bool (multiprocessing.sharedctypes.Value)
        """
        delay = 1./frequency

        while not stop_trigger:
            x1, y1 = self._get_position_change()
            coordinates.x += x1
            coordinates.y += y1

            time.sleep(delay)

    @staticmethod
    def list_connected(vendor_id=None, product_id=None):
        mouse_filter = _MouseFilter(vendor_id, product_id)

        return [Mouse(x) for x in usb.core.find(find_all=True, custom_match=mouse_filter)]


class Point(ctypes.Structure):
    """
    C-like structure to hold and share actual
    coordinates of the mouse between processes.
    """
    _fields_ = [('x', ctypes.c_double), ('y', ctypes.c_double)]


class _MouseFilter(object):

    def __init__(self, vendor_id=None, product_id=None):
        self.vendor_id = int(vendor_id) if vendor_id else None
        self.product_id = int(product_id) if product_id else None

    def __call__(self, device):
        if self.vendor_id and device.idVendor != self.vendor_id:
            return False

        if self.product_id and device.idProduct != self.product_id:
            return False

        for cfg in device:
            itf = usb.util.find_descriptor(cfg, bInterfaceClass=3, bInterfaceProtocol=2)
            if itf is not None:
                return True

        return False


if __name__ == "__main__":
    x = 0.0
    y = 0.0

    devs = Mouse.list_connected()

    m1 = devs[0]
    flag = 0
    while True:
        time.sleep(0.01)
        flag += 1
        x1, y1 = m1.get_position_change()
        x += x1
        y += y1
        if flag == 10:
            flag = 0
            print "x: %d : %d" % (x, y)

        #report = m1._read_report()
        #if report:
        #    print report
