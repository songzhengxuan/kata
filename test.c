#include <stdio.h>
int main(int argc, char **argv) {
	char *p = (char*) 0x1234;
	*p = 'a';
}
