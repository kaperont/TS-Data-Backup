import gi

from mainWindow import MainWindow

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class App:
    def __init__(self):
        self.tickets = {}
        self.main = MainWindow(self.tickets)
    
    def push_ticket(self, ticket, name, drive):
        self.tickets[ticket] = [ticket, name, drive]

if __name__ == "__main__":
    app = App()
    Gtk.main()