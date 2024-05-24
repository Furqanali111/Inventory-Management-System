import tkinter as tk
from tkinter import messagebox
import sqlite3
import os

# starting GUI
root = tk.Tk()
# giving name to application and setting its height and width
root.title("Inventory Stock System")
root.geometry("400x500")

# setting min and max size of the root window
root.minsize(450, 500)
root.maxsize(450, 500)

# creating frames
startwindow = tk.Frame(root)
adminlogin = tk.Frame(root)
admin_page = tk.Frame(root)
check_inventor = tk.Frame(root)
add_to_inventory = tk.Frame(root)
update_inventory = tk.Frame(root)
remove_inventory = tk.Frame(root)
customerlogin = tk.Frame(root)
customer_page = tk.Frame(root)
register_page = tk.Frame(root)
customer_check_inventory_page=tk.Frame(root)
view_cart=tk.Frame(root)
search_page=tk.Frame(root)
check_out=tk.Frame(root)
# database
db_file = 'warehouse.db'
#global variables
global customer_username,search_item

def startwindowfun():
    adminbut = tk.Button(startwindow, text="Admin Login", fg="black", height=2, width=20,
                         command=lambda: goto_admin_login(adminlogin))
    adminbut.pack(pady=20)
    customerbut = tk.Button(startwindow, text="Customer Login", fg="black", height=2, width=20,
                            command=lambda: goto_customer_login(customerlogin))
    customerbut.pack()

def goto_customer_login(frame):
    if startwindow.winfo_ismapped():  # if frame 1 is visible
        startwindow.pack_forget()  # hide frame 1
        customer_login_fun()
        frame.pack(pady=80, )  # show frame 2
    pass

def customer_login_fun():
    label_username = tk.Label(customerlogin, text='User Name:           ', font=("Arial", 11), justify='left', )
    label_username.grid(row=1, column=1)
    entry_username = tk.Entry(customerlogin)
    entry_username.grid(row=2, column=1, pady=(5, 15))

    label_password = tk.Label(customerlogin, text='Password:             ', font=("Arial", 11), justify='left')
    label_password.grid(row=3, column=1)
    entry_password = tk.Entry(customerlogin)
    entry_password.grid(row=4, column=1, pady=5)

    submit_button = tk.Button(customerlogin, text="Login", font=("Arial", 11), width=13, height=1,
                              command=lambda: login_customer(entry_username, entry_password))
    submit_button.grid(row=5, column=1, pady=10)

    register_button = tk.Button(customerlogin, text="Register", font=("Arial", 11), width=13, height=1,
                                command=goto_register_customer)
    register_button.grid(row=6, column=1, pady=10)

def goto_register_customer():
    # loading the registration form
    if customerlogin.winfo_ismapped():
        customerlogin.pack_forget()
        register_customer()
        register_page.pack(pady=10)

def register_customer():
    # creating label and entries boxes to register user
    label_name = tk.Label(register_page, text='Registration Form   ', font=("Arial", 11), justify='left')
    label_name.pack(anchor='center')

    label_name = tk.Label(register_page, text='Name:                     ', font=("Arial", 11), justify='left')
    label_name.pack()
    entry_name = tk.Entry(register_page)
    entry_name.pack(pady=5)

    label_phone = tk.Label(register_page, text='Phone Number:     ', font=("Arial", 11), justify='left')
    label_phone.pack()
    entry_phone = tk.Entry(register_page)
    entry_phone.pack(pady=5)

    label_email = tk.Label(register_page, text='Email Address:      ', font=("Arial", 11), justify='left')
    label_email.pack()
    entry_email = tk.Entry(register_page)
    entry_email.pack(pady=5)

    label_username = tk.Label(register_page, text='User Name:           ', font=("Arial", 11), justify='left', )
    label_username.pack()
    entry_username = tk.Entry(register_page)
    entry_username.pack(pady=(5, 15))

    label_password = tk.Label(register_page, text='Password:             ', font=("Arial", 11), justify='left')
    label_password.pack()
    entry_password = tk.Entry(register_page)
    entry_password.pack(pady=5)

    submit_but=tk.Button(register_page,text='Submit',font=("Arial",11),justify='left',width=15,height=1,
                         command=lambda :register(entry_name,entry_username,entry_phone,entry_password,entry_email))
    submit_but.pack(pady=5)
    submit_but=tk.Button(register_page,text='Go Back',font=("Arial",11),justify='left',width=15,height=1,command=go_back_to_customer_login)
    submit_but.pack(pady=5)

