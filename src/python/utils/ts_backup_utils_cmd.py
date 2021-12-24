import os
import platform
from subprocess import Popen
import texttable

try:    
    import hd_test
    import mount_drive
    import data_backup
except:
    import src.python.utils.hd_test as hd_test
    import src.python.utils.mount_drive as mount_drive
    import src.python.utils.data_backup as data_backup

def clearDisplay():
    os.system('cls' if os.name == 'nt' else 'clear')
    print('=== Cedarville TechStop Backup Utilities ==='.center(os.get_terminal_size().columns))
    print('By Kyle Peront and Samuel Jiang (Dec 2021)'.center(os.get_terminal_size().columns))
    print('ver 1.0.0'.center(os.get_terminal_size().columns))
    print()
    print()


def selectFunction() -> int:
    clearDisplay()
    print('Please select the functions below by typing in their corresponding numbers:')
    print('(1) Data Backup')
    print('(2) Hard Drive Test (Only works for un-encrypted drives)')
    print('(3) Mount Drive(s)')
    print()
    print()
    print()

    return int(input('Enter Selection: '))


def selectDrive() -> list:
    mountedDrives = mount_drive.listDrive()
    table = texttable.Texttable(os.get_terminal_size().columns)
    driveTable = [['#', 'DRIVE', 'DRIVE SIZE', 'PARTITION', 'PARTITION TYPE', 'PARTITION SIZE', 'MOUNTPOINT']]
    count = 1
    for drive in mountedDrives.values():
        if drive != None:
            parts = drive.get('parts')
            if parts != None:
                for part in parts.values():
                    partitionList = []
                    type = part.get('type')
                    if type == 'ntfs' or type == 'BitLocker' or type == 'apfs':
                        partitionList.append(str(count))
                        count += 1
                    else:
                        partitionList.append('')
                    partitionList.append(drive.get('name'))
                    partitionList.append(drive.get('size'))
                    partitionList.append(part.get('name'))
                    partitionList.append(part.get('type'))
                    partitionList.append(part.get('size'))
                    partitionList.append(part.get('mountpoint'))
                    if type == 'ntfs' or type == 'BitLocker' or type == 'apfs':
                        driveTable.append(partitionList)
        
    
    table.add_rows(driveTable)
    print(table.draw())
    return driveTable


def mountDrive(driveSelected) -> str:
    clearDisplay()
    mountpoint = ''
    while mountpoint == '':
        if driveSelected[4] == 'BitLocker':
            bitlockerKey = input('Please enter the BitLocker key: ')
            print('Mounting drive...', end='\r')
            mountpoint = mount_drive.mountPart('/dev/' + driveSelected[3], driveSelected[4], mountpoint=driveSelected[6], password=bitlockerKey)
        elif driveSelected[4] == 'apfs' and mount_drive.fileVaultOn('/dev/' + driveSelected[3]):
            fileVaultKey = input('Please enter the FileVault recovery key: ')
            print('Mounting drive...', end='\r')
            mountpoint = mount_drive.mountPart('/dev/' + driveSelected[3], driveSelected[4], mountpoint=driveSelected[6], password=fileVaultKey)
        else:
            print('Mounting drive...', end='\r')
            mountpoint = mount_drive.mountPart('/dev/' + driveSelected[3], driveSelected[4], driveSelected[6])
        
        if mountpoint == '':
            print('Mounting failed. Please Try Again')
            input()
        else:
            print('Drive mounted at ' + mountpoint + ' sucessfully!')
    input('Hit [Enter] to Continue')
    return mountpoint


