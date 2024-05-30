from tkinter import *
from tkinter import ttk, messagebox
import sqlite3

class Employee:
    def __init__(self, root):
        self.root = root
        
        self.root.title("Inventory Management System | developed by Arjun")
        self.root.config(bg="white")
        self.root.geometry("1400x900+0+0")
        self.root.focus_force()

        # Get screen width and height
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        

        # All variables
        self.var_emp_id = StringVar()
        self.var_gender = StringVar()  
        self.var_contact = StringVar()
        self.var_name = StringVar()
        self.var_DOJ = StringVar()
        self.var_DOB = StringVar()
        self.var_email = StringVar()
        self.var_pass = StringVar()
        self.var_utype = StringVar()
        self.var_salary = StringVar()
        self.var_search = StringVar()
        self.var_search_text = StringVar()

        # Search frame
        self.search_frame = LabelFrame(self.root, text="Search employee", font=("Arial", 12, "bold"), bd=2, relief=RIDGE, bg="light yellow")
        self.search_frame.place(x=300, y=20, width=750, height=70 )

        # Options
        cmb_search = ttk.Combobox(self.search_frame, textvariable=self.var_search, values=("select", "eid", "name", "contact"), state='readonly', justify=CENTER, font=("Arial", 12))
        cmb_search.place(x=10, y=9, width=180)
        cmb_search.current(0)

        txt_search = Entry(self.search_frame, textvariable=self.var_search_text, font=("Arial", 12), bg="light yellow")
        txt_search.place(x=200, y=10)

        btn_search = Button(self.search_frame, text="Search", command=self.search_employee, font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", cursor="hand2")
        btn_search.place(x=410, y=10, width=150, height=30)

        # Show All button
        btn_show_all = Button(self.search_frame, text="Show All", command=self.show_employees, font=("Arial", 12, "bold"), bg="#2196f3", fg="white", cursor="hand2")
        btn_show_all.place(x=570, y=10, width=150, height=30)

        # Title
        title = Label(self.root, text="Employee details", font=("Arial", 15, "bold"), bg="#0f4d7d", fg="white")
        title.place(x=50, y=100, width=1250)

        # Input fields
        # Row1
        lbl_empid = Label(self.root, text="Emp id", font=("Arial", 12, "bold"), bg="white")
        lbl_empid.place(x=50, y=150)
        txt_empid = Entry(self.root, textvariable=self.var_emp_id, font=("Arial", 12), bg="light yellow")
        txt_empid.place(x=150, y=150, width=180)

        lbl_gender = Label(self.root, text="Gender", font=("Arial", 12, "bold"), bg="white")
        lbl_gender.place(x=475, y=150)
        cmb_gender = ttk.Combobox(self.root, values=("select", "Male", "Female", "Other"), textvariable=self.var_gender, state='readonly', justify=CENTER, font=("Arial", 12))
        cmb_gender.place(x=575, y=150, width=180)
        cmb_gender.current(0)

        lbl_contact = Label(self.root, text="Contact", font=("Arial", 12, "bold"), bg="white")
        lbl_contact.place(x=900, y=150)
        txt_contact = Entry(self.root, textvariable=self.var_contact, font=("Arial", 12), bg="light yellow")
        txt_contact.place(x=1000, y=150, width=180)

        # Row2
        lbl_Name = Label(self.root, text="Name", font=("Arial", 12, "bold"), bg="white")
        lbl_Name.place(x=50, y=190)
        txt_Name = Entry(self.root, textvariable=self.var_name, font=("Arial", 12), bg="light yellow")
        txt_Name.place(x=150, y=190, width=190)

        lbl_DOB = Label(self.root, text="D.O.B.", font=("Arial", 12, "bold"), bg="white")
        lbl_DOB.place(x=475, y=190)
        txt_DOB = Entry(self.root, textvariable=self.var_DOB, font=("Arial", 12), bg="light yellow")
        txt_DOB.place(x=575, y=190, width=190)

        lbl_DOJ = Label(self.root, text="D.O.J.", font=("Arial", 12, "bold"), bg="white")
        lbl_DOJ.place(x=900, y=190)
        txt_DOJ = Entry(self.root, textvariable=self.var_DOJ, font=("Arial", 12), bg="light yellow")
        txt_DOJ.place(x=1000, y=190, width=190)

        # Row3
        lbl_email = Label(self.root, text="Email", font=("Arial", 12, "bold"), bg="white")
        lbl_email.place(x=50, y=230)
        txt_email = Entry(self.root, textvariable=self.var_email, font=("Arial", 12), bg="light yellow")
        txt_email.place(x=150, y=230, width=190)

        lbl_pass = Label(self.root, text="Password", font=("Arial", 12, "bold"), bg="white")
        lbl_pass.place(x=475, y=230)
        txt_pass = Entry(self.root, textvariable=self.var_pass, font=("Arial", 12), bg="light yellow")
        txt_pass.place(x=575, y=230, width=190)

        lbl_utype = Label(self.root, text="User Type", font=("Arial", 12, "bold"), bg="white")
        lbl_utype.place(x=900, y=235)
        cmb_utype = ttk.Combobox(self.root, values=("Admin/principal", "Employee"), textvariable=self.var_utype, state='readonly', justify=CENTER, font=("Arial", 12))
        cmb_utype.place(x=1000, y=235, width=190)
        cmb_utype.current(0)

        # Row4
        lbl_address = Label(self.root, text="Address", font=("Arial", 12, "bold"), bg="white")
        lbl_address.place(x=50, y=270)
        self.txt_address = Text(self.root, font=("Arial", 12), bg="light yellow", height=5)
        self.txt_address.place(x=150, y=270, width=400)

        # Add scrollbar to the address field
        scrollbar = Scrollbar(self.root, command=self.txt_address.yview)
        scrollbar.place(x=550, y=270, height=95)
        self.txt_address.config(yscrollcommand=scrollbar.set)

        lbl_salary = Label(self.root, text="Salary", font=("Arial", 12, "bold"), bg="white")
        lbl_salary.place(x=900, y=290)
        txt_salary = Entry(self.root, textvariable=self.var_salary, font=("Arial", 12), bg="light yellow")
        txt_salary.place(x=1000, y=290, width=180)

        # Buttons
        btn_add = Button(self.root, text="Save", command=self.add_employee, font=("Arial", 12, "bold"), bg="#2196f3", fg="white", cursor="hand2")
        btn_add.place(x=600, y=385, width=110, height=28)
        btn_update = Button(self.root, text="Update", command=self.update_employee, font=("Arial", 12, "bold"), bg="#4caf50", fg="white", cursor="hand2")
        btn_update.place(x=720, y=385, width=110, height=28)
        btn_delete = Button(self.root, text="Delete", command=self.confirm_delete, font=("Arial", 12, "bold"), bg="#f44336", fg="white", cursor="hand2")
        btn_delete.place(x=840, y=385, width=110, height=28)
        btn_clear = Button(self.root, text="Clear", command=self.clear, font=("Arial", 12, "bold"), bg="#607d8b", fg="white", cursor="hand2")
        btn_clear.place(x=960, y=385, width=110, height=28)

        # Employee Details
        emp_frame = Frame(self.root, bd=3, relief=RIDGE, bg="white")
        emp_frame.place(x=50, y=430, width=1250, height=200)

        # Create vertical scrollbar
        scrolly = Scrollbar(emp_frame, orient=VERTICAL)
        scrolly.pack(side=RIGHT, fill=Y)

        # Create horizontal scrollbar
        scrollx = Scrollbar(emp_frame, orient=HORIZONTAL)
        scrollx.pack(side=BOTTOM, fill=X)

        # Create the Treeview widget
        self.employee_table = ttk.Treeview(emp_frame, columns=("eid", "gender", "contact", "name", "DOJ", "DOB", "email", "pass", "utype", "salary", "address"), xscrollcommand=scrollx.set, yscrollcommand=scrolly.set)

        # Set column headings
        self.employee_table["show"] = "headings"
        self.employee_table.heading("eid", text="Emp ID")
        self.employee_table.heading("gender", text="Gender")
        self.employee_table.heading("contact", text="Contact")
        self.employee_table.heading("name", text="Name")
        self.employee_table.heading("DOJ", text="DOJ")
        self.employee_table.heading("DOB", text="DOB")
        self.employee_table.heading("email", text="Email")
        self.employee_table.heading("pass", text="Password")
        self.employee_table.heading("utype", text="User Type")
        self.employee_table.heading("salary", text="Salary")
        self.employee_table.heading("address", text="Address")
        self.employee_table.pack(fill=BOTH,expand=1)
        self.employee_table.bind("<ButtonRelease-1>", self.get_data) 
        # Set column widths
        columns = ["eid", "gender", "contact", "name", "DOJ", "DOB", "email", "pass", "utype", "salary", "address"]
        widths = [70, 100, 100, 100, 100, 100, 150, 100, 100, 100, 200]
        for col, width in zip(columns, widths):
            self.employee_table.column(col, width=width)

        # Attach scrollbars
        scrolly.config(command=self.employee_table.yview)
        scrollx.config(command=self.employee_table.xview)

        # Pack the Treeview widget
        self.employee_table.pack(fill=BOTH, expand=1)
        self.show_employees()

    def add_employee(self):
        con = sqlite3.connect(database=r'IMS.db')
        cur = con.cursor()
        try:
            if self.var_emp_id.get() == "":
                messagebox.showerror("Error", "Employee id must be required", parent=self.root)
            else:
                cur.execute("SELECT * FROM employee WHERE eid=?", (self.var_emp_id.get(),))
                row = cur.fetchone()
                if row is not None:
                    messagebox.showerror("Error", "This Employee id already assigned, try a different one", parent=self.root)
                else:
                    cur.execute("INSERT INTO employee (eid, gender, contact, name, DOJ, DOB, email, pass, utype, salary, address) VALUES (?,?,?,?,?,?,?,?,?,?,?)", (
                        self.var_emp_id.get(),
                        self.var_gender.get(),
                        self.var_contact.get(),
                        self.var_name.get(),
                        self.var_DOJ.get(),
                        self.var_DOB.get(),
                        self.var_email.get(),
                        self.var_pass.get(),
                        self.var_utype.get(),
                        self.var_salary.get(),
                        self.txt_address.get('1.0', END),
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Employee Added Successfully", parent=self.root)
                    self.show_employees()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def show_employees(self):
        con = sqlite3.connect(database=r'IMS.db')
        cur = con.cursor()
        try: 
            cur.execute("SELECT * FROM employee")
            rows = cur.fetchall()
            self.employee_table.delete(*self.employee_table.get_children())
            for row in rows:
                self.employee_table.insert('', END, values=row)
            
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def get_data(self, event):
        try:
            f = self.employee_table.focus()
            content = (self.employee_table.item(f))
            row = content['values']
            self.var_emp_id.set(row[0])
            self.var_gender.set(row[1])
            self.var_contact.set(row[2])
            self.var_name.set(row[3])
            self.var_DOJ.set(row[4])
            self.var_DOB.set(row[5])
            self.var_email.set(row[6])
            self.var_pass.set(row[7])
            self.var_utype.set(row[8])
            self.var_salary.set(row[9])
            self.txt_address.delete('1.0', END)
            self.txt_address.insert(END, row[10])
        except Exception as ex:
            messagebox.showerror("Error", f"Error while getting data: {str(ex)}", parent=self.root)

    def update_employee(self):
        con = sqlite3.connect(database=r'IMS.db')
        cur = con.cursor()
        try:
            cur.execute("UPDATE employee SET gender=?, contact=?, name=?, DOJ=?, DOB=?, email=?, pass=?, utype=?, salary=?, address=? WHERE eid=?", (
                self.var_gender.get(),
                self.var_contact.get(),
                self.var_name.get(),
                self.var_DOJ.get(),
                self.var_DOB.get(),
                self.var_email.get(),
                self.var_pass.get(),
                self.var_utype.get(),
                self.var_salary.get(),
                self.txt_address.get('1.0', END),
                self.var_emp_id.get(),
            ))
            con.commit()
            messagebox.showinfo("Success", "Employee Updated Successfully", parent=self.root)
            self.show_employees()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def confirm_delete(self):
        result = messagebox.askyesno("Delete Confirmation", "Are you sure you want to delete this employee?")
        if result:
            self.delete_employee()

    def delete_employee(self):
        con = sqlite3.connect(database=r'IMS.db')
        cur = con.cursor()
        try:
            if self.var_emp_id.get() == "":
                messagebox.showerror("Error", "Employee id must be required", parent=self.root)
            else:
                cur.execute("DELETE FROM employee WHERE eid=?", (self.var_emp_id.get(),))
                con.commit()
                messagebox.showinfo("Success", "Employee Deleted Successfully", parent=self.root)
                self.show_employees()
                self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def search_employee(self):
        con = sqlite3.connect(database=r'IMS.db')
        cur = con.cursor()
        try:
            if self.var_search.get() == "select" or self.var_search_text.get() == "":
                messagebox.showerror("Error", "Please select search filter and enter text to search", parent=self.root)
            else:
                cur.execute(f"SELECT * FROM employee WHERE {self.var_search.get()} LIKE '%{self.var_search_text.get()}%'")
                rows = cur.fetchall()
                if len(rows) != 0:
                    self.employee_table.delete(*self.employee_table.get_children())
                    for row in rows:
                        self.employee_table.insert('', END, values=row)
                else:
                    messagebox.showinfo("Info", "No record found", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def clear(self):
        self.var_emp_id.set("")
        self.var_gender.set("")  
        self.var_contact.set("")
        self.var_name.set("")
        self.var_DOJ.set("")
        self.var_DOB.set("")
        self.var_email.set("")
        self.var_pass.set("")
        self.var_utype.set("")
        self.var_salary.set("")
        self.txt_address.delete('1.0', END)

if __name__ == "__main__":
    root = Tk() 
    obj = Employee(root)
    root.mainloop()
