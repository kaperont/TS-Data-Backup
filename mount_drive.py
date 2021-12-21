from subprocess import run
import os
import hd_test

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
            driveDict[disk]['parts'][partName]["type"] = columns[3]
            driveDict[disk]['parts'][partName]["mountpoint"] = columns[4]
    
    print(driveDict)
    return driveDict


def mountBitLocker(partition, password):
    if hd_test.isSudo:
        # Make necessary directories
        os.mkdir('/mnt/bitlocker')
        os.mkdir('/mnt/bitlockervol')
        # Decrypt drive
        result = run(['dislocker', partition, '-u', password, '--', '/mnt/bitlocker'], capture_output=True)
        lines = result.stdout.decode('utf-8').splitlines()



def mountPart(partition, driveType, password = ''):
    # If the drive is BitLocker locked
    if driveType == 'BitLocker':
        mountBitLocker(partition, password)
        
listDrive()
