from py65.devices.mpu6502 import MPU
from py65.disassembler import Disassembler

import sys
import kernal

def loadfile(filename):
    with open(filename) as f:
        return [ord(i) for i in f.read()]

class Memory(object):
    def __init__(self):
        self.kernal = loadfile('roms/kernal.rom')
        self.basic  = loadfile('roms/basic.rom')
        self.ram = [0x00] * 0x10000
        self.do_log = False

    def __setitem__(self, address, value):
        self.ram[address] = value

    def __getitem__(self, address):
        if address == 0xd012:
            return 0

        if 0xe000 <= address and address <=0xffff:
            return self.kernal[address - 0xe000]

        if 0xa000 <= address and address <=0xbfff:
            return self.basic[address - 0xa000]

        return self.ram[address]

class C64(object):
    def __init__(self):
        self.mem = Memory()
        self.cpu = MPU()

        pc_low = self.mem[0xfffc]
        pc_hi  = self.mem[0xfffd]

        self.cpu.memory = self.mem
        self.cpu.pc     = (pc_hi << 8) + pc_low


    def step(self):
        pc = self.cpu.pc

        if kernal.base <= pc and pc <= kernal.end:
            kernal_function = kernal.resolve(pc)
            if kernal_function:
                kernal_function(self)
                self.cpu.inst_0x60() # RTS
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
    C64().run_for(1000000)
