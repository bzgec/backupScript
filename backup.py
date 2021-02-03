#!/usr/bin/python

def displayHelp():
    print("Script to make backup from Linux to external disk (NTFS).")
    print("Note that we are also deleting files from backup disk!!! This is because we don't want")
    print("to keep every movie on our PC.")
    print("This program must be run with python 3, tested with python 3.8.5.")
    print("")
    print("python backup.py [OPTION]")
    print("")
    print("Options:")
    print(" -h, --help    show this help")
    print(" -a, --all     backup all specified folders (don't ask which folders to backup)")
    print(" -c, --config  specify file which stores information about which folders to backup")
    print("               if this is not specified the script looks for backupConfig.py")
    print("               example: python -c myBackupConfig.py")
    print("                        python -c myBackupConfig")

class BackupClass:
    # Not using `-a` option because we are backuping to NTFS and we are not using `-p` option
    RSYNC_CMD_DRY_RUN="rsync -rltgoDvn --modify-window=1 --delete"
    RSYNC_CMD="rsync -rltgoDvP --modify-window=1 --delete"

    def __init__(self, destinationPath=0, disksToBackup=0):
        self.backupAllFolders = False  # backup all folders command line option argument flag (-a, --all)
        self.destinationPath = destinationPath
        self.disksToBackup = disksToBackup

        if disksToBackup != 0:
            # Set `shouldBackup` flags for each folder, default value is 0 meaning to not backup
            for diskToBackup in self.disksToBackup:
                for folder in diskToBackup["folders"]:
                    folder["shouldBackup"] = 0

    def setConfig(self, destinationPath, disksToBackup):
        self.destinationPath = destinationPath
        self.disksToBackup = disksToBackup

        # Set `shouldBackup` flags for each folder, default value is 0 meaning to not backup
        for diskToBackup in self.disksToBackup:
            for folder in diskToBackup["folders"]:
                folder["shouldBackup"] = 0

    def setBackupAllFolders(self):
        for diskToBackup in self.disksToBackup:
            for folder in diskToBackup["folders"]:
                folder["shouldBackup"] = 1
    def selectFoldersToBackup(self):
        print("Which folders to backup? (y/n)")

        for diskToBackup in self.disksToBackup:
            print('"' + diskToBackup["diskPath"] + '"' ' -> ' + '"' + self.destinationPath + '"')
            for folder in diskToBackup["folders"]:
                if "y" == input('  "' + folder["path"] + '": ').lower():
                    folder["shouldBackup"] = 1
                else:
                    folder["shouldBackup"] = 0


    # Check if rsync command is saying that there are no differences
    def checkDiff(self, rsyncOutStr):
        thereIsDiff = 0
        splittedStr = rsyncOutStr.split('\n')
        if len(splittedStr) != 5:  # There are exacly 4 '\n' characters in output is there are no changes
                                   # otherwise there are more '\n'characters
            thereIsDiff = 1

        return thereIsDiff

    # Start the backup for all the disks/files
    def startBackup(self):
        for diskToBackup in self.disksToBackup:
            self.backup(backup.destinationPath, diskToBackup["diskPath"], diskToBackup["folders"])

    # Backup specified folder
    def backup(self, destFolder, srcFolder, foldersToBackup):
        for folder in foldersToBackup:
            if folder["shouldBackup"] == 1:
                print(SEPARATOR)

                excludeStr = ""
                for excludeFile in folder["exclude"]:
                    # Note that we are not using --execlude={} because {} is actually
                    # a Bash Brace expansion - https://wiki.bash-hackers.org/syntax/expansion/brace
                    # Sooo /bin/sh doesn't support this - https://stackoverflow.com/a/22660171/14246508
                    excludeStr += "--exclude=" + excludeFile + " "

                cmd = self.RSYNC_CMD_DRY_RUN + ' ' + \
                      excludeStr + \
                      '"' + srcFolder + folder["path"] + '/" ' + \
                      '"' + destFolder + folder["path"] + '/"'
                print('\033[1mDRY run command: ' + cmd + '\033[0m')
                # returnedStr = os.system(cmd)
                returnedStr = os.popen(cmd).read()
                if self.checkDiff(returnedStr) == 1:
                    print(returnedStr)

                    cmd = self.RSYNC_CMD + ' ' + \
                          excludeStr + \
                          '"' + srcFolder + folder["path"] + '/" ' + \
                          '"' + destFolder + folder["path"] + '/"'
                    confirm = input('\033[1mRun command: ' + cmd + '? (y/n): \033[0m').lower()
                    if confirm == "y":
                        os.system(cmd)
                else:
                    print("No difference.")


import os
import sys
import getopt
import subprocess

SEPARATOR="#################################################################################"

# https://www.tutorialspoint.com/python/python_command_line_arguments.htm
def checkArgs(backup, argv):
    try:
        opts, args = getopt.getopt(argv, "hac:", ["help", "all", "config="])
    except getopt.GetoptError:
        displayHelp()
        sys.exit(1)

    for opt, arg in opts:
        if opt in ('-h', "--help"):
            displayHelp()
            sys.exit(0)
        elif opt in ("-c", "--config"):
            # import configuration file
            print(arg)
            arg = arg.replace(".py", "")
            from importlib import import_module
            backupConfig = import_module(arg)
            backup.setConfig(backupConfig.destinationPath, backupConfig.disksToBackup)
        elif opt in ("-a", "--all"):
            backup.backupAllFolders = True

def main(backup):
    # If destination path and disksToBackup are not yet set they are set now from backupConfig.py
    # file
    if backup.destinationPath == 0:
        import backupConfig
        backup.setConfig(backupConfig.destinationPath, backupConfig.disksToBackup)

    # Get which folders should be updated now
    print(SEPARATOR)
    if backup.backupAllFolders is False:
        backup.selectFoldersToBackup()
    else:
        print("Backing up all specified folders")
        backup.setBackupAllFolders()

    # Start backup, but first perform trial run
    backup.startBackup()

if __name__ == "__main__":
    backup = BackupClass()
    checkArgs(backup, sys.argv[1:])
    main(backup)
