SECTION .data
	EOL equ 10
	FILLCHR equ 32	; asic space character
	HBARCHR equ 196
	STRTROW equ 2	; Row where the graph begin

; The dataset is just a table of byte-length numbers
	Dataset db	9, 71, 17, 52, 55, 18, 29, 36, 18, 68, 77, 63, 58, 40, 0

	Message db "Data current as of 5/13/2009"
	MSGLEN equ $-Message

; This escape sequence will clear the console terminal and place
; text cursor to the origin (1, 1) on virtually all Linux concolse
	ClrHome db 27, "[2J", 27, "[01;01H"
	CLRLEN equ $-ClrHome

SECTION .bss
	COLS equ 81
	ROWS equ 25
	VidBuff resb COLS*ROWS

SECTION .text
	global _start

; This macro clears the Linux console terminal and sets the cursor position
; to 1,1, using a singe perdefined escape sequence
%macro ClearTerminal 0
	pushad
	mov eax, 4
	mov ebx, 1
	mov ecx, ClrHome
	mov edx, CLRLEN
	int 80H
	popad
%endmacro
	
Show: 
	pushad
	mov eax, 4
	mov ebx, 1
	mov ecx, VidBUff
	mov edx, COLS*ROWS
	int 80H
	popad
	ret
	

_start:
	mov eax, 4
	mov ebx, 1
	mov ecx, ClrHome
	mov edx, CLRLEN
	int 80h

	mov eax, 1
	mov ebx, 0
	int 80H
																

