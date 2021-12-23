from subprocess import Popen, PIPE, STDOUT
import os
import time
import re

def getMS() -> int:
    return int(round(time.time() * 1000))

def rsync_run(excludes:list, src, dest):

    # Check if dirs valid
    if os.path.exists(src):
        splitSrc = src.split('/')
        
        # Create dir if not exist
        if not os.path.exists(dest):
            print('Created Dest')
            os.mkdir(dest)
        
        rsyncCMD = ['rsync', '-rhv', '--progress', '--update', '--safe-links']
        for exclude in excludes:
            rsyncCMD.append('--exclude=' + exclude)
        rsyncCMD.append(src)
        rsyncCMD.append(dest)

        p = Popen(rsyncCMD, stdout=PIPE, stderr=STDOUT, text=True)

        # Log progress
        timeout_base = 0
        timeout_limit = 100000 # 100 seconds
        while True:
            if getMS() - timeout_base >= timeout_limit and timeout_base != 0:
                print('Some process taking too long')

            line =  p.stdout.readline()
            
            # Stop when stream ended
            if not line:
                break
            
            line = line.strip()
            splitLine = line.split()
            
            if line != '':
                # Start Line
                if line == 'sending incremental file list':
                    print('Reading directories')
                    timeout_base = getMS()
                # Get the skip outputs
                elif 'skipping' in line:
                    print(line)
                # 2nd to the last output
                elif 'sent' in line:
                    sentSize = splitLine[1]
                    avgSpeed = splitLine[6] + ' ' + splitLine[7]
                    print('Sent: ' + sentSize + '; Speed: ' + avgSpeed)
                # Last output
                elif 'total size' in line:
                    totalSize = splitLine[3]
                    print('Total Size: ' + totalSize)
                # Getting a new file
                elif splitSrc[-1] in line and 'B/s' not in line:
                    # Reset timer
                    timeout_base = getMS()
                    print('Copying: ' + line)
                # Probably the progress?
                elif 'B/s' in line:
                    copiedSize = splitLine[0]
                    progress = splitLine[1]
                    speed = splitLine[2]
                    timeLeft = splitLine[3]
                    print('Copying: ' + copiedSize + ' Percentage Completed: ' + progress + ' Rate: ' + speed + ' Estimated Time Left: ' + timeLeft, end='\r')
                    if len(splitLine) == 6:
                        numFileTransferred = int(re.search(r'\d+', splitLine[4]).group())
                        transferStat = list(map(int, re.findall(r'\d+', splitLine[5])))
                        print('\nCopied File #' + str(numFileTransferred) + ' There are ' + str(transferStat[0]) + '/' + str(transferStat[1]) + ' left')
    else:
        raise FileNotFoundError('Source Directory Not Found!')
