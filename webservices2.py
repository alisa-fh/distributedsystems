import Pyro4
import json
import urllib
import urllib.request

@Pyro4.expose

class getAddress(object):

    def __init__(self):
        self.prevAdd = {}

    def getAddressData(self, postcode):
        if postcode in self.prevAdd:
            print("in address cache")
            return self.prevAdd[postcode]

        try:
            postcode = postcode.replace(" ", "")
            url = "http://api.getthedata.com/postcode/" + postcode
            j = urllib.request.urlopen(url)
            str_response = j.read().decode('utf-8')
            js = json.loads(str_response)
            lat = float(js['data']['latitude'])
            long = float(js['data']['longitude'])
            addressData = [lat, long]
            self.prevAdd[postcode] = addressData
            return addressData
        except:
            return [];


addObj = getAddress()
daemon = Pyro4.Daemon()  # make a Pyro daemon
ns = Pyro4.locateNS()  # find the name server
uri = daemon.register(addObj)  # register the greeting maker as a Pyro object
ns.register("ns_getAddress1", uri)  # register the object with a name in the name server

print("Ready.")
daemon.requestLoop()  # start the event loop of the server to wait for calls
