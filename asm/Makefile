uppercaser1:	uppercaser1.o
	ld -o uppercaser1 uppercaser1.o
uppercaser1.o:	uppercaser1.asm
	nasm -f elf -o uppercaser1.o uppercaser1.asm
factor:	factor.o
	ld -o factor factor.o
factor.o:	factor.asm
	nasm -f elf -o factor.o factor.asm
hexdump1.exe:	hexdump1.o
	ld -o hexdump1.exe hexdump1.o
hexdump1.o: hexdump1.asm
	nasm -f elf -o hexdump1.o hexdump1.asm
clean:
	rm *.o
	rm *.exe
