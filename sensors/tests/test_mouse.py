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

        assert len(mice) > 0

        for mouse in mice:
            l1 = Mouse.list_connected(idVendor=mouse.usb_device.idVendor, idProduct=mouse.usb_device.idProduct)

            assert len(l1) > 0
            assert mouse.usb_device.idVendor == l1[0].usb_device.idVendor
            assert mouse.usb_device.idProduct == l1[0].usb_device.idProduct

    def test_read_report(self):
        m1 = Mouse.list_connected()[0]

        r1 = m1._read_report()  # TODO trigger real response
        if r1:
            assert len(r1) == m1.endpoint_in.wMaxPacketSize
