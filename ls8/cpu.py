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
        self.SP = 0xf3
        self.reg[-1] = self.SP
        self.HLT = 0b00000001
        self.LDI = 0b10000010
        self.PRN = 0b01000111
        self.NOP = 0b00000000
        self.ADD = 0b10100000
        self.MUL = 0b10100010
        self.PUSH = 0b01000101
        self.POP = 0b01000110

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
            operands = self.ram_read(self.PC) >> 6
            operand_a = self.ram_read(self.PC + 1)
            operand_b = self.ram_read(self.PC + 2)
            alu = self.ram_read(self.PC) >> 5 & 1
            IR = self.ram_read(self.PC)

            if alu:
                self.alu(IR,
                         operand_a, operand_b)

            if IR == self.LDI:
                self.reg[operand_a] = operand_b

            elif IR == self.HLT:
                self.running = False
                self.PC = 0

            elif IR == self.PRN:
                print(self.reg[operand_a])

            elif IR == self.PUSH:
                # decrement stack counter
                self.reg[-1] -= 1
                copy = self.reg[operand_a]
                self.ram_write(self.SP, copy)

            elif IR == self.POP:
                data = self.ram_read(self.SP)
                self.reg[operand_a] = data
                # increment stack counter
                self.SP += 1

            self.PC += operands + 1

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value
