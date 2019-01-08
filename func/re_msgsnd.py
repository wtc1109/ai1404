import sysv_ipc
import struct,binascii
#http://semanchuk.com/philip/sysv_ipc/#message_queue

if __name__ == '__main__':

    cam_id = "18054301230"
    cmos = 0
    _slot = 1
    pic_full_name = "/tmp/123.jpg"
    pic_w = 123
    pic_h = 124
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
    msg0 = struct.pack('32s2b128s2H2b',cam_id,cmos,_slot,pic_full_name,pic_w,pic_h,1,3)
    undis_param_t = struct.pack('4B8i4i4i',5,6,7,8,1200,1201,1202,1203,1204,1205,1206,1207,1300,1301,1302,1303,1304,1305,1306,1307)
    msg2 = struct.pack('12i',2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012)
    msg3 = struct.pack('12i', 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012)
    msg4 = struct.pack('2b4i128s',98,99,3001,3002,3003,3004,'sadfasdf')
    print binascii.hexlify(msg0)

    msg = msg0+undis_param_t+msg2+msg3+msg4
    q2 = sysv_ipc.MessageQueue(117507979, flags=sysv_ipc.IPC_CREAT)
    q2.send(msg, type=40964)
    q3 = sysv_ipc.MessageQueue(50397185, flags=sysv_ipc.IPC_CREAT)
    msg1 = q3.receive()
    print len(msg1[0])
    cam_id1,pic1,slot1 = struct.unpack("32s128sB",msg1[0][:161])
    print binascii.hexlify(cam_id1)
    #cam_id1, pic1, slot1 = struct.unpack_from("32s128sB", msg1[:160])
    q2.remove()