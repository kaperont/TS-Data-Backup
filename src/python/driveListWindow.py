# General Imports
from utils.mount_drive import listDrive

# GTK Imports
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk as gtk


class DriveListWindow(gtk.Dialog):

    def on_response(self, widget, response_id):
        selected = self.partitionBox.get_selected_row()
        text = selected.get_child().get_text()
        arr = text.split()
        print(arr)
        if arr[0] == "Partition:":
            print('here')
            self.response = gtk.ResponseType.CANCEL
            return

        self.response = gtk.ResponseType.OK
        self.partitionArr = text.split()

    def get_result(self):
        if self.response == gtk.ResponseType.OK:
            return self.partitionArr
        elif self.response == gtk.ResponseType.CANCEL:
            return []
    
    def __init__(self, parent):
        gtk.Dialog.__init__(self, "Drive List", parent, 0,
            (gtk.STOCK_CANCEL, gtk.ResponseType.CANCEL,
             gtk.STOCK_OK, gtk.ResponseType.OK))

        # Initialize Window
        self.set_size_request(600, 350)
        self.connect("response", self.on_response)
        self.set_title("Select Partition")
        self.partitionArr = []

        # Set the main box
        box = self.get_content_area()
        # vbox = gtk.Box(orientation=gtk.Orientation.VERTICAL, spacing=0)
        # self.add(vbox)

        # Grab the list of drives connected
        self.drives = listDrive()

        # Create a ListBox to insert partitions into
        self.partitionBox = gtk.ListBox()
        box.add(self.partitionBox)

        # Insert descriptions
        header = "Partition:   Size:   Filesystem:   Mountpoint:"
        style = "<span font-family='consolas'>" + header + "</span>"
        headerLabel = gtk.Label(label=header)
        headerLabel.set_markup(style)
        headerLabel.set_alignment(0,0)
        self.partitionBox.insert(headerLabel,0)
        # header = "------------------------------------------"
        # style = "<span font-family='consolas'>" + header + "</span>"
        # headerLabel = gtk.Label(label=header)
        # headerLabel.set_markup(style)
        # headerLabel.set_alignment(0,0)
        # self.partitionBox.insert(headerLabel,1)

        self.partitionBox.get_row_at_index(0).selectable = False

        # Loop through each drive to insert
        for drive in self.drives.keys():
            
            # Insert each partition to the ListBox
            partitions = self.drives[drive]['parts']
            i=2
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
                style = "<span font-family='consolas'>" + content + "</span>"
                partitionLabel = gtk.Label(label=content)
                partitionLabel.set_markup(style)
                partitionLabel.set_alignment(0,0)
                self.partitionBox.insert(partitionLabel, i)
                    
                i+=1

        self.show_all()
