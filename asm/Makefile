test_term: test_termio.asm
	nasm -f elf32 -g -o test_termio.o test_termio.asm
	ld -m elf_i386 -o test_termio test_termio.o
libcsandbox: libcsandbox.asm
	nasm -f elf32 -g -F stabs -o libcsandbox.o libcsandbox.asm
	gcc -m32 libcsandbox.o -o libcsandbox
test_term_bak: test_termio.asm
	nasm -f elf32 -g -o test_termio_bak.o test_termio_bak.asm
	ld -m elf_i386 -o test_termio test_termio_bak.o
russia: russia.asm
	nasm -f elf32 -g -o russia.o russia.asm
	ld -m elf_i386 -o russia.exe russia.o
vidbuff1.exe: vidbuff1.asm
	nasm -f elf -o vidbuff1.o vidbuff1.asm
	ld -o vidbuff1.exe vidbuff1.o
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
hexdump2.exe:	hexdump2.o
	ld -o hexdump2.exe hexdump2.o
hexdump2.o: hexdump2.asm
	nasm -f elf -o hexdump2.o hexdump2.asm
clean:
	rm *.o
	rm *.exe
