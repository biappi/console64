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
10 PRINT "HELLO"
20 PRINT " WORLD"
30 PRINT "  FROM"
```
```
LIST

10 PRINT "HELLO"
20 PRINT " WORLD"
30 PRINT "  FROM"
READY.
```

```
30
```
```
LIST

10 PRINT "HELLO"
20 PRINT " WORLD"
READY.
```
```
RUN
HELLO
 WORLD

READY.
```
