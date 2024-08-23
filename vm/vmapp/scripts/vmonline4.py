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
        #ic(self.memory)

    def load_program_from_file(self, filename):
        with open(filename, 'r') as f:
            lines = f.readlines()
        for i, line in enumerate(lines):
            line = line.strip() #remove \n
            if i * 2 < len(self.memory): #check if memory still available (80)
                self.memory[i * 2] = int(line[2:4], 16)   # first two hex, omit 0x
                self.memory[i * 2 + 1] = int(line[4:], 16) # second two hex
                # ic(line)
                # ic(line[2:4])
                # ic(line[4:])
                #ic(self.memory[i * 2])
                # ic(self.memory[i * 2+1])
                # ic(self.registers)

    def fetch(self):
        if self.program_counter >= len(self.memory) - 1: #check memory boundary
            self.halted = True
            return 0x0000  # NOP instruction
        instruction1 = self.memory[self.program_counter]
        instruction2 = self.memory[self.program_counter + 1]
        ic(instruction1)
        ic(instruction2)
        self.program_counter += 2                                               # PC increment to two bytes
        instruction = (instruction1 << 8) | instruction2                 # adding two 8 bits to be 16 bits instruction
        ic(instruction)
        self.instruction_register = instruction
        return instruction

    def decode_execute(self, instruction):
        ic(instruction)
        self.opcode = (instruction & 0xF000) >> 12
        self.operands = [
            (instruction & 0x0F00) >> 8,                            #decode and exe
            (instruction & 0x00F0) >> 4,
            instruction & 0x000F
        ]

        opcode = self.opcode
        a, b, c = self.operands

        if opcode == 0x0:                   # 0FFF No Operation
            if instruction == 0x0000:
                pass  # NOP

        elif opcode == 0x1:                # 1rxy
            r = a
            x = b
            y = c
            if (x << 4) | y < len(self.memory):
                self.registers[r] = self.memory[(x << 4) | y]
        elif opcode == 0x2:                                     #load xy value to r
            r = a
            x = b
            y = c
            self.registers[r] = (x << 4) | y
        elif opcode == 0x3:                                     #store r in memory xy
            r = a
            x = b
            y = c
            if (x << 4) | y < len(self.memory):
                self.memory[(x << 4) | y] = self.registers[r]

        elif opcode == 0x4:                                             # 40rs - Move Rr to Rs
            r = b
            s = c
            if a == 0x0:
                self.registers[s] = self.registers[r]
                # self.register[r] = 0                                  # if want to move , use it, else want to copy , omit it
            else:                                                             # 4trs -  Rt = Rr * Rs
                t = a
                self.registers[t] = self.registers[r] * self.registers[s]
        elif opcode == 0x5:                                             # add values from register[s] and register[t] as integers and store on register[r]
            r = a
            s = b
            t = c
            self.registers[r] = int(self.registers[s]) + int(self.registers[t])
            self.registers[r] &= 0xFFFF

        # Need to FIX ****
        elif opcode == 0x6:                                             # !not fixed - add values from register[s] and register[t] as floats and store(not fixed yet)
            r = a
            s = b
            t = c
            self.registers[r] = float(self.registers[s]) + float(self.registers[t])
        elif opcode == 0x7:                                             # OR operation with R[s] and R[t] then store in R[r]
            r = a
            s = b
            t = c
            self.registers[r] = self.registers[s] | self.registers[t]
        elif opcode == 0x8:                                              # AND operation with R[s] and R[t] then store in R[r]
            r = a
            s = b
            t = c
            self.registers[r] = self.registers[s] & self.registers[t]
        elif opcode == 0x9:                                              # XOR operation with R[s] and R[t] then store in R[r]
            r = a
            s = b
            t = c
            self.registers[r] = self.registers[s] ^ self.registers[t]
        elif opcode == 0xA:                                             # Rotate R[r] x bits right - need to ask
            r = a
            x = c
            self.registers[r] >>= x
        elif opcode == 0xB:                                             # Jump to xy if R[r] == R[0] - need to ask
            x = b
            y = c
            self.program_counter = (x << 4) | y
        elif opcode == 0xC:                                             # Stop or Halt
            self.halted = True
        elif opcode == 0xD:                                             # Load memory[Rs] into R[r] - attention to []
            r = b
            s = c
            if self.registers[s] < len(self.memory):
                self.registers[r] = self.memory[self.registers[s]]
        elif opcode == 0xE:                                             # Store R[r] in memory[Rs]
            r = b
            s = c
            if self.registers[s] < len(self.memory):
                self.memory[self.registers[s]] = self.registers[r]
        elif opcode == 0xF:                                             # Jump to address in R[t] according to R[r] and R[0]
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
            #ic(instruction)
            self.decode_execute(instruction)
            #ic(self.registers)

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
        self.decoded_instruction = ''

    def get_state(self):
        memory_state = []
        instruction_list = []
        for address in range(0, len(self.memory), 2):
            # only even instruction should show decoded instruction
            # odd instruction should omit it
            if self.program_counter % 2 == 0:
                instruction = (self.memory[address] << 8) | self.memory[address + 1]  # Combine two bytes into an instruction
                self.decoded_instruction = self.decode_instruction(instruction)  # Assuming you have a decode function    
            else:
                self.decoded_instruction = 'N/A'
            
            instruction_list.append(self.decoded_instruction)

            #ic(self.decoded_instruction)
            memory_state.append({
                'address': address // 2,
                'binaryvalue': format(instruction, '016b'),
                'hexvalue': format(instruction, '04x'),
                'ascii': chr(instruction & 0xFF) if 32 <= (instruction & 0xFF) <= 126 else '.',
                'integervalue': instruction,
                'floatvalue': float(instruction),  # If you have special float handling, adjust this
                'instruction': self.decoded_instruction,
                'memory':self.memory
            })

        return {
            'memory': self.memory,            
            'registers': self.registers,
            'program_counter': self.program_counter,
            'instruction_register': self.instruction_register,
            'opcode': self.opcode,
            'operands': self.operands,
            'halted': self.halted,
            'decoded_instruction': instruction_list
        }
    
    def decode_instruction(self, instruction):
        # Extracting fields from the instruction
        opcode = (instruction & 0xF000) >> 12
        r = (instruction & 0x0F00) >> 8
        x_or_s = (instruction & 0x00F0) >> 4
        y_or_t = (instruction & 0x000F)

        if instruction == 0x0FFF:
            return "NOP"
        elif opcode == 0x1:
            return f"Load memory[{x_or_s:02X}{y_or_t:02X}] into R{r}"
        elif opcode == 0x2:
            return f"Load value {x_or_s:02X}{y_or_t:02X} into R{r}"
        elif opcode == 0x3:
            return f"Store R{r} in memory[{x_or_s:02X}{y_or_t:02X}]"
        elif opcode == 0x4:
            return f"Move R{x_or_s} to R{r}"
        elif opcode == 0x5:
            return f"Add as ints R{x_or_s}, R{y_or_t}, put result in R{r}"
        elif opcode == 0x6:
            return f"Add as floats R{x_or_s}, R{y_or_t}, put result in R{r}"
        elif opcode == 0x7:
            return f"OR each bit of R{x_or_s}, R{y_or_t}, put result in R{r}"
        elif opcode == 0x8:
            return f"AND each bit of R{x_or_s}, R{y_or_t}, put result in R{r}"
        elif opcode == 0x9:
            return f"XOR each bit of R{x_or_s}, R{y_or_t}, put result in R{r}"
        elif opcode == 0xA:
            return f"Rotate R{x_or_s} {y_or_t} bits right"
        elif opcode == 0xB:
            return f"Jump to {x_or_s:02X}{y_or_t:02X} if R{r} equals R0"
        elif instruction == 0xC000:
            return "Halt"
        elif opcode == 0xD:
            return f"Load memory [R{y_or_t}] into R{r}"
        elif opcode == 0xE:
            return f"Store R{r} in memory [R{y_or_t}]"
        elif opcode == 0xF:
            condition_map = {
                0: "equals",
                1: "not equals",
                2: "greater or equal",
                3: "less or equal",
                4: "greater than",
                5: "less than"
            }
            condition = condition_map.get(x_or_s, "unknown")
            return f"Jump to address in R{y_or_t} if R{r} test R0 is {condition}"
        else:
            return "Unknown Instruction"


# Example usage
if __name__ == '__main__':
    vm = VirtualMachine()
    vm.load_program_from_file('machinecode.m')
    vm.run()

    mem = vm.memory[:132]
    #ic(mem)
    #ic(vm.registers)
