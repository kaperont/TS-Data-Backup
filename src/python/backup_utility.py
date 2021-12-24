import os

# Window Imports
try:
    from mainWindow import MainWindow
except:
    from src.python.mainWindow import MainWindow

# GTK Imports
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class App:

    def __init__(self, filepath):
        self.gladefile = filepath
        self.tickets = {}
        self.main = MainWindow(self.gladefile)
    
    def push_ticket(self, ticket, name, drive):
        self.tickets[ticket] = [ticket, name, drive]

def main():
    filepath = os.path.dirname(os.path.abspath(__file__)) + '/../glade/backup-utility.glade'

    app = App(filepath)
    Gtk.main()

if __name__ == "__main__":
    main()