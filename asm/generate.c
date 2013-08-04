#include <stdio.h>
#include <ctype.h>
int main(int argc, char **argv) {
		int i, j;
		for (i = 0; i < 256; ++i) {
				printf("db");
				for (j = 0; j < 16; ++j, ++i) {
						if (isprint(i)) {
								printf(" %xh", i);
						} else {
								printf(" 2Eh", i);
						}
				}
				--i;
				printf("\n");
		}
		return 0;
}
