section .data
	EndLine db "------------",10
	ONELINELEN equ $-EndLine
	MiddleLine db "1----------1",10

section .bss
	LineBuf resb 13
	Plate resb 200

section .text
	global _start

clearPlate:
	cld
	pushad
	mov al, ' '
	mov ecx, 200
	mov edi, Plate
	rep stosb
	popad
	ret

printPlate:
	pushad
	; add the first line
	mov ecx, ONELINELEN
	mov esi, EndLine
	mov edi, LineBuf
	rep movsb
	call printLineBuf
	;
	; print the middle 20 lines
	mov ebx, 20
	cld
	mov esi, Plate
printOneMiddleLine:
	mov al, '1'
	mov edi, LineBuf
	stosb
	mov ecx, 10
	rep movsb
	mov al, '1'
	stosb
	call printLineBuf
	sub ebx, 1
	jnz printOneMiddleLine
	; add the end line
	mov ecx, ONELINELEN
	mov esi, EndLine
	mov edi, LineBuf
	rep movsb
	call printLineBuf
	popad
	ret

printLineBuf:
	pushad
	; do the real print
	mov eax, 4
	mov ebx, 1
	mov ecx, LineBuf 
	mov edx, ONELINELEN 
	int 80h
	popad
	ret
	

_start:
	nop
	call clearPlate
	call printPlate

quit:
	mov eax, 1
	mov ebx, 0
	int 80h
