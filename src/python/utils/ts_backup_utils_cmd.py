import os
import hd_test

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

    selection = input('Enter Selection: ')


def dataBackup():
    clearDisplay()
    customer_name = input('Please enter the customer\'s name:')


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