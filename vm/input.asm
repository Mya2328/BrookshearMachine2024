; Clear display memory (0x80 to 0xFF)
LOADI R1, 80    ; Start address of display memory
LOADI R2, 0     ; Value to clear

CLEAR_LOOP:
STORE R2, R1    ; Clear memory at R1
ADD R1, R1, 1   ; Increment address
LOADI R3, FF    ; Load upper bound address
CMP R1, R3      ; Compare current address with upper bound
JLT CLEAR_LOOP  ; Jump to CLEAR_LOOP if R1 < FF

; Draw letter 'A' in a 10x10 grid
; Top horizontal line
LOADI R1, 88    ; Address 0x88
LOADI R2, 7E    ; 01111110 (top line of 'A')
STORE R2, R1    ; Store the line

; Next line
LOADI R1, 8A    ; Address 0x8A
LOADI R2, 81    ; 10000001
STORE R2, R1    ; Store the line

; Next line
LOADI R1, 8C    ; Address 0x8C
LOADI R2, 81    ; 10000001
STORE R2, R1    ; Store the line

; Next line (middle horizontal line)
LOADI R1, 8E    ; Address 0x8E
LOADI R2, FF    ; 11111111
STORE R2, R1    ; Store the line

; Next line
LOADI R1, 90    ; Address 0x90
LOADI R2, 81    ; 10000001
STORE R2, R1    ; Store the line

; Next line
LOADI R1, 92    ; Address 0x92
LOADI R2, 81    ; 10000001
STORE R2, R1    ; Store the line

; Next line
LOADI R1, 94    ; Address 0x94
LOADI R2, 81    ; 10000001
STORE R2, R1    ; Store the line

; Halt the program
HALT
