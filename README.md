Console 64
==========

This simple project is supposed to expose an emulation of the Commodore 64
in a UNIX console, just for the lolz.

memorymap.txt
-------------

This is a table from the Commodore 64 reference manual describing a bunch
of memory locations used by the ROMs.

Example
-------
```
willy@Minene console64 master$ python console64.py

    **** COMMODORE 64 BASIC V2 ****

 64K RAM SYSTEM  38911 BASIC BYTES FREE

READY.
10 PRINT "SUCA"

RUN

SUCA

READY.
LIST


10 PRINT "SUCA"
READY.
Traceback (most recent call last):
  File "console64.py", line 157, in <module>
    C64().run_for(1000000)
  File "console64.py", line 122, in run_for
    self.step()
  File "console64.py", line 116, in step
    func(self)
  File "console64.py", line 146, in xA560_c64input
    x = raw_input()
EOFError
willy@Minene console64 master$
```
