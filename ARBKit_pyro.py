import Pyro5.api
import os

@Pyro5.api.expose
class ARBKitSpinner(object):
    def heartbeat(self, msg):
        if(msg == "PING"):
            return("PONG")
        else:
            exit()
    
    @Pyro5.server.oneway
    def seppuku(self):
        os.kill(os.getpid())


def startDaemon():
    daemon = Pyro5.server.Daemon(port=49123) 
    uri = daemon.register(ARBKitSpinner, objectId="ARBKit_StaticDaemonAddr")
    print(uri)
    daemon.requestLoop()