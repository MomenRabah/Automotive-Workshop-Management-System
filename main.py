from classes import *
from methods import *
import json

# setting-up general window properties
window.geometry("1000x600")
window["bg"] = "#f5f6fa"
window.resizable("false", "false")
window.title("CM Center")
switch_page(main_page())

# to load and decode data from file
try:
    with open("data", "r") as file:
        data = json.load(file)

    for client in data.get("clients"):
        Client(client.get("name"), client.get("number"))

    for order in data.get("orders"):
        for client in clients:
            if client.number == order.get("client"):
                Order(client, order.get("number"), order.get("state"), order.get("description"), order.get("vehicle"),
                      order.get("price"))
                break
except Exception:
    pass


window.mainloop()


# to encode and save data to file
client2d = tuple({"name": client.name, "number": client.number} for client in clients)

order2d = tuple({"client": order.client.number, "number": order.number, "state": order.state,
                "description": order.description, "vehicle": order.vehicle, "price": order.price} for order in orders)

with open("data", "w") as file:
    json.dump({"clients": client2d, "orders": order2d}, file)
