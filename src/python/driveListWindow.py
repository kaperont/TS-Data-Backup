# General Imports
import os
try:
    from utils.mount_drive import listDrive
except:
    from src.python.utils.mount_drive import listDrive

# GTK Imports
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk as gtk
from gi.repository import Gdk as gdk


class DriveListWindow(gtk.Dialog):

    def on_response(self, widget, response_id):
        selected = self.partitionBox.get_selected_row()
        text = selected.get_child().get_text()
        arr = text.split()
        partName = arr[0]
        if partName == "Partition:":
            self.selectedPartition = None
            return

        self.selectedPartition = self.drives[partName[0:-1]]['parts'][partName]

    def get_result(self):
        return self.selectedPartition
    
    def __init__(self, parent):
        gtk.Dialog.__init__(self, "Drive List", parent, 0,
            (gtk.STOCK_CANCEL, gtk.ResponseType.CANCEL,
             gtk.STOCK_OK, gtk.ResponseType.OK))

        # Initialize Window
        self.set_size_request(600, 350)
        self.connect("response", self.on_response)
        self.set_title("Select Partition")
        self.selectedPartition = None

        # Load Stylesheet
        screen = gdk.Screen.get_default()
        provider = gtk.CssProvider()
        style_context = gtk.StyleContext()
        provider.load_from_path(os.path.dirname(os.path.abspath(__file__)) + "/../stylesheets/driveListWindow.css")
        style_context.add_provider_for_screen(screen, provider, gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        # Set the main box
        box = self.get_content_area()

        # Create Header Prompt
        headerLabel = gtk.Label(label="Select a Partition:")
        headerLabel.set_name("header")
        box.add(headerLabel)
        
        # Insert descriptions
        boxHeaderLabel = gtk.Label(label="Partition:   Size:   Filesystem:   Mountpoint:")
        boxHeaderLabel.set_name("boxHeaderLabel")
        boxHeaderLabel.set_alignment(0,0)
        box.add(boxHeaderLabel)

        # Grab the list of drives connected
        self.drives = listDrive()

        # Create a ListBox to insert partitions into
        self.partitionBox = gtk.ListBox()
        self.partitionBox.set_name("listbox")
        box.add(self.partitionBox)

        # Loop through each drive to insert
        for drive in self.drives.keys():
            
            # Insert each partition to the ListBox
            partitions = self.drives[drive]['parts']
            i=0
            for partition in partitions.keys():

                # Gather information from each partition
                j=0
                content = ""
                parts = partitions[partition]
                for part in parts:
                    content += parts[part]

                    if j == 0:
                        content = content.ljust(13)
                    elif j == 1:
                        content = content.ljust(21)
                    elif j == 2:
                        content = content.ljust(35)
                    elif j == 3:
                        content = content.ljust(66)
                
                    j+=1

                
                # Create a label for each partition then insert to the ListBox
                # style = "<span font-family='consolas'>" + content + "</span>"
                partitionLabel = gtk.Label(label=content)
                partitionLabel.set_name("partitionLabel")
                # partitionLabel.set_markup(style)
                partitionLabel.set_alignment(0,0)
                self.partitionBox.insert(partitionLabel, i)
                    
                i+=1

        self.show_all()
