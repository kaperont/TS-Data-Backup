import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class NewCustomerWindow(object):
    def onDestroy(self, object, data=None):
        self.window.destroy()

    def on_StartBackupButton_clicked(self, object, data=None):
        print("Beginning Backup...")

        customerNameEntry = self.builder.get_object("CustomerNameForm")
        ticketNumberEntry = self.builder.get_object("TicketNumberForm")
        srcDirectoryEntry = self.builder.get_object("SrcDirectoryForm")

        customerName = customerNameEntry.get_text()
        ticketNumber = ticketNumberEntry.get_text()
        srcDirectory = srcDirectoryEntry.get_text()

        if customerName and ticketNumber and srcDirectory:
            ticket = {'customerName': customerName, 'ticketNumber': ticketNumber, 'srcDirectory': srcDirectory}
            self.tickets[ticketNumber] = ticket
            print(self.tickets)
        else:
            print("Did not receive any data")

    def __init__(self, tickets):
        # Set the Gladefile to read from
        self.gladefile = "../glade/backup-utility.glade"

        # Create the GTK Builder from the Gladefile
        self.builder = Gtk.Builder()
        self.builder.add_from_file(self.gladefile)
        self.builder.connect_signals(self)

        # Locate the NewCustomerWindow and display
        self.window = self.builder.get_object("NewCustomerWindow")
        self.window.show()
        self.tickets = tickets