def register(name_en,username_en,phone_en,password_en,email_en):
    #getting values from the entry field
    name=name_en.get()
    username=username_en.get()
    phone=phone_en.get()
    password=password_en.get()
    email=email_en.get()
    # adding the login information of the user to the database
    if len(name) !=0 and len(username)!=0 and len(phone)!=0 and len(password)!=0 and len(email)!=0:
        phone=int(phone)
        conn.execute(
            "INSERT INTO customerlogin (name, phone_number, Email,user_name,password) VALUES (?,? ,? ,?,?)",(name,phone,email,username,password))
        go_back_to_customer_login()
    else:
        messagebox.showinfo("Error","Account not created try again")

def go_back_to_customer_login():
    if register_page.winfo_ismapped():
        register_page.pack_forget()
        for widget in register_page.winfo_children():
            widget.destroy()
        customer_login_fun()
        customerlogin.pack(pady=80)

def login_customer(username_en, password_en):
    global customer_username
    username = username_en.get()
    password = password_en.get()
    check = conn.execute('Select * FROM customerlogin WHERE user_name = ? And password = ?', (username, password))
    check12 = 0
    for x in check:
        check12 = x

    if check12:
        if customerlogin.winfo_ismapped():  # if frame 1 is visible
            customerlogin.pack_forget()  # hide frame 1
            customer_page_fun()
            customer_username = username
            customer_page.pack(pady=80)  # show frame 2
        pass
    else:
        messagebox.showinfo("Error", "Wrong username or password entered!")
    pass


def customer_page_fun():
    Check_inventory = tk.Button(customer_page, text="Check Inventory", width=20, height=2,
                                command=lambda :goto_customer_inventory_fun(customer_page))
    Check_inventory.pack(pady=15)
    Cart = tk.Button(customer_page, text="View Cart", width=20, height=2,command=goto_view_cart)
    Cart.pack()
    Search_item = tk.Button(customer_page, text="Search for item", width=20, height=2,command=go_to_search)
    Search_item.pack(pady=15)
    Check_out = tk.Button(customer_page, text="Check Out", width=20, height=2,command=go_to_checkout)
    Check_out.pack()

def go_to_checkout():
    if customer_page.winfo_ismapped():
        customer_page.pack_forget()
        check_out_fun()
        check_out.pack(fill="both",expand=True)

