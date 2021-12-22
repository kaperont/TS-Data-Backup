from subprocess import run
import os
import re
import sys
import time
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

    
# Check if the script is running with su privileges
def isSudo() -> bool:
    return os.geteuid() == 0


# Cancels all running tests
def cancelTask(drive):
    result = run(['smartctl', '-X', drive], capture_output=True)
    lines = result.stdout.decode('utf-8').splitlines()
    if len(lines) == 6:
        status = lines[5]
    else:
        print('Something is wrong')


# Checks the reported S.M.A.R.T. health
def checkDeviceHealth(drive) -> str:
    if isSudo():
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
def shortDST(drive, gui=False) -> bool:
    if isSudo():
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
                return False

            # Don't check too often
            time.sleep(5)
        
        return True
    else:
        print("Must have super user privileges. Try running with sudo?")


# Runs the long test
def longDST(drive):
    if isSudo():
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
                return

            # Don't check too often
            time.sleep(5)
    else:
        print("Must have super user privileges. Try running with sudo?")


if __name__ == '__main__':
    if len(sys.argv) > 1:
        try:
            shortDST(sys.argv[1], True)
        except:
            print("Could not check disk")
# checkDeviceHealth('/dev/sda')
#longDST('/dev/sdc')