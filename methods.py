import tkinter as tk
from PIL import ImageTk, Image
from tkinter.font import *
import re


# image holder object class. it is defined here so that it can be accessed from anywhere in the code.
# images have to be done in this complicated way because the python garbage collector deletes the image otherwise.
class Picture(tk.Frame):

    def __init__(self, master, width, height, image):
        tk.Frame.__init__(self, master)

    # Image.open ----> opens image file | ImageTk.PhotoImage ----> processes the file data and converts it to an image.
        self.width, self.height = width, height
        self.image = Image.open(image).resize((width, height))
        self.image = ImageTk.PhotoImage(self.image)

        self.label = tk.Label(self, image=self.image)
        self.label.pack()

    def set(self, file):
        self.image = Image.open(file).resize((self.width, self.height))
        self.image = ImageTk.PhotoImage(self.image)
        self.label.configure(image=self.image)


# setting-up the window and the current page variable.
window = tk.Tk()
current_page = None

# setting-up window background image.
background_image = Picture(window, 1000, 600, "images/car_mechanic.png")
background_image.place(x=0, y=0)

# setting-up notification label.
notification_label = tk.Label(master=window, bg="#f5f6fa")
notification_label.pack()

# setting-up the lists that will hold all clients and orders
clients = []
orders = []


# closes previous page and displays new page.
def switch_page(new_page):
    close_page()
    global current_page
    current_page = new_page
    current_page.place(relx=.5, rely=.5, anchor="center")


# closes previous page and clears notification text.
def close_page():
    if current_page is not None:
        for widget in current_page.winfo_children():
            widget.destroy()
        current_page.destroy()
    notification_label.pack_forget()


# deletes and order from the global list of orders and from its clients order list.
def delete_order(order):
    order.client.orders.remove(order)
    orders.remove(order)
    del order


# deletes the clients and all orders associated with the client.
def delete_client(client):
    global clients, orders
    for order in client.orders:
        orders.remove(order)
    clients.remove(client)
    del client


# searches for and returns client with matching name and number. if no client matches, the function returns (None).
def find_client(name, number):
    for client in clients:
        if client.name == name and client.number == number:
            return client


# checks whether the name and phone number are valid when creating a new client.
def check_validity(name, number):
    num_pattern = re.compile(r"^0[0-9]{9}$")
    name_pattern = re.compile(r"^[A-Za-z\s'-]{3,32}$")

    if type(name_pattern.match(name)) is not re.Match:
        return "invalid user name"
    elif type(num_pattern.match(number)) is not re.Match:
        return "invalid phone number"
    return "true"


# changes the way the number is written, so that it works regardless of whether the client used +966 instead of 0 or
# separated the numbers with spaces or dashes.
def correct(number):
    number = number.replace(" ",  "").replace("-",  "")
    if number[0:4] == "+966":
        number = "0" + number[4:]
    return number


# used to display a small notification in the top center of the page.
def notification(message, color):
    font = Font(family="helvetica", size=12, weight="bold")
    notification_label.config(font=font, text=message, fg=color)
    notification_label.pack(pady=10)
