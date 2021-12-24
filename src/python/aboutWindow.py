# GTK Imports
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class AboutWindow(object):

    # Destruction of Window
    def onDestroy(self, object, data=None):
        self.window.destroy()

    # AboutWindow init
    def __init__(self, gladefile):
        # Set the Gladefile to read from
        self.gladefile = gladefile

        # Create the GTK Builder from the Gladefile
        self.builder = Gtk.Builder()
        self.builder.add_from_file(self.gladefile)
        self.builder.connect_signals(self)

        # Locate the AboutWindow and display
        self.window = self.builder.get_object("AboutWindow")
        self.window.show()