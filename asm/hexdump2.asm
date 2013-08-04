; Executable name	: hexdump2
; Version			: 1.0
; Build using tese commands:
; 	nasm -f elf -g -F stabs hexdump2.asm
; 	ld -o hexdump2.exe hexdump2.o

SECTION .data
	TRASTABLE:
		db "0123456789ABCDEF"

SECTION .bss
	BUFFLEN EQU 10
	Buff resb BUFFLEN

	OUTBUFLEN EQU 10
	OutBuff resb OUTBUFLEN

SECTION .text
	GLOBAL _start

_start:
	nop
	nop
ReadOneChar:
	mov eax, 3
	mov ebx, 0
	mov ecx, Buff
	mov edx, 1
	int 80H
	cmp eax, 0
	je done

PrintHex:
	mov bl, byte [Buff]
	and bx, 000000F0H
	shr bx, 4
	mov cl, byte [TRASTABLE + ebx]
	mov byte [OutBuff], cl
	mov bl, byte [Buff]
	and bx, 0000000FH
	mov cl, byte [TRASTABLE + ebx]
	mov byte [OutBuff + 1], cl
	mov eax, 4
	mov ebx, 1
	mov ecx, OutBuff
	mov edx, 2
	int 80H
	jmp ReadOneChar

done:
	mov eax, 1
	mov ebx, 0
	int 80H
	
