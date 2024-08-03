def frame(header, addr, seqNo, msg):
    addr = str(addr).zfill(2)
    seqNo = str(seqNo).zfill(4)
    length = str(len(msg)).zfill(4)
    temp = chr(header)+addr+seqNo+length+msg
    return temp
