# General Imports
import os

# Window Imports
try:
    from newCustomerWindow import NewCustomerWindow
    from aboutWindow import AboutWindow
except:
    from src.python.newCustomerWindow import NewCustomerWindow
    from src.python.aboutWindow import AboutWindow

# GTK Imports
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk as gtk


class MainWindow(object):

    ##### MENU BAR ITEMS #####
    def on_AboutItem_activate(self, object):
        window = AboutWindow(self.gladefile)

    def on_NewFileItem_activate(self, object):
        print("Opening NewCustomerWindow")
        dialog = NewCustomerWindow(self.gladefile)
        response = dialog.run()

    def on_QuitFileItem_activate(self, object):
        print("Exiting Application from Menu Bar...")
        gtk.main_quit()
    ##### MENU BAR ITEMS #####


    ##### BUTTONS #####
    def on_NewCustomerButton_clicked(self, object):
        print("Opening NewCustomerWindow")

        # dialog = NewCustomerWindow(self.window)
        dialog = NewCustomerWindow(self.gladefile)
        response = None

        if response == gtk.ResponseType.OK:
            ticket = dialog.get_result()
            ticketNumber = ticket['ticketNumber']
            self.tickets[ticketNumber] = ticket
            print("Ticket %s was added" % ticketNumber)
        elif response == gtk.ResponseType.CANCEL:
            print("No Ticket was added")

    def on_CheckBackupsButton_clicked(self, object):
        None
    ##### BUTTONS #####


    ##### INITIALIZATION #####
    def __init__(self, gladefile):
        icon = os.path.dirname(os.path.abspath(__file__)) + '/../assets/drive.png'

        # Set the Gladefile to read from
        self.gladefile = gladefile

        # Create the GTK Builder from the Gladefile
        self.builder = gtk.Builder()
        self.builder.add_from_file(self.gladefile)
        self.builder.connect_signals(self)

        # Locate the MainWindow and display
        self.window = self.builder.get_object("MainWindow")
        self.window.connect("destroy", gtk.main_quit)
        self.window.set_title("TechStop Backup Utility")
        self.window.set_icon_from_file(icon)
        self.window.show()
    ##### INITIALIZATION #####
