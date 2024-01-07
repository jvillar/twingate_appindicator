#!/usr/bin/python3

import os
import sys
import gi
import webbrowser

try:
    gi.require_version('AyatanaAppIndicator3', '0.1')
    from gi.repository import AyatanaAppIndicator3 as AppIndicator
except ImportError:
    try:
        gi.require_version('AppIndicator3', '0.1')
        from gi.repository import AppIndicator3 as AppIndicator
    except ImportError:
        from gi.repository import AppIndicator
from gi.repository import Gtk, GLib, Gdk


class TwingateIndicator:

    def __init__(self):
        self.connected = None
        self.resources = []
        self.indicator = AppIndicator.Indicator.new(
            "twingate_appindicator",
            "calendar-tray",
            AppIndicator.IndicatorCategory.APPLICATION_STATUS)
        self.indicator.set_status(AppIndicator.IndicatorStatus.ACTIVE)
        self.update_twingate_status()

    def build_menu(self):
        menu = Gtk.Menu()
        if self.connected and len(self.resources) > 0:
            for resource in self.resources:
                resource_menu = Gtk.MenuItem(label=resource[0])

                resource_menu_submenu = Gtk.Menu()

                https_resource_menu_open_item = Gtk.MenuItem(label="Open in browser as https://")
                https_resource_menu_open_item.connect("activate", lambda widget, data: self.open_link(data), f'https://{resource[1]}')
                resource_menu_submenu.append(https_resource_menu_open_item)
                https_resource_menu_open_item.show()

                http_resource_menu_open_item = Gtk.MenuItem(label="Open in browser as http://")
                http_resource_menu_open_item.connect("activate", lambda widget, data: self.open_link(data), f'https://{resource[1]}')
                resource_menu_submenu.append(http_resource_menu_open_item)
                http_resource_menu_open_item.show()

                resource_menu_copy_item = Gtk.MenuItem(label="Copy to clipboard")
                resource_menu_copy_item.connect("activate", lambda widget, data: self.copy_to_clipboard(data), resource[1])
                resource_menu_submenu.append(resource_menu_copy_item)
                resource_menu_copy_item.show()

                resource_menu_submenu.show()

                resource_menu.set_submenu(resource_menu_submenu)

                resource_menu.show()
                menu.append(resource_menu)
            menu.append(Gtk.SeparatorMenuItem())
        toggle_connect_menu = Gtk.MenuItem(label=self.get_label())
        toggle_connect_menu.connect("activate", self.toggle_twingate)
        menu.append(toggle_connect_menu)
        toggle_connect_menu.show()
        menu.connect("deactivate", lambda widget: widget.destroy())
        self.indicator.set_menu(menu)

    def update_twingate_status(self):
        regenerate_menu = False

        connected = self.twingate_status()
        if self.connected != connected:
            self.connected = connected
            self.indicator.set_icon_full(self.get_icon(), "twingate")
            regenerate_menu = True

        resources = self.twingate_resources()
        if resources != self.resources:
            self.resources = resources
            regenerate_menu = True

        if regenerate_menu:
            self.build_menu()

        return True

    def get_label(self):
        return "Disconnect" if self.connected else "Connect"

    def get_icon(self):
        icon = "twingate-up.svg" if self.connected else "twingate-down.svg"
        return os.path.join(os.path.dirname(__file__), icon) 

    def twingate_resources(self):
        output = os.popen('twingate resources').read()
        resources = [o.split()[0:2] for o in output.split("\n")[1:]]
        return list(filter(lambda item: len(item) == 2, resources))

    def twingate_status(self):
        return os.popen('twingate status').read().startswith("online")

    def toggle_twingate(self, _=None):
        if self.connected:
            self.twingate_disconnect()
        else:
            self.twingate_connect()

    def twingate_connect(self, _=None):
        os.system("pkexec twingate start")
        os.system("twingate desktop-restart")

    def twingate_disconnect(self, _=None):
        os.system("pkexec twingate stop")
        os.system("twingate desktop-stop")

    def open_link(self, url):
        webbrowser.open(url)

    def copy_to_clipboard(self, text):
        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        clipboard.set_text(text, -1)
        clipboard.store()

    def main(self):
        GLib.timeout_add_seconds(0.5, self.update_twingate_status)
        Gtk.main()

    def quit(self, widget):
        sys.exit(0)


if __name__ == "__main__":
    TwingateIndicator().main()
