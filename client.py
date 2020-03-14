# saved as greeting-client.py
import Pyro4
import sys

def checkInt(aNum):
    try:
        int(aNum)
        return True
    except ValueError:
        return False

feServer = Pyro4.Proxy("PYRONAME:ns_frontEnd")    # use name server object lookup uri shortcut to create proxy

print("Welcome to Just Hungry, your online food ordering and delivery service.");
name = input("What is your name? ").strip()
cont = True;

while cont == True:
    #ask if want to make order or review orders
    actionSelect = input("Select an option: \n 1 - Make a food order\n 2 - Review your orders\n 3 - Exit system\n");

    if actionSelect == '1':
        print("You selected to make an order.")
        menu = feServer.getMenu();
        if menu == -1:
            print("Error - All servers are currently down.")
            print("Application closing.")
            sys.exit()
        for i in range(0, len(menu)):
            print(str(i+1) + ".\t\t\t Item: " + menu[i][0] + " Price: £" + str(menu[i][1]))
        inputError = False
        itemList = input("Input a list of the item IDs desired: ")
        itemList = itemList.replace(",", " ")
        itemList = itemList.split(" ")
        for element in itemList:
            if element == " " or element == "":
                itemList.remove(element)
            elif not checkInt(element):
                print("Error - " + element + " is not an item ID")
                inputError = True
                break;
            elif (int(element) - 1) not in range(0, len(menu)):
                print("Error - there is no item number " + element + ". Try again.")
                inputError = True
                break;

        if inputError == False:
            postcode = input("Input your postcode: ")
            status = feServer.makeOrder(itemList, name, postcode)
            if status == 0:
                print("Error - All servers are currently down.")
                print("Application closing.")
                sys.exit()
            elif status == -1:
                print("Error in creation of order.")
                print("Application closing.")
                sys.exit()
            elif status == 1:
                addressResult = feServer.getAddress(postcode);
                if addressResult == []:
                    print("Error in retrieving address data. Ensure postcode is valid.")
                elif addressResult == -1:
                    print("Error in retrieving address data. Servers are down.")
                elif isinstance((addressResult[0]), str):
                    print("Order has successfully been made to postcode " + postcode.upper() + " located in " + addressResult[0]
                          + " in the region " + addressResult[1] + ".")
                elif isinstance((addressResult[0]), float):
                    print("Order has successfully been made to postcode " + postcode.upper() + ". Longitude: " + str(addressResult[0])
                          + ". Latitude: " + str(addressResult[1]))



        doCont = input("To go back to menu, press Y. Otherwise, press any other key.\n")
        if doCont == 'Y' or doCont == 'y':
            cont = True
        else:
            cont = False

    elif actionSelect == '2':
        print("You selected to review your orders.")
        postcode = input("Input the postcode of orders to view: ")
        orders = feServer.getOrders(name, postcode)
        print(orders)
        if orders == -1:
            print("Error - All servers are currently down.")
            print("Application closing.")
            sys.exit()
        elif orders == []:
            print("No orders made to " + name + " at postcode " + postcode.upper())
        else:
            for order in orders:
                dateTime = order[2]
                name = order[0]
                address = order[1]
                items = order[3]
                print(dateTime + " Order sent to: " + name + " " + address + " Items: ")
                for item in items:
                    print(item)

        doCont = input("To continue, press Y. Otherwise, press any other key.\n")
        if doCont == 'Y' or doCont == 'y':
            cont = True
        else:
            cont = False

    elif actionSelect == '3':
        print("Thank you for your custom. Goodbye.")
        cont = False;
    else:
        print("Invalid input. Try again.\n")
sys.exit()


