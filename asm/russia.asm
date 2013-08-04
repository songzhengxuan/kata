section .data
	ClrHome db 27,"[2J", 27, "[01;01H"
	CLRLEN equ $-ClrHome
	EndLine db "------------",10
	ONELINELEN equ $-EndLine
	MiddleLine db "1----------1",10

section .bss
	LineBuf resb 13
	Plate resb 200
	PosX resb 1
	PosY resb 1
	UserInput resb 1

section .text
	global _start

initPos:
	mov byte [PosX], 0
	mov byte [PosY], 0
	ret

updatePos:
	mov eax, 3
	mov ebx, 0
	mov ecx, UserInput
	mov edx, 1
	int 80h
	mov al, byte [UserInput]
	cmp al, 'w'
	je .decY
	cmp al, 's'
	je .incY
	cmp al, 'a'
	je .decX
	cmp al, 'd'
	je .incX
	cmp al, 'q'
	jmp quit
.incX:
	mov al, byte [PosX]
	cmp al, 9
	jae .endUpdatePos
	add al, 1
	mov byte [PosX], al
	jmp .endUpdatePos
.decX:
	mov al, byte [PosX]
	cmp al, 0
	je .endUpdatePos
	sub al, 1
	mov byte [PosX], al
	jmp .endUpdatePos
.incY:
	mov al, byte [PosY]
	cmp al, 19
	jae .endUpdatePos
	add al, 1
	mov byte [PosY], al
	jmp .endUpdatePos
.decY:
	mov al, byte [PosY]
	cmp al, 0
	je .endUpdatePos
	sub al, 1
	mov byte [PosY], al
	jmp .endUpdatePos
.endUpdatePos:
	ret

updatePlate:
	call clearPlate
	xor eax, eax
	mov al, 10
	mov ah, byte [PosY]
	mul ah
	add al, byte [PosX]
	adc ah, 0
	mov byte [Plate + eax], '*'
	ret

clearScreen:
	pushad
	mov eax, 4
	mov ebx, 1
	mov ecx, ClrHome
	mov edx, CLRLEN
	int 80h
	popad
	ret

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
	call clearScreen
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
	call initPos
refresh:
	call updatePos 
	call updatePlate
	call printPlate
	jmp refresh

quit:
	mov eax, 1
	mov ebx, 0
	int 80h
