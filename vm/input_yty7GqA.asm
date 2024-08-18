# vmapp/scripts/asm3.py

class Assembler:
    def __init__(self):
        self.memory = [0] * 256  # Example memory size of 256 bytes
        self.registers = [0] * 16  # Example register count of 16
        self.instructions = {
            "NOP": 0x0,
            "LOAD": 0x1,
            "LOADI": 0x2,
            "STORE": 0x3,
            "ADD": 0x4,#MOVE
            "ADDS": 0x5,
            "ADDF": 0x6,
            "OR": 0x7,
            "AND": 0x8,
            "XOR": 0x9,
            "SHR": 0xA,
            "JMP": 0xB,
            "HALT": 0xC,
            "LOADS": 0xD,
            "STORES": 0xE,
            "JUMPT": 0xF,
        }

    def parse_line(self, line):
        parts = line.split()
        instr = parts[0].upper()

        if instr == "NOP":
            return "0x0000"
        elif instr == "HALT":
            return "0xC000"
        elif instr in {"LOAD", "STORE", "LOADI"}:
            r = int(parts[1][1], 16)
            xy = int(parts[2], 16)
            x = (xy & 0xF0) >> 4
            y = xy & 0x0F
            return f"0x{self.instructions[instr]:X}{r:X}{x:X}{y:X}"
        elif instr in {"ADD", "ADDS", "ADDF", "OR", "AND", "XOR"}:
            r = int(parts[1][1], 16)
            s = int(parts[2][1], 16)
            t = int(parts[3][1], 16)
            return f"0x{self.instructions[instr]:X}{r:X}{s:X}{t:X}"
        elif instr == "SHR":
            r = int(parts[1][1], 16)
            x = int(parts[2], 16)
            return f"0x{self.instructions[instr]:X}{r:X}{x:X}0"
        elif instr == "JMP":
            xy = int(parts[1], 16)
            x = (xy & 0xF0) >> 4
            y = xy & 0x0F
            return f"0x{self.instructions[instr]:X}0{x:X}{y:X}"
        elif instr in {"LOADS", "STORES"}:
            r = int(parts[1][1], 16)
            s = int(parts[2][1], 16)
            return f"0x{self.instructions[instr]:X}0{r:X}{s:X}"
        elif instr == "JUMPT":
            t = int(parts[1][1], 16)
            return f"0x{self.instructions[instr]:X}00{t:X}"
        else:
            raise ValueError(f"Unknown instruction: {instr}")

    def assemble(self, asm_code):
        machine_code = []
        lines = asm_code.strip().split('\n')
        for line in lines:
            line = line.strip()
            if line and not line.startswith(';'):  # Skip empty lines and comments
                mc = self.parse_line(line)
                machine_code.append(mc)
        return machine_code

    def save_to_file(self, machine_code, filename):
        with open(filename, 'w') as f:
            for mc in machine_code:
                f.write(mc + '\n')

    def assemble_from_file(self, input_filename, output_filename):
        with open(input_filename, 'r') as f:
            asm_code = f.read()
        machine_code = self.assemble(asm_code)
        self.save_to_file(machine_code, output_filename)

    def reset(self):
        self.memory = [0] * 256
        self.registers = [0] * 16


if __name__ == '__main__':
    # Example usage:
    asm_code = """
    NOP
    LOADI R1, 3
    LOADI R2, 4
    ADD R3, R1, R2
    STORE R3, 31
    LOADI R3, 1
    LOADI R4, 8
    ADD R5, R3, R4
    OR R1, R2, R3
    STORE R1, 32
    AND R4, R5, R6
    STORE R4, 33
    XOR R4, R5, R6
    STORE R4, 34
    SHR R4, 2 
    STORE R4, 35    
    HALT
    """

    assembler = Assembler()
    machine_code = assembler.assemble(asm_code)
    assembler.save_to_file(machine_code, 'output.b')  # Save to current directory

    # Print the assembled machine code to verify
    print(machine_code)
