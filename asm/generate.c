#include <stdio.h>
#include <ctype.h>

int base[][16] = {
	{
		0, 1, 0, 0,
		0, 1, 0, 0,
		0, 1, 0, 0,
		0, 1, 0, 0
		},
	{
		0, 1, 0, 0,
		0, 1, 1, 0,
		0, 0, 1, 0,
		0, 0, 0, 0
		},
	{
		0, 0, 0, 0,
		0, 1, 1, 0,
		0, 1, 1, 0,
		0, 0, 0, 0
		},
	{
		0, 0, 0, 0,
		0, 1, 1, 1,
		0, 1, 0, 0,
		0, 0, 0, 0
		},
	{
		0, 1, 0, 0,
		0, 1, 1, 0,
		0, 1, 0, 0,
		0, 0, 0, 0
		}
};

void printShape(int shape[]) {
	int i,j;
	for (i = 0; i < 4; ++i) {
		for (j = 0; j < 4; ++j) {
			if (shape[i*4+j] == 0) {
				printf(" ");
			} else {
				printf("*");
			}
		}
		printf("\n");
	}
	printf("\n");
}

void copyShape(int destShape[], int sourceShape[]) {
	int i = 0;
	for (i = 0; i < 16; ++i) {
		destShape[i] = sourceShape[i];
	}
}

// (i, j) to (3-j, i)
void rotateShape(int outShape[], int inShape[]) {
	int i,j;
	for (i = 0; i < 4; ++i) {
		for (j = 0; j < 4; ++j) {
			outShape[4*i + (3-j)] = inShape[4*j+i];
		}
	}
}

int shapeToNumber(int shape[]) {
	int i = 0;
	int result = 0;
	int f = (1<<16);
	for (i = 0; i < 16; ++i) {
		f = (f>>1);
		if (shape[i] == 1) {
			result |= f;
		}
	}
	return result;
}

int main(int argc, char **argv) {
	int i = 0;
	int buf[16];
	int buf2[16];
	for (i = 0; i < 5; ++i) {
		rotateShape(buf, base[i]);
		rotateShape(buf2, buf);
		printf("dw %d,%d,%d,%d\n", shapeToNumber(base[i]), shapeToNumber(buf), shapeToNumber(buf2), shapeToNumber(base[i]));
	}
	return 0;
}


