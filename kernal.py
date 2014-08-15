import sys
import getch

# HELPER FUNCTIONS
# ----------------

nr    = 39
base  = 0xff81
end   = base + (nr * 3)
impls = nr * [None]

# -

DO_LOG = False

# -

def kernal_not_impl(address):
    if not DO_LOG:
        def inner(f):
            return f
        return inner

    def inner(func):
        def log(c64):
            print "KERNAL %s] %s" % (func.__name__, func.__doc__)
        log.log = True
        slot = (address - base) / 3
        impls[slot] = log
        return func

    return inner

def kernal_impl(address):
    def inner(func):
        slot = (address - base) / 3
        impls[slot] = func
        return func
    return inner

def resolve(address):
    slot = (address - base) / 3
    impl = impls[slot]
    if getattr(impl, 'log', False):
        impl(None)
        return None
    else:
        return impl

# KERNAL IMPLEMENTATION
# ---------------------

@kernal_not_impl(0xff81)
def cint(c64):
    'Init Editor & Video Chips'
    pass

@kernal_not_impl(0xff84)
def ioinit(c64):
    'Init I/O Devices, Ports & Timers'
    pass

@kernal_not_impl(0xff87)
def ramtas(c64):
    'Init Ram & Buffers'
    pass

@kernal_not_impl(0xff8a)
def restor(c64):
    'Restore Vectors'
    pass

@kernal_not_impl(0xff8d)
def vector(c64):
    'Change Vectors For User'
    pass

@kernal_not_impl(0xff90)
def setmsg(c64):
    'Control OS Messages'
    pass

@kernal_not_impl(0xff93)
def secnd(c64):
    'Send SA After Listen'
    pass

@kernal_not_impl(0xff96)
def tksa(c64):
    'Send SA After Talk'
    pass

@kernal_not_impl(0xff99)
def memtop(c64):
    'Set/Read System RAM Top'
    pass

@kernal_not_impl(0xff9c)
def membot(c64):
    'Set/Read System RAM Bottom'
    pass

@kernal_not_impl(0xff9f)
def scnkey(c64):
    'Scan Keyboard'
    pass

@kernal_not_impl(0xffa2)
def settmo(c64):
    'Set Timeout In IEEE'
    pass

@kernal_not_impl(0xffa5)
def acptr(c64):
    'Handshake Serial Byte In'
    pass

@kernal_not_impl(0xffa8)
def ciout(c64):
    'Handshake Serial Byte Out'
    pass

@kernal_not_impl(0xffab)
def untalk(c64):
    'Command Serial Bus UNTALK'
    pass

@kernal_not_impl(0xffae)
def unlsn(c64):
    'Command Serial Bus UNLISTEN'
    pass

@kernal_not_impl(0xffb1)
def listn(c64):
    'Command Serial Bus LISTEN'
    pass

@kernal_not_impl(0xffb4)
def talk(c64):
    'Command Serial Bus TALK'
    pass

@kernal_not_impl(0xffb7)
def readss(c64):
    'Read I/O Status Word'
    pass

@kernal_not_impl(0xffba)
def setlfs(c64):
    'Set Logical File Parameters'
    pass

@kernal_not_impl(0xffbd)
def setnam(c64):
    'Set Filename'
    pass

@kernal_not_impl(0xffc0)
def iopen(c64):
    'Open Vector [f34a]'
    pass

@kernal_not_impl(0xffc3)
def iclose(c64):
    'Close Vector [f291]'
    pass

@kernal_not_impl(0xffc6)
def ichkin(c64):
    'Set Input [f20e]'
    pass

@kernal_not_impl(0xffc9)
def ichkout(c64):
    'Set Output [f250]'
    pass

@kernal_not_impl(0xffcc)
def iclrch(c64):
    'Restore I/O Vector [f333]'
    pass

@kernal_impl(0xffcf)
def ichrin(c64):
    'Input Vector, chrin [f157]'

    c64.cpu.p &= ~c64.cpu.CARRY

    c = getch.getch()
    if ord(c) == 0x03 or ord(c) == 0x04:
        sys.exit(1) # ^D and ^C

    sys.stdout.write(c)
    c64.cpu.a = ord(c)

@kernal_impl(0xffd2)
def ichrout(c64):
    'Output Vector, chrout [f1ca]'

    c64.cpu.p &= ~c64.cpu.CARRY

    c = c64.cpu.a

    if   c == 0x93: c = None
    elif c == 0x0a: c = None
    elif c == 0x0d: c = ord('\n')

    if c:
        sys.stdout.write(chr(c))

@kernal_not_impl(0xffd5)
def load(c64):
    'Load RAM From Device'
    pass

@kernal_not_impl(0xffd8)
def save(c64):
    'Save RAM To Device'
    pass

@kernal_not_impl(0xffdb)
def settim(c64):
    'Set Real-Time Clock'
    pass

@kernal_not_impl(0xffde)
def rdtim(c64):
    'Read Real-Time Clock'
    pass

@kernal_not_impl(0xffe1)
def istop(c64):
    'Test-Stop Vector [f6ed]'
    pass

@kernal_not_impl(0xffe4)
def igetin(c64):
    'Get From Keyboad [f13e]'
    pass

@kernal_not_impl(0xffe7)
def iclall(c64):
    'Close All Channels And Files [f32f]'
    pass

@kernal_not_impl(0xffea)
def udtim(c64):
    'Increment Real-Time Clock'
    pass

@kernal_not_impl(0xffed)
def screen(c64):
    'Return Screen Organization'
    pass

@kernal_not_impl(0xfff0)
def plot(c64):
    'Read / Set Cursor X/Y Position'
    pass

@kernal_not_impl(0xfff3)
def iobase(c64):
    'Return I/O Base Address'
    pass

