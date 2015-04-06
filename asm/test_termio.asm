section .data
	ClrHome db 27,"[2J", 27, "[01;01H"
	CLRLEN equ $-ClrHome
	filePath db "/dev/random", 0
	EndLine db "------------",10
	ONELINELEN equ $-EndLine
	MiddleLine db "1----------1",10
	PlateHeight equ 24
	PlateWidth equ 32
	NEWONELINELEN equ 32
	;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
	;; shapes
	;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
	Shapes:
	dw 17476,3840,8738,17476
	dw 17952,864,1122,17952
	dw 1632,1632,1632,1632
	dw 1856,1570,736,1856
	dw 17984,1824,610,17984
	dw 17476,3840,8738,17476
	dw 17952,864,1122,17952
	dw 1856,1570,736,1856

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
	TIME: equ 1<<5
	MIN: equ 1<<6


section .bss
	timer_count resb 4
	timer_expire_count resb 1
	LineBuf resb 32
	Plate resb 768 ;; 32 * 24
	PaintCountBuffer resb 1
	FixedSet resb 200
	PosX resb 1
	PosY resb 1
	PosXBuf resb 1
	PosYBuf resb 1
	UserInput resb 1
	LastMoveDirection resb 1
	ShapeBuf resb 16
	fileHandle resb 4
	buffer resb 4
	CurrentShape resb 1
	CurrentShapeBuf resb 1
	CurrentRotate resb 1
	CurrentRotateBuf resb 1

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
.updateWait:
	mov eax, dword [timer_count]
	add eax, 1
	mov dword [timer_count], eax
	cmp eax, 10000000
	jae .doUpdatePos
	jmp .updateWait
.doUpdatePos:
	mov dword [timer_count], 0
	mov eax, 3
	mov ebx, 0
	mov ecx, UserInput
	mov edx, 1
	int 80h
	cmp eax, 0
	jne .newinput
.debugPrint1:
	mov al, byte [timer_expire_count]
	add al, 1
	mov byte [timer_expire_count], al
.debugPrint2:
	cmp al, 12 ;; this is the sinme time tick number 
	jne .aTimerNotExpire
	mov byte [timer_expire_count], 0
	jmp .incY
.aTimerNotExpire:
	mov al, 0xff
	jmp .endUpdatePos
.newinput:
	mov al, byte [UserInput]
	cmp al, 'w'
	je .decY
	cmp al, 's'
	je .incY
	cmp al, 'a'
	je .decX
	cmp al, 'd'
	je .incX
	cmp al, 'j'
	je .rotate
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
.rotate:
	mov al, byte [CurrentRotate]
	add al, 1
	and al, 3
	mov byte [CurrentRotate], al
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
.debugwrite:
	mov byte [edi], bh
	inc edi
	mov edx, ecx
	shr edx, 2
	add bl, dl
	mov byte [edi], bl
	inc edi
	pop bx
.continue:
	inc ecx
	cmp ecx, 16
	jb .checkOneBit
.debuggetshapeout:
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
	mov al, byte [CurrentShape]
	mov byte [CurrentShapeBuf], al
	mov al, byte [CurrentRotate]
	mov byte [CurrentRotateBuf], al
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
	mov al, byte [CurrentShapeBuf]
	mov byte [CurrentShape], al
	mov al, byte [CurrentRotateBuf]
	mov byte [CurrentRotate], al
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
generateNewShape2:
	pushad
	;; open the file
	mov ecx, 0
	mov ebx, filePath
	mov edx, 01FFh;
	mov eax, 5
	int 80h
	mov dword [fileHandle], eax
	;; read the file
	mov ebx, dword [fileHandle]
	mov ecx, buffer
	mov eax, 3 ;; __NR_read
	mov edx, 4
	int 80h

	mov al, byte [buffer]
	and al, 7
	;; following 2 lines are real code
	mov byte [CurrentShape], al
	mov byte [CurrentRotate], 0
	;; following 2 lines are debug code
	;;mov byte [CurrentShape], 0
	;;mov byte [CurrentRotate], 0

	mov byte [PosX], 4
	mov byte [PosY], 0
	popad
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

stubforbreak:
	pushad
	popad
	ret

; update the shape stored in CX to plate
updateShapeToPlate:
	pushad
	mov edx, 0
	mov bl, '*'
.updateOneShapePos:
	mov al, byte [ecx + 1] ; +1 is the Y position
	add al, 1
	mov ah, byte [ecx]
	add ah, 1
	call drawOneCharToPlate
	add ecx, 2
	inc edx
	cmp edx, 4
	jne .updateOneShapePos
	popad
	ret

