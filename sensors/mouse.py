import usb


class Mouse(object):

    def __init__(self, usb_device):
        self.usb_device = usb_device

    @staticmethod
    def list_connected(vendor_id=None, product_id=None):
        mouse_filter = MouseFilter(vendor_id, product_id)

        return [Mouse(x) for x in usb.core.find(find_all=True, custom_match=mouse_filter)]


class MouseFilter(object):

    def __init__(self, vendor_id=None, product_id=None):
        self.vendor_id = vendor_id
        self.product_id = product_id

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

