    LOADI R0, 0x80  ; Start address in memory (0x80)

    ; Row 1: 0111110 -> 0x3E
    LOADI R1, 0x3E
    STORE R1, 0x80  ; Store at memory address 0x80

    ; Row 2: 1000001 -> 0x41
    LOADI R1, 0x41
    STORE R1, 0x81  ; Store at memory address 0x81

    ; Row 3: 1000001 -> 0x41
    LOADI R1, 0x41
    STORE R1, 0x82  ; Store at memory address 0x82

    ; Row 4: 1111111 -> 0x7F
    LOADI R1, 0x7F
    STORE R1, 0x83  ; Store at memory address 0x83

    ; Row 5: 1000001 -> 0x41
    LOADI R1, 0x41
    STORE R1, 0x84  ; Store at memory address 0x84

    ; Row 6: 1000001 -> 0x41
    LOADI R1, 0x41
    STORE R1, 0x85  ; Store at memory address 0x85

    ; Row 7: 1000001 -> 0x41
    LOADI R1, 0x41
    STORE R1, 0x86  ; Store at memory address 0x86

    HALT            ; End of program
