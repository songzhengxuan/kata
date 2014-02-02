section .data
	ClrHome db 27,"[2J", 27, "[01;01H"
	CLRLEN equ $-ClrHome
	EndLine db "------------",10
	ONELINELEN equ $-EndLine
	MiddleLine db "1----------1",10
	;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
	;; shapes
	;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
	Shapes:
	dw 17476,17476,17476,17476
	dw 1632,1632,1632,1632
	dw 56088,9792,56088,9792
	dw 19668,17984,3648,19520

	;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
	;; end of shapes
	;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
	
	;;;;;;;;;;;;;;;;;;;;;;;;;;;;
	;;;;;  termial control 
	;;;;;;;;;;;;;;;;;;;;;;;;;;;;
	termios: times 36 db 0
	stdin: equ 0
	ICANON: equ 1<<1
	ECHO: equ 1<<3


section .bss
	LineBuf resb 13
	Plate resb 200
	FixedSet resb 200
	PosX resb 1
	PosY resb 1
	PosXBuf resb 1
	PosYBuf resb 1
	UserInput resb 1
	ShapeBuf resb 16
	CurrentShape resb 1
	CurrentRotate resb 1

section .text
	global _start

initPos:
	mov byte [PosX], 0
	mov byte [PosY], 0
	ret

updatePos:
	pushad
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
	jmp .endUpdatePos
.incX:
	mov al, byte [PosX]
	;cmp al, 9
	;jae .endUpdatePos
	add al, 1
	mov byte [PosX], al
	jmp .endUpdatePos
.decX:
	mov al, byte [PosX]
	;cmp al, 0
	;je .endUpdatePos
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
	popad
	ret

;;;;;;;;;;;;;;
;; Parameter in:
;;	ah: shape index
;;	al: shape rotate
;;	bh: shape matrix x
;;	bl: shape matrix y
;;	ecx: out buf
getShapePosition:
	pushad
	push edi

	mov edi, ecx; save the dest addr to edi
	mov dx, ax ; first save ax
	xor eax, eax
	mov al, dh
	shl ax, 3 ; each shape contains 4 one word description
	add al, dl
	adc ah, 0
	add al, dl
	adc ah, 0
	mov ax, word [Shapes + eax] ;; fetch the shape description into ax
	mov ecx, 0
.checkOneBit:
	rcl ax, 1
	jnc .continue
	push bx
	mov edx, ecx
	and edx, 3h
	add bh, dl
	mov edx, ecx
	shr edx, 2
	add bl, dl
	mov byte [edi], bh
	inc edi
	mov byte [edi], bl
	inc edi
	pop bx
.continue:
	inc ecx
	cmp ecx, 16
	jb .checkOneBit

	pop edi
	popad
	ret

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; call this to save the current position to buf
saveCurrentPosition:
	push ax
	mov al, byte [PosX]
	mov byte [PosXBuf], al
	mov al, byte [PosY]
	mov byte [PosYBuf], al
	pop ax
	ret

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; call this to restore the current position to buf
restoreCurrentPosition:
	push ax
	mov al, byte [PosXBuf]
	mov byte [PosX], al
	mov al, byte [PosYBuf]
	mov byte [PosY], al
	ret

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; call this to check if the parameter positions is valid 
;; in $ecx: the shapebuf contains 4 point position
;; out $al: return 0 if the result is valid
;;			return 1 if the result is invalid but current shape is still
;;			return -1 if the result is invlaid and need generate next
checkShapeValidity:
	ret


;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; clear the fixed set 
clearFixedSet:
	pushad
	cld
	mov al, ' '
	mov ecx, 200
	mov edi, FixedSet
	rep stosb
	popad
	ret

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; call four pshapes pointed by ecx to fixed set
addShapeToFixedSet:
	pushad
	mov esi, ecx ;; move the input buf into esi
	mov ecx, 4 ;; ecx use as count register now
.addOnePoint:
	xor eax, eax
	mov ah, 10
	mov al, byte [esi + 2 * ecx - 1]
	mul ah
	add al, byte [esi + 2 * ecx - 2]
	mov byte [FixedSet + eax], '*'
	sub ecx, 1
	jnz .addOnePoint
	popad
	ret

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; draw the fixed set to the plate
paintFixedSetToPlate:
	pushad 
	cld
	mov ecx, 200
.testOneFixed:
	mov al, byte [FixedSet + ecx - 1]
	cmp al, '*'
	jne .testContinue
	mov byte [Plate + ecx -1], '*'
.testContinue:
	sub ecx, 1
	jnz .testOneFixed
	popad
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

