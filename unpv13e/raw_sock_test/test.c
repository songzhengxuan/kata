#include <netinet/in.h>
#include <netinet/ip.h>
#include <netinet/ip_icmp.h>

#include <sys/types.h>
#include <sys/socket.h>

#include <stdlib.h>

int sockfd;
void readloop(void);

int main(int argc, char **argv) {
	readloop();
	return 0;
}

void readloop(void) {
	int size;
	char recvbuf[1500];
	char controlbuf[1500];

	sockfd = socket(PF_INET, SOCK_RAW, IPPROTO_UDP);
	if (sockfd < 0) {
		perror("socket() error");
		exit(1);
	}

	size = 60 * 1024;
	setsockopt(sockfd, SOL_SOCKET, SO_RCVBUF, &size, sizeof(size));
}
