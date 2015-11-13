About
-----

The *vrSensors* project provides access to real-time position of optical mouse, connected via USB.
The only dependency is the pyusb library, which works via libusb [http://www.libusb.org](http://www.libusb.org).

Prerequisites
-------------

If you're on WINDOWS, follow the instructions here
http://www.libusb.org/wiki/libusb-win32

To check the installation, make sure that
- libusb0.sys is in windows\system32\drivers
- libusb0.dll is in windows\system32
- libusb0.dll is in windows\syswow64 (if 64bit)

If a mouse is automatically recognized as a HID device, one should follow steps described in Device Driver Installation.
After that the mouse should become a libusb-win32 type device and no longer impact the movement of the screen pointer.


If you're on LINUX, check this out [http://www.libusb.org/wiki/libusb-1.0](http://www.libusb.org/wiki/libusb-1.0)

there should be also a package for Debian systems:

```
sudo apt-get install libusb-1.0-0-dev
```

Make sure (!!) to run demo / tests / modules with sudo, as activating the communication with a device on Linux requires
detaching it from the kernel, which requires administrative priviledges.