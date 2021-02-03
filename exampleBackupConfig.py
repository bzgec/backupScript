
destinationPath = "/media/USER/Elements/"  # External disk path - this is where to backup

disksToBackup = [
    {
        "diskPath": "/home/USER/",  # Do not start active user directory with '~/' because it is going to fail
        "folders":
            [
                {"path": "Documents", "exclude": []},
                {"path": "Pictures", "exclude": []},
                {"path": "Projects", "exclude": ["__pycache__"]},
            ]
    },
    {
        "diskPath": "/media/USER/DISK/",
        "folders":
            [
                {"path": "Books", "exclude": []},
                {"path": "Music", "exclude": []},
                {"path": "Random", "exclude": []},
            ]
    },
]
