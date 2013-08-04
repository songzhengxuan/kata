; Executable name	: hexdump2
; Version			: 1.0
; Build using tese commands:
; 	nasm -f elf -g -F stabs hexdump2.asm
; 	ld -o hexdump2.exe hexdump2.o

SECTION .data
	TestIn: db "0123456789abcdefa test input for long"
	TestInLen: equ $-TestIn

	HexValueTable: db "0123456789abcdef"
	TRASTABLE: db "0123456789ABCDEF"
	ASICOUT: db "|................|",10
	HEXOUT: db "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 "
	ASIC_TAB:
db 2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,09h,0ah,2Eh,2Eh,2Eh,2Eh,2Eh
db 2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh
db 20h,21h,22h,23h,24h,25h,26h,27h,28h,29h,2ah,2bh,2ch,2dh,2eh,2fh
db 30h,31h,32h,33h,34h,35h,36h,37h,38h,39h,3ah,3bh,3ch,3dh,3eh,3fh
db 40h,41h,42h,43h,44h,45h,46h,47h,48h,49h,4ah,4bh,4ch,4dh,4eh,4fh
db 50h,51h,52h,53h,54h,55h,56h,57h,58h,59h,5ah,5bh,5ch,5dh,5eh,5fh
db 60h,61h,62h,63h,64h,65h,66h,67h,68h,69h,6ah,6bh,6ch,6dh,6eh,6fh
db 70h,71h,72h,73h,74h,75h,76h,77h,78h,79h,7ah,7bh,7ch,7dh,7eh,2Eh
db 2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh
db 2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh
db 2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh
db 2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh
db 2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh
db 2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh
db 2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh
db 2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh,2Eh
	

SECTION .bss
	ASICBUFLEN EQU 19
	AsicOutBuf resb ASICBUFLEN 

	HEXOUTBUFLEN EQU 48
	HexOutBuff resb HEXOUTBUFLEN 

	TmpChar resb 1

SECTION .text

clear_line:
	push cx
	push ebx
	mov cx, 48
	mov ebx, 47
fill_one_hex:
	mov al, byte [HEXOUT + ebx]
	mov byte [HexOutBuff + ebx], al
	dec ebx
	loop fill_one_hex
	mov cx, 19
	mov ebx, 18
fill_one_asic:
	mov al, byte [ASICOUT + ebx]
	mov byte [AsicOutBuf + ebx], al
	dec ebx
	loop fill_one_asic
	pop ebx
	pop cx
	ret

print_line:
	pushad
	mov eax, 4
	mov ebx, 1
	mov ecx, HexOutBuff
	mov edx, HEXOUTBUFLEN
	int 80H
	mov eax, 4
	mov ebx, 1
	mov ecx, AsicOutBuf 
	mov edx, ASICBUFLEN 
	int 80H
	popad
	ret


	GLOBAL _start
_start:
	nop
	nop
	call clear_line
	mov ecx, 0
	mov edx, 16
	mov esi, TestIn
	mov edi, AsicOutBuf
	add edi, 1
	mov ebp, HexOutBuff
convert_a_char:
; remember the current char 
	mov al, byte [esi + ecx]
	mov byte [edi + ecx], al
	mov byte [TmpChar], al
	and eax, 0f0H
	shr eax, 4
	mov bl, byte [HexValueTable + eax]
	mov byte [ebp], bl
	inc ebp 
	mov al, byte [TmpChar]
	and eax, 0fH
	mov bl, byte [HexValueTable + eax]
	mov byte [ebp], bl
	add ebp, 2
; inc the ecx value to convert next char
	inc ecx
	cmp ecx, edx
	jl convert_a_char
	call print_line

done:
	mov eax, 1
	mov ebx, 0
	int 80H
	
