LDI R0,Line ; Address for line of asterisks
LDI R1,0    ; Number of asterisks printed
LDI R2,1    ; Number of asterisks to print on the line
LDI R3,64   ; Max asterisks to print on a line
LDI R4,Loop ; Address for Loop
CALL R4     ; Call Loop
HLT
Loop:
PRA R0      ; Print asterisk
INC R1      ; Increment number of asterisks
CMP R1,R2   ; Compare asterisks printed to those needed
JNE R4      ; Jump back to print if not equal
INC R0      ; Point to newline
PRA R0      ; Print newline
DEC R0      ; Point back to asterisk
ADD R2,R2   ; Double the number to print on the next line
CMP R2,R3   ; Compare to max number of asterisks per line
JLE R4      ; Jump back to print new line if <=
RET         ; Return from subroutine
Line:
db 42       ; ASCII asterisk
db 10       ; ASCII newline
