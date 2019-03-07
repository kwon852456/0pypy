# -*- coding: utf-8 -*-

import ctypes




class Head(ctypes.Structure):
    _fields_ = [("z", ctypes.c_int),
                ("v0", ctypes.c_ubyte),("v1", ctypes.c_ubyte),("c0", ctypes.c_ubyte),("c1", ctypes.c_ubyte),
                ("t", ctypes.c_ulonglong),
                ("r",ctypes.c_int),
                ("y0",ctypes.c_ubyte),
                ("y1",ctypes.c_ubyte),("n",ctypes.c_ubyte),("d",ctypes.c_ubyte),
                ("h",ctypes.c_ushort),("w",ctypes.c_ushort),
                ("l",ctypes.c_int)]
    
class Y2(ctypes.Union):
    _fields_= [("h1", ctypes.c_ushort),
               ("t2", ctypes.c_ubyte * 2)]
    
class Y4(ctypes.Union):
    _fields_= [("i1", ctypes.c_int),
               ("f1", ctypes.c_float),
               ("t4", ctypes.c_ubyte * 4)]
        
class Y8(ctypes.Union):
    _fields_= [("n1", ctypes.c_ulonglong),
               ("d1", ctypes.c_double),
               ("t8", ctypes.c_ubyte * 8)]

class Yhd(ctypes.Structure):
    _fields_ = [("yHd",ctypes.c_ubyte * 32)]

def int_to_bytes1(x):
    return x.to_bytes(1, 'big')

def int_to_bytes2(x):
    return x.to_bytes(2, 'big')
    
def int_to_bytes4(x):
    return x.to_bytes(4, 'big')
    
def int_to_bytes8(x):
    return x.to_bytes(8, 'big')    

def int_from_bytes(xbytes):
    return int.from_bytes(xbytes, 'big')
        
    
def yHd_head(head):
    y2 = Y2() ; y4 = Y4() ; y8 = Y8() ; yHd = Yhd() ; y42 = Y4() ;
    
    y4.i1 = head.z
    yHd.yHd[0] = y4.t4[0] ; yHd.yHd[1] = y4.t4[1] ; yHd.yHd[2] = y4.t4[2] ; yHd.yHd[3] = y4.t4[3]
    
    yHd.yHd[4] = head.v0 ; yHd.yHd[5] = head.v1 ; yHd.yHd[6] = head.c0 ; yHd.yHd[7] = head.c1

    y8.n1 = head.t
    yHd.yHd[8] = y8.t8[0] ; yHd.yHd[9] = y8.t8[1] ; yHd.yHd[10] = y8.t8[2] ; yHd.yHd[11] = y8.t8[3] ;
    yHd.yHd[12] = y8.t8[4] ; yHd.yHd[13] = y8.t8[5] ; yHd.yHd[14] = y8.t8[6] ; yHd.yHd[15] = y8.t8[7] ;
    
    
    y4.i1 = head.r
    
    yHd.yHd[16] = y4.t4[0] ; yHd.yHd[17] = y4.t4[1] ; yHd.yHd[18] = y4.t4[2] ; yHd.yHd[19] = y4.t4[3] ;
    yHd.yHd[20] = head.y0 ; yHd.yHd[21] = head.y1 ; yHd.yHd[22] = head.n ; yHd.yHd[23] = head.d ;

    y2.h1 = head.h
    yHd.yHd[24] = y2.t2[0] ; yHd.yHd[25] = y2.t2[1] 
    
    y2.h1 = 0
    
    y2.h1 = head.w
    yHd.yHd[26] = y2.t2[0] ; yHd.yHd[27] = y2.t2[1] 

    
    y42.i1 = head.l
    yHd.yHd[28] = y42.t4[0] ; yHd.yHd[29] = y42.t4[1] ; yHd.yHd[30] = y42.t4[2] ; yHd.yHd[31] = y42.t4[3]

    return yHd

