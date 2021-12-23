import os
import hd_test
import mount_drive
import data_backup
import rsync
import texttable

def clearDisplay():
    os.system('cls' if os.name == 'nt' else 'clear')
    print('=== Welcome to TechStop Backup Utilities ==='.center(os.get_terminal_size().columns))
    print('By Kyle Peront and Samuel Jiang'.center(os.get_terminal_size().columns))
    print('ver 1.0.0'.center(os.get_terminal_size().columns))
    print()
    print()


def selectFunction() -> int:
    clearDisplay()
    print('Please select the functions below by typing in their corresponding numbers:')
    print('(1) Data Backup')
    print('(2) Hard Drive Test')
    print('(3) Mount Drive(s)')
    print()
    print()
    print()

    return int(input('Enter Selection: '))


def selectDrive(customer_name, ticket_id) -> list:
    clearDisplay()
    print('Customer Name:   ' + customer_name)
    print('Ticket Number:   ' + ticket_id)
    print('----')
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
        driveList = selectDrive(customer_name, ticket_id)
        print('Hit r to refresh the list. You can input .. to return to main menu.')
        driveSelection = input('Please enter the drive partition you wish to backup: ')
        if driveSelection == '..':
            return
    driveSelected = driveList[int(driveSelection)]

    clearDisplay()
    mountpoint = ''
    print(driveSelected)
    while mountpoint == '':
        if driveSelected[4] == 'BitLocker':
            bitlockerKey = input('Please enter the BitLocker key: ')
            print('Mounting drive...', end='\r')
            mountpoint = mount_drive.mountPart('/dev/' + driveSelected[3], driveSelected[4], driveSelected[6], bitlockerKey)
        elif driveSelected[4] == 'apfs' and mount_drive.fileVaultOn('/dev/' + driveSelected[3]):
            fileVaultKey = input('Please enter the FileVault recovery key: ')
            print('Mounting drive...', end='\r')
            mountpoint = mount_drive.mountPart('/dev/' + driveSelected[3], driveSelected[4], driveSelected[6], fileVaultKey)
        else:
            print('Mounting drive...', end='\r')
            mountpoint = mount_drive.mountPart('/dev/' + driveSelected[3], driveSelected[4], driveSelected[4])
        
        if mountpoint == '':
            print('Mounting failed. Please Try Again')
            input()
        else:
            print('Drive mounted at ' + mountpoint + ' sucessfully!')
    input('Hit [Enter] to Continue')

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
    print('\nThe utility is ready to start the data backup process. Do you want a verbose output or a simplified output?')
    print('(1) Verbose (With all the details concerning the backup)')
    print('(2) Simplified (A progress bar with single line outputs')
    select = input('\nEnter Selection: ')
    if select == 1:
        data_backup.backupData(customer_name, ticket_id, mountpoint, driveSelected[4], usersSelected)
    else:
        data_backup.backupData(customer_name, ticket_id, mountpoint, driveSelected[4], usersSelected, verbose=False)



def backup_utils():
    if not hd_test.isSudo():
        print('ERROR: This utility requires superuser privileges! Please run the script with sudo.')
        return

    while True:
        selection = selectFunction()
        if selection == 1:
            dataBackup()

if __name__=="__main__":
    backup_utils()