def check_out_fun():
    global customer_username
    head=tk.Label(check_out,text="CHECK OUT",font=("Arial",10))
    head.pack()

    order_items = conn.execute('SELECT id, menu_id,quantity, total_price FROM orders WHERE customer_username=?',
                               (customer_username,))

    # initializing the Canvas variable
    canvas = tk.Canvas(check_out)
    canvas.pack(side="left", fill="both", expand=True)
    # initializing the Scrollbar variable
    scrollbar = tk.Scrollbar(check_out, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    # configuring the Canvas
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    # initializing the inner frame variable
    inner_frame = tk.Frame(canvas)
    inner_frame.pack(fill="both", expand=True, padx=15)

    # creating the Canvas window
    canvas.create_window((0, 0), window=inner_frame, anchor="nw")

    # creating a label
    label_menu = tk.Label(inner_frame, text='Items')
    label_menu.pack(pady=2, anchor="center")
    # displaying data from the database on the screen
    totalprice=0.0
    for item in order_items:
        item_name = conn.execute('SELECT name FROM inventory WHERE id=?', (item[1],))
        for i in item_name:
            name_item = i
        label = tk.Label(inner_frame, text=f'{item[0]}. {name_item[0]} - {item[2]} - ${item[3]}')
        label.pack(pady=2, anchor="nw")
        totalprice+=float(item[3])

    labelpr=tk.Label(inner_frame,text="Total Price: ",font=("Arial",10))
    labelpr.pack(pady=2, anchor="nw")
    label_total_price=tk.Label(inner_frame,text=f"${totalprice}",font=("Arial",10))
    label_total_price.pack(pady=2, anchor="nw")

    check_out_but = tk.Button(inner_frame, text="Check out", fg="black", height=1, width=20, font=("Arial", 10),
                       command=lambda: check_out_fun2())
    check_out_but.pack(pady=7, anchor="nw")
    goback = tk.Button(inner_frame, text="GoBack", fg="black", height=1, width=20, font=("Arial", 10),
                       command=lambda: go_back_cuspage(check_out))
    goback.pack(pady=7, anchor="nw")

def check_out_fun2():
    order_items = conn.execute('DELETE FROM orders WHERE customer_username=?',
                               (customer_username,))
    messagebox.showinfo("Thank You","Do come back to buy more products")
    go_back_cuspage(check_out)
def go_to_search():
    # loading search paga
    if customer_page.winfo_ismapped():
        customer_page.pack_forget()
        search_fun()
        search_page.pack(fill="both",expand=True,pady=8,padx=5)

def search_fun():
    search_label=tk.Label(search_page,text="Enter Item name you want to search: ",font=("Arial",10))
    search_label.pack(padx=2,pady=3, anchor="nw")
    search_entry=tk.Entry(search_page)
    search_entry.pack(pady=3,padx=2, anchor="nw")

    search_button=tk.Button(search_page,text="Search",width=15,height=1,font=("Arial",10),command=lambda : search_fun2(search_entry.get()))
    search_button.pack(padx=2,pady=3, anchor="nw")

def search_fun2(search_name):
    global search_item
    search_item =search_name
    Search_items = conn.execute('SELECT id, name,Type, quantity,price FROM inventory WHERE name=?',
                               (search_name,))

    # initializing the Canvas variable
    canvas = tk.Canvas(search_page)
    canvas.pack(side="left", fill="both", expand=True)
    # initializing the Scrollbar variable
    scrollbar = tk.Scrollbar(search_page, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    # configuring the Canvas
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    # initializing the inner frame variable
    inner_frame = tk.Frame(canvas)
    inner_frame.pack(fill="both", expand=True, padx=15)

    # creating the Canvas window
    canvas.create_window((0, 0), window=inner_frame, anchor="nw")


    # displaying data from the database on the screen
    for item in Search_items:
        label = tk.Label(inner_frame, text=f'{item[0]}. {item[1]} - {item[2]} - {item[3]} - ${item[4]}')
        label.pack(pady=2, anchor="nw")

    lable = tk.Label(inner_frame, text="Enter id of item you want to buy: ", font=("Arial", 10))
    lable.pack(pady=5, anchor="nw")

    id_entry = tk.Entry(inner_frame)
    id_entry.pack(padx=5, anchor="nw")

    lable_quatntity = tk.Label(inner_frame,text="Enter quantity of item you want to buy: ",font=("Arial",10))
    lable_quatntity.pack(pady=5,anchor="nw")
    qun_entry=tk.Entry(inner_frame)
    qun_entry.pack(padx=5,anchor="nw")

    submit = tk.Button(inner_frame, text="Add to cart", fg="black", height=1, width=15,font=("Arial",11),
                       command=lambda: add_to_cart_search(id_entry.get(),qun_entry.get()))
    submit.pack(pady=10, anchor="nw")


    goback = tk.Button(inner_frame, text="GoBack", fg="black", height=1, width=15, font=("Arial", 10),
                       command=lambda: go_back_cuspage(search_page))
    goback.pack(pady=7, anchor="nw")

def add_to_cart_search(item_id,quantity=1):
    global customer_username
    Item_info = conn.execute('SELECT name,Type,quantity, price FROM inventory WHERE id = ?', (item_id))
    price = 0.0
    item_qun = 0
    for item in Item_info:
        price = item[3]
        item_qun = item[2]

    if int(item_qun) < int(quantity):
        messagebox.showinfo("Error", "Quantity of item is not available ")
        return
    else:
        price = float(price) * float(quantity)
        leftquantity = int(item_qun) - int(quantity)

    customer_info = conn.execute('SELECT phone_number FROM customerlogin WHERE user_name = ?',
                                 (str(customer_username),))
    for x in customer_info:
        phone_number = x[0]

    conn.execute("UPDATE inventory SET quantity = ? WHERE id = ?", (int(leftquantity), int(item_id)))

    conn.execute(
        "INSERT INTO orders (menu_id, quantity, total_price, customer_username,customer_phone) "
        "VALUES (?, ?, ?, ?,?)",
        (item_id, quantity, price, customer_username, phone_number)
    )
    gotosearchfun2()

def gotosearchfun2():
    if search_page.winfo_ismapped():
        for wid in search_page.winfo_children():
            wid.destroy()
        search_fun2(search_item)
        search_page.pack(fill="both",expand=True)

def goto_view_cart():
    if customer_page.winfo_ismapped():
        customer_page.pack_forget()
        view_cart_fun()
        view_cart.pack(fill="both",expand=True)

def view_cart_fun():
    global customer_username
    order_items = conn.execute('SELECT id, menu_id,quantity, total_price FROM orders WHERE customer_username=?',(customer_username,))

    # initializing the Canvas variable
    canvas = tk.Canvas(view_cart)
    canvas.pack(side="left", fill="both", expand=True)
    # initializing the Scrollbar variable
    scrollbar = tk.Scrollbar(view_cart, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    # configuring the Canvas
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    # initializing the inner frame variable
    inner_frame = tk.Frame(canvas)
    inner_frame.pack(fill="both", expand=True, padx=15)

    # creating the Canvas window
    canvas.create_window((0, 0), window=inner_frame, anchor="nw")

    # creating a label
    label_menu = tk.Label(inner_frame, text='INVENTORY')
    label_menu.pack(pady=2, anchor="center")
    # displaying data from the database on the screen
    for item in order_items:
        item_name=conn.execute('SELECT name FROM inventory WHERE id=?',(item[1],))
        for i in item_name:
            name_item=i
        label = tk.Label(inner_frame, text=f'{item[0]}. {name_item[0]} - {item[2]} - ${item[3]}')
        label.pack(pady=2, anchor="nw")

    goback = tk.Button(inner_frame, text="GoBack", fg="black", height=1, width=20,font=("Arial",10),
                       command=lambda: go_back_cuspage(view_cart))
    goback.pack(pady=7, anchor="nw")


def goto_customer_inventory_fun(frame):
    if frame.winfo_ismapped():
        frame.pack_forget()
        for widget in frame.winfo_children():
            widget.destroy()
        check_inventory_customer_fun()
        customer_check_inventory_page.pack(fill="both", expand=True, padx=5)

def check_inventory_customer_fun():
    # getting items from the inventory table from the database
    menu_items = conn.execute('SELECT id, name,Type,quantity, price FROM inventory')

    # initializing the Canvas variable
    canvas = tk.Canvas(customer_check_inventory_page)
    canvas.pack(side="left", fill="both", expand=True)
    # initializing the Scrollbar variable
    scrollbar = tk.Scrollbar(customer_check_inventory_page, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    # configuring the Canvas
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    # initializing the inner frame variable
    inner_frame = tk.Frame(canvas)
    inner_frame.pack(fill="both", expand=True, padx=15)

    # creating the Canvas window
    canvas.create_window((0, 0), window=inner_frame, anchor="nw")

    # creating a label
    label_menu = tk.Label(inner_frame, text='INVENTORY')
    label_menu.pack(pady=2, anchor="center")
    # displaying data from the database on the screen
    for item in menu_items:
        label = tk.Label(inner_frame, text=f'{item[0]}. {item[1]} - {item[2]} - {item[3]} - ${item[4]}')
        label.pack(pady=2, anchor="nw")

    lable = tk.Label(inner_frame,text="Enter id of item you want to buy: ",font=("Arial",11))
    lable.pack(pady=5,anchor="nw")

    id_entry=tk.Entry(inner_frame)
    id_entry.pack(padx=5,anchor="nw")


    lable_quatntity = tk.Label(inner_frame,text="Enter quantity of item you want to buy: ",font=("Arial",11))
    lable_quatntity.pack(pady=5,anchor="nw")

    qun_entry=tk.Entry(inner_frame)
    qun_entry.pack(padx=5,anchor="nw")


    submit = tk.Button(inner_frame, text="Add to cart", fg="black", height=1, width=20,font=("Arial",11),
                       command=lambda: add_to_cart(id_entry.get(),qun_entry.get()))
    submit.pack(pady=10, anchor="nw")

    # creating a go back fucntion
    goback = tk.Button(inner_frame, text="GoBack", fg="black", height=1, width=20,font=("Arial",11),
                       command=lambda: go_back_cuspage(customer_check_inventory_page))
    goback.pack(pady=7, anchor="nw")

def add_to_cart(item_id,quantity=1):
    global customer_username
    Item_info=conn.execute('SELECT name,Type,quantity, price FROM inventory WHERE id = ?',(item_id))
    price=0.0
    item_qun=0
    for item in Item_info:
        price=item[3]
        item_qun=item[2]

    if int(item_qun)<int(quantity):
        messagebox.showinfo("Error","Quantity of item is not available ")
        return
    else:
        price=float(price)*float(quantity)
        leftquantity=int(item_qun)-int(quantity)

    customer_info=conn.execute('SELECT phone_number FROM customerlogin WHERE user_name = ?',(str(customer_username),))
    for x in customer_info:
        phone_number=x[0]
    print(phone_number)
    conn.execute("UPDATE inventory SET quantity = ? WHERE id = ?", (int(leftquantity), int(item_id)))

    conn.execute(
        "INSERT INTO orders (menu_id, quantity, total_price, customer_username,customer_phone) "
        "VALUES (?, ?, ?, ?,?)",
        (item_id,quantity, price, customer_username,phone_number)
    )
    goto_customer_inventory_fun(customer_check_inventory_page)

def go_back_cuspage(Frame):
    if Frame.winfo_ismapped():
        for widget in Frame.winfo_children():
            widget.destroy()
        Frame.pack_forget()
        for widget in customer_page.winfo_children():
            widget.destroy()
        customer_page_fun()
        customer_page.pack(pady=80)

def goto_admin_login(frame):
    if startwindow.winfo_ismapped():  # if frame 1 is visible
        startwindow.pack_forget()  # hide frame 1
        admin_login_fun()
        frame.pack(pady=80)  # show frame 2

def admin_login_fun():
    label_username = tk.Label(adminlogin, text='User Name:           ', font=("Arial", 11), justify='left', )
    label_username.grid(row=1, column=1)
    entry_username = tk.Entry(adminlogin)
    entry_username.grid(row=2, column=1, pady=(5, 15))

    label_password = tk.Label(adminlogin, text='Password:             ', font=("Arial", 11), justify='left')
    label_password.grid(row=3, column=1)
    entry_password = tk.Entry(adminlogin)
    entry_password.grid(row=4, column=1, pady=5)

    submit_button = tk.Button(adminlogin, text="Login", font=("Arial", 11), width=13, height=1,
                              command=lambda: login_admin(entry_username, entry_password))
    submit_button.grid(row=5, column=1, pady=10)

def login_admin(username_en, password_en):
    username = username_en.get()
    password = password_en.get()
    check = conn.execute('Select * FROM adminlogin WHERE user_name = ? And password = ?', (username, password))
    check12 = 0
    for x in check:
        check12 = x

    if check12:
        if adminlogin.winfo_ismapped():  # if frame 1 is visible
            adminlogin.pack_forget()  # hide frame 1
            admin_page_fun()
            admin_page.pack(pady=80)  # show frame 2
        pass
    else:
        messagebox.showinfo("Error", "Wrong username or password entered!")

def admin_page_fun():
    Check_inventory = tk.Button(admin_page, text="Check Inventory", width=20, height=2,
                                command=goto_check_inventory_fun)
    Check_inventory.pack(pady=15)
    Add_to_inventory = tk.Button(admin_page, text="Add to Inventory", width=20, height=2,
                                 command=goto_Add_To_inventory_fun)
    Add_to_inventory.pack()
    update_inventory = tk.Button(admin_page, text="Update Inventory", width=20, height=2,
                                 command=goto_update_inventory_fun)
    update_inventory.pack(pady=15)
    remove_inventory = tk.Button(admin_page, text="Remove from Inventory", width=20, height=2,
                                 command=goto_remove_inventory_fun)
    remove_inventory.pack()

def goto_remove_inventory_fun():
    if admin_page.winfo_ismapped():
        admin_page.pack_forget()
        remove_inventory_fun()
        remove_inventory.pack(fill="both", expand=True, padx=5)


# removing items from inventory
def remove_inventory_fun():
    # creating a Canvas variable for the remove inventory frame
    canvas = tk.Canvas(remove_inventory)
    canvas.pack(side="left", fill="both", expand=True)

    # creating the Scroll barr variable for the update frame
    scrollbar = tk.Scrollbar(remove_inventory, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    # configuring the canvas
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    # initializing a inner frame so that we can scroll
    inner_frame = tk.Frame(canvas)
    inner_frame.pack(fill="both", expand=True)

    # initializing window for the canvas
    canvas.create_window((0, 0), window=inner_frame, anchor="nw")

    # creating a variable
    label = tk.Label(inner_frame, text='Remove From Inventory')
    label.pack(pady=2, anchor="center")

    # getting items from the database
    inventory_items = conn.execute('SELECT id, name,type, quantity,price FROM inventory')

    # displaying contents from the database on the screen
    for item in inventory_items:
        label = tk.Label(inner_frame, text=f'{item[0]}. {item[1]} - {item[2]} - {item[3]} - ${item[4]}')
        label.pack(pady=2, anchor="nw")

    # creating label and entry field
    label = tk.Label(inner_frame, text="Enter id of item you want to remove: ")
    label.pack(anchor="nw", pady=5, padx=2)
    ident = tk.Entry(inner_frame)
    ident.pack(anchor="nw", padx=5)

    # creating Button
    submit = tk.Button(inner_frame, text="Submit", fg="black", height=1, width=20,
                       command=lambda: remove_item_admin(ident))
    submit.pack(pady=10, padx=15, anchor="nw")

    goback = tk.Button(inner_frame, text="GoBack", fg="black", height=1, width=20,
                       command=lambda: go_back_adminpage(remove_inventory))
    goback.pack(pady=10, padx=15, anchor="nw")


def remove_item_admin(id_en):
    id = id_en.get()
    # deleting item from the database
    conn.execute('DELETE FROM inventory WHERE id = ?', (id,))
    go_back_adminpage(remove_inventory)

# changing frame
def goto_update_inventory_fun():
    if admin_page.winfo_ismapped():
        # forgeting the admin page and loading the update page
        admin_page.pack_forget()
        update_inventory_fun()
        update_inventory.pack(fill="both", expand=True, anchor="center")


# updating items in inventory
def update_inventory_fun():
    # creating a Canvas variable for the update frame
    canvas = tk.Canvas(update_inventory)
    canvas.pack(side="left", fill="both", expand=True)

    # creating the Scroll barr variable for the update frame
    scrollbar = tk.Scrollbar(update_inventory, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    # configuring the canvas
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    # initializing a inner frame so that we can scroll
    inner_frame = tk.Frame(canvas)
    inner_frame.pack(fill="both", expand=True)

    # initializing window for the canvas
    canvas.create_window((0, 0), window=inner_frame, anchor="nw")

    # creating a variable
    label = tk.Label(inner_frame, text='Update Inventory')
    label.pack(pady=2, anchor="center")

    # getting items from the database
    inventory_items = conn.execute('SELECT id, name,type, quantity,price FROM inventory')

    # displaying contents from the database on the screen
    for item in inventory_items:
        label = tk.Label(inner_frame, text=f'{item[0]}. {item[1]} - {item[2]} - {item[3]} - ${item[4]}')
        label.pack(pady=2, anchor="nw")

    # creating label and entry field
    label = tk.Label(inner_frame, text="Enter id of item you want to update: ")
    label.pack(anchor="nw", pady=5, padx=2)
    ident = tk.Entry(inner_frame)
    ident.pack(anchor="nw", padx=5)

    # creating label and entry field
    label = tk.Label(inner_frame, text="Enter new quantity:")
    label.pack(anchor="nw", padx=2)
    newqun = tk.Entry(inner_frame)
    newqun.pack(anchor="nw", padx=5)

    # creating Button
    submit = tk.Button(inner_frame, text="Submit", fg="black", height=1, width=20,
                       command=lambda: submit12(ident, newqun))
    submit.pack(pady=10, padx=15, anchor="nw")

    goback = tk.Button(inner_frame, text="GoBack", fg="black", height=1, width=20,
                       command=lambda: go_back_adminpage(update_inventory))
    goback.pack(pady=10, padx=15, anchor="nw")


def submit12(id_en, new_quan):
    id = id_en.get()
    quan = new_quan.get()
    # updating the database
    conn.execute("UPDATE inventory SET quantity = ? WHERE id = ?", (int(quan), int(id)))
    go_back_adminpage(update_inventory)


def goto_Add_To_inventory_fun():
    # loading the inventory frame
    if admin_page.winfo_ismapped():
        admin_page.pack_forget()
        Add_To_inventory_fun()
        add_to_inventory.pack(fill="both", expand=True, anchor="center")


def Add_To_inventory_fun():
    # creating label
    Head = tk.Label(add_to_inventory, text="ADD Item To Inventory", font=("Arial", 11))
    Head.pack(pady=5, anchor="center")

    # creating label and entry field
    label_name = tk.Label(add_to_inventory, text="Enter Item Name:", font=("Arial", 11), justify='right')
    label_name.pack(pady=5, padx=9, anchor="w")
    name_entry = tk.Entry(add_to_inventory)
    name_entry.pack(pady=3, padx=10, anchor="w")

    # creating label and entry field
    label_Type = tk.Label(add_to_inventory, text="Enter Item Type:", font=("Arial", 11), justify='right')
    label_Type.pack(pady=5, padx=9, anchor="w")
    Type_entry = tk.Entry(add_to_inventory)
    Type_entry.pack(pady=3, padx=10, anchor="w")

    # creating label and entry field
    label_Quantity = tk.Label(add_to_inventory, text="Enter Item Quantity:", font=("Arial", 11), justify='right')
    label_Quantity.pack(pady=5, padx=9, anchor="w")
    Quantity_entry = tk.Entry(add_to_inventory)
    Quantity_entry.pack(pady=3, padx=10, anchor="w")

    # creating label and entry field
    label_Price = tk.Label(add_to_inventory, text="Enter Item Price:", font=("Arial", 11), justify='right')
    label_Price.pack(pady=5, padx=9, anchor="w")
    Price_entry = tk.Entry(add_to_inventory)
    Price_entry.pack(pady=3, padx=10, anchor="w")

    # creating Buttons
    submit_button = tk.Button(add_to_inventory, text="Submit", font=("Arial", 10), width=15, height=1,
                              command=lambda: Add_item(name_entry, Type_entry, Quantity_entry, Price_entry))
    submit_button.pack(pady=5, padx=10, anchor="w")
    goback = tk.Button(add_to_inventory, text="Go Back", font=("Arial", 10), width=15, height=1,
                       command=lambda: go_back_adminpage(add_to_inventory))
    goback.pack(pady=5, padx=10, anchor="w")


def Add_item(name_en, type_en, quantity_en, price_en):
    # getting the value from the entry field
    name = name_en.get()
    type = type_en.get()
    quantity = quantity_en.get()
    price = price_en.get()
    # checking if the user have written something or not
    if len(name) != 0 and len(type) != 0 and len(quantity) != 0 and len(price) != 0:
        # inserting data into the database
        conn.execute(
            "INSERT INTO inventory (name, Type, quantity, price) "
            "VALUES (?, ?, ?, ?)",
            (name, type, quantity, price)
        )
    # going back to admin page
    go_back_adminpage(add_to_inventory)


def goto_check_inventory_fun():
    # loading the inventory frame
    if admin_page.winfo_ismapped():
        admin_page.pack_forget()
        check_inventory_fun()
        check_inventor.pack(fill="both", expand=True)


def check_inventory_fun():
    # getting items from the inventory table from the database
    menu_items = conn.execute('SELECT id, name,Type,quantity, price FROM inventory')

    # initializing the Canvas variable
    canvas = tk.Canvas(check_inventor)
    canvas.pack(side="left", fill="both", expand=True)
    # initializing the Scrollbar variable
    scrollbar = tk.Scrollbar(check_inventor, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    # configuring the Canvas
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    # initializing the inner frame variable
    inner_frame = tk.Frame(canvas)
    inner_frame.pack(fill="both", expand=True, padx=15)

    # creating the Canvas window
    canvas.create_window((0, 0), window=inner_frame, anchor="nw")

    # creating a label
    label_menu = tk.Label(inner_frame, text='INVENTORY')
    label_menu.pack(pady=2, anchor="center")
    # displaying data from the database on the screen
    for item in menu_items:
        label = tk.Label(inner_frame, text=f'{item[0]}. {item[1]} - {item[2]} - {item[3]} - ${item[4]}')
        label.pack(pady=2, anchor="nw")

    # creating a go back fucntion
    goback = tk.Button(inner_frame, text="GoBack", fg="black", height=1, width=20,
                       command=lambda: go_back_adminpage(check_inventor))
    goback.pack(pady=10, anchor="nw")


def go_back_adminpage(Frame):
    # loading the admin page and deleting the widget of the previous frame
    if Frame.winfo_ismapped():
        for widget in Frame.winfo_children():
            widget.destroy()
        Frame.pack_forget()
        admin_page.pack(pady=80)


# creating database
def createdatabase():
    # Create a table for the amdin login
    conn.execute('''CREATE TABLE IF NOT EXISTS adminlogin
                     (id INTEGER PRIMARY KEY,
                      user_name TEXT NOT NULL,
                      name Text,
                      phone_number REAL,
                      password TEXT)''')
    # Insert data into the Adminlogin table
    conn.execute(
        "INSERT INTO adminlogin (user_name, name, phone_number,password) VALUES ('admin', 'Tester', +945852682,'112233')")

    # creating customerlogin table
    conn.execute('''CREATE TABLE IF NOT EXISTS customerlogin
                     (id INTEGER PRIMARY KEY,
                      name Text,
                      phone_number INT,
                      Email Text,
                      user_name TEXT NOT NULL,
                      password TEXT)''')

    # creating inventory table
    conn.execute('''CREATE TABLE IF NOT EXISTS inventory
                     (id INTEGER PRIMARY KEY,
                      name TEXT NOT NULL,
                      Type TEXT,
                      quantity INT,
                      price REAL NOT NULL)''')

    # Insert data into the inventory table
    conn.execute(
        "INSERT INTO inventory (name, Type, quantity, price) VALUES ('Turkey Club Sandwich', 'Food', 5, 7.99)")
    conn.execute(
        "INSERT INTO inventory (name, Type, quantity, price) VALUES ('Classic Cheese Sandwich', 'Food', 6, 5.99)")
    conn.execute(
        "INSERT INTO inventory (name, Type, quantity, price) VALUES ('TV', 'Electronics', 7, 6.99)")
    conn.execute(
        "INSERT INTO inventory (name, Type, quantity, price) VALUES ('Computer', 'Electronic',200, 8.99)")
    conn.execute("INSERT INTO inventory (name, Type, quantity, price) VALUES ('Gloves', 'Wearables',150, 1.99)")
    conn.execute("INSERT INTO inventory (name, Type, quantity, price) VALUES ('Shorts', 'Wearables',160, 0.99)")

    # creating order table
    conn.execute('''CREATE TABLE IF NOT EXISTS orders
                     (id INTEGER PRIMARY KEY,
                      menu_id INTEGER NOT NULL,
                      quantity INTEGER NOT NULL,
                      total_price REAL NOT NULL,
                      customer_username TEXT NOT NULL,
                      customer_phone TEXT NOT NULL
                      )''')


if __name__ == "__main__":
    startwindowfun()
    if not os.path.isfile(db_file):
        conn = sqlite3.connect(db_file)
        createdatabase()
    else:
        conn = sqlite3.connect(db_file)

    startwindow.pack(pady=150)
    root.mainloop()
    conn.commit()
    conn.close()
