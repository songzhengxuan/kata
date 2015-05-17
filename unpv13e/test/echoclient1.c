#include "unp.h"

void sigpipe_handler(int sig) {
	printf("encounter SIGPIPE\n");
}

void str_cli2(FILE *fp, int sockfd);
int main(int argc, char **argv) {
	int sockfd;
	struct sockaddr_in servaddr;
	if (argc != 2)
		err_quit("usage: %s <IPaddress>", argv[0]);

	sockfd = Socket(AF_INET, SOCK_STREAM, 0);

	bzero(&servaddr, sizeof(servaddr));
	servaddr.sin_family = AF_INET;
	servaddr.sin_port = htons(SERV_PORT);
	Inet_pton(AF_INET, argv[1], &servaddr.sin_addr);

	Sigfunc *handler = &sigpipe_handler;
	Signal(SIGPIPE, handler);

	Connect(sockfd, (SA*) &servaddr, sizeof(servaddr));
	str_cli2(stdin, sockfd);


	exit(0);
}

void str_cli2(FILE *fp, int sockfd) {
	char sendline[MAXLINE], recvline[MAXLINE];
	while (Fgets(sendline, MAXLINE, fp) != NULL) {
		sleep(2);
		Writen(sockfd, sendline, strlen(sendline));
		sleep(2);
		Writen(sockfd, sendline, strlen(sendline));
		if (Readline(sockfd, recvline, MAXLINE) == 0)
			err_quit("str_cli: server terminated prematurely\n");

		Fputs(recvline, stdout);
	}
}
