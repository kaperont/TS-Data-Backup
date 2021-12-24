# General Imports
import os

# GTK Imports
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk as gtk
from gi.repository import Gdk as gdk


class BitLockerKeyDialog(gtk.Dialog):

    def on_response(self, widget, response_id):
        self.bitlockerKey = self.keyEntry.get_text()
        
        if not self.bitlockerKey:
            self.bitlockerKey = None
            self.keyEntry.grab_focus_without_selecting()
            # return

    def get_result(self):
        return self.bitlockerKey
    
    def __init__(self, parent):
        gtk.Dialog.__init__(self, "BitLocker Key", parent, 0,
            (gtk.STOCK_CANCEL, gtk.ResponseType.CANCEL,
             gtk.STOCK_OK, gtk.ResponseType.OK))

        # Initialize Window
        self.set_size_request(600, 200)
        self.connect("response", self.on_response)
        self.set_title("Insert BitLocker Key")
        self.bitlockerKey = None

        # Load Stylesheet
        screen = gdk.Screen.get_default()
        provider = gtk.CssProvider()
        style_context = gtk.StyleContext()
        provider.load_from_path(os.path.dirname(os.path.abspath(__file__)) + "/../stylesheets/keyWindows.css")
        style_context.add_provider_for_screen(screen, provider, gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        # Set the main box
        box = self.get_content_area()

        # Create Header Prompt
        headerLabel = gtk.Label(label="Enter the BitLocker Key:")
        headerLabel.set_name("label")
        box.add(headerLabel)

        # Create an Entry to insert the BitLocker key
        self.keyEntry = gtk.Entry()
        self.keyEntry.set_name("entry")
        box.add(self.keyEntry)

        self.show_all()


class APFSKeyDialog(gtk.Dialog):

    def on_response(self, widget, response_id):
        self.apfsKey = self.keyEntry.get_text()
        
        if not self.apfsKey:
            self.apfsKey = None
            return

    def get_result(self):
        return self.apfsKey
    
    def __init__(self, parent):
        gtk.Dialog.__init__(self, "APFS Key", parent, 0,
            (gtk.STOCK_CANCEL, gtk.ResponseType.CANCEL,
             gtk.STOCK_OK, gtk.ResponseType.OK))

        # Initialize Window
        self.set_size_request(600, 200)
        self.connect("response", self.on_response)
        self.set_title("Insert APFS Key")
        self.apfsKey = None

        # Load Stylesheet
        screen = gdk.Screen.get_default()
        provider = gtk.CssProvider()
        style_context = gtk.StyleContext()
        provider.load_from_path(os.path.dirname(os.path.abspath(__file__)) + "../stylesheets/keyWindows.css")
        style_context.add_provider_for_screen(screen, provider, gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        # Set the main box
        box = self.get_content_area()

        # Create Header Prompt
        headerLabel = gtk.Label(label="Enter the APFS Key:")
        headerLabel.set_name("label")
        box.add(headerLabel)

        # Create an Entry to insert the BitLocker key
        self.keyEntry = gtk.Entry()
        self.keyEntry.set_name("entry")
        self.keyEntry.set_placeholder_text("Press OK for no password")
        box.add(self.keyEntry)

        self.show_all()
