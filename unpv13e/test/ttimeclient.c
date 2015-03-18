#include "unp.h"
int main(int argc, char **argv) {
	int connfd, n;
	char recvline[MAXLINE + 1];
	connfd = socket(AF_INET, SOCK_STREAM, 0); 
	struct sockaddr_in addr;
	bzero(&addr, sizeof(addr));
	addr.sin_family = AF_INET;
	addr.sin_port = htons(13);
	if (inet_pton(AF_INET, argv[1], &addr.sin_addr) < 0)
		err_quit("inet_pton error");
	if (connect(connfd, (struct sockaddr*)&addr, sizeof(addr)) < 0)
		err_sys("Connect error");
	while ((n = read(connfd, recvline, MAXLINE)) > 0) {
		recvline[n] = 0;
		if (fputs(recvline, stdout) == EOF) {
			err_sys("fputs error");
		}
	}
	if (n < 0)
		err_sys("read error");
	exit(0);
}
