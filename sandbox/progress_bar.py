import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib


class ProgressBarWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="ProgressBar")
        self.set_border_width(10)
        self.set_size_request(440, 175)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        self.label = Gtk.Label(label="Checking Disk...")
        vbox.pack_start(self.label, True, True, 6)

        self.progressbar = Gtk.ProgressBar()
        vbox.pack_start(self.progressbar, True, True, 0)

        button = Gtk.CheckButton(label="Show text")
        button.connect("toggled", self.on_show_text_toggled)
        vbox.pack_start(button, True, True, 0)

        # self.timeout_id = GLib.timeout_add(500, self.on_timeout, None)

    def on_show_text_toggled(self, button):
        show_text = button.get_active()
        if show_text:
            text = "some text"
        else:
            text = None
        self.progressbar.set_text(text)
        self.progressbar.set_show_text(show_text)

        self.pulse()
    
    def pulse(self):
        new_value = self.progressbar.get_fraction() + 0.10

        if new_value == 1.00:
            return False

        self.progressbar.set_fraction(new_value)


# win = ProgressBarWindow()
# win.connect("destroy", Gtk.main_quit)
# win.show_all()
# Gtk.main()