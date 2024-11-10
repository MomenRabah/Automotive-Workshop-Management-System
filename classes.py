import tkinter
from tkinter import ttk
from methods import *


# ~~~~~~~~~~~~~~~~~~~~ classes ~~~~~~~~~~~~~~~~~~~~
class Order:
    def __init__(self, client, number, state, description, vehicle, price):
        self.client = client
        self.number = number
        self.price = price
        self.state = state
        self.description = description
        self.vehicle = vehicle
        self.info = {'Order number': self.number, 'Order state': self.state,
                     'Order description': self.description, 'Order vehicle': self.vehicle,
                     'Order price': self.price}
        orders.append(self)
        self.client.orders.append(self)

    def edit(self):
        switch_page(edit_order_page(self))


class Client:
    user = "Client"

    def __init__(self, name, number):
        self.name = name
        self.number = number
        self.orders = []
        clients.append(self)


# ~~~~~~~~~~~~~~~~~~~~ page functions ~~~~~~~~~~~~~~~~~~~~
# function for the ( button_review ) button in ( review_order_page() ).
def review_order(name, number):
    client = find_client(name, correct(number))
    if client is not None:
        switch_page(orders_page(client))
    else:
        notification("no such client exists", "red")


# function for the ( button_new_order ) button in ( new_order_page() ).
def make_order(name, number, desc, model):
    number = correct(number)
    client = find_client(name, number)
    if client is not None:
        order = Order(client, len(orders), "pending", desc, model, "to be evaluated")
        switch_page(successful_order_page(client, order))
    else:
        validity = check_validity(name, number)
        if validity == "true":
            client = Client(name, number)
            order = Order(client, len(orders), "pending", desc, model, "to be evaluated")
            switch_page(successful_order_page(client, order))
        else:
            notification(validity, "red")


# function for the ( button_del ) button in ( edit_order_page() ).
def remove_order(order):
    delete_order(order)
    switch_page(order_deleted_page())


# function for the ( button_edit ) button in ( edit_order_page() ).
def update_order(order, state, price):
    order.state = state
    order.price = price
    notification("Order has been updated", "green")


# function for the ( login ) button in ( Password() ).
def check_password(password):
    if password == "Cm10":
        switch_page(admin_page())
    else:
        notification("invalid passcode!", "red")


# ~~~~~~~~~~~~~~~~~~~~ pages ~~~~~~~~~~~~~~~~~~~~
"""
page format:

def page_name():               <------ if the page is for a client of an order enter (client) or (order) as a parameter.

    page_frame = tk.Frame()        <------ all of the page contents has to be inside this frame.

    (page content: button, labels, other frames, etc)

    return page_frame              <------ don't forget to return the frame so that it can be packed in to the window.
    
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

to switch pages:
lambda: switch_page(page_name()) 
        or
lambda: switch_page(page_name(parameter))  <------ some pages require (client) or (order) as parameter.
    
"""

# fonts: color=#273c75
sub_font = Font(family="helvetica", size=12, weight="normal")
title_font = Font(family="helvetica", size=18, weight="bold")


def main_page():
    background_image.set("images/car_mechanic.png")
    page_frame = tk.Frame(bg="#f5f6fa")

    logo = Picture(page_frame, 150, 150, "images/logo.png")
    logo.pack()

    # 1st window Titles
    title_frame = tk.Frame(master=page_frame, bg="#f5f6fa")
    sub_label = tk.Label(master=title_frame, text="Wellcome to", fg="#273c75", bg="#f5f6fa", font=sub_font)
    main_label = tk.Label(master=title_frame, text="CM Center", fg="#273c75", bg="#f5f6fa", font=title_font)
    sub_label.pack()
    main_label.pack()
    title_frame.pack(pady=30, padx=60)

    # 1st window buttons : color=#273c75
    button_client = tk.Button(master=page_frame, text="Customer Page", height=2, width=30, bg="#273c75", fg="#f5f6fa",
                              command=lambda: switch_page(client_page()))
    button_admin = tk.Button(master=page_frame, text="Admin Page", height=2, width=30, bg="#273c75", fg="#f5f6fa",
                             command=lambda: switch_page(password_page()))
    button_info = tk.Button(master=page_frame, text="Info Page", height=2, width=30, bg="#273c75", fg="#f5f6fa",
                            command=lambda: switch_page(info_page_1()))
    button_admin.pack(pady=10)
    button_client.pack(pady=10)
    button_info.pack(pady=10)

    return page_frame


