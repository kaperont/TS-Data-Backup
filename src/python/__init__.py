
try:
    from aboutWindow import AboutWindow
    from backup_utility import *
    from mainWindow import MainWindow
    from newCustomerWindow import NewCustomerWindow
    from checkDiskProgressWindow import CheckDiskProgressWindow
except:
    from src.python.aboutWindow import AboutWindow
    from src.python.backup_utility import *
    from src.python.mainWindow import MainWindow
    from src.python.newCustomerWindow import NewCustomerWindow
    from src.python.checkDiskProgressWindow import CheckDiskProgressWindow
