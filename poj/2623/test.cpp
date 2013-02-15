#include <stdio.h>
#include <stdlib.h>
#include <algorithm>

void printSemiSum(unsigned int a, unsigned int b);
void sortNumbers(unsigned int *data, int length);
int main(int argc, char **argv) {
	int length, t;
	scanf("%d", &length);
	unsigned int * data = (unsigned int *) malloc(length * sizeof(unsigned int));
	for (t = 0; t < length; ++t) {
		scanf("%u", data + t);
	}
	std::sort(data, data + length);
	//sortNumbers(data, length);
	if (length & 0x01) {
		printf("%u.0", data[length / 2]);
	} else if (length > 0) {
		printSemiSum(data[length / 2 - 1], data[length / 2]);
	}
	printf("\n");
}

// sort number using insertion sort, Failed on Time Limit
void sortNumbers(unsigned int *data, int length) {
	int i, j;
	for (i = 1; i < length; ++i) {
		unsigned int temp = data[i];
		j = i - 1;
		while ((j >= 0) && (data[j] > temp)) {
			data[j + 1] = data[j];
			--j;
		}
		data[j + 1] = temp;
	}
}

void quickSortNumbers(unsigned int *data, int length) {
	
}

void printSemiSum(unsigned int a, unsigned int b) {
	unsigned int diff = b - a;
	if (diff & 0x01) {
		printf("%u.5", a + (diff>>1));
	} else {
		printf("%u.0", a + (diff>>1));
	}
}
