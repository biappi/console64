Console 64
==========

This simple project is supposed to expose an emulation of the Commodore 64
in a UNIX console, just for the lolz.

Status
------

Simple BASIC commands should work. LOAD / SAVE functionality is implemented.

List the current working directory using ```LOAD"$"``` then ```LIST```.

Docs
----
A bit of C64 documentation can be found in the ```docs/``` directory. The annotated
ROM disassembly is particularly useful. Thanks Marko Makela!

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

Loading example
---------------

```
willy@Minene console64 master$ python console64.py

    **** COMMODORE 64 BASIC V2 ****

 64K RAM SYSTEM  38911 BASIC BYTES FREE

READY.
LOAD"$"

READY.
LIST

10 DIRECTORY LISTING OF:
20    /USERS/WILLY/SOURCES/CONSOLE64
30
40 LOAD"HELLOWORLD.CBM":END
50
60 LOAD A FILE USING A GOTO<NR> STATEMENT
READY.
GOTO40
HELLO
WORLD

READY.
LIST

10 PRINT"HELLO"
20 PRINT"WORLD"
30 END
READY.
30 PRINT"THIS IS RETROWSOME!"
SAVE"RETROWSOME"

READY.
NEW

READY.
LOAD"RETROWSOME.CBM"

READY.
LIST

10 PRINT"HELLO"
20 PRINT"WORLD"
30 PRINT"THIS IS RETROWSOME!"
READY.
```
