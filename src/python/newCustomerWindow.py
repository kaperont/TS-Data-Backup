# General Imports
from os import path
from subprocess import run
from utils.hd_test import shortDST, longDST

# Window Imports
from checkDiskProgressWindow import CheckDiskProgressWindow
from driveListWindow import DriveListWindow

# GTK Imports
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk as gtk


class NewCustomerWindow(object):

    def on_SelectPartitionButton_clicked(self, object):
        dialog = DriveListWindow(self.window)
        response = dialog.run()
        
        if response == gtk.ResponseType.OK:
            self.partition = dialog.get_result()
            if not self.partition:
                print("No Partition was selected")
            else:
                srcPartitionEntry = self.builder.get_object("SrcPartitionForm")
                srcPartitionEntry.set_text(self.partition[-1])
                print("The Partition %s was Selected" % self.partition[-1])
        elif response == gtk.ResponseType.CANCEL:
            print("No Partition was selected")
        
        dialog.destroy()

    # Start Backup Button has been clicked
    def on_StartBackupButton_clicked(self, object, data=None):

        # Grab the input objects
        customerNameEntry = self.builder.get_object("CustomerNameForm")
        ticketNumberEntry = self.builder.get_object("TicketNumberForm")
        srcPartitionEntry = self.builder.get_object("SrcPartitionForm")

        # Extract the data from the input objects
        customerName = customerNameEntry.get_text()
        ticketNumber = ticketNumberEntry.get_text()
        srcPartition = srcPartitionEntry.get_text()

        # Check for empty forms - If one exists, set its focus to alert user
        if not customerName:
            print("Customer's name was not declared")
            customerNameEntry.grab_focus_without_selecting()
            return
        elif not ticketNumber:
            print("Ticket number was not declared")
            ticketNumberEntry.grab_focus_without_selecting()
            return
        elif not srcPartition:
            print("Source partition was not declared")
            srcPartitionEntry.grab_focus_without_selecting()
            return

        # Extract the drive to test
        drive = self.partition[0]
        drivePath = '/dev/' + drive[0:-1]
        
        # Otherwise, create a "ticket" and push it to the dict
        self.ticket = {'customerName': customerName, 'ticketNumber': ticketNumber, 'srcPartition': srcPartition}
        print(self.ticket)

        # Hopefully show progress window...
        self.progressWindow.show()

        # Run drive test
        if self.progressWindow.shortDST(drivePath):
            print("%s passed the hard drive test.\nBeginning Backup..." % drivePath)

    # NewCustomerWindow init
    def __init__(self):
        # Set the Gladefile to read from
        self.gladefile = "../glade/backup-utility.glade"

        # Create the GTK Builder from the Gladefile
        self.builder = gtk.Builder()
        self.builder.add_from_file(self.gladefile)
        self.builder.connect_signals(self)

        # Locate the NewCustomerWindow and display
        self.window = self.builder.get_object("NewCustomerWindow")
        self.window.set_title("New Customer")
        self.window.show()

        # Initialize the Progress Window
        self.progressWindow = CheckDiskProgressWindow()