from py65.devices import mpu6502


class MPU(mpu6502.MPU):
    """
    The 65Org16 is a derivative of the 6502 architecture
      - with 32-bit address space (by using 16-bit bytes)
      - with no specific support for 8-bit bytes
      - with BCD mode not supported
      - and otherwise all opcodes and addressing modes are like the NMOS 6502
      - sign bit is bit 15, overflow bit is bit 14

    One implementation can be found here:
    https://github.com/BigEd/verilog-6502/wiki
    """

    BYTE_WIDTH = 16
    BYTE_FORMAT = "%04x"
    ADDR_WIDTH = 32
    ADDR_FORMAT = "%08x"

    def __init__(self, *args, **kwargs):
        mpu6502.MPU.__init__(self, *args, **kwargs)
        self.name = '65Org16'
        self.waiting = False
        self.IrqTo = (1 << self.ADDR_WIDTH) - 2
        self.ResetTo = (1 << self.ADDR_WIDTH) - 4
        self.NMITo = (1 << self.ADDR_WIDTH) - 6
        self.NEGATIVE = 1 << 15
        self.OVERFLOW = 1 << 14

    def step(self):
        if self.waiting:
            self.processorCycles += 1
        else:
            mpu6502.MPU.step(self)
        return self

    # Make copies of the lists
    instruct = mpu6502.MPU.instruct[:]
    cycletime = mpu6502.MPU.cycletime[:]
    extracycles = mpu6502.MPU.extracycles[:]
    disassemble = mpu6502.MPU.disassemble[:]

    def reprformat(self):
        return ("%s   PC     AC   XR   YR   SP  NV---------BDIZC\n" +
                "%s: %08x %04x %04x %04x %04x %s")
