# General Imports
try:
    from utils.mount_drive import mountPart, unmountPart
except:
    from src.python.utils.mount_drive import mountPart, unmountPart

# Window Imports
try:
    from checkDiskProgressWindow import progress_main
    from driveListWindow import DriveListWindow
    from keyWindows import APFSKeyDialog, BitLockerKeyDialog
except:
    from src.python.checkDiskProgressWindow import progress_main
    from src.python.driveListWindow import DriveListWindow
    from src.python.keyWindows import APFSKeyDialog, BitLockerKeyDialog

# GTK Imports
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk as gtk


class NewCustomerWindow(object):


    def unlockBitlocker(self, partitionPath):
        bitlockerDialog = BitLockerKeyDialog(self.window)
        bitlockerResponse = bitlockerDialog.run()

        if bitlockerResponse == gtk.ResponseType.OK:
            # If response is OK, grab the result
            self.bitlockerKey = bitlockerDialog.get_result()

            # Check for valid result
            if self.bitlockerKey is None:
                print("No BitLocker Key Provided")
                return None
            
            print("BitLocker Key: %s" % self.bitlockerKey)
        elif bitlockerResponse == gtk.ResponseType.CANCEL:
            print("No BitLocker Key Provided")
            return None

        bitlockerDialog.destroy()
        self.encrypted = True
        return mountPart(partition=partitionPath, driveType="BitLocker", password=self.bitlockerKey)

    def unlockAPFS(self, partitionPath):
        apfsDialog = APFSKeyDialog(self.window)
        apfsResponse = apfsDialog.run()

        if apfsResponse == gtk.ResponseType.OK:
            # If response is OK, grab the result
            self.apfsKey = apfsDialog.get_result()

            # Check for valid result
            if self.apfsKey is None:
                print("No BitLocker Key Provided")
                return None
            
            print("BitLocker Key: %s" % self.apfsKey)
        elif apfsResponse == gtk.ResponseType.CANCEL:
            print("No BitLocker Key Provided")
            return None

        apfsDialog.destroy()
        self.encrypted = True
        return mountPart(partition=partitionPath, driveType="apfs", password=self.apfsKey)

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
                    # Destroy old dialog
                    dialog.destroy()
                    # Unlock bitlocker and retrieve mountpoint
                    mountpoint = self.unlockBitlocker(partitionPath)
                    # Verify bitlocker key was successful and mountpoint was set
                    if not mountpoint:
                        return

                elif type == 'apfs':
                    # Destroy old dialog
                    dialog.destroy()
                    # Unlock APFS and retrieve mountpoint
                    mountpoint = self.unlockAPFS(partitionPath)
                    # Verify APFS key was successful and mountpoint was set
                    if not mountpoint:
                        return

                elif type == 'ntfs':
                    # self.encrypted = True
                    None
                
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
        
        if not self.encrypted:
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
            # Open a progress Window which also performs the hard drive test
            progress_main(self.drivePath)
        else:
            print("Cannot run hard drive test on encrypted drives")

        self.window.destroy()

    # NewCustomerWindow init
    def __init__(self, gladefile):
        # Set the Gladefile to read from
        self.gladefile = gladefile

        # Create the GTK Builder from the Gladefile
        self.builder = gtk.Builder()
        self.builder.add_from_file(self.gladefile)
        self.builder.connect_signals(self)

        # Locate the NewCustomerWindow and display
        self.window = self.builder.get_object("NewCustomerWindow")
        self.window.set_title("New Customer")
        self.window.show()

        # Initialize the "global" variables
        # self.progressWindow = CheckDiskProgressWindow(self.gladefile)
        self.partition = None
        self.drivePath = '/dev/'
        self.encrypted = False
