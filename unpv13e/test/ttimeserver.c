#include "unp.h"
#include <time.h>

int main(int argc, char **argv) {
	int connfd, clientfd;
	struct sockaddr_in serveraddr;
	struct sockaddr_in clientaddr;
	socklen_t clientaddrlen;
	if ((connfd = socket(AF_INET, SOCK_STREAM, 0)) < 0)
		err_sys("socket error");
	bzero(&serveraddr, sizeof(serveraddr));
	serveraddr.sin_family = AF_INET;
	serveraddr.sin_port = htons(13); 
	if ((inet_pton(AF_INET, argv[1], &serveraddr.sin_addr)) < 0)
		err_sys("ptons error");
	if ((bind(connfd, &serveraddr, sizeof(serveraddr))) < 0)
		err_sys("bind error");
	if (listen(connfd, 5) != 0)
		err_sys("listen error");
	time_t t;
	char buf[32];
	for (;;) {
		clientfd = accept(connfd, &clientaddr, &clientaddrlen);
		if (clientfd < 0)
			err_sys("accpet error");
		time(&t);
		memset(buf, 0, sizeof(buf));
		snprintf(buf, 32, "%d", t);
		write(clientfd, buf, 32);
		close(clientfd);
	}
	exit(0);
}
