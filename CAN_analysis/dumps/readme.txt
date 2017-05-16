Old filenames as recieved from the guys at illuminati:
REVERSE With Digital Toggle SMART ED Drivetrain Slow Drive Long  Enable SMART 352.2vSeven 323.5V 0x01 switch byte.csv
With Digital Toggle SMART ED Drivetrain Slow Drive Enable 324.6v 0x101 .csv
Renamed to:
REVERSE_SMART.csv
FORWARD_SMART.csv
Also changed 0x01 ignition enable message to 0x101, added 0x100 at end for disable.
Use my modified candue GVRET software to make this work. Digital pin 7 should be connected to load switch.

Also got some files I constructed to enable and disable the DC/DC converter. 112_on.csv and 112_off.csv Replay with long delay (1s?) between messages. Seems to work consistantly.