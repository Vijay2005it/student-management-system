from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3

window = Tk()
window.title("Student Management System")
window.geometry("1000x800")
window.config(bg="grey")

class DB:
    def __init__(self, db):
        self.con = sqlite3.connect(db)
        self.c = self.con.cursor()

        self.c.execute("""
            CREATE TABLE IF NOT EXISTS data(
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                roll_no TEXT NOT NULL,
                age INTEGER NOT NULL,
                gender TEXT NOT NULL
            )
        """)
        self.con.commit()

    def insert(self, name, roll_no, age, gender):
        insert = "INSERT INTO data VALUES(NULL, ?, ?, ?, ?)"
        self.c.execute(insert, (name, roll_no, age, gender))
        self.con.commit()

    def fetch(self):
        # id ah hidden ah use panrom, UI la show panna matom
        self.c.execute("SELECT id, name, roll_no, age, gender FROM data")
        return self.c.fetchall()

    def update(self, id, name, roll_no, age, gender):
        self.c.execute(
            "UPDATE data SET name=?, roll_no=?, age=?, gender=? WHERE id=?",
            (name, roll_no, age, gender, id)
        )
        self.con.commit()


vijay = DB("student.db")

def add_std():
    name = name_entry.get()
    roll_no = roll_entry.get()
    age = age_entry.get()
    gender = gender_entry.get()

    if name == "" or roll_no == "" or age == "" or gender == "":
        messagebox.showerror("Error", "All fields are required")
        return

    if not age.isdigit():
        messagebox.showwarning("Age", "Age must be a number")
        return
    age = int(age)

    vijay.insert(name, roll_no, age, gender)

    name_entry.delete(0, END)
    roll_entry.delete(0, END)
    age_entry.delete(0, END)
    gender_entry.delete(0, END)

    refresh_tree()


def refresh_tree():
    for item in tree.get_children():
        tree.delete(item)

    for row in vijay.fetch():
        id, name, roll, age, gender = row
        tree.insert("", "end", values=(name, roll, age, gender), iid=id)


def select_btn():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Error", "Select a record first")
        return

    record_id = selected[0] 
    values = tree.item(record_id, "values")

    name_entry.delete(0, END)
    roll_entry.delete(0, END)
    age_entry.delete(0, END)
    gender_entry.delete(0, END)

    name_entry.insert(0, values[0])
    roll_entry.insert(0, values[1])
    age_entry.insert(0, values[2])
    gender_entry.insert(0, values[3])


def update_btn():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Error", "Select a record first")
        return

    record_id = selected[0]

    name = name_entry.get()
    roll_no = roll_entry.get()
    age = age_entry.get()
    gender = gender_entry.get()

    if name == "" or roll_no == "" or age == "" or gender == "":
        messagebox.showerror("Error", "All fields are required")
        return

    if not age.isdigit():
        messagebox.showwarning("Age", "Age must be a number")
        return
    age = int(age)

    # DB update
    vijay.update(record_id, name, roll_no, age, gender)

    refresh_tree()
    messagebox.showinfo("Success", "Record Updated Successfully")


def delete_btn():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Error", "Select a record first")
        return

    record_id = selected[0]

    confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this record?")
    if confirm:
        vijay.c.execute("DELETE FROM data WHERE id=?", (record_id,))
        vijay.con.commit()

        refresh_tree()
        messagebox.showinfo("Deleted", "Record Deleted Successfully")

    name_entry.delete(0, END)
    roll_entry.delete(0, END)
    age_entry.delete(0, END)
    gender_entry.delete(0, END)





lab_tittle = Label(text="Student Management System", width=10,
                   font=("italic", 15, "bold"), bg="green", pady=10, padx=500)
lab_tittle.grid(columnspan=10, pady=10)

lab_name = Label(window, text="Name :", width=10,
                 font=("italic", 15, "bold"), bg="whitesmoke", border=5)
lab_name.grid(row=1, column=0)

name_entry = Entry(window, width=20, font=("italic", 15), border=5)
name_entry.grid(row=1, column=1, padx=10, pady=10)

lab_roll_no = Label(window, text="Roll no :", width=10,
                    font=("italic", 15, "bold"), bg="whitesmoke", border=5)
lab_roll_no.grid(row=2, column=0)

roll_entry = Entry(window, width=20, font=("italic", 15), border=5)
roll_entry.grid(row=2, column=1, padx=10, pady=10)

lab_age = Label(window, text="Age :", width=10,
                font=("italic", 15, "bold"), bg="whitesmoke", border=5)
lab_age.grid(row=3, column=0)

age_entry = Entry(window, width=20, font=("italic", 15), border=5)
age_entry.grid(row=3, column=1, padx=10, pady=10)

lab_gender = Label(window, text="Gender :", width=10,
                   font=("italic", 15, "bold"), bg="whitesmoke", border=5)
lab_gender.grid(row=4, column=0)

gender_entry = Entry(window, width=20, font=("italic", 15), border=5)
gender_entry.grid(row=4, column=1, padx=10, pady=10)

add_btn = Button(text="Add", bg="blue", fg="white", width=10, padx=10, pady=5,
                 font=("italic", 15, "bold"), activebackground="white", activeforeground="blue",
                 borderwidth=5, border=5, command=add_std)
add_btn.grid(row=5, column=1)

select_btnn = Button(text="Select", bg="purple", fg="white", width=10, padx=10, pady=5,
                     font=("italic", 15, "bold"), activebackground="white", activeforeground="purple",
                     borderwidth=5, border=5, command=select_btn)
select_btnn.grid(row=5, column=2)

update_btnn = Button(text="Update", bg="green", fg="white", width=10, padx=10, pady=5,
                     font=("italic", 15, "bold"), activebackground="white", activeforeground="green",
                     borderwidth=5, border=5, command=update_btn)
update_btnn.grid(row=5, column=3)

delete_btn = Button(text="Delete", bg="red", fg="white", width=10, padx=10, pady=5,
                     font=("italic", 15, "bold"), activebackground="white", activeforeground="red",
                     borderwidth=5, border=5, command=delete_btn)
delete_btn.grid(row=5, column=4)

# Columns (without ID)
columns = ("Name", "Roll no", "Age", "Gender")
tree = ttk.Treeview(window, columns=columns, show="headings", height=15)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150, anchor=CENTER)

tree.grid(row=6, column=0, columnspan=3, padx=20, pady=20)

refresh_tree()
window.mainloop() 