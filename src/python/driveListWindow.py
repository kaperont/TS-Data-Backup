import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk as gtk
from utils.mount_drive import listDrive

class DriveListWindow(gtk.Dialog):

    def on_response(self, widget, response_id):
        selected = self.partitionBox.get_selected_row()
        text = selected.get_child().get_text()
        print(text)
        self.partitionArr = text.split()

    def get_result(self):
        return self.partitionArr
    
    def __init__(self, parent):
        gtk.Dialog.__init__(self, "Drive List", parent, 0,
            (gtk.STOCK_CANCEL, gtk.ResponseType.CANCEL,
             gtk.STOCK_OK, gtk.ResponseType.OK))
        # Initialize Window
        # super().__init__(title="Drive List")
        self.set_size_request(600, 350)
        self.connect("response", self.on_response)
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

        # Loop through each drive to insert
        for drive in self.drives.keys():
            
            # Insert each partition to the ListBox
            partitions = self.drives[drive]['parts']
            i=0
            for partition in partitions.keys():

                # Gather information from each partition
                content = ""
                parts = partitions[partition]
                for part in parts:
                    content += parts[part]
                    content += "   "
                
                # Create a label for each partition then insert to the ListBox
                style = "<span font-family='consolas'>" + content + "</span>"
                partitionLabel = gtk.Label(label=content)
                partitionLabel.set_markup(style)
                partitionLabel.set_alignment(0,0)
                self.partitionBox.insert(partitionLabel, i)
                    
                i+=1

        # Crerate a button for submitting which partition to use
        # self.submitButton = gtk.Button("Submit")
        # self.submitButton.set_margin_left(150)
        # self.submitButton.set_margin_right(150)
        # self.submitButton.set_margin_bottom(100)
        # self.submitButton.connect("clicked", self.on_SubmitButton_clicked)
        # box.add(self.submitButton)

        self.show_all()


# win = DriveListWindow()
# win.connect("destroy", gtk.main_quit)
# win.show_all()
# gtk.main()