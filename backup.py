#!/usr/bin/python

import os
import sys
import getopt


def displayHelp():
    print("""\
Script to make backup from Linux to external disk (NTFS).

Note that rsync command can also delete files!!!
You must set "no-delete" option in configuration file if you don't want to
delete files on backup disk/folder.

Tested with python 3.8.5.

python backup.py [OPTION]

Options:
  -h, --help        show this help

  -a, --all         backup all specified folders (don't ask which folders to backup)

  -c, --config      specify file which stores information about which folders to backup
                    if this is not specified the script looks for backupConfig.py
                    example: python backup.py -c myBackupConfig.py
                             python backup.py -c myBackupConfig

  -n, --no-confirm  No need to confirm rsync command execution
                    CAUTION: This option causes that all rsync command are executed
                             without any user interaction. Note that rsync command
                             can delete files (set "no-delete" option in config file
                             if you don't want to delete files on backup disk/folder)
""")


class BackupClass:
    # Not using `-a` option because we are backuping to NTFS and we are not using `-p` option

    def __init__(self, backupConfig=0):
        self.backupAllFolders = False  # backup all folders command line option argument flag (-a, --all)
        self.noConfirmRsync = False  # No need to confirm before executing rsync command (-n, --no-confirm)
        self.backupConfig = backupConfig

        if backupConfig != 0:
            # Set `shouldBackup` flags for each folder, default value is 0 meaning to not backup
            self.setBackupAllFolders(0)

    def setConfig(self, backupConfig):
        self.backupConfig = backupConfig

        # Set `shouldBackup` flags for each folder, default value is 0 meaning to not backup
        self.setBackupAllFolders(0)

    def setBackupAllFolders(self, shouldBackupOption):
        for diskToBackup in self.backupConfig:
            for element in diskToBackup["toBackup"]:
                for folder in element["folders"]:
                    folder["shouldBackup"] = shouldBackupOption

    def selectFoldersToBackup(self):
        print("Which folders to backup? (y/n)")

        for diskToBackup in self.backupConfig:
            print('"' + diskToBackup["mainPath"] + '"' ' -> ' + '"' + diskToBackup["destinationPath"] + '"')
            for element in diskToBackup["toBackup"]:
                for folder in element["folders"]:
                    try:
                        srcFolder = element["commonPath"] + folder["path"]
                    except KeyError:
                        srcFolder = folder["path"]
                    if "y" == input('  "' + srcFolder + '": ').lower():
                        folder["shouldBackup"] = 1
                    else:
                        folder["shouldBackup"] = 0

    # Check if rsync command is saying that there are no differences
    def checkDiff(self, rsyncOutStr):
        thereIsDiff = 0
        splittedStr = rsyncOutStr.split('\n')

        # There are exactly 4 '\n' characters in output if there are no changes
        # otherwise there are more '\n' characters
        if len(splittedStr) != 5:

            thereIsDiff = 1

        return thereIsDiff

    # Start the backup for all the disks/files
    def startBackup(self):
        for diskToBackup in self.backupConfig:
            self.backup(diskToBackup["destinationPath"], diskToBackup["mainPath"], diskToBackup["toBackup"])

    # Setup additional parameters
    def setupAdditionalParam(self, rsyncCmd, folder):
        try:
            for additionalParam in folder["options"]:
                if additionalParam == "no-delete":
                    # Remove "--delete" option
                    rsyncCmd = rsyncCmd.replace(" --delete", "")
        except KeyError:
            # No "options" specified
            print("No options specified")
            pass

        return rsyncCmd

    # Setup exclude options
    def setupExcludeOptions(self, folder):
        excludeStr = ""

        # Check if exclude options are specified
        try:
            for excludeOption in folder["exclude"]:
                # Note that we are not using --execlude={} because {} is actually
                # a Bash Brace expansion - https://wiki.bash-hackers.org/syntax/expansion/brace
                # Sooo /bin/sh doesn't support this - https://stackoverflow.com/a/22660171/14246508
                excludeStr += "--exclude=" + excludeOption + " "
        except KeyError:
            # No "exclude" specified
            print("No exclude specified")
            pass

        return excludeStr

    # Backup specified folder
    def backup(self, destFolder, srcFolder, toBackup):
        for element in toBackup:

            # self.setupSrcDestPath(srcFolder, destFolder, )
            # Check if current element has common path specified
            try:
                srcPath = srcFolder + element["commonPath"]
                destPath = destFolder + element["commonPath"]
            except KeyError:
                srcPath = srcFolder
                destPath = destFolder

            os.popen("mkdir -p " + destPath)

            for folder in element["folders"]:
                if folder["shouldBackup"] == 1:
                    print(SEPARATOR)
                    dryRunParam = "-n"
                    realRunParam = "-P"
                    rsyncCmd = "rsync -rltgoDv --modify-window=1 --delete"

                    # Check for additional parameters
                    rsyncCmd = self.setupAdditionalParam(rsyncCmd, folder)

                    # Check if exclude options are specified
                    excludeStr = self.setupExcludeOptions(folder)

                    cmd = rsyncCmd + " " + dryRunParam + " " + \
                        excludeStr + \
                        '"' + srcPath + folder["path"] + '/" ' + \
                        '"' + destPath + folder["path"] + '/"'
                    print('\033[1mDRY run command: ' + cmd + '\033[0m')
                    # returnedStr = os.system(cmd)
                    returnedStr = os.popen(cmd).read()
                    if self.checkDiff(returnedStr) == 1:
                        print(returnedStr)

                        cmd = rsyncCmd + " " + realRunParam + " " + \
                            excludeStr + \
                            '"' + srcPath + folder["path"] + '/" ' + \
                            '"' + destPath + folder["path"] + '/"'

                        if self.noConfirmRsync is True:
                            os.system(cmd)
                        else:
                            confirm = input('\033[1mRun command: ' + cmd + '? (y/n): \033[0m').lower()
                            if confirm == "y":
                                os.system(cmd)
                    else:
                        print("No difference.")


# Bind raw_input() to input() in Python 2
try:
    input = raw_input
except NameError:
    pass

SEPARATOR = "#################################################################################"


# https://www.tutorialspoint.com/python/python_command_line_arguments.htm
def checkArgs(backup, argv):
    try:
        opts, args = getopt.getopt(argv, "hac:n", ["help", "all", "config=", "no-confirm"])
    except getopt.GetoptError:
        displayHelp()
        sys.exit(1)

    for opt, arg in opts:
        if opt in ('-h', "--help"):
            displayHelp()
            sys.exit(0)
        elif opt in ("-c", "--config"):
            # import configuration file
            arg = arg.replace(".py", "")
            from importlib import import_module
            backupConfig = import_module(arg)
            backup.setConfig(backupConfig.backupConfig)
        elif opt in ("-a", "--all"):
            backup.backupAllFolders = True
        elif opt in ("-n", "--no-confirm"):
            backup.noConfirmRsync = True


def main(backup):
    # If destination path and backupConfig are not yet set they are set now from backupConfig.py
    # file
    if backup.backupConfig == 0:
        import backupConfig
        backup.setConfig(backupConfig.backupConfig)

    # Get which folders should be updated now
    print(SEPARATOR)
    if backup.backupAllFolders is False:
        backup.selectFoldersToBackup()
    else:
        print("Backing up all specified folders")
        backup.setBackupAllFolders(1)

    # Start backup, but first perform trial run
    backup.startBackup()


if __name__ == "__main__":
    backup = BackupClass()
    checkArgs(backup, sys.argv[1:])
    main(backup)