def client_page():
    background_image.set("images/empty.png")
    page_frame = tk.Frame(bg="#f5f6fa")

    label = tk.Label(master=page_frame, text="Client Page", bg="#f5f6fa", fg="#273c75",height=3 ,font=title_font)
    label.pack()

    button_new_order = tk.Button(master=page_frame, text="make new order", height=2, width=30, bg="#273c75",
                                 fg="#f5f6fa", command=lambda: switch_page(new_order_page()))
    button_new_order.pack(pady=10)
    button_review_order = tk.Button(master=page_frame, text="review an order", height=2, width=30, bg="#273c75",
                                    fg="#f5f6fa", command=lambda: switch_page(review_order_page()))
    button_review_order.pack(pady=10)

    button_back = tk.Button(master=page_frame, text="back", width=15, bg="#273c75", fg="#f5f6fa",
                            command=lambda: switch_page(main_page()))
    button_back.pack(pady=20)

    return page_frame


def admin_page():
    background_image.set("images/empty.png")
    page_frame = tk.Frame(bg="#f5f6fa")

    small_font = Font(family="helvetica", size=9, weight="normal")
    big_font = Font(family="helvetica", size=10, weight="bold")

    main_label = tk.Label(master=page_frame, text="Admin Page", fg="#273c75", bg="#f5f6fa", font=title_font)
    main_label.pack(pady=10)

    if len(orders) != 0:
        sub_label = tk.Label(master=page_frame, text="Submitted orders:", fg="#273c75", bg="#f5f6fa", font=sub_font)
        sub_label.pack(pady=30)

        a = "#7f8fa6"  # first row background #7f8fa6
        b = "white"  # first row text

        c = "#f5f6fa"  # even column background
        d = "#273c75"  # even column text
        e = "#273c75"  # odd column text

        frame = tk.Frame(master=page_frame)
        label_number = tk.Label(master=frame, text="  Order Number  ", font=big_font, fg=b, bg=a, height=2)
        label_name = tk.Label(master=frame, text="  Client Name  ", font=big_font, fg=b, bg=a, height=2)
        label_state = tk.Label(master=frame, text="  Order State  ", font=big_font, fg=b, bg=a, height=2)
        label_desc = tk.Label(master=frame, text="  Description  ", font=big_font, fg=b, bg=a, height=2)
        label_vehicle = tk.Label(master=frame, text="  Vehicle  ", font=big_font, fg=b, bg=a, height=2)
        label_price = tk.Label(master=frame, text="  Price  ", font=big_font, fg=b, bg=a, height=2)
        label_edit = tk.Label(master=frame, text="  Edit  ", font=big_font, fg=b, bg=a, height=2)
        label_number.grid(row=0, column=0, sticky="nsew")
        label_name.grid(row=0, column=1, sticky="nsew")
        label_state.grid(row=0, column=2, sticky="nsew")
        label_desc.grid(row=0, column=3, sticky="nsew")
        label_vehicle.grid(row=0, column=4, sticky="nsew")
        label_price.grid(row=0, column=5, sticky="nsew")
        label_edit.grid(row=0, column=6, sticky="nsew")

        i = 1
        for order in orders:
            label_number_i = tk.Label(master=frame, text=order.number, font=small_font, fg=e)
            label_name_i = tk.Label(master=frame, text=order.client.name, font=small_font, fg=d,)
            label_state_i = tk.Label(master=frame, text=order.state, font=small_font, fg=e)
            label_desc_i = tk.Label(master=frame, text=order.description, font=small_font, fg=d,)
            label_vehicle_i = tk.Label(master=frame, text=order.vehicle, font=small_font, fg=e)
            label_price_i = tk.Label(master=frame, text=order.price, font=small_font, fg=d, )
            label_number_i.grid(row=i, column=0, padx=5, sticky="nsew")
            label_name_i.grid(row=i, column=1, padx=5, sticky="nsew")
            label_state_i.grid(row=i, column=2, padx=5, sticky="nsew")
            label_desc_i.grid(row=i, column=3, padx=5, sticky="nsew")
            label_vehicle_i.grid(row=i, column=4, padx=5, sticky="nsew")
            label_price_i.grid(row=i, column=5, padx=5, sticky="nsew")
            button_edit = tk.Button(master=frame, text=f"edit", height=1, width=7, bg="#273c75", fg="#f5f6fa",
                                    command=order.edit)
            button_edit.grid(row=i, column=6, padx=20, pady=10)
            i += 1

        frame.pack()
    else:
        label_no_orders = tk.Label(master=page_frame, text="No orders have been submitted   ):", fg="#273c75",
                                   bg="#f5f6fa", font=sub_font)
        label_no_orders.pack(pady=15)

    button_back = tk.Button(master=page_frame, text="back", height=1, width=15, bg="#273c75", fg="#f5f6fa",
                            command=lambda: switch_page(main_page()))
    button_back.pack(pady=30)

    return page_frame


