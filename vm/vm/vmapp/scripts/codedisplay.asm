    LOADI R0, 0x80  ; Start address in memory (0x80)

    ; Row 1: 01111110 -> 0x7E
    LOADI R1, 0x7E
    STORE R1, 0x80  ; Store at memory address 0x80

    ; Row 2: 10000001 -> 0x81
    LOADI R1, 0x81
    STORE R1, 0x81  ; Store at memory address 0x81

    ; Row 3: 10000001 -> 0x81
    LOADI R1, 0x81
    STORE R1, 0x82  ; Store at memory address 0x82

    ; Row 4: 11111111 -> 0xFF
    LOADI R1, 0xFF
    STORE R1, 0x83  ; Store at memory address 0x83

    ; Row 5: 10000001 -> 0x81
    LOADI R1, 0x81
    STORE R1, 0x84  ; Store at memory address 0x84

    ; Row 6: 10000001 -> 0x81
    LOADI R1, 0x81
    STORE R1, 0x85  ; Store at memory address 0x85

    ; Row 7: 10000001 -> 0x81
    LOADI R1, 0x81
    STORE R1, 0x86  ; Store at memory address 0x86

    HALT             ; End of program
