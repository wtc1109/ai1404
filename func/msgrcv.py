from posix_ipc import MessageQueue as MsgQ
import sysv_ipc
import os

if __name__ == '__main__':
    q = MsgQ("/tmp", flags=os.O_CREAT,mode=0666)
    q.send("adfg")
    rec = q.receive(1)
    print rec
    q.close()
    q.unlink()

    q2 = sysv_ipc.MessageQueue(16842753,flags=sysv_ipc.IPC_CREAT)
    q2.send("sferogh", type=1)

