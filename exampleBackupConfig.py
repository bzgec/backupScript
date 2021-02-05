"""
Special "folders" options:
- exclude: specify which files/folders/patterns to not include in the backup
- options: specify special options for rsync command
  - no-delete: keep files/folders which don't exist on source path but exist on destination path
               (this is useful for folders like Pictures...)
"""

backupConfig = [
    {
        "destinationPath":  "/media/USER/Elements/",  # External disk path - this is where to backup
        "mainPath": "/home/USER/",  # Do not start active user directory with '~/' because it is going to fail
        "toBackup": [
            {
                "commonPath": "Documents/",
                "folders": [
                    {"path": "Notion"},
                    {"path": "storage"},
                    {"path": "apps", "exclude": ['squashfs-root']},
                ]
            },
            {
                "folders": [
                    {"path": "Pictures", "options": ["no-delete"]},
                    {"path": "Projects", "exclude": ["__pycache__"]},
                ]
            },
        ]
    },
    {
        "destinationPath": "/media/USER/Elements/",  # External disk path - this is where to backup
        "mainPath": "/media/USER/SlimBoi/",
        "toBackup": [
            {
                "folders": [
                    {"path": "Books"},
                    {"path": "Music"},
                    {"path": "Random"},
                ]
            },
        ]
    },
]
