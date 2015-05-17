#include <arpa/inet.h>
#include <stdio.h>
#include <errno.h>

int main(int argc, char **argv) {
	struct in_addr addr;
	int ret = inet_aton("8.8.8.8", &addr);
	printf("ret is %d\n", ret);
	perror("what?");
	return 0;
}
