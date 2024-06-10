class BrookshearMachine:
    def __init__(self):
        self.memory = [0] * 256
        self.registers = [0] * 16

    def load_memory(self, address, value):
        if 0 <= address < len(self.memory):
            self.memory[address] = value

    def fetch(self, address):
        if 0 <= address < len(self.memory):
            return self.memory[address]
        return None

    def add_integers(self, rs, rt):
        print(f"Adding registers {rs} and {rt}: {self.registers[rs]} + {self.registers[rt]}")
        self.registers[rs] = (self.registers[rs] + self.registers[rt]) & 0xFFFF
        print(f"Result: {self.registers[rs]}")

    def add_floats(self, rs, rt):
        self.registers[rs] = float(self.registers[rs]) + float(self.registers[rt])

    def or_bits(self, rs, rt):
        self.registers[rs] |= self.registers[rt]

    def and_bits(self, rs, rt):
        self.registers[rs] &= self.registers[rt]

    def xor_bits(self, rs, rt):
        self.registers[rs] ^= self.registers[rt]

    def rotate_right(self, rs, bits):
        bits = bits % 16  # Ensure bits is within 0-15
        self.registers[rs] = (self.registers[rs] >> bits) | ((self.registers[rs] << (16 - bits)) & 0xFFFF)

    def multiply_integers(self, rs, rt):
        print(f"Multiplying registers {rs} and {rt}: {self.registers[rs]} * {self.registers[rt]}")
        self.registers[rs] = (self.registers[rs] * self.registers[rt]) & 0xFFFF
        print(f"Result: {self.registers[rs]}")

    def execute(self, instruction):
        opcode = (instruction >> 12) & 0xF
        rs = (instruction >> 8) & 0xF
        rt = (instruction >> 4) & 0xF
        immediate = instruction & 0xFF

        print(f"Executing instruction: {hex(instruction)}, opcode: {opcode}, rs: {rs}, rt: {rt}, immediate: {immediate}")

        if opcode == 0x0:  # No Operation
            pass
        elif opcode == 0x1:  # Load memory[xy] into Rs
            self.registers[rs] = self.memory[immediate]
        elif opcode == 0x2:  # Load value xy into Rs
            self.registers[rs] = immediate
        elif opcode == 0x3:  # Store Rs in memory[xy]
            self.memory[immediate] = self.registers[rs]
        elif opcode == 0x4:  # Move Rt to Rs
            self.registers[rs] = self.registers[rt]
        elif opcode == 0x5:  # Add as ints Rs, Rt, put result in Rs
            self.add_integers(rs, rt)
        elif opcode == 0x6:  # Add as floats Rs, Rt, put result in Rs
            self.add_floats(rs, rt)
        elif opcode == 0x7:  # OR each bit of Rs, Rt, put result in Rs
            self.or_bits(rs, rt)
        elif opcode == 0x8:  # AND each bit of Rs, Rt, put result in Rs
            self.and_bits(rs, rt)
        elif opcode == 0x9:  # XOR each bit of Rs, Rt, put result in Rs
            self.xor_bits(rs, rt)
        elif opcode == 0xA:  # Rotate Rs x bits right
            self.rotate_right(rs, rt)
        elif opcode == 0xB:  # Jump to xy if Rs equals R0
            if self.registers[rs] == self.registers[0]:
                return immediate  # New program counter
        elif opcode == 0xC:  # Halt
            return -1  # Special value to indicate halt
        elif opcode == 0xD:  # Load memory[Rs] into Rt
            self.registers[rt] = self.memory[self.registers[rs]]
        elif opcode == 0xE:  # Store Rt in memory[Rs]
            self.memory[self.registers[rs]] = self.registers[rt]
        elif opcode == 0xF:  # Conditional jump
            test = (instruction >> 4) & 0xF
            if (test == 0 and self.registers[rs] == self.registers[0]) or \
               (test == 1 and self.registers[rs] != self.registers[0]) or \
               (test == 2 and self.registers[rs] > self.registers[0]) or \
               (test == 3 and self.registers[rs] <= self.registers[0]) or \
               (test == 4 and self.registers[rs] < self.registers[0]) or \
               (test == 5 and self.registers[rs] >= self.registers[0]):
                return immediate  # New program counter
        return None  # Continue execution
