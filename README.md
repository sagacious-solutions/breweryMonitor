# Create GPIO permissions

Run all these commands to get GPIO working


These commands should allow GPIO to be modified by pi, however it doesn't seem to work.
That being said, running the last 4 after system boot does allow sudo to access the gpio

Currently the last 4 are run from setGpioPermissions.py as part of main.py start. This
allows sudo to access GPIO any time it runs.

```
sudo groupadd gpio
sudo usermod -aG gpio pi
su pi
sudo chgrp gpio /sys/class/gpio/export
sudo chgrp gpio /sys/class/gpio/unexport
sudo chmod 775 /sys/class/gpio/export
sudo chmod 775 /sys/class/gpio/unexport
```