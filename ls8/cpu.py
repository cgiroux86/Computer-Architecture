"""CPU functionality."""

import sys
import re


class CPU:
    """Main CPU class."""

    def __init__(self):
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.running = True
        self.PC = 0
        self.HLT = 0b00000001
        self.LDI = 0b10000010
        self.PRN = 0b01000111
        self.NOP = 0b00000000
        self.ADD = 0b10100000
        self.MUL = 0b10100010

        """Construct a new CPU."""

    def load(self, filename):
        """Load a program into memory."""
        address = 0
        print(filename)
        try:
            with open(filename) as f:
                for line in f:
                    try:
                        self.ram[address] = int(
                            re.findall(r'^[0-9]*', line)[0], 2)
                        address += 1
                    except ValueError:
                        pass
        except:
            print(f'unable to open file: {filename}')
            sys.exit(1)
        print(self.ram)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        if op == self.ADD:
            self.reg[reg_a] += self.reg[reg_b]
        elif op == self.MUL:
            self.reg[reg_a] *= self.reg[reg_b]

        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

    def run(self):
        # self.load(filename)

        while self.running:
            operands = self.ram[self.PC] >> 6
            alu = self.ram[self.PC] >> 5 & 1
            IR = self.ram[self.PC]
            if alu:
                self.alu(IR,
                         self.ram[self.PC + 1], self.ram[self.PC + 2])
            if IR == 130:
                self.reg[self.ram[self.PC + 1]] = self.ram[self.PC + 2]
            elif IR == 1:
                self.running = False
                self.PC = 0
            elif IR == 71:
                print(self.reg[self.ram[self.PC + 1]])
            self.PC += operands + 1

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value
