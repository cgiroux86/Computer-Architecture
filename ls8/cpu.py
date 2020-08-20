"""CPU functionality."""

import sys
import re
import os


class CPU:
    """Main CPU class."""

    def __init__(self):
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.running = True
        self.PC = 0
        self.SP = 0xf4
        self.reg[-1] = self.SP
        self.HLT = 0b00000001
        self.LDI = 0b10000010
        self.PRN = 0b01000111
        self.NOP = 0b00000000
        self.ADD = 0b10100000
        self.SUB = 0b10100001
        self.MUL = 0b10100010
        self.DIV = 0b10100011
        self.MOD = 0b10100100
        self.PUSH = 0b01000101
        self.POP = 0b01000110
        self.CALL = 0b01010000
        self.RET = 0b00010001
        self.lookup = {self.LDI: self.loadInt,
                       self.HLT: self.halt, self.PRN: self.prnt, self.PUSH: self.pushItem, self.POP: self.popItem, self.RET: self.rtrn, self.CALL: self.callFn}

        """Construct a new CPU."""

    def load(self, filename):
        """Load a program into memory."""
        address = 0
        try:
            with open(filename) as f:
                for line in f:
                    try:
                        self.ram[address] = int(
                            re.findall(r'^[0-9]*', line)[0], 2)
                        address += 1
                    except ValueError:
                        continue
        except:
            print(f'unable to open file: {filename}')
            sys.exit(1)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        if op == self.ADD:
            self.reg[reg_a] += self.reg[reg_b]
        elif op == self.MUL:
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == self.SUB:
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == self.DIV:
            # check for zero divisor
            if self.reg[reg_b] == 0:
                raise Exception('zero divisor')
            else:
                self.reg[reg_a] /= self.reg[reg_b]
        elif op == self.MOD:
            # check for zero divisor
            if self.reg[reg_b] == 0:
                raise Exception('zero divisor')
            else:
                self.reg[reg_a] %= self.reg[reg_b]

        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.PC,
            # self.fl,
            # self.ie,
            self.ram_read(self.PC),
            self.ram_read(self.PC + 1),
            self.ram_read(self.PC + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

    def loadInt(self, operand_a, operand_b):
        self.reg[operand_a] = operand_b

    def halt(self, operand_a, operand_b):
        self.running = False
        self.PC = 0

    def prnt(self, operand_a, operand_b):
        print(self.reg[operand_a])

    def pushItem(self, operand_a, operand_b):
        self.SP -= 1
        copy = self.reg[operand_a]
        print(copy)
        self.ram_write(self.SP, copy)
        print(self.ram)

    def popItem(self, operand_a, operand_b):
        data = self.ram_read(self.SP)
        self.reg[operand_a] = data
        # increment stack counter
        self.SP += 1

    def callFn(self, operand_a, operand_b):
        self.SP -= 1
        self.ram[self.SP] = self.PC + 2
        self.PC = self.reg[operand_a]
        # print(self.PC)

    def rtrn(self, operand_a, operand_b):
        self.PC = self.ram[self.SP]
        self.SP += 1

    def incrementPC(self, fn, operands):
        if fn == self.CALL or fn == self.RET:
            self.PC += 0
        else:
            self.PC += operands + 1

    def run(self):
        while self.running:
            # right shift 6 to get total op length
            operands = self.ram_read(self.PC) >> 6
            operand_a = self.ram_read(self.PC + 1)
            operand_b = self.ram_read(self.PC + 2)
            # right shift 5, mask with 1 to find out whether it's an ALU op
            alu = self.ram_read(self.PC) >> 5 & 1
            IR = self.ram_read(self.PC)

            if alu:
                self.alu(IR,
                         operand_a, operand_b)

            else:
                self.lookup[IR](operand_a, operand_b)
            self.incrementPC(IR, operands)

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value


# cpu = CPU()
# # filename = sys.argv[1]
# cpu.load('ls8/examples/call.ls8')
# cpu.run()
