import os

commandsToRun = [
    'sudo chgrp gpio /sys/class/gpio/export',
    'sudo chgrp gpio /sys/class/gpio/unexport',
    'sudo chmod 775 /sys/class/gpio/export',
    'sudo chmod 775 /sys/class/gpio/unexport'
]

def setPermissions():
    for cmd in commandsToRun :
        os.system(cmd)