clearTerminalScreen:
	pushad
	mov eax, 4
	mov ebx, 1
	mov ecx, ClrHome
	mov edx, CLRLEN
	int 80h
	popad
	ret

clearPlate:
	pushad
	cld
	mov al, ' '
	mov ecx, 200
	mov edi, Plate
	rep stosb
	popad
	ret


stubforbreak:
	pushad
	popad
	ret

; update the shape stored in CX to plate
updateShapeToPlate:
	pushad
	mov ebx, 0
.updateOneShapePos:
	mov al, byte [ecx + 1] ; +1 is the Y position
	mov ah, 10
	mul ah
	mov dl, byte [ecx]
	add al, dl
	mov byte [Plate + eax], '*'
	add ecx, 2
	inc ebx
	cmp ebx, 4
	jne .updateOneShapePos
	popad
	ret

paintPlate:
	pushad
	call clearTerminalScreen
	; add the first line
	mov ecx, ONELINELEN
	mov esi, EndLine
	mov edi, LineBuf
	rep movsb
	call printLineBuf
	; print the middle 20 lines
	mov ebx, 20
	cld
	call paintFixedSetToPlate
	mov esi, Plate
printOneMiddleLine:
	mov al, '1' ;; print the left bound
	mov edi, LineBuf
	stosb
	mov ecx, 10
	rep movsb
	mov al, '1' ;; print the right bound
	stosb
	call printLineBuf
	sub ebx, 1
	jnz printOneMiddleLine
	; print the end line
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

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; terminal control procedure
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

read_stdin_termios:
	push eax
	push ebx
	push ecx
	push edx

	mov eax, 36h
	mov ebx, stdin
	mov ecx, 5401h
	mov edx, termios
	int 80h

	pop edx
	pop ecx
	pop ebx
	pop eax
	ret

write_stdin_termios:
	push eax
	push ebx
	push ecx
	push edx

	mov eax, 36h
	mov ebx, stdin
	mov ecx, 5402h
	mov edx, termios
	int 80h

	pop edx
	pop ecx
	pop ebx
	pop eax
	ret

canonical_off:
	call read_stdin_termios

	; clear canonical bit in local mode flags
	push eax
	mov eax, ICANON
	not eax
	and [termios+12], eax
	pop eax

	call write_stdin_termios
	ret

echo_off:
	call read_stdin_termios
	; clear echo bit in local mode flags
	push eax
	mov eax, ECHO
	not eax
	and [termios+12], eax
	pop eax
	call write_stdin_termios
	ret

canonical_on:
	call read_stdin_termios

	; set canonical bit in local mode flags
	or dword [termios+12], ICANON
	
	call write_stdin_termios
	ret

echo_on:
	call read_stdin_termios

	; set echo bit in local mode flags
	or dword [termios+12], ECHO

	call write_stdin_termios
	ret

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;  end of terminal control procedure
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;;start of test procedure
test_move:
	pushad
	call echo_off
	call canonical_off
	call clearFixedSet
	mov byte [CurrentShape], 3
	mov byte [CurrentRotate], 0
	mov byte [PosY], 6
	mov byte [PosX], 1
.testrefresh:
	call clearPlate
	mov ah, byte [CurrentShape]; shape index
	mov al, byte [CurrentRotate] ; shape rotate index
	mov bh, byte [PosX] ; matrix x
	mov bl, byte [PosY] ; matrix y
	mov ecx, ShapeBuf
	call getShapePosition
	mov ecx, ShapeBuf	
	;;call addShapeToFixedSet
	call updateShapeToPlate
	call paintPlate
	call updatePos ;; wait to read next position
	call checkShapeValidity
	jmp .testrefresh
.testquit:
	popad
	ret
	

_start:
	nop
	;; test move procedure
	call test_move
	jmp quit
	;; end of test move procedure

	;; test 
	call echo_off
	call canonical_off
	mov ah, 3 ; shape index
	mov al, 0 ; shape rotate index
	mov bl, 4 ; matrix y
	mov bh, 4 ; matrix x
	mov ecx, ShapeBuf
	call getShapePosition
	mov ax, word [ShapeBuf]
	mov bx, word [ShapeBuf + 2]
	mov cx, word [ShapeBuf + 4]
	mov dx, word [ShapeBuf + 6]
	nop
	call clearPlate
	mov ecx, ShapeBuf	
	call updateShapeToPlate
	call paintPlate
	nop
	;; end of test

	call echo_off
	call canonical_off
	call initPos
refresh:
	call updatePos 
	call updatePlate
	call paintPlate
	jmp refresh

quit:
	call echo_on
	call canonical_on
	mov eax, 1
	mov ebx, 0
	int 80h
