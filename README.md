# TM5-700_DataLog
Logging data from the registers of the TM5-700

This is a bit of code to Log data from the TM5-700 through modbus.

few things to note:
- make sure your laptop IP is 10.38.4.35
- that you have installed all the necessary python libraries
- the code has been written in python version 3.7.3
- the code has been written to gather the Z coordinate of the tcp and the Z force every 0.05 seconds, but can easily be changed to read different data.
- the library pyModbusTCP had version 0.2.0.
