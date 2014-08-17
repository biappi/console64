from py65.devices.mpu6502 import MPU
from py65.disassembler import Disassembler

import sys
import kernal

def loadfile(filename):
    with open(filename) as f:
        return [ord(i) for i in f.read()]

# io_map = (
#     (0xD000, 0xD3FF, 'VIC (Video Controller)'),
#     (0xD400, 0xD7FF, 'SID (Sound Synthesizer)'),
#     (0xD800, 0xDBFF, 'Color RAM'),
#     (0xDC00, 0xDCFF, 'CIA1 (Keyboard)'),
#     (0xDD00, 0xDDFF, 'CIA2 (Serial Bus, User Port/RS-232)'),
#     (0xDE00, 0xDEFF, 'Open I/O slot #l (CP/M Enable)'),
#     (0xDF00, 0xDFFF, 'Open I/O slot #2 (Disk)'),
# )
 
# import maps
# 
# ioregisters = maps.load_ioregisters()
# 
# def io_thing(address):
#     for i in ioregisters:
#         if i.start <= address and address <= i.end:
#             return i.comment
# 
#     return 'N/A'

class Memory(object):
    def __init__(self):
        self.kernal = loadfile('roms/kernal.rom')
        self.basic  = loadfile('roms/basic.rom')
        self.ram = [0x00] * 0x10000

    def __setitem__(self, address, value):
#        if 0xd000 <= address and address <=0xdfff:
#            print "IO WRITE: %04x - %02x - %s" % (address, value, io_thing(address))
        self.ram[address] = value

    def __getitem__(self, address):
        if address == 0xd012:
            return 0

        if 0xe000 <= address and address <=0xffff:
            return self.kernal[address - 0xe000]

        if 0xa000 <= address and address <=0xbfff:
            return self.basic[address - 0xa000]

#        if 0xd000 <= address and address <=0xdfff:
#            print "IO READ: %02x - %s" % (address, io_thing(address))
#            return 0

        return self.ram[address]

class Patches(object):
    def __init__(self):
        self.patches = {}

        for name, func in vars(self.__class__).iteritems():
            try:
                addr = int(name[1:5], 16)
                self.patches[addr] = func
            except:
                pass 

    def __getitem__(self, address):
        if address in self.patches:
            return self.patches[address]
        else:
            return None

    def xA560_basic_raw_input(c64):
        line = raw_input()

        for i, char in enumerate(line):
            c64.cpu.memory[0x0200 + i] = ord(char)

        c64.cpu.memory[0x0200 + len(line)] = 0x00
        c64.cpu.x = 0xff
        c64.cpu.y = 0x01
        c64.cpu.inst_0x60() # RTS

class C64(object):
    def __init__(self):
        self.mem     = Memory()
        self.cpu     = MPU()
        self.patches = Patches()
        self.dis     = Disassembler(self.cpu)

        pc_low = self.mem[0xfffc]
        pc_hi  = self.mem[0xfffd]

        self.cpu.memory = self.mem
        self.cpu.pc     = (pc_hi << 8) + pc_low

        self.trace = False

    def step(self):
        pc = self.cpu.pc

        if self.trace:
            print "0x%04x - %s" % (pc, self.dis.instruction_at(pc)[1])

        if kernal.base <= pc and pc <= kernal.end:
            kernal_function = kernal.resolve(pc)
            if kernal_function:
                kernal_function(self)
                self.cpu.inst_0x60() # RTS
                return

        patch = self.patches[pc]
        if patch:
            patch(self)
            return

        self.cpu.step()

    def run_for(self, cycles):
        for x in xrange(cycles):
            self.step()
        print
        print 'Emulation over, did %d CPU cycles.' % cycles

    def run_until(self, end_pc):
        while self.cpu.pc != end_pc:
            self.step()

def run():
    C64().run_until(0xa560)

if __name__ == '__main__':
    #run()
    C64().run_for(1000000)
