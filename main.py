# General Imports
import argparse
import os
import sys

# Main function imports
from src.python.backup_utility import main as main_gui
from src.python.utils.ts_backup_utils_cmd import backup_utils as main_terminal

# If run as main
if __name__ == '__main__':

    # Check for sudo privileges
    if not os.geteuid() == 0:
        print('ERROR: This utility requires superuser privileges! Please run the script with sudo.')
        sys.exit()

    # Create parser
    parser = argparse.ArgumentParser(description='A data backup utility with both gui and command line interfaces')
    parser.add_argument('interface', type=str, nargs='*', help='Distinguish which interface to use [\'gui\' or \'terminal\']')
    args = parser.parse_args()
    
    # Check for correct input
    if not args.interface:
        print("Starting the GUI version...")
        main_gui()
    elif args.interface[0].upper() == 'GUI':
        print("Starting the GUI version...")
        main_gui()
    elif args.interface[0].upper() == 'TERMINAL' or args.interface.upper() == 'COMMAND-LINE':
        print("Starting the command line version...")
        main_terminal()
    else:
        parser.print_help()