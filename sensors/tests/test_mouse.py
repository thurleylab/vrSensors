import unittest
import json

from sensors.mouse import Mouse


class TestMouse(unittest.TestCase):
    """
    Run tests from main project folder.
    Apply sudo rights if on Linux (may be needed to detach mouse from the kernel).
    """

    def setUp(self):
        with open("sensors/devices.json", "r") as f:
            self.devices = json.load(f)

    def tearDown(self):
        pass

    def test_list_connected(self):
        mice = Mouse.list_connected()

        assert len(mice) >= len(self.devices)

        for dev in self.devices:
            mice = Mouse.list_connected(vendor_id=dev['vendor_id'], product_id=dev['product_id'])

            assert len(mice) > 0

            mouse = mice[0]
            assert mouse.usb_device.idVendor == dev['vendor_id']
            assert mouse.usb_device.idProduct == dev['product_id']

    def test_read_report(self):
        m1 = Mouse.list_connected()[0]

        r1 = m1._read_report()  # TODO trigger real response
        if r1:
            assert len(r1) == m1.endpoint_in.wMaxPacketSize
