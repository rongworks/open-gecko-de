#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk
import os
import dbus


class LogoutWindow:

    def cancel(self, widget, event, data=None):
        gtk.main_quit()
        return False

    def logout(self, widget):
        os.system("openbox --exit")

    def suspend(self, widget):
        bus = dbus.SystemBus()
        bus_object = bus.get_object("org.freedesktop.UPower",
                "/org/freedesktop/UPower")
        bus_object.Suspend(0, dbus_interface="org.freedesktop.UPower")

    def reboot(self, widget):
        bus = dbus.SystemBus()
        bus_object = bus.get_object("org.freedesktop.ConsoleKit",
                "/org/freedesktop/ConsoleKit/Manager")
        bus_object.Restart(dbus_interface="org.freedesktop.ConsoleKit.Manager")

    def shutdown(self, widget):
        bus = dbus.SystemBus()
        bus_object = bus.get_object("org.freedesktop.ConsoleKit",
                "/org/freedesktop/ConsoleKit/Manager")
        bus_object.Stop(dbus_interface="org.freedesktop.ConsoleKit.Manager")

    def __init__(self):

        # Create a new window.
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title("Exit? Choose an option:")
        self.window.set_resizable(False)
        self.window.set_position(1)
        self.window.connect("delete_event", self.cancel)
        self.window.set_border_width(20)

        # Create a box to pack widgets into.
        self.box = gtk.HBox(False, 0)
        self.window.add(self.box)

        # Create cancel button.
        self.cancel_button = gtk.Button("Cancel")
        self.cancel_button.connect("clicked", self.cancel, "Changed me mind :)")
        self.box.pack_start(self.cancel_button, True, True, 0)
        self.cancel_button.show()

        # Create logout button.
        self.logout_button = gtk.Button("Log out")
        self.logout_button.connect("clicked", self.logout)
        self.box.pack_start(self.logout_button, True, True, 0)
        self.logout_button.show()

        # Create suspend button.
        self.suspend_button = gtk.Button("Suspend")
        self.suspend_button.connect("clicked", self.suspend)
        self.box.pack_start(self.suspend_button, True, True, 0)
        self.suspend_button.show()

        # Create reboot button.
        self.reboot_button = gtk.Button("Reboot")
        self.reboot_button.connect("clicked", self.reboot)
        self.box.pack_start(self.reboot_button, True, True, 0)
        self.reboot_button.show()

        # Create shutdown button.
        self.shutdown_button = gtk.Button("Shutdown")
        self.shutdown_button.connect("clicked", self.shutdown)
        self.box.pack_start(self.shutdown_button, True, True, 0)
        self.shutdown_button.show()

        for button in (self.cancel_button, self.logout_button,
                self.suspend_button, self.reboot_button, self.shutdown_button):
            button.set_border_width(10)

        self.box.show()
        self.window.show()


def main():
    gtk.main()


if __name__ == "__main__":
    gogogo = LogoutWindow()
main()