SECTION .bss
	BUFFLEN equ 16
	Buff:	resb BUFFLEN
SECTION .data
	HexStr: db "hello", 10

SECTION .text

global _start

_start:
	nop
	mov eax, 4
	mov ebx, 1
	mov ecx, HexStr
	mov edx, 5
	int 80H
	
	mov eax, 1
	mov ebx, 0
	int 80H

