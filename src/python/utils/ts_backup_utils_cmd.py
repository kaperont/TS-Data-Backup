import os
import hd_test
import mount_drive
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
    
    clearDisplay()
    print('Customer Name:   ' + customer_name)
    print('Ticket Number:   ' + ticket_id)
    print('----')
    mountedDrives = mount_drive.listDrive()
    table = texttable.Texttable(os.get_terminal_size().columns)
    driveTable = [['#', 'DRIVE', 'DRIVE SIZE', 'PARTITION', 'PARTITION TYPE', 'PARTITION SIZE', 'MOUNTPOINT', 'SUPPORTED?']]
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
                        partitionList.append('Yes')
                    else:
                        partitionList.append('No')
                    driveTable.append(partitionList)
        
    
    table.add_rows(driveTable)
    print(table.draw())
    driveSelection = input('Please enter the drive partition you wish to backup: ')


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