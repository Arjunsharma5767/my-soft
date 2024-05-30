from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sqlite3

class Category:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1400x700+0+0")
        self.root.title("Inventory Management System | Developed by Arjun")
        self.root.config(bg="#f0f0f0")
        self.root.focus_force()

        # Variables
        self.Var_name = StringVar()

        # Title
        lbl_title = Label(self.root, text="Enter category Name", font=("Arial", 30), bg="#184a45", fg="white")
        lbl_title.pack(side=TOP, fill=X, padx=10, pady=10)

        # Manage product category
        lbl_name = Label(self.root, text="Manage product category", font=("Arial", 30))
        lbl_name.place(x=50, y=100)
        self.entry_name = Entry(self.root, textvariable=self.Var_name, font=("Arial", 18), bg="light yellow")
        self.entry_name.place(x=50, y=170, width=300)
        btn_add = Button(self.root, text="Add", font=("Arial", 18), bg="#4caf50", fg="white", cursor="hand2", command=self.add_category)
        btn_add.place(x=360, y=170, width=150, height=30)
        btn_delete = Button(self.root, text="Delete", font=("Arial", 18), bg="red", fg="white", cursor="hand2", command=self.delete_category)
        btn_delete.place(x=520, y=170, width=150, height=30)

        # Category Details
        cat_frame = Frame(self.root, bd=3, relief=RIDGE, bg="white")
        cat_frame.place(x=722, y=70, width=500, height=150)

        # Create vertical scrollbar
        scrolly = Scrollbar(cat_frame, orient=VERTICAL)
        scrolly.pack(side=RIGHT, fill=Y)

        # Create horizontal scrollbar
        scrollx = Scrollbar(cat_frame, orient=HORIZONTAL)
        scrollx.pack(side=BOTTOM, fill=X)

        # Create the Treeview widget
        self.category_table = ttk.Treeview(cat_frame, columns=("cid", "name"), xscrollcommand=scrollx.set, yscrollcommand=scrolly.set)

        # Set column headings
        self.category_table["show"] = "headings"
        self.category_table.heading("cid", text="Category ID")
        self.category_table.heading("name", text="Name")

        # Set column widths
        columns = ["cid", "name"]
        widths = [100, 100]
        for col, width in zip(columns, widths):
            self.category_table.column(col, width=width)

        # Attach scrollbars
        scrolly.config(command=self.category_table.yview)
        scrollx.config(command=self.category_table.xview)

        # Pack the Treeview widget
        self.category_table.pack(fill=BOTH, expand=1)

        # Load Images
        self.load_images()

        # Database Connection
        self.conn = sqlite3.connect("IMS.db")
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS Category (category_id INTEGER PRIMARY KEY, name TEXT)")
        self.conn.commit()

        # Show existing categories
        self.show_category_details()

    def add_category(self):
        name = self.Var_name.get()
        if name:
            self.cur.execute("INSERT INTO Category (name) VALUES (?)", (name,))
            self.conn.commit()
            self.show_category_details()
            messagebox.showinfo("Success", "Category added successfully.")
            self.Var_name.set("")
        else:
            messagebox.showerror("Error", "Please enter a category name.")

    def delete_category(self):
        # Get the selected item from the Treeview
        selected_item = self.category_table.selection()

        # Check if an item is selected
        if selected_item:
            confirmation = messagebox.askyesno("Delete Confirmation", "Are you sure you want to delete this category?")
            if confirmation:
                try:
                    # Get category id from the selected item
                    category_id = self.category_table.item(selected_item, "values")[0]

                    # Delete from Treeview
                    self.category_table.delete(selected_item)

                    # Delete from database
                    self.cur.execute("DELETE FROM Category WHERE cid=?", (category_id,))
                    self.conn.commit()

                    # Show success message
                    messagebox.showinfo("Success", "Category deleted successfully.")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to delete category: {e}")
        else:
            # Show error message if no item is selected
            messagebox.showerror("Error", "Please select a category to delete.")

    def show_category_details(self):
        # Clear existing data
        for row in self.category_table.get_children():
            self.category_table.delete(row)

        # Fetch data from the database
        self.cur.execute("SELECT * FROM Category")
        rows = self.cur.fetchall()

        # Populate the Treeview
        for row in rows:
            self.category_table.insert("", END, values=row)

    def load_images(self):
        try:
            # Load Image 1
            self.im1 = Image.open("Images/im1.jpg")
            # Resize and place Image 1
            self.im1 = self.im1.resize((600, 400))
            self.photo1 = ImageTk.PhotoImage(self.im1)
            self.label_im1 = Label(self.root, image=self.photo1, bd=2, relief=RAISED)
            self.label_im1.place(x=50, y=220)

            # Load Image 2
            self.im2 = Image.open("Images/acc.jpg")
            # Resize and place Image 2
            self.im2 = self.im2.resize((600, 400))
            self.photo2 = ImageTk.PhotoImage(self.im2)
            self.label_im2 = Label(self.root, image=self.photo2, bd=2, relief=RAISED)
            self.label_im2.place(x=670, y=220)

        except FileNotFoundError as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = Tk()
    obj = Category(root)
    root.mainloop()
    