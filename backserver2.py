# saved as greeting-server.py
import Pyro4

@Pyro4.expose
class Delivereat(object):
    def __init__(self):
        self.menu = [["Apple", 0.99], ["Smoked Salmon", 4], ["Frozen Pizza", 1.55], ["Chocolate Milkshake", 3]];
        self.orders = [["john", "DH14PZ", "01022019", ["apple", "smoked salmon"]], ["enoch", "GU214JD", "05032019", ["apple"]]];
        self.deliverObj = Pyro4.Proxy("PYRONAME:ns_delivereat0")
        self.deliverObj1 = Pyro4.Proxy("PYRONAME:ns_delivereat1")

    def getMenu(self):
        return self.menu;

    def updateOrders(self, updatedOrders):
        try:
            print("Orders passed to update:")
            print(updatedOrders)
            self.orders = updatedOrders
            print("Orders have been updated:")
            print(self.orders);
        except:
            print("Error updating orders")

    def updateOthers(self):
        finalOrders = self.orders
        try:
            orders0 = self.deliverObj.getAllOrders()
            for order in orders0:
                if order not in self.orders:
                    finalOrders.append(order)
            self.orders = finalOrders
        except:
            orders0 = 0
        try:
            orders1 = self.deliverObj1.getAllOrders()
            for order in orders1:
                if order not in self.orders:
                    finalOrders.append(order)
        except:
            orders1 = 0
        print("finalOrders in backserver2:")
        print(finalOrders)
        if orders0 != 0:
            self.deliverObj.updateOrders(finalOrders)
        if orders1 != 0:
            self.deliverObj1.updateOrders(finalOrders)
        self.orders = finalOrders

    def getAllOrders(self):
        return self.orders

    def getOrders(self, name, postcode):
        print("In getOrders:")
        print(self.orders)
        postcode = postcode.replace(" ", "")
        postcode = postcode.upper()
        orderArray = [];
        for entry in self.orders:
            if (entry[0] == name) and (entry[1] == postcode):
                orderArray.append(entry);
        return orderArray;

    def makeOrder(self, itemList, name, postcode, currentTime):
        postcode = postcode.replace(" ", "")
        postcode = postcode.upper()
        try:
            formattedItemList = [];
            for item in itemList:
                formattedItemList.append(self.menu[int(item)-1][0]);
            newOrder = [name, postcode, currentTime, formattedItemList];
            self.orders.append(newOrder);
            self.updateOthers()
            return 1
        except:
            return -1


Deliver = Delivereat()
ns = Pyro4.locateNS()                  # find the name server
try:
    existing = ns.lookup("ns_delivereat2")
    daemon = Pyro4.core.Daemon(port = existing.port)
    daemon.register(Deliver, objectId=existing.port)
except:
    daemon = Pyro4.core.Daemon()
    uri = daemon.register(Deliver)
    ns.register("ns_delivereat2", uri)

print("Ready.")
daemon.requestLoop()                   # start the event loop of the server to wait for calls