drawFixedSetToPlate:
	pushad
	mov esi, 0 
	mov ecx, 20
	mov al, 1
	mov ah, 1
.loopforline:
.loopforsingle:
	mov bl, byte [FixedSet + esi] 
	call drawOneCharToPlate
	add esi, 1
	add ah, 1
	cmp ah, 11
	jne .loopforsingle
	sub ecx, 1
	jz .quit
	add al, 1
	mov ah, 1
	jmp .loopforline
.quit:
	popad
	ret


;;;;
;; input: 
;;		ah: the x pos of target char
;;		al: the y pos of target char
;;		bl: the char to draw on target pos
drawOneCharToPlate:
	pushad
	mov edx, eax
	mov eax, 0
	mov al, dl
	shl eax, 5
	add al, dh
	mov byte [Plate + eax], bl
	popad
	ret

clearPlate2:
	pushad
	mov ecx, 768
.loop1:
	mov byte [Plate + ecx], ' ' 
	sub ecx, 1
	jnz .loop1
	mov ecx, 24
.loop2:
	mov eax, ecx
	sub eax, 1
	shl eax, 5
	add eax, 31
	mov byte [Plate + eax], 10
	sub ecx, 1
	jnz .loop2
	mov al, 21
.drawPlateBound:
	mov ah, 11 
	mov bl, '-'
.drawPlateBoundLoop:
	call drawOneCharToPlate
	cmp ah, 0
	je .quitDrawPlateBoundLoop
	sub ah, 1
	jmp .drawPlateBoundLoop
.quitDrawPlateBoundLoop:
	cmp al, 0
	je .quitDrawPlateBound
	mov al, 0
	jmp .drawPlateBound
.quitDrawPlateBound:
	mov al, 21
	mov bl, '.'
.drawVertLine:
	sub al, 1
	mov ah, 0
	call drawOneCharToPlate
	mov ah, 11
	call drawOneCharToPlate
	cmp al, 1
	jne .drawVertLine
	popad
	ret

;; new paint plate 
paintPlate2:
	pushad
	call clearTerminalScreen
	mov eax, 0
	mov byte [PaintCountBuffer], 25;; should be 24, but add 1 line for debug out
	mov al, byte [PaintCountBuffer]
	mov edi, 0
.paintOneLine:
	cmp al, 0
	je .quit
	mov ebx, 1
	lea ecx, [Plate + edi]
	mov eax, 4
	mov edx, 32 
	int 80h
	add edi, 32
	mov al, byte [PaintCountBuffer]
	sub al, 1
	mov byte [PaintCountBuffer], al
	jmp .paintOneLine
.quit:
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

set_min_time:
	call read_stdin_termios
	;;and eax, 0
	;;mov al, byte [termios+23]
	mov byte [termios+23], 0
	call write_stdin_termios
	ret

unset_min_time:
	call read_stdin_termios
	mov byte [termios+23], 1
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
	call set_min_time
	call clearFixedSet
	mov byte [CurrentShape], 3
	mov byte [CurrentRotate], 0
	mov byte [PosY], 17
	mov byte [PosX], 1
.testrefresh:
	mov ah, byte [CurrentShape]; shape index
	mov al, byte [CurrentRotate] ; shape rotate index
	mov bh, byte [PosX] ; matrix x
	mov bl, byte [PosY] ; matrix y
	mov ecx, ShapeBuf
	call clearPlate2
	call drawFixedSetToPlate
	call getShapePosition
	mov ecx, ShapeBuf	
	call updateShapeToPlate
	call paintPlate2
	call saveCurrentPosition
.waituserinput:
	call updatePos ;; wait to read next position
	cmp al, 0xff
	je .waituserinput
	call stubforbreak
	push ax ;; save the move direction
	mov ah, byte [CurrentShape]; shape index
	mov al, byte [CurrentRotate] ; shape rotate index
	mov bh, byte [PosX] ; matrix x
	mov bl, byte [PosY] ; matrix y
	mov ecx, ShapeBuf
	call getShapePosition ;; save the new shape into ShapeBuf
.break1:
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
	call generateNewShape2
	jmp .testrefresh
.testquit:
	popad
	ret


_start:
	nop
	call clearFixedSet
	call clearPlate2
	call test_move
	jmp quit
quit:
	call echo_on
	call canonical_on
	mov eax, 1
	mov ebx, 0
	int 80h
