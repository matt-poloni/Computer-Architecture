LDI R0,Asterisk  ; Address for line of asterisks
LD R0,R0         ; Switch to actual asterisk character
LDI R1,0         ; Number of asterisks printed
LDI R2,1         ; Number of asterisks to print on the line
LDI R3,64        ; Max asterisks to print on a line
LDI R4,StartLoop ; Address for StartLoop
StartLoop:
PRA R0           ; Print asterisk
INC R1           ; Increment number of asterisks
CMP R1,R2        ; Compare asterisks printed to those needed
JNE R4           ; JUMP BACK to print if not equal
LDI R1,0         ; Reset printed asterisks
LDI R0,Newline   ; Point to newline address
LD R0,R0         ; Switch to actual newline character
PRA R0           ; Print newline
LDI R0,Asterisk  ; Point back to asterisk
LD R0,R0         ; Switch back to actual asterisk character
ADD R2,R2        ; Double the num to print on the next line
CMP R2,R3        ; Compare to max num of asterisks per line
JLE R4           ; JUMP BACK to print if less than or equal
HLT
Asterisk:
db 42            ; ASCII asterisk
Newline:
db 10            ; ASCII newline
