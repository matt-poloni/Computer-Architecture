"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 0x100 # 256 in hex
        self.reg = [0] * 0b1000 # 8 in binary
        sp = 0b111 # 7 in binary
        self.reg[sp] = 0xF4 # 244 in hex
        self.pc = 0

        def LDI(index, integer): self.reg[index] = integer
        def PRN(index, b=None): print(self.reg[index])
        def PUSH(index, b=None):
            self.reg[sp] -= 1
            self.ram[self.reg[sp]] = self.reg[index]
        def POP(index, b=None):
            self.reg[index] = self.ram[self.reg[sp]]
            self.reg[sp] += 1
        def CALL(index, b=None):
            self.reg[sp] -= 1
            self.ram[self.reg[sp]] = self.pc + 2
            self.pc = self.reg[index]
        def RET(a=None, b=None):
            self.pc = self.ram[self.reg[sp]]
            self.reg[sp] += 1

        self.opcodes = {
            0b00000000: 'NOP',
            0b00000001: 'HLT',
            0b10000010: LDI,
            0b01000111: PRN,
            0b01000101: PUSH,
            0b01000110: POP,
            0b01010000: CALL,
            0b00010001: RET,
            # ALU ops
            0b10100000: 'ADD',
            0b10100010: 'MUL'
        }
    
    def ram_read(self, mar):
        if mar > 255:
            raise Exception(f"RAM does not extend to {mar}")
        return self.ram[mar]
    
    def ram_write(self, mar, mdr):
        if mar > 255:
            raise Exception(f"RAM does not extend to {mar}")
        self.ram[mar] = mdr

    def load(self):
        """Load a program into memory."""
        if len(sys.argv) < 2:
            raise Exception("Please specify the program to load")
        address = 0
        with open(sys.argv[1]) as f:
            for line in f:
                if len(line) > 0 and line[0] in ['0', '1']:
                    self.ram_write(address, int(line[:8], 2))
                    address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        def ADD(a, b): self.reg[a] += self.reg[b]
        def MUL(a, b): self.reg[a] *= self.reg[b]

        alu_opcodes = {
            0b10100000: ADD,
            0b10100010: MUL
        }

        if op in alu_opcodes:
            alu_opcodes[op](reg_a, reg_b)
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        while (op_fn := self.opcodes[(ir := self.ram[self.pc])]) != 'HLT':
            num_args = ir >> 6 # Grab 7th/8th bits
            operand_a = self.ram[self.pc + 1] if num_args > 0 else None
            operand_b = self.ram[self.pc + 2] if num_args > 1 else None
            
            # Skip function call if no-op
            if op_fn != 'NOP':
                # Check if it's an ALU op
                if (ir & 0b00100000) >> 5:
                    self.alu(ir, operand_a, operand_b)
                else:
                    op_fn(operand_a, operand_b)
            # Check if op DOESN'T set PC
            if ((ir & 0b00010000) >> 4) ^ 1: # XOR flips the bit
                self.pc += (num_args + 1)
