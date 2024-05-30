from tkinter import *
from PIL import Image, ImageTk
import time
import sqlite3
from tkinter import messagebox
from employee import Employee
from supplier import Supplier
from category import Category
from product import Product
import sys
import os
import database

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class IMS:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1400x700+0+0")
        self.root.title("Store Management System | developed by Arjun")
        self.root.config(bg="white")
        self.image_folder = 'images'

        # Load images
        try:
            self.icon_title = PhotoImage(file=resource_path("images/img1.png"))
            self.icon_menu = Image.open(resource_path("images/img2.png"))
            self.icon_menu = self.icon_menu.resize((100, 150))
            self.icon_menu = ImageTk.PhotoImage(self.icon_menu)
            self.icon_side = PhotoImage(file=resource_path("images/img3.gif"))
        except FileNotFoundError as e:
            messagebox.showerror("Image Load Error", f"Failed to load images: {e}", parent=self.root)
        
        # Title Label
        
        title = Label(self.root, text=" Store Management System ", image=self.icon_title, compound=LEFT, font=("forte", 20, "bold"), bg="#010C48", fg="white", anchor="w", padx=20)
        title.place(x=0, y=0, relwidth=1, height=40)
        title = Label(self.root, text="       Government polytechnic college Jammu",  compound=LEFT, font=("forte", 20, "bold"), bg="#010C48", fg="white", anchor="w", padx=20)
        title.place(x=0, y=35, relwidth=1, height=40)
        # Clock
        self.lbl_clock = Label(self.root, text="", font=("times new roman", 15), bg="#4d636d", fg="white")
        self.lbl_clock.place(x=0, y=75, height=40, relwidth=1)
        
        # Left Menu
        self.create_left_menu()
        
        # Content Labels
        self.lbl_employee = Label(self.root, text="Total Employee \n [0]", bd=5, relief=RIDGE, bg="#33bbf9", fg="white", font=("goudy old style", 20, "bold"))
        self.lbl_employee.place(x=300, y=120, height=150, width=300)
        
        self.lbl_supplier = Label(self.root, text="Total Supplier \n [0]", bd=5, relief=RIDGE, bg="#ff5722", fg="white", font=("goudy old style", 20, "bold"))
        self.lbl_supplier.place(x=650, y=120, height=150, width=300)
        
        self.lbl_category = Label(self.root, text="Total category \n [0]", bd=5, relief=RIDGE, bg="pink", fg="white", font=("goudy old style", 20, "bold"))
        self.lbl_category.place(x=1000, y=120, height=150, width=300)
        
        self.lbl_product = Label(self.root, text="Total product \n [0]", bd=5, relief=RIDGE, bg="#607d8b", fg="white", font=("goudy old style", 20, "bold"))
        self.lbl_product.place(x=300, y=300, height=150, width=300)
        
        # Footer Label
        self.lbl_footer = Label(self.root, text="SMS STORE MANAGEMENT SYSTEM | DEVELOPED BY ARJUN \n FOR ANY TECHNICAL ISSUE CONTACT 6005499159 ", font=("times new roman", 12), bg="#4d636d", fg="white")
        self.lbl_footer.pack(side=BOTTOM, fill=X)
        
        self.update_clock()
        self.update_content()
    
    def update_clock(self):
        current_time = time.strftime('%H:%M:%S %p')
        current_date = time.strftime('%d-%m-%Y')
        self.lbl_clock.config(text=f"Welcome to Store Management System \t\t Date: {current_date} \t\t Time: {current_time}")
        self.lbl_clock.after(1000, self.update_clock)
    
    def create_left_menu(self):
        # Left Menu Logo
        left_menu = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        left_menu.place(x=0, y=115, width=200, height=700)
        lbl_menu_logo = Label(left_menu, image=self.icon_menu)
        lbl_menu_logo.pack(side=TOP, fill=X)
        
        # Menu Label
        lbl_menu = Label(left_menu, text="Menu", font=("times new roman", 20, "bold"), bg="green")
        lbl_menu.pack(side=TOP, fill=X)
        
        # Menu Buttons
        btn_employee = Button(left_menu, text="Employee", command=self.employee_window, image=self.icon_side, compound=LEFT, padx=5, anchor=W, font=("times new roman", 20, "bold"), bg="White", bd=3, cursor="hand2")
        btn_employee.pack(side=TOP, fill=X)
        
        btn_category = Button(left_menu, text="Category", command=self.category_window, image=self.icon_side, compound=LEFT, padx=5, anchor=W, font=("times new roman", 20, "bold"), bg="White", bd=3, cursor="hand2")
        btn_category.pack(side=TOP, fill=X)
        
        btn_supplier = Button(left_menu, text="Supplier", command=self.supplier_window, image=self.icon_side, compound=LEFT, padx=5, anchor=W, font=("times new roman", 20, "bold"), bg="White", bd=3, cursor="hand2")
        btn_supplier.pack(side=TOP, fill=X)
        
        btn_product = Button(left_menu, text="Product", command=self.product_window, image=self.icon_side, compound=LEFT, padx=5, anchor=W, font=("times new roman", 20, "bold"), bg="White", bd=3, cursor="hand2")
        btn_product.pack(side=TOP, fill=X)
    
    def employee_window(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = Employee(self.new_win)
    
    def category_window(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = Category(self.new_win)
    
    def supplier_window(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = Supplier(self.new_win)
    
    def product_window(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = Product(self.new_win)
    
    def update_content(self):
        try:
            # Connect to the database
            con = sqlite3.connect(resource_path(r'IMS.db'))
            cur = con.cursor()
            
            # Fetch data for employees
            cur.execute("SELECT COUNT(*) FROM employee")
            total_employees = cur.fetchone()[0]
            self.lbl_employee.config(text=f'Total Employee \n [{total_employees}]')
            
            # Fetch data for suppliers
            cur.execute("SELECT COUNT(*) FROM supplier")
            total_suppliers = cur.fetchone()[0]
            self.lbl_supplier.config(text=f'Total Supplier \n [{total_suppliers}]')
            
            # Fetch data for categories
            cur.execute("SELECT COUNT(*) FROM category")
            total_categories = cur.fetchone()[0]
            self.lbl_category.config(text=f'Total category \n [{total_categories}]')
            
            # Fetch data for products
            cur.execute("SELECT COUNT(*) FROM products")
            total_products = cur.fetchone()[0]
            self.lbl_product.config(text=f'Total product \n [{total_products}]')
            
        except sqlite3.Error as e:
            # Display error message if database access fails
            messagebox.showerror("Database Error", f"Error accessing database: {e}", parent=self.root)
        finally:
            # Close the database connection
            if con:
                con.close()
        
        # Schedule the update_content method to run every 1000 milliseconds (1 second)
        self.root.after(1000, self.update_content)

if __name__ == "__main__":
    import database
    root = Tk()
    obj = IMS(root)
    root.mainloop()
