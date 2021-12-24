# General Imports
import os
import re
import time
from subprocess import run

# GTK Imports
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class CheckDiskProgressWindow(object):

    # Destruction of Window
    def onDestroy(self, object, data=None):
        self.window.destroy()

    def destroy(self):
        self.window.destroy()

    def show(self):
        self.window.show()

    def increment(self):
        val = self.progressbar.get_fraction()
        val += 0.10
        self.progressbar.set_fraction(val)


    def on_ProgressContinue_clicked(self, object):
        print("Closing Progress Bar")
        self.window.close()
        # self.shortDST('/dev/sdb')

    def on_ProgressShowMore_toggled(self, object):
        show_text = object.get_active()
        print(show_text)
        if show_text:
            self.terminal.set_visible(True)
        else:
            self.terminal.set_visible(False)


    # Check if the script is running with su privileges
    def isSudo(self) -> bool:
        return os.geteuid() == 0


    # Cancels all running tests
    def cancelTask(self, drive):
        result = run(['smartctl', '-X', drive], capture_output=True)
        lines = result.stdout.decode('utf-8').splitlines()
        if len(lines) == 6:
            status = lines[5]
        else:
            print('Something is wrong')


    # Checks the reported S.M.A.R.T. health
    def checkDeviceHealth(self, drive) -> str:
        if self.isSudo():
            result = run(['smartctl', '-H', drive], capture_output=True)
            lines = result.stdout.decode('utf-8').splitlines()

            # There is a SMART Status not supported if there are 8 lines
            if len(lines) == 8:
                overallHealth = lines[5].split(':')
                status = overallHealth[1].strip()
                print(status + ' using an Attribute check.\n' + lines[4])
            # Proper output would be 6 lines
            elif len(lines) == 6:
                overallHealth = lines[4].split(':')
                status = overallHealth[1].strip()
                print(status)
            else:
                print('Something is wrong...')


    # Run's the short HD test
    def shortDST(self, drive) -> bool:
        if os.geteuid() == 0:

            result = run(['smartctl', '--test=short', drive], capture_output=True)
            lines = result.stdout.decode('utf-8').splitlines()
            # print(lines)
            # print(len(lines))
            # Most likely successful if there are more than 4 lines
            if len(lines) == 10:
                estimateCompleteTime = int(re.search(r'\d+', lines[7]).group())
                estimateCompleteDate = lines[8][24:]
                print('estimate complete: ' + str(estimateCompleteTime) + ' minute(s)')
                print('estimate complete date: ' + estimateCompleteDate)

            remaining = ''
            while remaining != '00%':
                result = run(['smartctl', '-l', 'selftest', drive], capture_output=True)
                # The most recent result should be at the very top
                results = result.stdout.decode('utf-8').splitlines()
                columns = results[6].split()
                # 11 columns means still in progress
                if len(columns) == 11:
                    statusMsg = columns[5] + ' ' + columns[6] + ' ' + columns[7]
                    remaining = columns[8]
                    lifeInDriveRemain = columns[9]
                    # LBA means Logic Block Address
                    LBAFirstError = columns[10]
                    print(statusMsg + ' with percent left: ' + remaining)
                    self.increment()
                    
                # 10 means complete
                elif len(columns) == 10:
                    statusMsg = columns[4] + ' ' + columns[5] + ' ' + columns[6]
                    remaining = columns[7]
                    lifeInDriveRemain = columns[8]
                    # LBA means Logic Block Address
                    LBAFirstError = columns[9]
                    print(statusMsg + ' with percent left: ' + remaining)
                    self.increment()
                    break
                else:
                    print('Something is wrong')
                    return False

                # Don't check too often
                time.sleep(5)
                
            self.window.close()
            return True
        else:
            print("Must have super user privileges. Try running with sudo?")


    # Runs the long test
    def longDST(self, drive):
        if self.isSudo():
            result = run(['smartctl', '--test=long', drive], capture_output=True)
            lines = result.stdout.decode('utf-8').splitlines()
            print(lines)
            print(len(lines))
            # Most likely successful if there are more than 4 lines
            if len(lines) == 10:
                estimateCompleteTime = int(re.search(r'\d+', lines[7]).group())
                print('estimate complete: ' + str(estimateCompleteTime) + ' minute(s)')
                estimateCompleteDate = lines[8][24:]
                print('estimate complete date: ' + estimateCompleteDate)
            
            remaining = ''
            while remaining != '00%':
                result = run(['smartctl', '-l', 'selftest', drive], capture_output=True)
                # The most recent result should be at the very top
                results = result.stdout.decode('utf-8').splitlines()
                columns = results[6].split()
                # 11 columns means still in progress
                if len(columns) == 11:
                    statusMsg = columns[5] + ' ' + columns[6] + ' ' + columns[7]
                    remaining = columns[8]
                    lifeInDriveRemain = columns[9]
                    # LBA means Logic Block Address
                    LBAFirstError = columns[10]
                    print(statusMsg + ' with percent left: ' + remaining)
                # 10 means complete
                elif len(columns) == 10:
                    statusMsg = columns[4] + ' ' + columns[5] + ' ' + columns[6]
                    remaining = columns[7]
                    lifeInDriveRemain = columns[8]
                    # LBA means Logic Block Address
                    LBAFirstError = columns[9]
                    print(statusMsg + ' with percent left: ' + remaining)
                    break
                else:
                    print('Something is wrong')

                # Don't check too often
                time.sleep(5)
        else:
            print("Must have super user privileges. Try running with sudo?")


    # CheckDiskProgressWindow init
    def __init__(self, gladefile):
        # Set the Gladefile to read from
        self.gladefile = gladefile

        # Create the GTK Builder from the Gladefile
        self.builder = Gtk.Builder()
        self.builder.add_from_file(self.gladefile)
        self.builder.connect_signals(self)

        # Locate the AboutWindow and display
        self.window = self.builder.get_object("CheckDiskProgressWindow")
        self.progressbar = self.builder.get_object("CheckDiskProgressBar")
        self.terminal = self.builder.get_object("ProgressTerminal")
