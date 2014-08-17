import sys
import getch
import os

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

def int16_to_int8(number):
    return (number & 0xff00) >> 8, number & 0x00ff

def int8_to_int16(hi, lo):
    return (hi << 8) + lo

def hex_dump(i, byte):
    if (i % 16) == 0:
        print " %04x | " % i,

    i += 1

    print '%02x' % byte,
    if (i % 4) == 0:
        print '',
    if (i % 16) == 0:
        print

# ERROR CONSTANTS
# ---------------

E_TOOMANYFILES       = 0x01
E_FILEOPEN           = 0x02
E_FILENOTOPEN        = 0x03
E_FILENOTFOUND       = 0x04
E_DEVICENOTPRESENT   = 0x05
E_NOTINPUTFILE       = 0x06
E_NOTOUTPUTFILE      = 0x07
E_MISSINGFILENAME    = 0x08
E_ILLEGALDEVICENR    = 0x09
E_NEXTWITHOUTFOR     = 0x0A
E_SYNTAX             = 0x0B
E_RETURNWITHOUTGOSUB = 0x0C
E_OUTOFDATA          = 0x0D
E_ILLEGALQUANTITY    = 0x0E
E_OVERFLOW           = 0x0F
E_OUTOFMEMORY        = 0x10
E_UNDEFDSTATEMENT    = 0x11
E_BADSUBSCRIPT       = 0x12
E_REDIMDARRAY        = 0x13
E_DIVISIONBYZERO     = 0x14
E_ILLEGALDIRECT      = 0x15
E_TYPEMISMATCH       = 0x16
E_STRINGTOOLONG      = 0x17
E_FILEDATA           = 0x18
E_FORMULATOOCOMPLEX  = 0x19
E_CANTCONTINUE       = 0x1A
E_UNDEFDFUNCTION     = 0x1B
E_VERIFY             = 0x1C
E_LOAD               = 0x1D
E_BREAK              = 0x1E

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

@kernal_impl(0xffd5)
def load(c64):
    'Load RAM From Device'

    name_len = c64.mem[0x00b7]
    name_ptr = int8_to_int16(c64.mem[0x00bc], c64.mem[0x00bb])
    name = ''

    if name_len == 0:
        c64.cpu.p |= c64.cpu.CARRY
        c64.cpu.a  = E_MISSINGFILENAME
        return

    for i in xrange(name_len):
        name += chr(c64.mem[name_ptr + i])

    if name == '$':
        cwd = os.getcwd()
        message = ['DIRECTORY LISTING OF:', '   ' + cwd.upper(), ' ']

        directory_listing = filter(lambda i: i.endswith('.CBM'),
                                   os.listdir(cwd))
        directory_listing = filter(lambda i: not i.startswith('.'),
                                   os.listdir(cwd))
        directory_listing = filter(lambda i: i.upper() == i,
                                   os.listdir(cwd))
        directory_listing = ('\x93"%s":\x80' % i for i in directory_listing)
        # 0x93 - BASIC token for 'LOAD'
        # 0x80 - BASIC token for 'END'

        directory_listing = list(directory_listing)

        if len(directory_listing):
            message.extend(directory_listing)
            message.extend([' ', 'LOAD A FILE USING A GOTO<NR> STATEMENT'])
        else:
            message.append('NO *.CBM BASIC IN THE DIRECTORY')
            message.append('(FILENAME MUST BE UPPERCAE)')

        bytes_to_load = list(encode_lines(message))
    else:
        try:
            bytes_to_load = open(name).read()
            bytes_to_load = (ord(i) for i in bytes_to_load)
            bytes_to_load = list(bytes_to_load)
        except:
            c64.cpu.p |= c64.cpu.CARRY
            c64.cpu.a  = E_NOTINPUTFILE
            return

    c64.mem[0xc3] = c64.cpu.x
    c64.mem[0xc4] = c64.cpu.y
    c64.mem[0x93] = c64.cpu.a

    store_into = c64.cpu.x + (c64.cpu.y << 8)
    store_end = store_into + len(bytes_to_load)

    for i, byte in enumerate(bytes_to_load):
        c64.mem[store_into + i] = byte

    c64.cpu.p &= ~c64.cpu.CARRY
    c64.cpu.a = 0
    c64.cpu.y, c64.cpu.x = int16_to_int8(store_end)

@kernal_impl(0xffd8)
def save(c64):
    'Save RAM To Device'

    name_len = c64.mem[0x00b7]
    name_ptr = int8_to_int16(c64.mem[0x00bc], c64.mem[0x00bb])
    name = ''

    if name_len == 0:
        c64.cpu.p |= c64.cpu.CARRY
        c64.cpu.a  = E_MISSINGFILENAME
        return

    c64.cpu.p &= ~c64.cpu.CARRY

    start_ptr_1 = c64.cpu.a
    start_ptr   = int8_to_int16(c64.mem[start_ptr_1 + 1], c64.mem[start_ptr_1])
    end_ptr     = int8_to_int16(c64.cpu.y, c64.cpu.x)

    file_no     = c64.mem[0x00b8]
    addr2       = c64.mem[0x00b9]
    dev_no      = c64.mem[0x00ba]

    for i in xrange(name_len):
        name += chr(c64.mem[name_ptr + i])

    name = name.upper() + '.CBM'
    to_save = ''.join(chr(c64.mem[i]) for i in xrange(start_ptr, end_ptr + 1))

    open(name, 'w').write(to_save)

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

# BASIC LISTING ENCODING
# ----------------------

# Thank you, random internet guy
# http://www.pagetable.com/?p=273

def encode_lines(lines):
    current = 0x0401 # apparently it's the start of VIC-20
                     # BASIC ram, which will be however
                     # rebased by the C64 BASICv2

    for i, line in enumerate(lines):
        next_line = current + len(line) + 2 + 2 + 1 # 2 = space for next ptr
                                                    # 2 = space for line number
                                                    # 1 = space for end-of-line

        line_no_hi,   line_no_lo   = int16_to_int8((i + 1) * 10)
        next_line_hi, next_line_lo = int16_to_int8(next_line)

        current = next_line

        yield next_line_lo
        yield next_line_hi

        yield line_no_lo
        yield line_no_hi

        for char in line:
            yield ord(char)

        yield 0x00

    yield 0x00
    yield 0x00

