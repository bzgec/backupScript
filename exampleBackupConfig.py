backupConfig = [
    {
        "destinationPath":  "/media/USER/Elements/",  # External disk path - this is where to backup
        "mainPath": "/home/USER/",  # Do not start active user directory with '~/' because it is going to fail
        "toBackup":
            [
                {
                    "commonPath": "Documents/",
                    "folders":
                        [
                            {"path": "Notion", "exclude": []},
                            {"path": "storage", "exclude": []},
                            {"path": "apps", "exclude": ['squashfs-root']},
                        ]
                },
                {
                    "folders": [
                        {"path": "Pictures", "exclude": []},
                        {"path": "Projects", "exclude": ["__pycache__"]},
                    ]
                }
            ]
    },
    {
        "destinationPath": "/media/USER/Elements/",  # External disk path - this is where to backup
        "mainPath": "/media/USER/SlimBoi/",
        "toBackup":
            [
                {
                    "folders":
                    [
                        {"path": "Books", "exclude": []},
                        {"path": "Music", "exclude": []},
                        {"path": "Random", "exclude": []},
                    ]
                }
            ]
    },
]
