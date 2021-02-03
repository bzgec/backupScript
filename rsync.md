# rsync
- utility for efficiently transferring and synchronizing files between a computer and an external
  hard drive and across networked computers by comparing the modification times and sizes of files.
- Generic syntax:
  ```
  rsync \[OPTION\] … SRC … \[USER@\]HOST:DEST
  rsync \[OPTION\] … \[USER@\]HOST:SRC \[DEST\]
  ```
- Typical usage:
```
rsync -av --delete SRC DEST

-a           archive mode; equals -rlptgoD (no -H,-A,-X)
  -r         recurse into directories
  -l         copy symlinks as symlinks
  -p         preserve permissions
  -t         preserve modification times
  -g         preserve group
  -o         preserve owner (super-user only)
  -D         same as --devices (preserve device files (super-user only)) --specials (preserve special files)
  -v         increase verbosity
  --delete   delete extraneous files from destination dirs
  -H         preserve hard links
  -A         preserve ACLs (implies --perms)
  -X         preserve extended attributes
```
- Other useful options:
  - `-n`: perform a trial run with no changes made
  - `-z`: compress file data during the transfer
  - `-u`: skip files that are newer on the receiver
  - `-i`: output a change-summary for all updates
  - `--modify-window=1`: basically in windows filesystems time is kept in even numbers (or some
    such problem). This command tells `rsync` to ignore file changes that are only 1 second in
    difference from the original. It is almost impossible that you will create a file, sync it,
    and in ONE second make a change and want to sync it again. So it is safe to use this option
    and it means that `rsync` will not back up everything every time simply because of a one
    second change.

## Resources
- [Wikipedia](https://en.wikipedia.org/wiki/Rsync)
- [phoenixnap.com - rsync back up data](https://phoenixnap.com/kb/rsync-back-up-data)
- [ubuntuforums.org - HOWTO: Backup using Rsync to NTFS](https://ubuntuforums.org/showthread.php?t=820425)
