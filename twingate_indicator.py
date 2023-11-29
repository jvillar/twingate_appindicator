#!/usr/bin/python
import os, sys, gi
try:
    gi.require_version('AyatanaAppIndicator3', '0.1')
    from gi.repository import AyatanaAppIndicator3 as AppIndicator
except ImportError:
    try:
        gi.require_version('AppIndicator3', '0.1')
        from gi.repository import AppIndicator3 as AppIndicator
    except ImportError:
        from gi.repository import AppIndicator
from gi.repository import Gtk, GLib

class TwingateIndicator:
    
    def __init__(self):
        self.connected = None
        self.indicator = AppIndicator.Indicator.new(
            "twingate_appindicator", "calendar-tray", AppIndicator.IndicatorCategory.APPLICATION_STATUS
        )
        self.indicator.set_status(AppIndicator.IndicatorStatus.ACTIVE)
        self.menu_setup()
        self.indicator.set_menu(self.menu)

    def menu_setup(self):
        self.menu = Gtk.Menu()
        self.connect_menu = Gtk.MenuItem(label="Connect")
        self.dissconnect_menu = Gtk.MenuItem(label="Dissconnect")
        self.connect_menu.connect("activate", self.twingate_connect)
        self.dissconnect_menu.connect("activate", self.twingate_dissconnect)
        self.dissconnect_menu.show()
        self.connect_menu.show()
        self.quit_item = Gtk.MenuItem(label="Quit")
        self.quit_item.connect("activate", self.quit)
        self.quit_item.show()

    def update_state(self):
        connected = self.twingate_status()
        if self.connected != connected:
            self.connected = connected
            self.indicator.set_icon_full(self.get_icon(), "twingate")
            if self.connected:
                self.connect_menu.hide()
                self.dissconnect_menu.show()
            else:
                self.connect_menu.show()
                self.dissconnect_menu.hide()
        return True
    
    def get_icon(self):
        icon = "twingate-up.svg" if self.connected else "twingate-down.svg"
        return os.path.join(os.path.dirname(__file__), icon) 
    
    def twingate_status(self):
        return os.popen('twingate status').read().startswith("online")
        
    def twingate_connect(self, _):
        os.system("pkexec twingate start")

    def twingate_dissconnect(self, _):
       os.system("pkexec twingate stop")
    
    def main(self):
        GLib.timeout_add_seconds(1, self.update_state)
        self.menu.append(self.connect_menu)
        self.menu.append(self.dissconnect_menu)
        self.menu.append(self.quit_item)
        Gtk.main()

    def quit(self, widget):
        sys.exit(0)
        
       
if __name__ == "__main__":
    TwingateIndicator().main()

