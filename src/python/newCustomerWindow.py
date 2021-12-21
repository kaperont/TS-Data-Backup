import gi
import os
import subprocess

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from utils.hd_test import shortDST, longDST
from os import path

def check_output(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    output = process.communicate()
    retcode = process.poll()
    if retcode:
            raise subprocess.CalledProcessError(retcode, command, output=output[0])
    return output 

class NewCustomerWindow(object):
    # Destruction of Window
    def onDestroy(self, object, data=None):
        self.window.destroy()

    # Start Backup Button has been clicked
    def on_StartBackupButton_clicked(self, object, data=None):

        # Grab the input objects
        customerNameEntry = self.builder.get_object("CustomerNameForm")
        ticketNumberEntry = self.builder.get_object("TicketNumberForm")
        srcDirectoryEntry = self.builder.get_object("SrcDirectoryForm")

        # Extract the data from the input objects
        customerName = customerNameEntry.get_text()
        ticketNumber = ticketNumberEntry.get_text()
        srcDirectory = srcDirectoryEntry.get_filename()

        # If one of the fields is empty, do nothing and return
        if not customerName or not ticketNumber or not srcDirectory:
            print("Did not recieve any data")
            return
        
        # Otherwise, create a "ticket" and push it to the dict
        ticket = {'customerName': customerName, 'ticketNumber': ticketNumber, 'srcDirectory': srcDirectory}
        self.tickets[ticketNumber] = ticket
        print(self.tickets)

        # try:
        #     command = 'sudo python3 utils/hd_test.py ' + srcDirectory
        #     subprocess.check_output(command, shell=True)
        # except subprocess.CalledProcessError as e:
        #     print ('e.output: ', e.output)
        
        if shortDST(srcDirectory):
            print("%s passed the hard drive test.\nBeginning Backup..." % srcDirectory)

    # NewCustomerWindow init
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