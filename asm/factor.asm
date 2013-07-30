SECTION .bss
	BuffIn resb 1
	BuffOut resb 1

SECTION .data
	HexStr: db "hello", 10

SECTION .text

global _start

_start:
	nop
	mov eax, 3
	mov ebx, 0
	mov ecx, BuffIn 
	mov edx, 1
	int 80h

	mov al, byte [BuffIn]
	mov bl, byte [BuffIn]

DoMul:
	mul bl
	sub bl, 1
	jnz DoMul
	mov byte [BuffOut], al

Write:
	mov eax, 4
	mov ebx, 1
	mov ecx, BuffOut
	mov edx, 1
	int 80h
	
	mov eax, 1
	mov ebx, 0
	int 80H

