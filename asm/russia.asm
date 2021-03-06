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

	DebugOutput: db "------------",10

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
	TIME: equ 1<<4
	MIN: equ 1<<5


section .bss
	LineBuf resb 13
	Plate resb 200
	FixedSet resb 200
	PosX resb 1
	PosY resb 1
	PosXBuf resb 1
	PosYBuf resb 1
	UserInput resb 1
	LastMoveDirection resb 1
	ShapeBuf resb 16
	CurrentShape resb 1
	CurrentRotate resb 1

section .text
	global _start

initPos:
	mov byte [PosX], 0
	mov byte [PosY], 0
	ret

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; return al: 0 for up, 1 for right, 2 for down, 3 for left
updatePos:
	push ebx
	push ecx
	push edx

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
	add al, 1
	mov byte [PosX], al
	mov al, 1
	jmp .endUpdatePos
.decX:
	mov al, byte [PosX]
	sub al, 1
	mov byte [PosX], al
	mov al, 3
	jmp .endUpdatePos
.incY:
	mov al, byte [PosY]
	add al, 1
	mov byte [PosY], al
	mov al, 2
	jmp .endUpdatePos
.decY:
	mov al, byte [PosY]
	sub al, 1
	mov byte [PosY], al
	mov al, 0
	jmp .endUpdatePos
.endUpdatePos:
	pop edx
	pop ecx
	pop ebx
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
	pop ax
	ret

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; call this to check if the parameter positions is valid 
;; in $al: last move direction, eax will be change
;; in $ecx: the shapebuf contains 4 point position
;; out $eax(al): return 0 if the result is valid
;;			return 1 if the result is invalid but current is still alive
;;			return 2 if the current should add to fixed set 
checkPositionValidity:
	push edx
	push ebx
	mov byte [LastMoveDirection], al
	mov edx, 0
.checkOnePosition: 
	;; first check x position
	mov bl, byte [ecx + 2 * edx]
	cmp bl, 10
	jae .rangeInvalid
	;; then check y position
	mov bl, byte [ecx + 2 * edx + 1] ;; then check y position
	cmp bl, 20
	jae .rangeInvalid

	;; then check if is occupied
	xor eax, eax
	mov ah, bl
	mov al, 10
	mul ah
	add al, byte [ecx + 2 * edx] ;;
	adc ah, 0
	mov bl, byte [FixedSet + eax];
	cmp bl, '*'
	je .rangeInvalid

	add edx, 1 ;; checkOnePosition loop
	cmp edx, 4
	jne .checkOnePosition

	;; all check passed
	mov al, 0 ;; set the default value
	jmp .quit

.rangeInvalid:
	mov al, byte [LastMoveDirection]
	cmp al, 2
	je .quit
	mov al, 1
.quit:
	pop ebx
	pop edx
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

;; in:
;;		al: the x position of target
;;		ah: the y position of target
;; out:
;;		al: the target char
getCharOfFixedSet:
	push ebx
	push edx
	mov bl, al
	mov bh, ah
	mov eax, 0
	mov al, bh 
	mov ah, 10
	mul ah
	mov bh, 0
	add ax, bx
	mov al, byte [FixedSet + eax]
	pop edx
	pop ebx
	ret

;; in:
;;		al: x
;;		ah: y
;;		bl: target char
;; no ouput
setCharOfFixedSet:
	push edx
	push ebx
	mov bl, al
	mov bh, ah
	mov eax, 0
	mov al, bh
	mov ah, 10
	mul ah
	mov bh, 0
	add ax, bx
	pop ebx
	mov byte [FixedSet + eax], bl
	pop edx
	ret

;;in:
;;		al: the y position of target line
;;out:
;;		ah: 1 if is all full, 0 if not all full
isLineFull:
	push ebx
	push ecx
	push edx
	mov bl, al
	mov cl, 10
.isLineFullCheckOneChar:
	sub cl, 1
	mov al, cl 
	mov ah, bl
	call getCharOfFixedSet 
	cmp al, 20h
	je .lineIsNotfullExit
	cmp cl, 0
	jne .isLineFullCheckOneChar
	jmp .lineIsFullExit
.lineIsNotfullExit:
	mov ah, 0
	jmp .exit
.lineIsFullExit:
	mov ah, 1
	jmp .exit
.exit:
	pop edx
	pop ecx
	pop ebx
	ret

;; in:
;;		al: the y position of targetLine
;; no output
clearLine:
	push ebx
	push eax
	push ecx
	cmp al, 0
	je .newheadline
	mov bl, al
	mov ah, 10
	mul ah
	mov cx, ax
	add ax, 10
.moveOneChar:
	sub ax, 1
	sub cx, 1
	jz .newheadline
	mov bl, byte[FixedSet + eax - 10]
	mov byte[FixedSet + eax], bl
	jmp .moveOneChar
.newheadline:
	mov ecx, 10
.newACharInHead:
	mov byte[FixedSet + ecx - 1], ' '
	sub cx, 1
	jnz .newACharInHead
	pop ecx
	pop eax
	pop ebx
	ret

;;;;;;;;;;;;;;;;;;;;;
;; call to clear full line
clearAllFullLine:
	pushad
	mov cl, 19
.oneline:
	mov al, cl
	call isLineFull
	cmp ah, 1
	jne .continue
	mov al, cl
	call clearLine
	add cl, 1
.continue:
	cmp cl, 0
	je .quit
	sub cl, 1
	jmp .oneline
.quit:
	popad
	ret

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; generate a new shape and set it's position to 4, 0
generateNewShape:
	pushad
	mov byte [CurrentShape], 1
	mov byte [CurrentRotate], 0
	mov byte [PosX], 4
	mov byte [PosY], 0
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
	cmp al, ' '
	je .testContinue
	mov byte [Plate + ecx -1], al
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

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; paint the plate to screen, first paint the fixed set to plate
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
	mov byte [PosY], 17
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
	call saveCurrentPosition
	call updatePos ;; wait to read next position
	call stubforbreak
	push ax ;; save the move direction
	mov ah, byte [CurrentShape]; shape index
	mov al, byte [CurrentRotate] ; shape rotate index
	mov bh, byte [PosX] ; matrix x
	mov bl, byte [PosY] ; matrix y
	mov ecx, ShapeBuf
	call getShapePosition ;; save the new shape into ShapeBuf
	call stubforbreak
	pop ax ;; restore the move direction
	call stubforbreak
	mov ecx, ShapeBuf
	call checkPositionValidity
	cmp al, 0 
	je .check_case0
	cmp al, 1
	je .check_case1
	cmp al, 2
	je .check_case2
.check_case0:
	jmp .testrefresh
.check_case1:
	call restoreCurrentPosition
	jmp .testrefresh
.check_case2:
	call restoreCurrentPosition
	mov ah, byte [CurrentShape]; shape index
	mov al, byte [CurrentRotate] ; shape rotate index
	mov bh, byte [PosX] ; matrix x
	mov bl, byte [PosY] ; matrix y
	mov ecx, ShapeBuf
	call getShapePosition ;; save the new shape into ShapeBuf
	call addShapeToFixedSet
	call clearAllFullLine
	;; begin of test code
	;; end of test code
	call generateNewShape
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
