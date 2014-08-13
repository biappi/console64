from py65.devices.mpu6502 import MPU

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

    def __setitem__(self, address, value):
        self.ram[address] = value
        print '(write) [%04x] = %02x' % (address, value)

    def __getitem__(self, address):
        v = None

        for overlay, data in self.overlays:
            if address in overlay:
                v = ord(data[address - overlay.start])

        if v is None:
            v = self.ram[address]

        print '(read)  [%04x] = %02x' % (address, v)
        return v

    def add_overlay(self, data, start, end):
        self.overlays.append((MemoryRange(start, end), data))

    def overlay_file(self, filename, start, end):
        with open(filename) as f:
            self.add_overlay(f.read(), start, end)

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
        for c in self.comments:
            if address in c:
                print '        %s' % c

mem = Memory()
cpu = MPU()

cpu.memory = MemoryCommenter(mem)
cpu.pc = mem[0xfffc] + (mem[0xfffd] << 8)

for x in xrange(30):
    cpu.step()