def dataBackup():
    clearDisplay()
    print('Please provide the information requested below. You can input .. to return to main menu.')
    customer_name = str(input('Please enter the customer\'s name: '))
    if customer_name == '..':
        return
    
    clearDisplay()
    print('Customer Name:   ' + customer_name)
    print('----')
    print('Please provide the information requested below. You can input .. to return to main menu.')
    ticket_id = str(input('Please enter the ticket number from TDX: '))
    if ticket_id == '..':
        return
    
    driveSelection = 'r'
    driveList = []
    while driveSelection == 'r':
        clearDisplay()
        print('Customer Name:   ' + customer_name)
        print('Ticket Number:   ' + ticket_id)
        print('----')
        driveList = selectDrive()
        print('Hit r to refresh the list. You can input .. to return to main menu.')
        driveSelection = input('Please enter the drive partition you wish to backup: ')
        if driveSelection == '..':
            return
    driveSelected = driveList[int(driveSelection)]

    mountpoint = mountDrive(driveSelected)

    clearDisplay()
    print('Customer Name:   ' + customer_name)
    print('Ticket Number:   ' + ticket_id)
    print('Selected Drive:  ' + driveSelected[3] + ' (' + driveSelected[5] + ' ' + driveSelected[4] + ')')
    print('----')
    print('Select the users that you would like to backup')
    users = data_backup.scanUsers(driveSelected[4], mountpoint)
    count = 1
    for user in users:
        print('(' + str(count) + ') ' + user)
        count += 1
    print('(' + str(count) + ') All')
    print('\n (To select multiple users, enter the numbers separated with space.)')
    selection = input('Enter Selection(s): ')
    usersSelected = []
    if selection == str(count):
        usersSelected = users
    else:
        selectionNums = selection.split()
        for num in selectionNums:
            usersSelected.append(users[int(num) - 1])
    
    clearDisplay()
    print('You have selected user(s):\n' + str(usersSelected))
    print('\nThe utility is ready to start the data backup process.')
    input('\nHit [Enter] to start')
    backupDir = data_backup.backupData(customer_name, ticket_id, mountpoint, driveSelected[4], usersSelected)

    print('\n\n Backup Completed to ' + backupDir)
    input('Hit [Enter] to return to main menu')


def hardDriveTest():
    driveSelection = 'r'
    driveTable = []
    while driveSelection == 'r':
        clearDisplay()
        print('Please select the drive to be tested: ')
        mountedDrives = mount_drive.listDrive()
        table = texttable.Texttable(os.get_terminal_size().columns)
        driveTable = [['#', 'DRIVE', 'DRIVE SIZE']]
        count = 1
        for drive in mountedDrives.values():
            if drive != None:
                driveList = []
                driveList.append(str(count))
                count += 1
                driveList.append(drive.get('name'))
                driveList.append(drive.get('size'))
                driveTable.append(driveList)
            
        
        table.add_rows(driveTable)
        print(table.draw())
        print('Hit r to refresh the list. You can input .. to return to main menu.')
        driveSelection = input('Please enter the drive: ')
        if driveSelection == '..':
            return
    driveSelected = driveTable[int(driveSelection)]

    clearDisplay()
    print('Select the test you would like to perform')
    print('(1) Check Device Health')
    print('(2) Short DST')
    print('(3) Long DST')
    print('Please provide the information requested below. You can input .. to return to main menu.')
    testSelected = input('Please enter the test: ')
    if testSelected == '1':
        clearDisplay()
        print('Checking Device Health')
        hd_test.checkDeviceHealth('/dev/' + driveSelected[1])
    elif testSelected == '2':
        clearDisplay()
        print('Performing Short DST')
        hd_test.shortDST('/dev/' + driveSelected[1])
    elif testSelected == '3':
        clearDisplay()
        print('Performing Long DST')
        hd_test.longDST('/dev/' + driveSelected[1])

    input()

def open_file(path):
    if platform.system() == "Windows":
        os.startfile(path)
    elif platform.system() == "Darwin":
        Popen(["open", path])
    else:
        Popen(["xdg-open", path])


def mountDrives():
    driveSelection = 'r'
    driveList = []
    while driveSelection == 'r':
        clearDisplay()
        print('Please select the drive that you would like to mount:')
        driveList = selectDrive()
        print('Hit r to refresh the list. You can input .. to return to main menu.')
        driveSelection = input('Please enter the drive partition you wish to mount: ')
        if driveSelection == '..':
            return
    driveSelected = driveList[int(driveSelection)]
    
    mountpoint = mountDrive(driveSelected)

    clearDisplay()
    open_file(mountpoint)
    text = ''
    while text != 'unmount':
        text = input('Enter "unmount" to unmount ' + driveSelected[3] + ' (' + driveSelected[5] + ' ' + driveSelected[4] + '): ')
    
    mount_drive.unmountPart(driveSelected[4], mountpoint)


def backup_utils():
    if not hd_test.isSudo():
        print('ERROR: This utility requires superuser privileges! Please run the script with sudo.')
        return

    while True:
        selection = selectFunction()
        if selection == 1:
            dataBackup()
        elif selection == 2:
            hardDriveTest()
        elif selection == 3:
            mountDrives()

if __name__=="__main__":
    backup_utils()