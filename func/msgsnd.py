import sysv_ipc
import struct,binascii
#http://semanchuk.com/philip/sysv_ipc/#message_queue

if __name__ == '__main__':

    cam_id = "18054301230"

    pic_full_name = "/tmp/123.jpg"

    slot_count = 3

    slot_install = 5
    slot_bitmap = 7

    is_manual = 1

    slot_region = [[10,10,43,12,13,78,60,89],[10,10,43,12,13,78,60,89],[10,10,43,12,13,78,60,89]]#; // 12

    pic_type = 1#; //

    pic_w = 500#; //

    pic_h = 678 #;
    region0 = struct.pack('8i',*[slot_region[0][i] for i in range(8)])
    region1 = struct.pack('8i', *[slot_region[1][i] for i in range(8)])
    region2 = struct.pack('8i', *[slot_region[2][i] for i in range(8)])
    msg0 = struct.pack('32s128s4b',cam_id,pic_full_name,slot_count,slot_install,slot_bitmap,is_manual)
    print binascii.hexlify(msg0)
    msg2 = struct.pack('3i',pic_type,pic_w,pic_h)
    msg = msg0+region0+region1+region2+msg2
    q2 = sysv_ipc.MessageQueue(117507979, flags=sysv_ipc.IPC_CREAT)
    q2.send(msg, type=40964)
    q3 = sysv_ipc.MessageQueue(50397185, flags=sysv_ipc.IPC_CREAT)
    msg1 = q3.receive()
    print len(msg1[0])
    cam_id1,pic1,slot1 = struct.unpack("32s128sB",msg1[0][:161])
    print binascii.hexlify(cam_id1)
    #cam_id1, pic1, slot1 = struct.unpack_from("32s128sB", msg1[:160])
    q2.remove()