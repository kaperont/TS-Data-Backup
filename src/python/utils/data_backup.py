from subprocess import run
import mount_drive
import hd_test

def backupData(customer_name, ticket_number, partition):
    # TODO: Make those reconfigurable via GUI
    BACKUP_SERVER_PART_1 = 'sda3'
    BACKUP_SERVER_PART_2 = 'sdb2'
    BACKUP_SERVER_MOUNT_1 = '/'
    BACKUP_SERVER_MOUNT_2 = '/home/techstop/NET_TRANSFER/BACKUP2'

    drivesMounted = mount_drive.listDrive()
    drive = drivesMounted.get(BACKUP_SERVER_PART_1[:3])
    # If the drive exists
    if drive != None:
        parts = drive.get('parts')
        # If there are partitions
        if parts != None:
            part = parts.get(BACKUP_SERVER_PART_1)
            # If the partition is found
            if part != None:
                if part.get('mountpoint') == BACKUP_SERVER_MOUNT_1:
                    print('Backup server 1 mounted!')
                else:
                    if hd_test.isSudo():
                        run(['mount', '/dev/' + BACKUP_SERVER_PART_1, BACKUP_SERVER_MOUNT_1])
                    else:
                        print('Mounting requires sudo privileges!')
    else:
        print('Backup server 1 not found!')

backupData('abc',12345, 'dev/sdb2')