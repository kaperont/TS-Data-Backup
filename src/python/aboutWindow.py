import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class AboutWindow(object):
    def onDestroy(self, object, data=None):
        self.window.destroy()

    def __init__(self, tickets):
        # Set the Gladefile to read from
        self.gladefile = "../ui/backup-utility.glade"

        # Create the GTK Builder from the Gladefile
        self.builder = Gtk.Builder()
        self.builder.add_from_file(self.gladefile)
        self.builder.connect_signals(self)

        # Locate the AboutWindow and display
        self.window = self.builder.get_object("AboutWindow")
        self.window.show()
        self.tickets = tickets