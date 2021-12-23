# General Imports
from utils.mount_drive import mountPart, unmountPart

# Window Imports
from checkDiskProgressWindow import CheckDiskProgressWindow
from driveListWindow import DriveListWindow

# GTK Imports
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk as gtk


class NewCustomerWindow(object):

    def on_SelectPartitionButton_clicked(self, object):
        # Open the drive selection dialog
        dialog = DriveListWindow(self.window)
        response = dialog.run()
        
        if response == gtk.ResponseType.OK:
            # If response is OK, grab the result
            self.partition = dialog.get_result()

            # If the result is None, say so; otherwise, set the Entry Form
            if self.partition is None:
                print("No Partition was selected")
            else:
                # Extract data from the result
                partition = self.partition['name']
                size = self.partition['size']
                type = self.partition['type']
                mountpoint = self.partition['mountpoint']

                # Create paths
                partitionPath = '/dev/' + partition
                self.drivePath += partition[0:-1]

                # Check for an encrypted drive
                if type == '':
                    print('There is no filesystem!')
                    return
                elif type == 'BitLocker':
                    mountpoint = mountPart(partition=partitionPath, driveType=type, password='682198-010989-363242-107250-566379-316712-080817-593428')
                    self.encrypted = True
                elif type == 'apfs':
                    self.encrypted = True
                elif type == 'ntfs':
                    self.encrypted = True
                
                if mountpoint == '':
                    print("There is no mountpoint!")
                    return
                
                # Grab and set the source partition entry form
                srcPartitionEntry = self.builder.get_object("SrcPartitionForm")
                srcPartitionEntry.set_text(mountpoint)

                # Give some good feedback :)
                print("The Partition %s was Selected at Mountpoint: %s" % (partition, mountpoint))

        elif response == gtk.ResponseType.CANCEL:
            # If response is CANCEL, continue
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
        
        # If hard drive is not encrypted, run a quick hard drive test before proceeding
        if not self.encrypted:

            # Hopefully show progress window...
            self.progressWindow.show()

            # Run drive test
            if self.progressWindow.shortDST(self.drivePath):
                print("%s passed the hard drive test.\nBeginning Backup..." % self.drivePath)
        else:
            print("Cannot run hard drive test on encrypted drives")

        self.window.destroy()

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

        # Initialize the "global" variables
        self.progressWindow = CheckDiskProgressWindow()
        self.partition = None
        self.drivePath = '/dev/'
        self.encrypted = False
