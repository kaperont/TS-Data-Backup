import gi

from backup_utility import App
from newCustomerWindow import NewCustomerWindow
from aboutWindow import AboutWindow

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class MainWindow(object):

    def on_NewCustomerButton_clicked(self, object, data=None):
        print("Opening NewCustomerWindow")
        window = NewCustomerWindow(self.tickets)

    def on_AboutItem_activate(self, object, data=None):
        window = AboutWindow(self.tickets)

    def on_NewFileItem_activate(self, object, data=None):
        window = NewCustomerWindow(self.tickets)

    def on_QuitFileItem_activate(self, object):
        print("Exiting Application from Menu Bar...")
        Gtk.main_quit()

    def __init__(self, tickets):
        # Set the Gladefile to read from
        self.gladefile = "../ui/backup-utility.glade"

        # Create the GTK Builder from the Gladefile
        self.builder = Gtk.Builder()
        self.builder.add_from_file(self.gladefile)
        self.builder.connect_signals(self)

        # Locate the MainWindow and display
        self.window = self.builder.get_object("MainWindow")
        self.window.connect("destroy", Gtk.main_quit)
        self.window.show()
        self.tickets = tickets