def password_page():
    background_image.set("images/empty.png")
    page_frame = tk.Frame(bg="#f5f6fa")
    main_label = tk.Label(master=page_frame, text="Passcode", fg="#273c75", bg="#f5f6fa", font=title_font)
    main_label.pack(pady=30)

    entry_code = tk.Entry(master=page_frame, width=35, font=sub_font, bg="#f5f6fa", show="*")
    entry_code.pack(pady=30)

    login = tk.Button(master=page_frame, text="login", height=2, width=30, bg="#273c75", fg="#f5f6fa",
                      command=lambda: check_password(entry_code.get()))
    login.pack(pady=20)

    button_back = tk.Button(master=page_frame, text="back", height=1, width=15, bg="#273c75", fg="#f5f6fa",
                            command=lambda: switch_page(main_page()))
    button_back.pack(pady=15)
    return page_frame


def new_order_page():
    page_frame = tk.Frame(bg="#f5f6fa")

    label1 = tk.Label(master=page_frame, text="New Order: ", bg="#f5f6fa", fg="#273c75", font=title_font)
    label1.pack(pady=40)

    details_frame = tk.Frame(master=page_frame, bg="#f5f6fa")
    buttons_frame = tk.Frame(master=page_frame, bg="#f5f6fa")

    details_frame.pack()
    buttons_frame.pack(pady=25)

    label_frame = tk.Frame(master=details_frame, bg="#f5f6fa")
    entry_frame = tk.Frame(master=details_frame, bg="#f5f6fa")

    label_frame.pack(side="left")
    entry_frame.pack(side="right")

    labels = tk.Label(master=label_frame, text="name:\n \nphone number:\n \nmodel:\n \ndescription: ", font=sub_font, bg="#f5f6fa", fg="#273c75",justify="left", width=20)
    labels.pack()

    entry_name = tk.Entry(master=entry_frame, width=35, font=sub_font)
    entry_name.pack(pady=7)

    entry_number = tk.Entry(master=entry_frame, width=35, font=sub_font)
    entry_number.pack(pady=7)

    entry_model = tk.Entry(master=entry_frame, width=35, font=sub_font)
    entry_model.pack(pady=7)

    entry_desc = tk.Entry(master=entry_frame, width=35, font=sub_font)
    entry_desc.pack(pady=7)

    button_new_order = tk.Button(master=buttons_frame, text="Make Order", height=2, width=30, bg="#273c75",
                                 fg="#f5f6fa", command=lambda: make_order(entry_name.get(), entry_number.get(),
                                                                          entry_desc.get(), entry_model.get()))
    button_new_order.pack(pady=15)

    button_back = tk.Button(master=buttons_frame, text="back", height=1, width=15, bg="#273c75", fg="#f5f6fa",
                            command=lambda: switch_page(client_page()))
    button_back.pack(pady=20)

    return page_frame


def successful_order_page(client, order):
    page_frame = tk.Frame(bg="#f5f6fa")

    label1 = tk.Label(master=page_frame, text="your order has been submitted successfully!", bg="#f5f6fa", fg="#273c75",
                      font=title_font)
    label2 = tk.Label(master=page_frame, text="Order review:", bg="#f5f6fa", fg="#273c75", font=sub_font)
    label1.pack(pady=60)
    label2.pack(pady=20)

    frame = tk.Frame(master=page_frame, bg="#f5f6fa")
    label1 = tk.Label(text=f"Order number:  {order.number}  |   State:  {order.state}  |   "
                           f"Description:  {order.description}  |   Vehicle:  {order.vehicle} "
                           f" |  Price:  {order.price}", master=frame, height=3, bg="#f5f6fa", fg="#273c75")
    label1.pack(side="left")
    frame.pack()

    button_back_client = tk.Button(master=page_frame, text="Back to client page", height=2, width=30, bg="#273c75",
                                   fg="#f5f6fa", command=lambda: switch_page(client_page()))
    button_back_client.pack(pady=10)
    button_back_client = tk.Button(master=page_frame, text="see client history", height=2, width=30, bg="#273c75",
                                   fg="#f5f6fa", command=lambda: switch_page(orders_page(client)))
    button_back_client.pack(pady=10)

    return page_frame


