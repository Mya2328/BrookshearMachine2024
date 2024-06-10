from django.shortcuts import render
from .brookshear_machine import BrookshearMachine


def index(request):
    if request.method == 'POST':
        instructions = request.POST.get('instructions', '')

        if not instructions:
            return render(request, 'emulator/index.html', {'error': 'Please enter instructions.'})

        # Debugging: Print instructions to check if they're captured correctly
        print(f"Received instructions: {instructions}")

        # Split instructions into 16-bit chunks
        try:
            instructions = [instructions[i:i + 4] for i in range(0, len(instructions), 4)]
            instructions = [int(instr, 16) for instr in instructions]
        except ValueError:
            return render(request, 'emulator/index.html', {'error': 'Invalid hex value provided.'})

        # Initialize the emulator
        bm = BrookshearMachine()

        # Load instructions into memory
        for idx, instruction in enumerate(instructions):
            if idx < 256:
                bm.load_memory(idx, instruction)
            else:
                return render(request, 'emulator/index.html',
                              {'error': 'Too many instructions. Memory limit exceeded.'})

        # Execute the instructions
        pc = 0
        while pc >= 0 and pc < 256:
            instr = bm.fetch(pc)
            if instr is None:
                break
            pc += 1
            new_pc = bm.execute(instr)
            if new_pc is not None:
                pc = new_pc
            if pc == -1:
                break

        # Debugging: Print registers and memory
        print(f"Registers: {bm.registers}")
        print(f"Memory: {bm.memory[:16]}")

        context = {
            'registers': bm.registers,
            'memory': bm.memory[:16],  # Display the first 16 memory locations for simplicity
        }
        return render(request, 'emulator/emulator.html', context)

    return render(request, 'emulator/index.html')
