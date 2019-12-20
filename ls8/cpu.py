"""CPU functionality."""
import sys
from datetime import datetime

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 0x100 # 256 in hex
        self.reg = [0] * 0b1000 # 8 in binary
        SP = 0b111 # 7 in binary
        self.reg[SP] = 0xF4 # 244 in hex
        IS = 0b110 # 6 in binary
        IM = 0b101 # 5 in binary
        self.pc = 0
        self.fl = 0

        def LDI(a, b):
            self.reg[a] = b
        def PRN(a, b):
            print(self.reg[a])
        def PRA(a, b):
            print(chr(self.reg[a]), end="")
        def PUSH(a, b):
            self.reg[SP] -= 1
            self.ram[self.reg[SP]] = self.reg[a]
        def POP(a, b):
            self.reg[a] = self.ram[self.reg[SP]]
            self.reg[SP] += 1
        def CALL(a, b):
            self.reg[SP] -= 1
            self.ram[self.reg[SP]] = self.pc + 2
            JMP(a, b)
        def RET(a, b):
            self.pc = self.ram[self.reg[SP]]
            self.reg[SP] += 1
        def ST(a, b):
            self.ram[self.reg[a]] = self.reg[b]
        def LD(a, b):
            self.reg[a] = self.ram[self.reg[b]]
        def JMP(a, b):
            self.pc = self.reg[a]
        def JEQ(a, b):
            if (self.fl & 1): JMP(a, b)
            else: self.pc += 2
        def JNE(a, b):
            if (self.fl & 1) ^ 1: JMP(a, b)
            else: self.pc += 2
        def JLE(a, b):
            if (self.fl & 0b101): JMP(a, b)
            else: self.pc += 2

        self.ops = {
            0b00000000: 'NOP',
            0b00000001: 'HLT',
            0b10000010: LDI,
            0b01000111: PRN,
            0b01001000: PRA,
            0b01000101: PUSH,
            0b01000110: POP,
            0b01010000: CALL,
            0b00010001: RET,
            0b10000100: ST,
            0b10000011: LD,
            0b01010100: JMP,
            0b01010101: JEQ,
            0b01010110: JNE,
            0b01011001: JLE
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
        def ADD(a, b):
            self.reg[a] += self.reg[b]
        def INC(a, b):
            self.reg[a] += 1
        def DEC(a, b):
            self.reg[a] -= 1
        def MUL(a, b):
            self.reg[a] *= self.reg[b]
        def CMP(a, b):
            val_a = self.reg[a]
            val_b = self.reg[b]
            if val_a < val_b: self.fl = 0b100
            elif val_a > val_b: self.fl = 0b10
            else: self.fl = 1
        def AND(a, b):
            self.reg[a] &= self.reg[b]
        def OR(a, b):
            self.reg[a] |= self.reg[b]
        def XOR(a, b):
            self.reg[a] ^= self.reg[b]
        def NOT(a, b):
            self.reg[a] = ~self.reg[a]
        def SHL(a, b):
            self.reg[a] <<= self.reg[b]
        def SHR(a, b):
            self.reg[a] >>= self.reg[b]
        def MOD(a, b):
            if b == 0: raise Exception("Cannot divide by 0")
            self.reg[a] %= self.reg[b]

        alu_opcodes = {
            0b10100000: ADD,
            0b01100101: INC,
            0b01100110: DEC,
            0b10100010: MUL,
            0b10100111: CMP,
            0b10101000: AND,
            0b10101010: OR,
            0b10101011: XOR,
            0b01101001: NOT,
            0b10101100: SHL,
            0b10101101: SHR,
            0b10100100: MOD
        }

        if op in alu_opcodes:
            alu_opcodes[op](reg_a, reg_b)
        else:
            raise Exception(f"{hex(op)} is not a supported ALU operation")

    def opcodes(self, op):
        if op in self.ops: return self.ops[op]
        # If it's supposed to be an ALU op, send it there
        elif (op & 0b00100000) >> 5:
            return lambda a, b: self.alu(op, a, b)
        else:
            raise Exception(f"{hex(op)} is not a supported operation")

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
        while (op_fn := self.opcodes(ir := self.ram[self.pc])) != 'HLT':
            num_args = ir >> 6 # Grab 7th/8th bits
            operand_a = self.ram[self.pc + 1] if num_args > 0 else None
            operand_b = self.ram[self.pc + 2] if num_args > 1 else None
            
            # Skip function call if no-op
            if op_fn != 'NOP':
                op_fn(operand_a, operand_b)
            # Check if op DOESN'T set PC
            if ((ir & 0b00010000) >> 4) ^ 1: # XOR against 1 flips the bit
                self.pc += (num_args + 1)