def review_order_page():
    page_frame = tk.Frame(bg="#f5f6fa")

    title_label = tk.Label(master=page_frame, text="Review an Order", bg="#f5f6fa", fg="#273c75", font=title_font)
    title_label.pack(pady=40)

    frame_name = tk.Frame(master=page_frame, bg="#f5f6fa")
    frame_number = tk.Frame(master=page_frame, bg="#f5f6fa")

    label_name = tk.Label(master=frame_name, width=15, text="User Name: ", bg="#f5f6fa", fg="#273c75", font=sub_font)
    entry_name = tk.Entry(master=frame_name, width=30, bg="#f5f6fa", fg="#273c75",)

    label_number = tk.Label(master=frame_number, width=15, text="phone number: ", bg="#f5f6fa", fg="#273c75",
                            font=sub_font)
    entry_number = tk.Entry(master=frame_number, width=30, bg="#f5f6fa", fg="#273c75",)

    label_name.pack(side=tk.LEFT)
    entry_name.pack(side=tk.RIGHT)

    label_number.pack(side=tk.LEFT)
    entry_number.pack(side=tk.RIGHT)

    button_review = tk.Button(master=page_frame, text="Review", height=2, width=30, bg="#273c75", fg="#f5f6fa",
                              command=lambda: review_order(entry_name.get(), entry_number.get()))

    frame_name.pack(pady=20)
    frame_number.pack(pady=20)
    button_review.pack(pady=25)

    button_back = tk.Button(master=page_frame, text="back",  height=1, width=15, bg="#273c75", fg="#f5f6fa",
                            command=lambda: switch_page(client_page()))
    button_back.pack(pady=10)

    return page_frame


def orders_page(client):
    page_frame = tk.Frame(bg="#f5f6fa")

    label = tk.Label(master=page_frame, text=f" {client.name}'s order history", height=5, bg="#f5f6fa", fg="#273c75",
                     font=title_font)
    label2 = tk.Label(master=page_frame, text="submitted orders: ", bg="#f5f6fa", fg="#273c75", font=sub_font)
    label.pack(pady=10)
    label2.pack(pady=10)

    for order in client.orders:
        label1 = tk.Label(text=f"Order number:  {order.number}  |   State:  {order.state}  |   "
                               f"Description:  {order.description}  |   Vehicle:  {order.vehicle} "
                               f" |  Price:  {order.price}", master=page_frame, height=3, bg="#f5f6fa", fg="#273c75", )
        label1.pack()

    button_new_order = tk.Button(master=page_frame, text="make new order", height=2, width=30, bg="#273c75",
                                 fg="#f5f6fa", command=lambda: switch_page(new_order_page()))
    button_new_order.pack(pady=20)

    button_back = tk.Button(master=page_frame, text="back", height=1, width=15, bg="#273c75", fg="#f5f6fa",
                            command=lambda: switch_page(client_page()))
    button_back.pack()

    return page_frame


def edit_order_page(order):

    page_frame = tk.Frame(bg="#f5f6fa")
    status = ('pending', 'Received', 'In Progress', 'Repaired/Completed')
    status_dict = {'pending': 0, 'Received': 1, 'In Progress': 2, 'Repaired/Completed': 3}

    label_title = tk.Label(master=page_frame, text="Edit Order", fg="#273c75", bg="#f5f6fa", font=title_font)
    label_title.pack(pady=30)

    frame_order = tk.Frame(master=page_frame, bg="#f5f6fa")

    frame_label = tk.Frame(master=frame_order, bg="#f5f6fa")

    labels = tk.Label(master=frame_label, text="Client Name:\n \nClient Number:\n \nVehicle Model:\n \nOrder State:\n \nDescription:\n \nprice:",
                      bg="#f5f6fa", fg="#273c75", font=sub_font, width=20, justify="left")

    labels.pack(padx=5, pady=5)
    frame_label.pack(side="left")

    frame_info = tk.Frame(master=frame_order, bg="#f5f6fa")
    label_name_info = tk.Label(master=frame_info, text=order.client.name, bg="#f5f6fa", fg="#273c75", font=sub_font)
    label_name_info.pack(padx=5, pady=5)
    label_number_info = tk.Label(master=frame_info, text=order.client.number, bg="#f5f6fa", fg="#273c75", font=sub_font)
    label_number_info.pack(padx=5, pady=5)
    label_model_info = tk.Label(master=frame_info, text=order.vehicle, bg="#f5f6fa", fg="#273c75", font=sub_font)
    label_model_info.pack(padx=5, pady=5)
    car_status = ttk.Combobox(master=frame_info, value=status, state='readonly', width=18, font=sub_font)
    car_status.current(status_dict.get(order.state))
    car_status.pack(padx=10, pady=7)
    label_desc_info = tk.Label(master=frame_info, text=order.description, bg="#f5f6fa", fg="#273c75", font=sub_font)
    label_desc_info.pack(padx=5, pady=5)
    entry_price = tk.Entry(master=frame_info, fg="#273c75", width=20, font=sub_font)
    entry_price.insert(0, order.price)
    entry_price.pack(padx=5, pady=7)
    frame_info.pack()

    frame_order.pack(padx=50, pady=5)

    frame_buttons = tk.Frame(master=page_frame, bg="#f5f6fa")

    button_edit = tk.Button(master=frame_buttons, text="Update order", height=2, width=15, bg="#273c75", fg="#f5f6fa",
                            command=lambda: update_order(order, car_status.get(), entry_price.get()))
    button_edit.pack(side="left", padx=10, pady=20)
    button_del = tk.Button(master=frame_buttons, text="delete order", height=2, width=15, bg="#273c75", fg="#f5f6fa",
                           command=lambda: remove_order(order))
    button_del.pack(side="right", padx=10, pady=20)

    frame_buttons.pack()

    button_back = tk.Button(master=page_frame, text="back", height=1, width=15, bg="#273c75", fg="#f5f6fa",
                            command=lambda: switch_page(admin_page()))
    button_back.pack(padx=10, pady=15)

    return page_frame


