import os

class HardDriveTests:
    drive = None
    
    # Check if the script is running with su privileges
    def isSudo() -> bool:
        return os.geteuid() == 0

    def shortDST(self):
        if self.isSudo():
            



    def __init__(self, drive):
        self.drive = Device(drive)
