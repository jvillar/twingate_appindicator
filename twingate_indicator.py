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
        self.indicator = AppIndicator.Indicator.new("twingate_appindicator", "calendar-tray", AppIndicator.IndicatorCategory.APPLICATION_STATUS)
        self.indicator.set_status(AppIndicator.IndicatorStatus.ACTIVE)
        self.menu_setup()
        self.indicator.set_menu(self.menu)

    def menu_setup(self):
        self.menu = Gtk.Menu()
        self.toggle_connect_menu = Gtk.MenuItem(label="")
        self.toggle_connect_menu.connect("activate", self.toggle_twingate)
        self.menu.append(self.toggle_connect_menu)
        self.toggle_connect_menu.show()
        
    def update_state(self):
        connected = self.twingate_status()
        if self.connected != connected:
            self.connected = connected
            self.indicator.set_icon_full(self.get_icon(), "twingate")
            self.toggle_connect_menu.set_label(self.get_label())
        return True
    
    def get_label(self):
        return "Disconnect" if self.connected else "Connect"
        
    def get_icon(self):
        icon = "twingate-up.svg" if self.connected else "twingate-down.svg"
        return os.path.join(os.path.dirname(__file__), icon) 
    
    def twingate_status(self):
        return os.popen('twingate status').read().startswith("online")
    
    def toggle_twingate(self, _=None):
        if self.connected:
            self.twingate_disconnect()
        else:
            self.twingate_connect()
        
    def twingate_connect(self, _=None):
        os.system("pkexec twingate start")

    def twingate_disconnect(self, _=None):
       os.system("pkexec twingate stop")
    
    def main(self):
        GLib.timeout_add_seconds(0.5, self.update_state)
        Gtk.main()

    def quit(self, widget):
        sys.exit(0)
       
if __name__ == "__main__":
    TwingateIndicator().main()
