# Backup script
## Info
This is python script used to backup folders to external hard drive.
It uses [rsync](./rsync.md) command to check if files/folders need to be copied before the
actual copying.

For now only Linux systems are supported (don't know how it is on Windows and [rsync](./rsync.md)
command).

### Intentions
- replace manual copying of important/special files
- make copying more efficient (copy only those files which have changed).

[Here](./rsync.md) you can check from some information about `rsync` command.

Note that before actual copying/backuping a *dry run* command is run which shows what a real command
is going to do.
The default [rsync](./rsync.md) command: `rsync -rltgoDvP --modify-window=1 --delete`.

## Usage
- You must specify which folders/disks to backup. This information is stored in a
  configuration file.
  - Configuration file:
    - [example](./exampleBackupConfig.py)
    - [detailed description](./README.md/#configuration-file)
  - How to pass configuration file to the script:
    - create `backupConfig.py` file in the same directory as [backup.py](./backup.py) script
      this way you don't need to specify configuration file when you launch the script,
      so script can be launched like this: `python backup.py`
    - pass configuration file as an argument when you launch the script:
      - `python backup.py -c myBackupConfig.py`
      - `python backup.py -c myBackupConfig`
- The script first runs a *dry run* which shows what a real command is going to do. This is used
  because that way we can cancel if we see that something would go wrong. So first a *dry run*
  command is run and than you get prompted is a real command should be run.
  ![demo](./Res/demo.gif)
- Run `python backup.py -h` to see all the available options for configuration of this script.

## Configuration file
- [Example](./exampleBackupConfig.py)
### Special "folders" options:
- `exclude`: specify which files/folders/patterns to *not* include in the backup
- `options`: specify special options for `rsync` command
  - `no-delete`: keep files/folders which don't exist on source path but exist on destination path
               (this is useful for folders like Pictures...)

## Suggestions
If you have any suggestions please let me know (you can submit pull request, open a discussion or
open an issue).

## License
See the [LICENSE](./LICENSE.md) file for license rights and limitations (MIT).
