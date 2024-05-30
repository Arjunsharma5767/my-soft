from tkinter import *
from tkinter import ttk, messagebox
import sqlite3

class Supplier:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1400x900+0+0")
        self.root.title("Inventory Management System | Developed by Arjun")
        self.root.config(bg="#f0f0f0")
        self.root.focus_force()

        # Variables
        self.var_sup_invoice = StringVar()
        self.var_contact = StringVar()
        self.var_name = StringVar()
        self.var_description = StringVar()
        self.var_search = StringVar()
        self.var_search_text = StringVar()

        # Search frame
        self.search_frame = LabelFrame(self.root, text="Search Supplier", font=("Arial", 12, "bold"), bd=2, relief=RIDGE, bg="#e6e6e6")
        self.search_frame.place(x=722, y=60, width=595, height=70)

        # Search options
        lbl_search = Label(self.search_frame, text="Search by Invoice:", bg="#e6e6e6", font=("Arial", 12))
        lbl_search.place(x=10, y=9)

        txt_search = Entry(self.search_frame, textvariable=self.var_search_text, font=("Arial", 12), bg="white", bd=2, relief=GROOVE)
        txt_search.place(x=160, y=10, width=200)

        btn_search = Button(self.search_frame, text="Search", command=self.search_Supplier, font=("Arial", 12), bg="#4CAF50", fg="white", bd=2, relief=RAISED, cursor="hand2")
        btn_search.place(x=370, y=10, width=80, height=30)

        btn_see_all = Button(self.search_frame, text="See All", command=self.show_Suppliers, font=("Arial", 12), bg="#607d8b", fg="white", bd=2, relief=RAISED, cursor="hand2")
        btn_see_all.place(x=460, y=10, width=80, height=30)

        # Title
        title = Label(self.root, text="Supplier Details", font=("Arial", 20, "bold"), bg="#0f4d7d", fg="white")
        title.place(x=50, y=10, width=1275,height=40)

        # Input fields
        # Row1
        lbl_Supplier_invoice = Label(self.root, text="Invoice No:", font=("Arial", 12), bg="#f0f0f0")
        lbl_Supplier_invoice.place(x=50, y=100)
        txt_Supplier_invoice = Entry(self.root, textvariable=self.var_sup_invoice, font=("Arial", 12), bg="white", bd=2, relief=GROOVE)
        txt_Supplier_invoice.place(x=200, y=100, width=180)

        # Row2
        lbl_name = Label(self.root, text="Name:", font=("Arial", 12), bg="#f0f0f0")
        lbl_name.place(x=50, y=150)
        txt_name = Entry(self.root, textvariable=self.var_name, font=("Arial", 12), bg="white", bd=2, relief=GROOVE)
        txt_name.place(x=200, y=150, width=180)

        # Row3
        lbl_contact = Label(self.root, text="Contact:", font=("Arial", 12), bg="#f0f0f0")
        lbl_contact.place(x=50, y=200)
        txt_contact = Entry(self.root, textvariable=self.var_contact, font=("Arial", 12), bg="white", bd=2, relief=GROOVE)
        txt_contact.place(x=200, y=200, width=200)

        # Row4
        lbl_description = Label(self.root, text="Description:", font=("Arial", 12), bg="#f0f0f0")
        lbl_description.place(x=50, y=250)
        self.txt_description = Text(self.root, font=("Arial", 12), bg="white", bd=2, relief=GROOVE, height=5)
        self.txt_description.place(x=200, y=250, width=350,height=190)

        # Description scrollbar
        scrollbar = Scrollbar(self.root, command=self.txt_description.yview)
        scrollbar.place(x=600, y=290, height=140)
        self.txt_description.config(yscrollcommand=scrollbar.set)

        # Buttons
        btn_add = Button(self.root, text="Save", command=self.add_Supplier, font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", bd=2, relief=RAISED, cursor="hand2")
        btn_add.place(x=100, y=500, width=100, height=30)
        btn_update = Button(self.root, text="Update", command=self.update_Supplier, font=("Arial", 12, "bold"), bg="#FFC107", fg="black", bd=2, relief=RAISED, cursor="hand2")
        btn_update.place(x=225, y=500, width=100, height=30)
        btn_delete = Button(self.root, text="Delete", command=self.confirm_delete_Supplier, font=("Arial", 12, "bold"), bg="#f44336", fg="white", bd=2, relief=RAISED, cursor="hand2")
        btn_delete.place(x=350, y=500, width=100, height=30)
        btn_clear = Button(self.root, text="Clear", command=self.clear, font=("Arial", 12, "bold"), bg="#607d8b", fg="white", bd=2, relief=RAISED, cursor="hand2")
        btn_clear.place(x=475, y=500, width=100, height=30)

        # Supplier Details
        sup_frame = Frame(self.root, bd=3, relief=RIDGE, bg="#f0f0f0")
        sup_frame.place(x=722, y=150, width=600, height=400)

        # Vertical scrollbar
        scrolly = Scrollbar(sup_frame, orient=VERTICAL)
        scrolly.pack(side=RIGHT, fill=Y)

        # Horizontal scrollbar
        scrollx = Scrollbar(sup_frame, orient=HORIZONTAL)
        scrollx.pack(side=BOTTOM, fill=X)

        # Treeview widget
        self.Supplier_table = ttk.Treeview(sup_frame, columns=("invoice", "contact", "name", "desc"), xscrollcommand=scrollx.set, yscrollcommand=scrolly.set)

        # Column headings
        self.Supplier_table["show"] = "headings"
        self.Supplier_table.heading("invoice", text="Invoice")
        self.Supplier_table.heading("contact", text="Contact")
        self.Supplier_table.heading("name", text="Name")
        self.Supplier_table.heading("desc", text="Description")
        self.Supplier_table.pack(fill=BOTH, expand=1)
        self.Supplier_table.bind("<ButtonRelease-1>", self.get_data)

        # Column widths
        columns = ["invoice", "contact", "name", "desc"]
        widths = [100, 100, 150, 300]
        for col, width in zip(columns, widths):
            self.Supplier_table.column(col, width=width)

        # Scrollbars
        scrolly.config(command=self.Supplier_table.yview)
        scrollx.config(command=self.Supplier_table.xview)

        # Pack Treeview widget
        self.Supplier_table.pack(fill=BOTH, expand=1)

        self.show_Suppliers()

    def add_Supplier(self):
        con = sqlite3.connect(database=r'IMS.db')
        cur = con.cursor()
        try:
            if self.var_sup_invoice.get() == "":
                messagebox.showerror("Error", "Invoice must be required", parent=self.root)
            else:
                cur.execute("SELECT * FROM Supplier WHERE invoice=?", (self.var_sup_invoice.get(),))
                row = cur.fetchone()
                if row is not None:
                    messagebox.showerror("Error", "This invoice number already assigned, try a different one", parent=self.root)
                else:
                    cur.execute("INSERT INTO Supplier (invoice, contact, name, desc) VALUES (?,?,?,?)", (
                        self.var_sup_invoice.get(),
                        self.var_contact.get(),
                        self.var_name.get(),
                        self.txt_description.get('1.0', END),
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Supplier Added Successfully", parent=self.root)
                    self.show_Suppliers()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def show_Suppliers(self):
        con = sqlite3.connect(database=r'IMS.db')
        cur = con.cursor()
        try: 
            cur.execute("SELECT * FROM Supplier")
            rows = cur.fetchall()
            self.Supplier_table.delete(*self.Supplier_table.get_children())
            for row in rows:
                self.Supplier_table.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def get_data(self, event):
        try:
            f = self.Supplier_table.focus()
            content = (self.Supplier_table.item(f))
            row = content['values']
            self.var_sup_invoice.set(row[0])
            self.var_contact.set(row[1])
            self.var_name.set(row[2])
            self.txt_description.delete('1.0', END)
            self.txt_description.insert(END, row[3])
        except Exception as ex:
            messagebox.showerror("Error", f"Error while getting data: {str(ex)}", parent=self.root)

    def update_Supplier(self):
        con = sqlite3.connect(database=r'IMS.db')
        cur = con.cursor()
        try:
            if self.var_sup_invoice.get()=="":
                messagebox.showerror("Error","Invoice number must be required",parent=self.root)
            cur.execute("UPDATE Supplier SET contact=?, name=?, desc=? WHERE invoice=?", (
                self.var_contact.get(),
                self.var_name.get(),
                self.txt_description.get('1.0', END),
                self.var_sup_invoice.get(),
            ))
            con.commit()
            messagebox.showinfo("Success", "Supplier Updated Successfully", parent=self.root)
            self.show_Suppliers()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def confirm_delete_Supplier(self):
        result = messagebox.askquestion("Delete Supplier", "Are you sure you want to delete this Supplier?", icon='warning')
        if result == 'yes':
            self.delete_Supplier()

    def delete_Supplier(self):
        con = sqlite3.connect(database=r'IMS.db')
        cur = con.cursor()
        try:
            if self.var_sup_invoice.get() == "":
                messagebox.showerror("Error", "Supplier ID must be required", parent=self.root)
            else:
                cur.execute("DELETE FROM Supplier WHERE invoice=?", (self.var_sup_invoice.get(),))
                con.commit()
                messagebox.showinfo("Success", "Supplier Deleted Successfully", parent=self.root)
                self.show_Suppliers()
                self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def search_Supplier(self):
        con = sqlite3.connect(database=r'IMS.db')
        cur = con.cursor()
        try:
            if self.var_search_text.get() == "":
                messagebox.showerror("Error", "Please enter text to search", parent=self.root)
            else:
                cur.execute(f"SELECT * FROM Supplier WHERE invoice LIKE '%{self.var_search_text.get()}%'")
                rows = cur.fetchall()
                if len(rows) != 0:
                    self.Supplier_table.delete(*self.Supplier_table.get_children())
                    for row in rows:
                        self.Supplier_table.insert('', END, values=row)
                else:
                    messagebox.showinfo("Info", "No record found", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def clear(self):
        self.var_sup_invoice.set("")
        self.var_contact.set("")
        self.var_name.set("")
        self.txt_description.delete('1.0', END)

if __name__ == "__main__":
    root = Tk() 
    obj = Supplier(root)
    root.mainloop()