def order_deleted_page():
    page_frame = tk.Frame(bg="#f5f6fa")

    label_title = tk.Label(text="The order has been deleted successfully", font=title_font, master=page_frame,
                           bg="#f5f6fa", fg="#273c75")
    label_title.pack()

    button_back = tk.Button(master=page_frame, text="back to admin page", height=2, width=15, bg="#273c75",
                            fg="#f5f6fa", command=lambda: switch_page(admin_page()))
    button_back.pack(padx=10, pady=50)

    return page_frame

def contributors_page():

    background_image.set("images/empty.png")
    page_frame = tk.Frame(bg="#f5f6fa")
    label_title = tk.Label(text="Program Contributors", font=title_font, master=page_frame,
                           bg="#f5f6fa", fg="#273c75")
    label_title.pack()

    label_desc = tk.Label(text="Mohamed Sadiq,\nteam leader and in charge of user and order classes\n \n"
                               "\nRaed Al-Mizal,\nin charge of the program's functionality and stores customer data in an external file.\n \n"
                               "\nMuhammad Aref,\nin charge of the admin class and its interfaces.\n \n"
                               "\nMoamen Rabah,\nthe program's graphical user interface and wireframe developer\n \n"
                               "\nAbdullah Al-Attiyah,\nAssistant Graphical User Interface Developer", font=sub_font, master=page_frame,
                          bg="#f5f6fa", fg="#273c75" , justify="left" )
    label_desc.pack(pady=45)

    frame_buttons = tk.Frame(master=page_frame, bg="#f5f6fa")
    button_back = tk.Button(master=frame_buttons, text="back", width=15, bg="#273c75", fg="#f5f6fa", height=1,
                            command=lambda: switch_page(info_page_1()))
    button_back.pack(pady=10)

    frame_buttons.pack()
    return page_frame

def info_page_1():

    background_image.set("images/empty.png")
    page_frame = tk.Frame(bg="#f5f6fa")
    label_title = tk.Label(text="Program Description", font=title_font, master=page_frame,
                           bg="#f5f6fa", fg="#273c75")
    label_title.pack()

    label_desc = tk.Label(text="Our project is an application made for those who have car workshops.  It has two divided"
                               "\nsections, one for customers and one for admins. In the customers'  section, customers can"
                               "\nplace new orders and review all the orders that they have placed. In the admins' section,"
                               "\nadmins can review all orders from all the customers, change orders"
                               "\nstatus, and evaluate the price for orders.\n", font=sub_font, master=page_frame,
                          bg="#f5f6fa", fg="#273c75",)
    label_desc.pack(pady=50)

    frame_buttons = tk.Frame(master=page_frame, bg="#f5f6fa")
    button_back = tk.Button(master=frame_buttons, text="back", width=15, bg="#273c75", fg="#f5f6fa", height=2,
                            command=lambda: switch_page(main_page()))
    button_back.pack(side="left", padx=10)
    button_more = tk.Button(master=frame_buttons, text="See Contributors", width=15, bg="#273c75", fg="#f5f6fa",
                            height=2, command=lambda: switch_page(contributors_page()))
    button_more.pack(side="right", padx=10)
    frame_buttons.pack()

    return page_frame

