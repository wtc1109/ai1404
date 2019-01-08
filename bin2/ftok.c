#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <sys/ipc.h>
#include <sys/types.h>
#include <sys/msg.h>
#include <error.h>

int main(void)
{
	key_t rkey,skey,rkey2,skey2, rerkey,reskey;
	skey = ftok("/mnt",6);
	if(skey == -1){
		printf("ftok false\n");
		return 0;
	}
	printf("skey=%d\n",skey);
	
	rkey = ftok("/mnt",5);
	if(rkey == -1){
		printf("ftok false\n");
		return 0;
	}
	printf("rkey=%d\n",rkey);



	reskey = ftok("/home/bluecard/hvpd",7);
	if(skey == -1){
		printf("ftok false\n");
		return 0;
	}
	printf("skey=%d\n",reskey);

	rerkey = ftok("/home/bluecard/hvpd",8);
	if(rkey == -1){
		printf("ftok false\n");
		return 0;
	}
	printf("rkey=%d\n",rerkey);

	FILE *fp;
	fp = fopen("key.txt","w");
	if(NULL == fp){
		printf("open file false\n");
		return 0;
	}
	char buff[128];
	sprintf(buff,"{\"send\":\"%d\",\"recv\":\"%d\",\"resend\":\"%d\",\"rerecv\":\"%d\"}",skey,rkey,reskey,rerkey);
	fwrite(buff,strlen(buff),1,fp);
	fclose(fp);
	return 0;
}

