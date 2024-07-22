# vmapp/scripts/vmonline4.py

from vmapp.scripts.asm3 import Assembler
from icecream import ic

class VirtualMachine:
    def __init__(self, assembler=None):
        self.assembler = assembler if assembler else Assembler()
        self.memory = [0] * 256  # Initialize memory with 256 bytes
        self.registers = [0] * 16  # Initialize 16 registers
        self.program_counter = 0
        self.halted = False
        self.instruction_register = 0
        self.opcode = 0
        self.operands = [0, 0, 0]
        ic(self.memory)

    def load_program_from_file(self, filename):
        with open(filename, 'r') as f:
            lines = f.readlines()
        for i, line in enumerate(lines):
            line = line.strip()
            if i * 2 < len(self.memory):
                self.memory[i * 2] = int(line[:4], 16)
                self.memory[i * 2 + 1] = int(line[4:], 16)
                ic(line)
                ic(self.memory[:40])
                ic(self.registers)

    def fetch(self):
        if self.program_counter >= len(self.memory) - 1:
            self.halted = True
            return 0x0000  # NOP instruction
        instruction1 = self.memory[self.program_counter]
        instruction2 = self.memory[self.program_counter + 1]
        ic(instruction1)
        ic(instruction2)
        self.program_counter += 2
        instruction = (instruction1 << 8) | instruction2
        ic(instruction)
        self.instruction_register = instruction
        return instruction

    def decode_execute(self, instruction):
        ic(instruction)
        self.opcode = (instruction & 0xF000) >> 12
        self.operands = [
            (instruction & 0x0F00) >> 8,
            (instruction & 0x00F0) >> 4,
            instruction & 0x000F
        ]

        opcode = self.opcode
        a, b, c = self.operands

        if opcode == 0x0:
            if instruction == 0x0000:
                pass  # NOP
        elif opcode == 0x1:
            r = a
            x = b
            y = c
            if (x << 4) | y < len(self.memory):
                self.registers[r] = self.memory[(x << 4) | y]
        elif opcode == 0x2:
            r = a
            x = b
            y = c
            self.registers[r] = (x << 4) | y
        elif opcode == 0x3:
            r = a
            x = b
            y = c
            if (x << 4) | y < len(self.memory):
                self.memory[(x << 4) | y] = self.registers[r]
        elif opcode == 0x4:
            r = b
            s = c
            if a == 0x0:
                self.registers[s] = self.registers[r]
            else:
                t = a
                self.registers[t] = self.registers[r] * self.registers[s]
        elif opcode == 0x5:
            r = a
            s = b
            t = c
            self.registers[r] = int(self.registers[s]) + int(self.registers[t])
            self.registers[r] &= 0xFFFF
        elif opcode == 0x6:
            r = a
            s = b
            t = c
            self.registers[r] = float(self.registers[s]) + float(self.registers[t])
        elif opcode == 0x7:
            r = a
            s = b
            t = c
            self.registers[r] = self.registers[s] | self.registers[t]
        elif opcode == 0x8:
            r = a
            s = b
            t = c
            self.registers[r] = self.registers[s] & self.registers[t]
        elif opcode == 0x9:
            r = a
            s = b
            t = c
            self.registers[r] = self.registers[s] ^ self.registers[t]
        elif opcode == 0xA:
            r = a
            x = c
            self.registers[r] >>= x
        elif opcode == 0xB:
            x = b
            y = c
            self.program_counter = (x << 4) | y
        elif opcode == 0xC:
            self.halted = True
        elif opcode == 0xD:
            r = b
            s = c
            if self.registers[s] < len(self.memory):
                self.registers[r] = self.memory[self.registers[s]]
        elif opcode == 0xE:
            r = b
            s = c
            if self.registers[s] < len(self.memory):
                self.memory[self.registers[s]] = self.registers[r]
        elif opcode == 0xF:
            r = a
            x = b
            t = c
            if r == 0x0:
                if self.registers[t] < len(self.memory):
                    self.program_counter = self.memory[self.registers[t]]
            else:
                test_result = False
                if x == 0:
                    if self.registers[r] == self.registers[x]:
                        test_result = True
                elif x == 1:
                    if self.registers[r] != self.registers[x]:
                        test_result = True
                elif x == 2:
                    if self.registers[r] >= self.registers[x]:
                        test_result = True
                elif x == 3:
                    if self.registers[r] <= self.registers[x]:
                        test_result = True
                elif x == 4:
                    if self.registers[r] > self.registers[x]:
                        test_result = True
                elif x == 5:
                    if self.registers[r] == self.registers[x]:
                        test_result = True
                if test_result:
                    if self.registers[t] < len(self.memory):
                        self.program_counter = self.memory[self.registers[t]]

    def step(self):
        if not self.halted:
            instruction = self.fetch()
            ic(instruction)
            self.decode_execute(instruction)
            ic(self.registers)

    def run(self):
        while not self.halted:
            self.step()
        return {"halted": self.halted}

    def reset(self):
        self.assembler.reset()
        self.memory = [0] * 256
        self.registers = [0] * 16
        self.program_counter = 0
        self.halted = False
        self.instruction_register = 0
        self.opcode = 0
        self.operands = [0, 0, 0]

    def get_state(self):
        return {
            'memory': self.memory,
            'registers': self.registers,
            'program_counter': self.program_counter,
            'instruction_register': self.instruction_register,
            'opcode': self.opcode,
            'operands': self.operands,
            'halted': self.halted
        }

# Example usage
if __name__ == '__main__':
    vm = VirtualMachine()
    vm.load_program_from_file('machinecode.m')
    vm.run()

    mem = vm.memory[:132]
    ic(mem)
    ic(vm.registers)
