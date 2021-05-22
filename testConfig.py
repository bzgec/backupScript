"""
Special "folders" options:
- exclude: specify which files/folders/patterns to not include in the backup
- options: specify special options for rsync command
  - no-delete: keep files/folders which don't exist on source path but exist on destination path
               (this is useful for folders like Pictures...)
"""

backupConfig = [
    {
        "destinationPath": "/home/bzgec/Projects/backupScript/test/dest/",  # External disk path - this is where to backup
        "mainPath": "/home/bzgec/Projects/backupScript/test/src/",  # Do not start active user directory with '~/' because it is going to fail
        "toBackup": [
            {
                "folders": [
                    {"path": "test"},  # Normal backup test
                    {"path": "test_exclude", "exclude": ['exclude_folder', '*.adoc']},  # Test exclude option
                    {"path": "test_no-delete", "options": ["no-delete"]},  # Test no-delete option
                ]
            },

            # Test commonPath
            {
                "commonPath": "test_commonPath/",
                "folders": [
                    {"path": "folder1"},
                    {"path": "folder2"},
                    {"path": "folder3"},
                ]
            },
        ]
    },

    # Test multiple path/disk setup
    {
        "destinationPath": "/home/bzgec/Projects/backupScript/test/dest/",  # External disk path - this is where to backup
        "mainPath": "/home/bzgec/Projects/backupScript/test/src/",  # Do not start active user directory with '~/' because it is going to fail
        "toBackup": [
            {
                "commonPath": "test_multiPath/",
                "folders": [
                    {"path": "test"},
                ]
            },
        ]
    },
]
