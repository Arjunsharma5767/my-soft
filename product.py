from tkinter import *
from tkinter import ttk, messagebox
import sqlite3

class Product:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1400x900+0+0")
        self.root.title("Inventory Management System | Developed by Arjun")
        self.root.config(bg="white")
        self.root.focus_force()
        
        #variables
        self.var_cat = StringVar()
        self.var_supplier = StringVar()
        self.cat_list=[]
        self.sup_list=[]
        self.var_name = StringVar()
        self.var_price = StringVar()
        self.var_qty = StringVar()
        self.var_status = StringVar()
        self.var_search = StringVar()
        self.var_search_text = StringVar()
        self.fetch_cat_sup()

        # Product frame
        self.Product_Frame = Frame(self.root, bd=3, relief=RIDGE)
        self.Product_Frame.place(x=47, y=40, width=500, height=620)

        # Title
        title = Label(self.root, text="Stock Details", font=("Arial", 15, "bold"), bg="#0f4d7d", fg="white")
        title.place(x=55, y=5, width=1250)
        
        labels = [("Category", 50), ("Supplier", 150), ("Product Name", 250), ("Price (single item)", 350), ("Quantity", 450), ("Status", 550)]
        
        for lbl_text, y_pos in labels:
            lbl = Label(self.root, text=lbl_text, font=("Arial", 15, "bold"))
            lbl.place(x=55, y=y_pos)
        
        # entry
        cmb_cat = ttk.Combobox(self.Product_Frame, textvariable=self.var_cat, values=self.cat_list, state='readonly',
                        justify=CENTER, font=("Arial", 12))
        cmb_cat.place(x=200, y=30, width=200, height=30)
        if self.cat_list:
            cmb_cat.current(0 if len(self.cat_list) > 0 else -1)

        cmb_sup = ttk.Combobox(self.Product_Frame, textvariable=self.var_supplier, values=self.sup_list, state='readonly',
                        justify=CENTER, font=("Arial", 12))
        cmb_sup.place(x=200, y=120, width=200, height=30)
        if self.sup_list:
            cmb_sup.current(0 if len(self.sup_list) > 0 else -1)


        txt_name = Entry(self.root, textvariable=self.var_name, font=("Arial", 15, "bold"), bg="lightyellow" )
        txt_name.place(x=230, y=250)

        txt_price = Entry(self.root, textvariable=self.var_price, font=("Arial", 15, "bold"), bg="lightyellow" )
        txt_price.place(x=230, y=350)

        txt_quantity = Entry(self.root, textvariable=self.var_qty, font=("Arial", 15, "bold"), bg="lightyellow" )
        txt_quantity.place(x=230, y=450)

        cmb_status = ttk.Combobox(self.Product_Frame, textvariable=self.var_status, values=("Active","Inactive"),
                                    state='readonly', justify=CENTER, font=("Arial", 12))
        cmb_status.place(x=200, y=500 ,width=200,height=30)              
        cmb_status.current(0)

        # Buttons
        btn_add = Button(self.Product_Frame, text="Save", command=self.add_product, font=("Arial", 12, "bold"),
                            bg="#2196f3", fg="white", cursor="hand2")
        btn_add.place(x=10, y=550, width=100, height=40)
        
        btn_update = Button(self.Product_Frame, text="Update", command=self.update_product, font=("Arial", 12, "bold"),
                                bg="#4caf50", fg="white", cursor="hand2")
        btn_update.place(x=120, y=550, width=100, height=40)
        
        btn_delete = Button(self.Product_Frame, text="Delete", command=self.confirm_delete, font=("Arial", 12, "bold"),
                                bg="#f44336", fg="white", cursor="hand2")
        btn_delete.place(x=230, y=550, width=100, height=40)
        
        btn_clear = Button(self.Product_Frame, text="Clear", command=self.clear, font=("Arial", 12, "bold"),
                                bg="#607d8b", fg="white", cursor="hand2")
        btn_clear.place(x=340, y=550, width=100, height=40)
        
        # Search frame
        self.search_frame = LabelFrame(self.root, text="Search Product", font=("Arial", 12, "bold"), bd=2, relief=RIDGE, bg="light yellow")
        self.search_frame.place(x=560, y=40, width=744, height=80 )

        # Options
        cmb_search = ttk.Combobox(self.search_frame, textvariable=self.var_search, values=("select", "pid", "category", "supplier", "name"), state='readonly', justify=CENTER, font=("Arial", 12))
        cmb_search.place(x=10, y=9, width=180)
        cmb_search.current(0)

        txt_search = Entry(self.search_frame, textvariable=self.var_search_text, font=("Arial", 12), bg="white")
        txt_search.place(x=200, y=10)

        btn_search = Button(self.search_frame, text="Search", command=self.search_product, font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", cursor="hand2")
        btn_search.place(x=410, y=10, width=150, height=30)
        # Product Details
        p_frame = Frame(self.root, bd=3, relief=RIDGE, bg="white")
        p_frame.place(x=560, y=120, width=745, height=542)

        # Create vertical scrollbar
        scrolly = Scrollbar(p_frame, orient=VERTICAL)
        scrolly.pack(side=RIGHT, fill=Y)

        # Create horizontal scrollbar
        scrollx = Scrollbar(p_frame, orient=HORIZONTAL)
        scrollx.pack(side=BOTTOM, fill=X)

        # Create the Treeview widget
        self.product_table = ttk.Treeview(p_frame, columns=("pid", "category", "supplier", "name", "price", "quantity", "status", "total_cost"), xscrollcommand=scrollx.set, yscrollcommand=scrolly.set)

        # Set column headings
        self.product_table["show"] = "headings"
        self.product_table.heading("pid", text="Pid")
        self.product_table.heading("category", text="Category")
        self.product_table.heading("supplier", text="Supplier")
        self.product_table.heading("name", text="Product Name")
        self.product_table.heading("price", text="Price")
        self.product_table.heading("quantity", text="Quantity")
        self.product_table.heading("status", text="Status")
        self.product_table.heading("total_cost", text="Total Cost")
        self.product_table.pack(fill=BOTH,expand=1)
        self.product_table.bind("<ButtonRelease-1>", self.get_data) 
        # Set column widths
        columns = ["pid", "category", "supplier", "name", "price", "quantity", "status", "total_cost"]
        widths = [50, 150, 150, 200, 100, 100, 100, 100]
        for col, width in zip(columns, widths):
            self.product_table.column(col, width=width)

        # Attach scrollbars
        scrolly.config(command=self.product_table.yview)
        scrollx.config(command=self.product_table.xview)

        # Pack the Treeview widget
        self.product_table.pack(fill=BOTH, expand=1)
        self.show_products()

        # Show All button
        btn_show_all = Button(self.search_frame, text="Show All", command=self.show_products, font=("Arial", 12, "bold"), bg="#2196f3", fg="white", cursor="hand2")
        btn_show_all.place(x=570, y=10, width=150, height=30)
       
    def fetch_cat_sup(self):
        try:
            con = sqlite3.connect(database=r'IMS.db')
            cur = con.cursor()
            cur.execute("SELECT name FROM category")
            cat = cur.fetchall()
            if len(cat) > 0:
                self.cat_list = ["select"] + [i[0] for i in cat]
                
            cur.execute("SELECT name FROM supplier")
            sup = cur.fetchall()
            if len(sup) > 0:
                self.sup_list = ["select"] + [i[0] for i in sup]
            
            con.close()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        
    def add_product(self):
        try:
            if self.var_name.get() == "":
                messagebox.showerror("Error", "Product name must be required", parent=self.root)
            else:
                con = sqlite3.connect(database=r'IMS.db')
                cur = con.cursor()
                cur.execute("INSERT INTO products (category, supplier, name, price, quantity, status) VALUES (?,?,?,?,?,?)", (
                    self.var_cat.get(),
                    self.var_supplier.get(),
                    self.var_name.get(),
                    self.var_price.get(),
                    self.var_qty.get(),
                    self.var_status.get()
                ))
                con.commit()
                con.close()
                messagebox.showinfo("Success", "Product Added Successfully", parent=self.root)
                self.show_products()  # Update the product list
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def update_product(self):
        try:
            if self.var_name.get() == "":
                messagebox.showerror("Error", "Product name must be required", parent=self.root)
            else:
                con = sqlite3.connect(database=r'IMS.db')
                cur = con.cursor()
                cur.execute("UPDATE products SET category=?, supplier=?, price=?, quantity=?, status=? WHERE name=?", (
                    self.var_cat.get(),
                    self.var_supplier.get(),
                    self.var_price.get(),
                    self.var_qty.get(),
                    self.var_status.get(),
                    self.var_name.get()
                ))
                con.commit()
                con.close()
                messagebox.showinfo("Success", "Product Updated Successfully", parent=self.root)
                self.show_products()  # Update the product list
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def confirm_delete(self):
        result = messagebox.askyesno("Delete Confirmation", "Are you sure you want to delete this product?")
        if result:
            self.delete_product()

    def delete_product(self):
        try:
            if self.var_name.get() == "":
                messagebox.showerror("Error", "Product name must be required", parent=self.root)
            else:
                con = sqlite3.connect(database=r'IMS.db')
                cur = con.cursor()
                cur.execute("DELETE FROM products WHERE name=?", (self.var_name.get(),))
                con.commit()
                con.close()
                messagebox.showinfo("Success", "Product Deleted Successfully", parent=self.root)
                self.show_products()  # Update the product list
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def clear(self):
        self.var_cat.set("select")
        self.var_supplier.set("select")
        self.var_name.set("")
        self.var_price.set("")
        self.var_qty.set("")
        self.var_status.set("")

    def search_product(self):
        try:
            if self.var_search.get() == "select" or self.var_search_text.get() == "":
                messagebox.showerror("Error", "Please select search filter and enter text to search", parent=self.root)
            else:
                con = sqlite3.connect(database=r'IMS.db')
                cur = con.cursor()
                cur.execute(f"SELECT * FROM products WHERE {self.var_search.get()} LIKE ?", ('%' + self.var_search_text.get() + '%',))
                rows = cur.fetchall()
                con.close()
                if len(rows) != 0:
                    for item in self.product_table.get_children():
                        self.product_table.delete(item)
                    for row in rows:
                        total_cost = float(row[4]) * float(row[5])
                        self.product_table.insert('', END, values=row + (total_cost,))
                else:
                    messagebox.showinfo("Info", "No record found", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def show_products(self):
        try:
            con = sqlite3.connect(database=r'IMS.db')
            cur = con.cursor()
            cur.execute("SELECT * FROM products")
            rows = cur.fetchall()
            con.close()
            if rows:
                for item in self.product_table.get_children():
                    self.product_table.delete(item)
                for row in rows:
                    total_cost = float(row[4]) * float(row[5])
                    self.product_table.insert('', END, values=row + (total_cost,))
            else:
                messagebox.showinfo("Info", "No records found", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def get_data(self, event):
        try:
            item = self.product_table.selection()[0]
            data = self.product_table.item(item, "values")
            if data:
                self.var_cat.set(data[1])
                self.var_supplier.set(data[2])
                self.var_name.set(data[3])
                self.var_price.set(data[4])
                self.var_qty.set(data[5])
                self.var_status.set(data[6])
            else:
                messagebox.showerror("Error", "Please select a valid row", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

if __name__ == "__main__":
    root = Tk()
    obj = Product(root)
    root.mainloop()
