import gi
import os
import re
import subprocess
import time
import pdb

from checkDiskProgressWindow import CheckDiskProgressWindow
from driveListWindow import DriveListWindow
from subprocess import run

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
    
    def openProgressBar(self, src):
        self.progressWindow = CheckDiskProgressWindow()

    def on_SelectPartitionButton_clicked(self, object):
        dialog = DriveListWindow(self.window)
        response = dialog.run()
        
        if response == Gtk.ResponseType.OK:
            result = dialog.get_result()
            print(result)
            srcPartitionEntry = self.builder.get_object("SrcPartitionForm")
            srcPartitionEntry.set_text(result[-1])
            print("The OK button was clicked")
        elif response == Gtk.ResponseType.CANCEL:
            print("The Cancel button was clicked")
        
        dialog.destroy()

    # Start Backup Button has been clicked
    def on_StartBackupButton_clicked(self, object, data=None):

        # Grab the input objects
        customerNameEntry = self.builder.get_object("CustomerNameForm")
        ticketNumberEntry = self.builder.get_object("TicketNumberForm")
        srcDirectoryEntry = self.builder.get_object("SrcPartitionForm")

        # Extract the data from the input objects
        customerName = customerNameEntry.get_text()
        ticketNumber = ticketNumberEntry.get_text()
        srcDirectory = srcDirectoryEntry.get_text()

        # If one of the fields is empty, do nothing and return
        if not customerName or not ticketNumber or not srcDirectory:
            print("Did not recieve any data")
            return
        
        # Otherwise, create a "ticket" and push it to the dict
        ticket = {'customerName': customerName, 'ticketNumber': ticketNumber, 'srcDirectory': srcDirectory}
        self.tickets[ticketNumber] = ticket
        print(self.tickets)

        self.progressWindow.show()

        if self.progressWindow.shortDST(srcDirectory):
            print("%s passed the hard drive test.\nBeginning Backup..." % srcDirectory)

    # NewCustomerWindow init
    def __init__(self, tickets):
        # Set the Gladefile to read from
        self.gladefile = "../glade/backup-utility.glade"

        # Create the GTK Builder from the Gladefile
        self.builder = Gtk.Builder()
        self.builder.add_from_file(self.gladefile)
        self.builder.connect_signals(self)
        # pdb.set_trace()

        # Locate the NewCustomerWindow and display
        self.window = self.builder.get_object("NewCustomerWindow")
        self.window.show()
        
        self.tickets = tickets
        self.progressWindow = CheckDiskProgressWindow()