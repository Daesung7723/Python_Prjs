# 메시지를 캡슐화하여 프레임을 구성하는 프로그램

def frame(start_ch, addr, seqNo, msg):
    return f'{start_ch:c}{addr:02d}{seqNo:04d}{len(msg):04d}{msg}'

if __name__ == '__main__':
    start_ch = 0x05
    addr = 2
    seqNo = 1
    
    msg = input('your message: ')
    capsule = frame(start_ch, addr, seqNo, msg)
    print(f'생성된 프레임: {capsule}')
