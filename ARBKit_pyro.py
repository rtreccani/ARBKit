import Pyro5.api
import os, sys
from time import sleep
import serial


@Pyro5.api.expose #expose the entire object to the pyro api
class ARBKitSpinner(object):
    _must_shutdown = False
    ser = serial.Serial()


    def heartbeat(self, msg): #heartbeat. if it sees PING, it returns PONG
        if(msg == "PING"):
            return("PONG")
        else:
            pass #eventually call seppuku from here once seppuku works


    @Pyro5.server.oneway #prevents the calling function waiting for an answer
    def kill(self): #called to stop the daemon
        self._must_shutdown = True
    

    def connect(self,port, baud):
        self.ser.port = port
        self.ser.baud = baud
        try:
            self.ser.open()
            return(True)
        except Exception as e:
            return(False)
        


#calling function that starts the ARBKitSpinner daemon class
def startDaemon():
    daemon = Pyro5.server.Daemon(port=49123) #listen on the port 49123
    a = ARBKitSpinner()
    #use a static name which removes the need for a nameserver. cheap and easy
    uri = daemon.register(a, objectId="ARBKit_StaticDaemonAddr")
    print(uri)
    #spin on the daemon
    daemon.requestLoop(loopCondition=lambda: not a._must_shutdown)
    #exit the program??
    exit()

if __name__ == "__main__":
    startDaemon()