def head_yHd(yHd):
    head = Head() ; y2 = Y2() ; y4 = Y4() ; y8 = Y8() ; y42 = Y4() ;
    
    y4.t4[0] = yHd.yHd[0] ; y4.t4[1] = yHd.yHd[1] ; y4.t4[2] = yHd.yHd[2] ; y4.t4[3] = yHd.yHd[3] ;
    head.z = y4.i1
    
    head.v0 = yHd.yHd[4] ; head.v1 = yHd.yHd[5] ;  head.c0 = yHd.yHd[6] ; head.c1 = yHd.yHd[7] ;
    
    
    y8.t8[0] = yHd.yHd[8] ; y8.t8[1] = yHd.yHd[9] ; y8.t8[2] = yHd.yHd[10] ; y8.t8[3] = yHd.yHd[11] ;
    y8.t8[4] = yHd.yHd[12] ; y8.t8[5] = yHd.yHd[13] ; y8.t8[6] = yHd.yHd[14] ; y8.t8[7] = yHd.yHd[15] ;
    
    head.t = y8.n1
    
    y4.t4[0] = yHd.yHd[16] ; y4.t4[1] = yHd.yHd[17] ; y4.t4[2] = yHd.yHd[18] ; y4.t4[3] = yHd.yHd[19] ;
    head.r = y4.i1
    
    head.y0 = yHd.yHd[20] ; head.y1 = yHd.yHd[21] ; head.n = yHd.yHd[22] ; head.d = yHd.yHd[23] ;     
    
    y2.t2[0] = yHd.yHd[24] ; y2.t2[1] = yHd.yHd[25] ;
    head.h = y2.h1
    
    y2.t2[0] = yHd.yHd[26] ; y2.t2[1] = yHd.yHd[27] ;
    head.w = y2.h1
    
    y42.t4[0] = yHd.yHd[28] ; y42.t4[1] = yHd.yHd[29] ; y42.t4[2] = yHd.yHd[30] ; y42.t4[3] = yHd.yHd[31] ; 
    head.l = y42.i1
    
    return head

def headEnc_s(string):
    head = Head()
    head.v0 = ctypes.c_ubyte(1) ; head.v1 = ctypes.c_ubyte(0) ; head.c0 = ctypes.c_ubyte(3) ; head.c1 = ctypes.c_ubyte(0)
    head.t = ctypes.c_ulonglong(0) ; head.r = ctypes.c_int(0) ;
    head.y0 = ctypes.c_ubyte(1) ; head.y1 = ctypes.c_ubyte(0) ;
    head.n = ctypes.c_ubyte(0) ; head.d = ctypes.c_ubyte(1) ;
    head.h = ctypes.c_ushort(1) ; head.w = ctypes.c_ushort(len(string)) ; head.l = ctypes.c_int(head.h * head.w * head.d)
    head.z = ctypes.c_int(head.l + 32)
    
    return head

def headEnc_ws(string):
    head = Head()
    head.v0 = ctypes.c_ubyte(1) ; head.v1 = ctypes.c_ubyte(0) ; head.c0 = ctypes.c_ubyte(3) ; head.c1 = ctypes.c_ubyte(0)
    head.t = ctypes.c_ulonglong(0) ; head.r = ctypes.c_int(0) ;
    head.y0 = ctypes.c_ubyte(1) ; head.y1 = ctypes.c_ubyte(0) ;
    head.n = ctypes.c_ubyte(0) ; head.d = ctypes.c_ubyte(1) ;
    head.h = ctypes.c_ushort(1) ; head.w = ctypes.c_ushort(len(bytes(string.encode("utf-8"))) + 1) ; head.l = ctypes.c_int(head.h * head.w * head.d)
    head.z = ctypes.c_int(head.l + 32)
    
    return head

def yHdr_s(string):
    head = headEnc_s(string)
    yHdr_To_send = bytes(head) + string.encode()
    return yHdr_To_send

def yHdr_ws(string):
    head = headEnc_ws(string)
    
    #yHdr_To_send = bytes(head) + string.encode("utf-16le")
    yHdr_To_send = bytes(head) + string.encode("utf-8") + "\0".encode("utf-8")


    '''
    #디버그 코드 
    print(bytes(head))
    print(string.encode("utf-16le"))
    
    for i in range(32 , 34):
        print(yHdr_To_send[i])
    '''

    #print(bytes(head))
    return yHdr_To_send


def s_yHdr(yhdr):
    y4 = Y4()
    
    y4.t4[0] = ctypes.c_ubyte(yhdr[0]) 
    y4.t4[1] = ctypes.c_ubyte(yhdr[1])
    y4.t4[2] = ctypes.c_ubyte(yhdr[2])
    y4.t4[3] = ctypes.c_ubyte(yhdr[3])

    sizeOfData = y4.i1
    
    #print(f"sizeOfData = {sizeOfData}")
    
    rawData = yhdr[32:sizeOfData]   
    return rawData.decode("utf-8")

def ws_yHdr(yhdr):
    y4 = Y4()
    
    y4.t4[0] = ctypes.c_ubyte(yhdr[0]) 
    y4.t4[1] = ctypes.c_ubyte(yhdr[1])
    y4.t4[2] = ctypes.c_ubyte(yhdr[2])
    y4.t4[3] = ctypes.c_ubyte(yhdr[3])

    sizeOfData = y4.i1
    
    #print(f"sizeOfData = {sizeOfData}")
    
    rawData = yhdr[32:sizeOfData]
    
    return rawData.decode("utf-8")
    
