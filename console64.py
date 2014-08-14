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

    def __setitem__log(self, address, value):
        self.ram[address] = value
        if self.do_log:
            self.log('\t(write) [%04x] = %02x %s' % (address, value, repr(chr(value))))

    def __setitem__(self, address, value):
        self.ram[address] = value

    def __getitem__log(self, address):
        v = None

        if address == 0xd012:
            return 0

        for overlay, data in self.overlays:
            if address in overlay:
                v = data[address - overlay.start]

        if v is None:
            v = self.ram[address]

        if self.do_log:
            self.log('\t(read)  [%04x] = %02x' % (address, v))

        return v

    def __getitem__(self, address):
        if address == 0xd012:
            return 0

        for overlay, data in self.overlays:
            if address in overlay:
                return data[address - overlay.start]

        return self.ram[address]

    def add_overlay(self, data, start, end):
        self.overlays.append((MemoryRange(start, end), data))

    def overlay_file(self, filename, start, end):
        with open(filename) as f:
            data = [ord(i) for i in f.read()]
            self.add_overlay(data, start, end)

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

class C64(object):
    def __init__(self):
        self.mem = Memory()
        self.cpu = MPU()

        pc_low = self.mem[0xfffc]
        pc_hi  = self.mem[0xfffd]

        self.cpu.memory = self.mem
        self.cpu.pc     = (pc_hi << 8) + pc_low

        self.native_funcs = []

        for name, func in vars(self.__class__).iteritems():
            try:
                addr = int(name[1:5], 16)
                self.native_funcs.append((addr, func))
            except:
                pass

    def step(self):
        for addr, func in self.native_funcs:
            if self.cpu.pc == addr:
                func(self)

        self.cpu.step()

    def run_for(self, cycles):
        for x in xrange(cycles):
            self.step()

    def run_until(self, end_pc):
        while self.cpu.pc != end_pc:
            self.step()

    def xFFD2_c64print(self):
        c = self.cpu.a

        if c == 0x93:
            pass

        elif c == 0x0a:
            pass

        elif c == 0x0d:
            sys.stdout.write('\n')

        else:
            sys.stdout.write(chr(c))

    def xA560_c64input(self):
        x = raw_input()
        y = 0

        for i in x:
            self.cpu.memory[0x0200 + y] = ord(i)
            y += 1

        self.cpu.memory[0x0200 + y] = 0x0d
        self.cpu.x = y
        self.cpu.pc = 0xaaca

#C64().run_for(1000000)
def run():
    C64().run_until(0xa560)

