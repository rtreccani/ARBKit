import serial
import random
import signal
import time

#open the serial link, at a baud of 3M
ser = serial.Serial('COM15', 3000000)
#clear it out to prevent any issues from previous runs
ser.flush()

#this handler captures ctrl+c events and cleanly closes the serial link before exiting/
def handler(signum, frame):
    ser.close()
    exit()
#lock that handler to ctrl+C
signal.signal(signal.SIGINT, handler)

#we can only address 256MB of ram, and each value can only be one byte. check that. 
def writeToRam(addr,val):
    if(addr>268435455 or val >255):
        print("invalid value in address or val for write")
        ser.close()
        exit()

    #87=W for Write. 4 byte address, and then the value as well. total 6 bytes to transmit 1 byte.
    packet =int(87).to_bytes(1, 'little') + addr.to_bytes(4, 'little') + val.to_bytes(1,'little')
    bytesSent = ser.write(packet)
    #if we didn't send all 6 bytes, throw an error and quit.
    if(bytesSent != 6):
        print("full packet not sent on write")
        ser.close()
        exit()
    return    

#can only address 256MB ram. Value is the exepcted value given this is a test program. 
def readFromRam(addr,val):
    if(addr>268435455 or val >255):
        print("invalid value in address or val for read")
        ser.close()
        exit()
    
    #82 = R for Read, 4 byte address, 5 byte total.
    packet =int(82).to_bytes(1, 'little') + addr.to_bytes(4, 'little')
    bytesSent = ser.write(packet) 
    #if not all 5 bytes sent, then throw an error.
    if(bytesSent != 5):
        print("full packet not sent on read")
        ser.close()
        exit()
    #get back one byte from the serial link, and compare against expected value.                                                                    
    inval = ser.read(1)
    if(inval[0] != bytes([val])[0]):
        print("read error: invalid value")
        ser.close()
        exit()
    return

#take in a starting address and an array of data (constrained 0-255) and bulk transfer.
def burstWrite(addr, data):
    dataLen = len(data)-1
    #bounds checking to see if the data fits in memory
    if(addr + dataLen >= 268435455):
        print('trying to write to more RAM than exists')
    #66 is B for Burst
    ser.write(int(66).to_bytes(1, 'big'))
    #preamble containing the address
    preamble = addr.to_bytes(4, 'big')
    ser.write(preamble)
    #preamble containing the data length
    preamble = dataLen.to_bytes(4, 'big')
    ser.write(preamble)
    #steam the rest of the data, cast into bytes.
    ser.write(bytes(data))
    return


#read back a given amount of bytes, starting at a given address.
def burstRead(addr, len):
    #80 = P = Playback (running out of numbers)
    ser.write((80).to_bytes(1, 'big'))
    #preamble of the starting address
    preamble = addr.to_bytes(4, 'big')
    ser.write(preamble)
    #preamble of the read length
    preamble = len.to_bytes(4, 'big')
    ser.write(preamble)
    #wait until we receive the right number of samples in buffer
    while(ser.in_waiting < len):
        pass
    #read them all and return
    return(ser.read(len))



SAMPLES = 4000

#create a blank array of samples
testSeq = []
for i in range(0,SAMPLES):
    testSeq.append (0)


while True:
    #generate a random amount of samples
    for i in range(0,SAMPLES):
        testSeq[i] = random.randint(0,255)

    #start time measurement, burst write, then burst read. stop time measurement
    tic = time.time()
    burstWrite(0, testSeq)
    a = burstRead(0, SAMPLES)
    toc = time.time() - tic

    #if the readback data is not equal to written data, there's a problem
    if(a != bytes(testSeq)):
        print("two sequences not equal")
        ser.close()
        exit()
    
    #print some debug info.
    print('successfully wrote and read back ', SAMPLES, ' bytes in ', toc, " seconds, data rate ", 2*SAMPLES/toc, "B/s")

