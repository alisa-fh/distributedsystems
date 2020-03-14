# saved as greeting-server.py
import Pyro4
import datetime;
import json
import urllib
import urllib.request

@Pyro4.expose
class ServerSelect(object):
    def __init__(self):
        self.deliverObj = Pyro4.Proxy("PYRONAME:ns_delivereat0")
        self.deliverObj1 = Pyro4.Proxy("PYRONAME:ns_delivereat1")
        self.deliverObj2 = Pyro4.Proxy("PYRONAME:ns_delivereat2")
        self.addressObj = Pyro4.Proxy("PYRONAME:ns_getAddress")
        self.addressObj1 = Pyro4.Proxy("PYRONAME:ns_getAddress1")
        self.serverList = [self.deliverObj, self.deliverObj1, self.deliverObj2]
        self.primaryServer = 0;
        self.serversDown = [0,0,0] #indicate if servers were recently down

    def switchServer(self):
        success = 0
        i = 0
        while success == 0 and i < len(self.serverList):
            try:
                if self.serversDown[i] == 1:
                    self.serverList[i] = Pyro4.Proxy("PYRONAME:ns_delivereat" + i)
                    self.serverList[i].updateOthers()
                self.serverList[i].getMenu()
                self.primaryServer = i
                self.serversDown[i] = 0
                success = 1
            except:
                self.serversDown[i] = 1
                i += 1
        if success == 0:
            return -1
        else:
            return 0


    def getMenu(self):
        status = 0
        while status == 0:
            try:
                menu = self.serverList[self.primaryServer].getMenu()
                status = 1
            except:
                status = self.switchServer()
                if status == -1:
                    return -1

        return menu

    def getOrders(self, name, postcode):
        status = 0
        while status == 0:
            try:
                orders = self.serverList[self.primaryServer].getOrders(name, postcode)
                status = 1
            except:
                status = self.switchServer()
                if status == -1:
                    return -1

        return orders


    def makeOrder(self, itemList, name, postcode):
        currentTime = datetime.datetime.now();
        currentTime = str(currentTime)[:19];

        status = 0
        while status == 0:
            try:
                orderStatus = self.serverList[self.primaryServer].makeOrder(itemList, name, postcode, currentTime)
                status = 1
            except:
                status = self.switchServer()
                if status == -1:
                    return -1

        return orderStatus


    def getAddress(self, postcode):
        try:
            addressData = self.addressObj.getAddressData(postcode)
            return addressData
        except:
            try:
                addressData = self.addressObj1.getAddressData(postcode)
                return addressData
            except:
                print("Error - Unable to retrieve address data")
                return -1


daemon = Pyro4.Daemon()                # make a Pyro daemon
ns = Pyro4.locateNS()                  # find the name server
uri = daemon.register(ServerSelect)   # register the greeting maker as a Pyro object
ns.register("ns_frontEnd", uri)   # register the object with a name in the name server

print("Ready.")
daemon.requestLoop()                   # start the event loop of the server to wait for calls