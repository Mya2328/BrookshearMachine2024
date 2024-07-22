# vmapp/views.py

from django.http import JsonResponse
from django.shortcuts import render
from django.core.files.storage import default_storage
from .scripts.asm3 import Assembler
from .scripts.vmonline4 import VirtualMachine

assembler = Assembler()
vm = VirtualMachine(assembler)

def home(request):
    return render(request, 't1.html')

def call_asm3(request):
    code = request.GET.get('code', """
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
    """)  # Example code
    assembler.assemble(code)
    return JsonResponse({'status': 'assembled', 'memory': assembler.get_memory()})

def call_vmonline4_step(request):
    vm.step()
    return JsonResponse(vm.get_state())

def call_vmonline4_reset(request):
    vm.reset()
    return JsonResponse(vm.get_state())

def call_vmonline4_run(request):
    vm.run()
    return JsonResponse(vm.get_state())

def call_vmonline4_load(request):
    vm.reset()
    vm.load_program_from_file('machinecode.m')
    return JsonResponse(vm.get_state())

def upload_file(request):
    if request.method == 'POST':
        input_file = request.FILES['input_file']
        input_filename = default_storage.save('input.asm', input_file)
        output_filename = 'machinecode.m'

        assembler.assemble_from_file(input_filename, output_filename)

        with open(output_filename, 'r') as f:
            machine_code = f.read()

        return JsonResponse({'status': 'assembled', 'machine_code': machine_code})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
