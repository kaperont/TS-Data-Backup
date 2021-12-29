# General Imports
import os
import pdb
import re
import time
import threading
from subprocess import run

# GTK Imports
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk as gtk
from gi.repository import Gdk as gdk
from gi.repository import GLib


def progress_main(drive):
    gladefile = os.path.dirname(os.path.abspath(__file__)) + '/../glade/backup-utility.glade'

    # Create the GTK Builder from the Gladefile
    builder = gtk.Builder()
    builder.add_from_file(gladefile)

    # Grab some objects
    window = builder.get_object("CheckDiskProgressWindow")
    progressbar = builder.get_object("CheckDiskProgressBar")
    terminalContainer = builder.get_object("TerminalWindow")
    terminal = builder.get_object("ProgressTerminal")
    progressContinue = builder.get_object("ProgressContinue")
    progressShowMore = builder.get_object("ProgressShowMore")

    # Load Stylesheet
    screen = gdk.Screen.get_default()
    provider = gtk.CssProvider()
    style_context = gtk.StyleContext()
    provider.load_from_path(os.path.dirname(os.path.abspath(__file__)) + "/../stylesheets/checkDiskProgresWindow.css")
    style_context.add_provider_for_screen(screen, provider, gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    # Handle ProgressContinue button handler
    def on_ProgressContinue_clicked(object):
        print("Closing Progress Bar")
        window.close()

    # Handle ProgressShowMore toggler handler
    def on_ProgressShowMore_toggled(object):
        show_text = object.get_active()
        if show_text:
            terminalContainer.set_visible(True)
            window.resize(400,350)
        else:
            terminalContainer.set_visible(False)
            window.resize(400,200)

    # Update Progress Bar
    def update_progess(msg):
        # Update Progress Bar
        val = progressbar.get_fraction()
        val += 0.10001
        progressbar.set_fraction(val)

        # Update terminal
        label = gtk.Label(label=msg)
        label.set_name("terminalInput")
        label.set_visible(True)
        print('msg:   %s' % msg)
        terminal.pack_start(label, True, True, 5)

        # Enable the continue button
        if val > 0.99:
            progressContinue.set_sensitive(True)

        return False

    # Run's the short HD test
    def shortDST(drive) -> bool:
        if os.geteuid() == 0:
            result = run(['smartctl', '--test=short', drive], capture_output=True)
            lines = result.stdout.decode('utf-8').splitlines()
            # Most likely successful if there are more than 4 lines
            if len(lines) == 10:
                estimateCompleteTime = int(re.search(r'\d+', lines[7]).group())
                estimateCompleteDate = lines[8][24:]
                print('estimate complete: ' + str(estimateCompleteTime) + ' minute(s)')
                print('estimate complete date: ' + estimateCompleteDate)

            remaining = ''
            previous = '100%'
            i=0
            while remaining != '00%':
                result = run(['smartctl', '-l', 'selftest', drive], capture_output=True)
                # The most recent result should be at the very top
                results = result.stdout.decode('utf-8').splitlines()
                for result in results:
                    columns = result.split()
                    if len(columns) == 11 and columns[1] == '1':
                        statusMsg = columns[5:8]
                        statusMsg = ' '.join(statusMsg)
                        remaining = columns[8]
                        msg = statusMsg + ' with percent left: ' + remaining
                        print(msg, end='                                  \r')
                        if remaining != previous:
                            previous = remaining
                            GLib.idle_add(update_progess, msg)
                            i+=1
                        break
                    elif len(columns) == 10 and columns[1] == '1':
                        statusMsg = columns[4:7]
                        statusMsg = ' '.join(statusMsg)
                        remaining = columns[7]
                        msg = statusMsg + ' with percent left: ' + remaining
                        print(msg, end='                                  \r')
                        if remaining != previous:
                            previous = remaining
                            GLib.idle_add(update_progess, msg)
                            i+=1
                        break

                # Don't check too often
                time.sleep(5)
            
            # Get the final result
            result = run(['smartctl', '-l', 'selftest', drive], capture_output=True)
            # The most recent result should be at the very top
            results = result.stdout.decode('utf-8').splitlines()
            columns = results[6].split()
            statusMsg = columns[4] + ' ' + columns[5] + ' ' + columns[6]
            print('\n' + statusMsg)
            
            return True
        else:
            print("Must have super user privileges. Try running with sudo?")

    # Set window title
    window.set_title("Checking Disk...")

    # Connect signals
    progressContinue.connect("clicked", on_ProgressContinue_clicked)
    progressShowMore.connect("toggled", on_ProgressShowMore_toggled)

    # Display the window
    window.show_all()

    # Set terminal invisible
    if progressShowMore.get_active():
        terminalContainer.set_visible(True)
        window.resize(400,350)
    else:
        terminalContainer.set_visible(False)
        window.resize(400,200)

    # Initialize and start a shortDST thread
    thread = threading.Thread(target=shortDST, args=(drive,), daemon=True)
    thread.start()
