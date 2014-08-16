class MemoryMapItem(object):
    def __init__(self, line):
        self.name    = line[:7].strip()
        self.start   = line[8:12].strip()
        self.end     = line[13:17].strip()
        self.comment = line[18:].strip()

        self.end = self.start if self.end == '' else self.end

        self.start = int(self.start, 16)
        self.end   = int(self.end,   16)

    def __repr__(self):
        return "(0x%04x, 0x%04x, '%s', '%s')" % (self.start, self.end, self.name, self.comment)

def load_memorymap():
    all_memory = []
    with open('memorymap.txt') as memorymap:
        for line in memorymap:
            try:    all_memory.append(MemoryMapItem(line))
            except: pass

    return all_memory

class SUCA(Exception): pass

class IORegistersItem(object):
    def __init__(self, line):
        self.start   = line[2:6]
        self.end     = line[7:11].strip()
        self.comment = line[35:].rstrip()

        if self.end.endswith('FF'):
            raise Exception()

        self.end = self.start if self.end == '' else self.end

        self.start = int(self.start, 16)
        self.end   = int(self.end,   16)

    def __repr__(self):
        return '(0x%04x, 0x%04x, "%s")' % (self.start, self.end, self.comment)

def load_ioregisters():
    all_io = []
    with open('ioregisters.txt') as registers:
        for line in registers:
            try:    all_io.append(IORegistersItem(line))
            except: pass

    return all_io
