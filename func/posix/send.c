#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <sys/ipc.h>
#include <sys/types.h>
#include <sys/msg.h>
#include <error.h>

struct msgbuf
{
	long mtype;
	char mtext[512];
};

int main()
{
	int msqid;
	struct msgbuf buf, buf1;
	int flag;
	int sendlength, recvlength;
	
	key_t ikey;
	ikey = ftok(".",1);
	if(ikey == -1){
		printf("ftok false\n");
		return 0;
	}
	msqid = msgget(ikey,0666|IPC_CREAT);
	if(msqid < 0){
		printf("msqid = %d, false\n",msqid);
		return 0;
	}
	buf.mtype = 1;
	sprintf(buf.mtext,"adfasiuhg");
	flag = msgsnd(msqid, &buf, 512,0);
	printf("msgsnd = %d\n",flag);
	return 0;
}
