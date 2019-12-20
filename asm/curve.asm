LDI R0,42 ; ASCII code for asterisk
LDI R1,0  ; Running total of line's printed asterisks
LDI R2,1  ; Number of asterisks to print on the line
LDI R3,64 ; Max asterisks to print
LDI R4,15 ; Return address for loop
PRN R2    ; Print asterisk
INC R1    ; Increment printed asterisks
CMP R1,R2 ; Compared printed total to number to print
JNE R4    ; Jump back to print if not equal
LDI R1,0  ; Reset printed total to zero
ADD R2,R2 ; Double the number to print on the next line
CMP R2,R3 ; Compare to max number of asterisks per line
JLE R4    ; Jump back to print new line if less than or equal
HLT       ; End program
