    LOADI R0, 0x80  ; Start address in memory (0x80)

    ; Row 1: 01111110 -> 0x7E
    LOADI R1, 0x18
    STORE R1, 0x80  ; Store at memory address 0x80
    LOADI R1, 0x3C
    STORE R1, 0x84  ; Store at memory address 0x80
    LOADI R1, 0x66
    STORE R1, 0x88  ; Store at memory address 0x80
    LOADI R1, 0x7E
    STORE R1, 0x8C  ; Store at memory address 0x80
    LOADI R1, 0x42
    STORE R1, 0x90  ; Store at memory address 0x80   

    LOADI R1, 0x7C
    STORE R1, 0x98  ; Store at memory address 0x80
    LOADI R1, 0x42
    STORE R1, 0x9C  ; Store at memory address 0x80
    LOADI R1, 0x7E
    STORE R1, 0xA0  ; Store at memory address 0x80
    LOADI R1, 0x7E
    STORE R1, 0xA4  ; Store at memory address 0x80
    LOADI R1, 0x42
    STORE R1, 0xA8  ; Store at memory address 0x80  
    LOADI R1, 0x7C
    STORE R1, 0xAC  ; Store at memory address 0x80 

    LOADI R1, 0x7C
    STORE R1, 0xB4  ; Store at memory address 0x80
    LOADI R1, 0x40
    STORE R1, 0xB8  ; Store at memory address 0x80
    LOADI R1, 0x40
    STORE R1, 0xBC  ; Store at memory address 0x80
    LOADI R1, 0x40
    STORE R1, 0xC0  ; Store at memory address 0x80
    LOADI R1, 0x40
    STORE R1, 0xC4  ; Store at memory address 0x80  
    LOADI R1, 0x7C
    STORE R1, 0xC8  ; Store at memory address 0x80  

    HALT             ; End of program
