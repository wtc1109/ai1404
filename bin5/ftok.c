#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <sys/ipc.h>
#include <sys/types.h>
#include <sys/msg.h>
#include <error.h>

int main(void)
{
	key_t rkey,skey, rkey2,skey2,rerkey,reskey;
	skey = ftok("/mnt",6);
	if(skey == -1){
		printf("ftok false\n");
		return 0;
	}
	printf("skey=%d, 0x%X\n",skey,skey);
	
	rkey = ftok("/mnt",5);
	if(rkey == -1){
		printf("ftok false\n");
		return 0;
	}
	printf("rkey=%d, 0x%X\n",rkey,rkey);


    skey2 = ftok("/mnt",0xb5);
	if(skey2 == -1){
		printf("ftok false\n");
		return 0;
	}
	printf("skey2=%u,0x%X\n",skey2,skey2);

	rkey2 = ftok("/mnt",0xb5);
	if(rkey2 == -1){
		printf("ftok false\n");
		return 0;
	}
	printf("rkey2=%u,0x%X\n",rkey2,rkey2);



	reskey = ftok("/home/bluecard/hvpd",7);
	if(skey == -1){
		printf("ftok false\n");
		return 0;
	}
	printf("skey=%d, 0x%X\n",reskey, reskey);

	rerkey = ftok("/home/bluecard/hvpd",8);
	if(rkey == -1){
		printf("ftok false\n");
		return 0;
	}
	printf("rkey=%d, 0x%X\n",rerkey, rerkey);

	FILE *fp;
	fp = fopen("key.txt","w");
	if(NULL == fp){
		printf("open file false\n");
		return 0;
	}
	char buff[128];
	sprintf(buff,"{\"send\":\"%d\",\"recv\":\"%d\",\"send2\":\"%u\",\"recv2\":\"%u\",\"resend\":\"%d\",\"rerecv\":\"%d\"}"
	        ,skey,rkey,skey2,rkey2,reskey,rerkey);
	fwrite(buff,strlen(buff),1,fp);
	fclose(fp);
	return 0;
}

