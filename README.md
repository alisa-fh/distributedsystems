# Just Hungry Distributed Systems Assignment
Just Hungry is a food ordering system configured as a distributed system,
fulfilling  location, relocation, replication and failure transparency requirements.  
A client places orders, which are stored and can be retrieved.  
Address data is also provided to the user based off the provided postcode.


## How to run Just Hungry

On Python 2.7 or 3.5 and newer, install Pyro4:

```
pip install pyro4
```
Ensuring you are in the correct directory, run the following commands, each 
in separate terminals:


```
pyro4-ns

python feserver.py

python backserver.py

python backserver1.py

python backserver2.py

python webservices.py

python webservices2.py

python client.py
```
The first command runs the name server, the second the front end server, followed by the
three back-end servers, two web service servers, and finally, the client program.

Follow the instructions provided by the client program to place and retrieve orders.

# Web Services

Two open-source postcode APIs were used in the implementation of my program in order
to retrieve more information about a postcode provided by a user.  
These are:

https://postcodes.io/  
https://www.getthedata.com/open-postcode-geo-api
