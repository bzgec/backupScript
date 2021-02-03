# Backup script
## Info
This is python script used to backup folders to external hard drive.
It uses [rsync](./rsync.md) command to check if files/folders need to be copied before the actual copying.
For now only Linux systems are supported (don't know how it is on Windows and [rsync](./rsync.md) command).

This script is intended to replace manual copying of important/special files and make copying more
efficient (copy only those files which have changed).

[Here](./rsync.md) you can check from some information about `rsync` command.

Script must be run with python 3 because of the `input()` function usage.

## Usage
You must specify which folders/disks to backup. This can be done in two ways:
- create `backupConfig.py` file in the same directory as [backup.py](.backup.py) script
  this way you don't need to specify configuration file when you launch the script,
  so script can be launched like this: `python backup.py`
- pass configuration file as an argument when you launch the script:
  - `python backup.py -c myBackupConfig.py`
  - `python backup.py -c myBackupConfig`
- [This](./exampleBackupConfig.py) example shows how this configuration file should look.
- Run `python backup.py -h` to see all the available options for configuration of this script.

## Suggestions
If you have any suggestions please let me know (you can submit pull request, open a discussion or
open an issue).

## License
See the [LICENSE](./LICENSE.md) file for license rights and limitations (MIT).
