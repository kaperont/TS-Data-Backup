from subprocess import run
import os
import hd_test

# Lists all the drives and partitions using lsblk
def listDrive():
    result = run(['lsblk', '-o', 'NAME,TYPE,SIZE,FSTYPE,MOUNTPOINT'], capture_output=True)
    drives = result.stdout.decode('utf-8').splitlines()

    driveDict = {}
    disk = ''
    for drive in drives:
        columns = drive.split()
        # We got a disk
        if columns[1] == 'disk':
            disk = columns[0]
            driveDict[columns[0]] = {}
            driveDict[columns[0]]['name'] = columns[0]
            driveDict[columns[0]]['size'] = columns[2]
            driveDict[disk]['parts'] = {}
        # We got a partition
        elif columns[1] == 'part':
            partName = columns[0][2:]
            driveDict[disk]['parts'][partName] = {}
            driveDict[disk]['parts'][partName]["name"] = partName
            driveDict[disk]['parts'][partName]["size"] = columns[2]
            if len(columns) >= 4:
                driveDict[disk]['parts'][partName]["type"] = columns[3]
            else:
                driveDict[disk]['parts'][partName]["type"] = ''
            if len(columns) == 5:
                driveDict[disk]['parts'][partName]["mountpoint"] = columns[4]
            else:
                driveDict[disk]['parts'][partName]["mountpoint"] = ''
    print(driveDict)
    return driveDict


# Unlocks and mounts a BitLocker encrypted drives
def mountBitLocker(partition, password):
    if hd_test.isSudo():
        # Check and make necessary directories
        bitlockerDir = '/mnt/bitlocker'
        driveMountDir = '/media/bitlockervol'
        # Create dir if does not exist
        if not os.path.isdir(bitlockerDir):
            print(bitlockerDir + ' not found. Creating')
            os.mkdir(bitlockerDir)
        # Make sure nothing has been mounted already
        elif len(os.listdir(bitlockerDir)) != 0:
            print('Something had been mounted to ' + bitlockerDir + '. Cleaning.')
            result = run(['umount', bitlockerDir], capture_output=True)
            output = result.stdout.decode('utf-8').splitlines()
            # Something is wrong with the unmount if there is an output
            if len(output) != 0:
                print(output)
        # Create dir if does not exist
        if not os.path.isdir(driveMountDir):
            print(driveMountDir + ' does not exist. Creating')
            os.mkdir(driveMountDir)
        elif len(os.listdir(driveMountDir)) != 0:
            print('Something had been mounted to ' + driveMountDir + '. Cleaning.')
            result = run(['umount', driveMountDir], capture_output=True)
            output = result.stdout.decode('utf-8').splitlines()
            # Something is wrong with the unmount if there is an output
            if len(output) != 0:
                print(output)
            
        
        # Decrypt drive
        result = run(['dislocker', '-v', '-V', partition, '--recovery-password=' + password, '--', bitlockerDir], capture_output=True)
        output = result.stdout.decode('utf-8').splitlines()
        # Something is wrong if the output is not empty
        if len(output) != 0:
            # Password incorrect error could be handled here
            print(output)
        else:
            # Mount the dislocked file
            result = run(['mount', '-o', 'loop,rw', bitlockerDir + '/dislocker-file', driveMountDir], capture_output=True)
            output = result.stdout.decode('utf-8').splitlines()
            if len(output) != 0:
                # This is most likely an error related to Windows hibernation file
                print(output)
            else:
                print(partition + ' Mounted!')
    else:
        print('This process requires sudo privileges!')


# Unmounts all BitLocker encrypted drives
def unmountBitLocker():
    if hd_test.isSudo():
        print('Unmounting Bitlocker')
        bitlockerDir = '/mnt/bitlocker'
        driveMountDir = '/media/bitlockervol'
        # Unmount the bitlocker volume first. REQUIRED!!!
        result = run(['umount', driveMountDir], capture_output=True)
        output = result.stdout.decode('utf-8').splitlines()
        # Something is wrong with the unmount if there is an output
        if len(output) != 0:
            print(output)
        # Unmount the bitlocker
        result = run(['umount', bitlockerDir], capture_output=True)
        output = result.stdout.decode('utf-8').splitlines()
        # Something is wrong with the unmount if there is an output
        if len(output) != 0:
            print(output)
    else:
        print('This process requires sudo privileges!')


# Mount un-encrypted Windows drive
def mountWindows(partition, mountpoint):
    if hd_test.isSudo():
        driveMountDir = '/media/windows'
        if mountpoint != '':
            print('Drive already mounted automatically!')
        else:
            # Create dir if does not exist
            if not os.path.isdir(driveMountDir):
                print(driveMountDir + ' does not exist. Creating')
                os.mkdir(driveMountDir)
            elif len(os.listdir(driveMountDir)) != 0:
                print('Something had been mounted to ' + driveMountDir + '. Cleaning.')
                result = run(['umount', driveMountDir], capture_output=True)
                output = result.stdout.decode('utf-8').splitlines()
                # Something is wrong with the unmount if there is an output
                if len(output) != 0:
                    print(output)
            
            # Mount windows drive
            result = run(['mount', '-o', 'loop,rw', partition, driveMountDir], capture_output=True)
            output = result.stdout.decode('utf-8').splitlines()
            if len(output) != 0:
                # This is most likely an error related to Windows hibernation file
                print(output)
            else:
                print(partition + ' Mounted!')
    else:
        print('This process requires sudo privileges!')


def unmountWindows(mountpoint):
    if hd_test.isSudo():
        driveMountDir = '/media/windows'
        if mountpoint != '':
            result = run(['umount', mountpoint], capture_output=True)
            output = result.stdout.decode('utf-8').splitlines()
            # Something is wrong with the unmount if there is an output
            if len(output) != 0:
                print(output)
        else:
            # Create dir if does not exist
            if not os.path.isdir(driveMountDir):
                print(driveMountDir + ' does not exist. Creating')
                os.mkdir(driveMountDir)
            elif len(os.listdir(driveMountDir)) != 0:
                result = run(['umount', driveMountDir], capture_output=True)
                output = result.stdout.decode('utf-8').splitlines()
                # Something is wrong with the unmount if there is an output
                if len(output) != 0:
                    print(output)


# Main mounting method for all mountings
def mountPart(partition, driveType, mountpoint = '', password = ''):
    # If the drive is BitLocker locked
    if driveType == 'BitLocker':
        mountBitLocker(partition, password)
    # Most likely an un-encrypted Windows drive
    elif driveType == 'ntfs':
        mountWindows(partition, mountpoint)

