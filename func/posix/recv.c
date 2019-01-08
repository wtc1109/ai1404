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
	ikey = ftok("/tmp",1);
	if(ikey == -1){
		printf("ftok false\n");
		return 0;
	}
	printf("key=%d\n",ikey);
	msqid = msgget(ikey,0666|IPC_CREAT);
	if(msqid < 0){
		printf("msqid = %d, false\n",msqid);
		return 0;
	}
	buf.mtype = 1;
	sprintf(buf.mtext,"adfasiuhg");
	flag = msgrcv(msqid, &buf, 512,0,0);
	printf("msgrcv = %d\n",flag);
	if(flag >= 0){
		printf("type = %d\n",buf.mtype);
		printf("msg = %s\n",buf.mtext);
	}
	sleep(5);
	return 0;
}
