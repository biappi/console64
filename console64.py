from py65.devices.mpu6502 import MPU
from py65.disassembler import Disassembler

import sys

class MemoryRange(object):
    def __init__(self, start, end):
        self.start = start
        self.end   = end

    def __contains__(self, address):
        return self.start <= address and address <= self.end

class Comment(MemoryRange):
    def __init__(self, line):
        self.name    = line[:7].strip()
        self.start   = line[8:12].strip()
        self.end     = line[13:17].strip()
        self.comment = line[18:].strip()

        self.end = self.start if self.end == '' else self.end

        self.start = int(self.start, 16)
        self.end   = int(self.end,   16)

    def __str__(self):
        if not self.name:
            return self.comment
        return '%s (%s)' % (self.comment, self.name)

class Memory(object):
    def __init__(self):
        self.overlays = []
        self.overlay_file('roms/kernal.rom',    0xe000, 0xffff)
        self.overlay_file('roms/character.rom', 0xd000, 0xdfff)
        self.overlay_file('roms/basic.rom',     0xa000, 0xbfff)
        self.ram = [0x00] * 0x10000
        self.do_log = False

    def __setitem__(self, address, value):
        self.ram[address] = value
        self.log('\t(write) [%04x] = %02x %s' % (address, value, repr(chr(value))))

    def __getitem__(self, address):
        v = None

        if address == 0xd012:
            return 0

        for overlay, data in self.overlays:
            if address in overlay:
                v = ord(data[address - overlay.start])

        if v is None:
            v = self.ram[address]

        self.log('\t(read)  [%04x] = %02x' % (address, v))
        return v

    def add_overlay(self, data, start, end):
        self.overlays.append((MemoryRange(start, end), data))

    def overlay_file(self, filename, start, end):
        with open(filename) as f:
            self.add_overlay(f.read(), start, end)

    def log(self, l):
        if self.do_log:
            print l

class MemoryCommenter(object):
    def __init__(self, memory):
        self.memory = memory
        with open('memorymap.txt') as memorymap:
            self.comments = [Comment(line) for line in memorymap]

    def __setitem__(self, address, value):
        self.memory[address] = value
        self.comment(address)

    def __getitem__(self, address):
        v = self.memory[address]
        self.comment(address)
        return v

    def comment(self, address):
        if not self.memory.do_log:
            return
        for c in self.comments:
            if address in c:
                print '\t        %s' % c

def c64print_(cpu):
    c = cpu.a
    num = ord('0') <= c <= ord('9')
    upp = ord('A') <= c <= ord('Z')
    low = ord('a') <= c <= ord('z')

    if num or upp or low:
        s = '(%s)' % chr(c)
    else:
        s = ''

    print '%02x %03d' % (c, c), s
    return

def c64print(cpu):
    c = cpu.a

    if c == 0x93:
        pass

    elif c == 0x0a:
        pass

    elif c == 0x0d:
        sys.stdout.write('\n')

    else:
        sys.stdout.write(chr(c))

def c64input(cpu):
    x = raw_input()
    y = 0

    for i in x:
        cpu.memory[0x0200 + y] = ord(i)
        y += 1

    cpu.memory[0x0200 + y] = 0x0d
    cpu.x = y
    cpu.pc = 0xaaca

mem = Memory()
cpu = MPU()
dis = Disassembler(cpu)

cpu.memory = MemoryCommenter(mem)
cpu.pc = mem[0xfffc] + (mem[0xfffd] << 8)

for x in xrange(1000000):
    if cpu.pc == 0xffd2:
        c64print(cpu)

    if cpu.pc == 0xA560:
        # mem.do_log = 1
        c64input(cpu)

    if mem.do_log:
        mem.do_log = False
        print '%04X %s' % (cpu.pc, dis.instruction_at(cpu.pc)[1])
        mem.do_log = True

    cpu.step()

