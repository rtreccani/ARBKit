import serial
import random
import signal
import time

ser = serial.Serial('COM15', 3000000)
ser.flush()

def handler(signum, frame):
    ser.close()
    exit()
signal.signal(signal.SIGINT, handler)

def writeToRam(addr,val):
    if(addr>268435455 or val >255):
        print("invalid value in address or val for write")
        ser.close()
        exit()

    packet =int(87).to_bytes(1, 'little') + addr.to_bytes(4, 'little') + val.to_bytes(1,'little')
    bytesSent = ser.write(packet)
    if(bytesSent != 6):
        print("full packet not sent on write")
        ser.close()
        exit()
    return    



def readFromRam(addr,val):
    if(addr>268435455 or val >255):
        print("invalid value in address or val for read")
        ser.close()
        exit()
    
    packet =int(82).to_bytes(1, 'little') + addr.to_bytes(4, 'little')
    bytesSent = ser.write(packet)
    if(bytesSent != 5):
        print("full packet not sent on read")
        ser.close()
        exit()
                                                                         
    inval = ser.read(1)
    if(inval[0] != bytes([val])[0]):
        print("read error: invalid value")
        ser.close()
        exit()
    return

def burstWrite(addr, data):
    dataLen = len(data)-1
    if(addr + dataLen >= 268435455):
        print('trying to write to more RAM than exists')
    ser.write(int(66).to_bytes(1, 'big'))
    preamble = addr.to_bytes(4, 'big')
    ser.write(preamble)
    preamble = dataLen.to_bytes(4, 'big')
    ser.write(preamble)
    ser.write(bytes(data))
    return


def burstRead(addr, len):
    ser.write((80).to_bytes(1, 'big'))
    preamble = addr.to_bytes(4, 'big')
    ser.write(preamble)
    preamble = len.to_bytes(4, 'big')
    ser.write(preamble)
    while(ser.in_waiting < len):
        pass
    return(ser.read(len))



SAMPLES = 4000

testSeq = []
for i in range(0,SAMPLES):
    testSeq.append (0)


while True:
    tic = time.time()
    for i in range(0,SAMPLES):
        testSeq[i] = random.randint(0,255)
    #print(testSeq)

    # for addr,val in enumerate(testSeq):
    #     writeToRam(addr,val)
    burstWrite(0, testSeq)
    a = burstRead(0, SAMPLES)
    toc = time.time() - tic

    if(a != bytes(testSeq)):
        print("two sequences not equal")
        ser.close()
        exit()
    # print('atomic read')
    # for addr,val in enumerate(testSeq):
    #     readFromRam(addr, val)

    toc = time.time() - tic
    print('successfully wrote and read back ', SAMPLES, ' bytes in ', toc, " seconds, data rate ", 2*SAMPLES/toc, "B/s")

