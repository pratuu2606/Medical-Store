# Medical Management System using Tkinter and SQLite
# Attractive UI version with Image

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

# ---------------- DATABASE SETUP ----------------
conn = sqlite3.connect("medical.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS medicines (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    company TEXT,
    quantity INTEGER,
    price REAL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    medicine_name TEXT,
    quantity INTEGER,
    total REAL,
    date TEXT
)
""")

conn.commit()

# ---------------- MAIN WINDOW ----------------
root = tk.Tk()
root.title("Medical Management System")
root.geometry("1000x620")
root.config(bg="#f4f6f9")

# ---------------- STYLE ----------------
style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="#b81b89", foreground="white")
style.configure("Treeview", font=("Segoe UI", 10), rowheight=25)

# ---------------- HEADER ----------------
header = tk.Frame(root, bg="#b42986", height=80)
header.pack(fill=tk.X)

# Add image (place hospital.png in same folder)
try:
    logo_img = tk.PhotoImage(file="hospital.png")
    logo = tk.Label(header, image=logo_img, bg="#a41167")
    logo.place(x=20, y=10)
except:
    pass

header_title = tk.Label(
    header,
    text="Medical Management System",
    font=("Segoe UI", 22, "bold"),
    bg="#c926ab",
    fg="white"
)
header_title.pack(pady=20)

# ---------------- FUNCTIONS ----------------
def add_medicine():
    if name_var.get() == "" or qty_var.get() == "" or price_var.get() == "":
        messagebox.showerror("Error", "All fields are required")
        return

    cursor.execute(
        "INSERT INTO medicines (name, company, quantity, price) VALUES (?, ?, ?, ?)",
        (name_var.get(), company_var.get(), int(qty_var.get()), float(price_var.get()))
    )
    conn.commit()
    messagebox.showinfo("Success", "Medicine Added Successfully")
    clear_fields()
    show_medicines()


def show_medicines():
    for row in medicine_table.get_children():
        medicine_table.delete(row)

    cursor.execute("SELECT * FROM medicines")
    for row in cursor.fetchall():
        medicine_table.insert('', tk.END, values=row)


def clear_fields():
    name_var.set("")
    company_var.set("")
    qty_var.set("")
    price_var.set("")


def sell_medicine():
    selected = medicine_table.focus()
    if not selected:
        messagebox.showerror("Error", "Select a medicine")
        return

    data = medicine_table.item(selected)['values']
    med_id, name, company, qty, price = data

    sell_qty = int(sell_qty_var.get())
    if sell_qty > qty:
        messagebox.showerror("Error", "Not enough stock")
        return

    total = sell_qty * price
    date = datetime.now().strftime("%d-%m-%Y %H:%M")

    cursor.execute(
        "INSERT INTO sales (medicine_name, quantity, total, date) VALUES (?, ?, ?, ?)",
        (name, sell_qty, total, date)
    )
    cursor.execute(
        "UPDATE medicines SET quantity = quantity - ? WHERE id = ?",
        (sell_qty, med_id)
    )
    conn.commit()

    messagebox.showinfo("Success", f"Sold Successfully\nTotal: ₹{total}")
    sell_qty_var.set("")
    show_medicines()


# ---------------- VARIABLES ----------------
name_var = tk.StringVar()
company_var = tk.StringVar()
qty_var = tk.StringVar()
price_var = tk.StringVar()
sell_qty_var = tk.StringVar()

# ---------------- INPUT FRAME ----------------
input_frame = tk.LabelFrame(root, text="Add Medicine", font=("Segoe UI", 11, "bold"), bg="#f4f6f9")
input_frame.place(x=20, y=100, width=360, height=360)

labels = ["Medicine Name", "Company", "Quantity", "Price"]
vars = [name_var, company_var, qty_var, price_var]

for i, (text, var) in enumerate(zip(labels, vars)):
    tk.Label(input_frame, text=text, bg="#f4f6f9").grid(row=i, column=0, padx=10, pady=10, sticky='w')
    tk.Entry(input_frame, textvariable=var).grid(row=i, column=1, padx=10, pady=10)

btn_frame = tk.Frame(input_frame, bg="#f4f6f9")
btn_frame.grid(row=4, column=0, columnspan=2, pady=15)

tk.Button(btn_frame, text="Add Medicine", command=add_medicine, bg="#2e7d32", fg="white", width=15).pack(side=tk.LEFT, padx=5)
tk.Button(btn_frame, text="Clear", command=clear_fields, width=10).pack(side=tk.LEFT)

# ---------------- SELL FRAME ----------------
sell_frame = tk.LabelFrame(root, text="Sell Medicine", font=("Segoe UI", 11, "bold"), bg="#f4f6f9")
sell_frame.place(x=20, y=480, width=360, height=120)

tk.Label(sell_frame, text="Sell Quantity", bg="#f4f6f9").grid(row=0, column=0, padx=10, pady=10)
tk.Entry(sell_frame, textvariable=sell_qty_var).grid(row=0, column=1, padx=10, pady=10)

tk.Button(sell_frame, text="Sell", command=sell_medicine, bg="#c62828", fg="white", width=15).grid(row=1, column=1, pady=5)

# ---------------- TABLE + IMAGE FRAME ----------------
right_frame = tk.Frame(root, bg="#f4f6f9")
right_frame.place(x=400, y=100, width=570, height=500)

# ---- TOP: TABLE ----
table_frame = tk.Frame(right_frame, bg="#f4f6f9")
table_frame.pack(fill=tk.BOTH, expand=True)

scroll_y = ttk.Scrollbar(table_frame, orient=tk.VERTICAL)

medicine_table = ttk.Treeview(
    table_frame,
    columns=("ID", "Name", "Company", "Qty", "Price"),
    yscrollcommand=scroll_y.set,
    show='headings'
)

scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
scroll_y.config(command=medicine_table.yview)

for col in ("ID", "Name", "Company", "Qty", "Price"):
    medicine_table.heading(col, text=col)
    medicine_table.column(col, anchor=tk.CENTER)

medicine_table.pack(fill=tk.BOTH, expand=True)

# ---- BOTTOM: PHARMA IMAGE ----
image_frame = tk.Frame(right_frame, bg="#f4f6f9", height=180)
image_frame.pack(fill=tk.X)

try:
    pharma_img = tk.PhotoImage(file="pharma.png")
    pharma_label = tk.Label(image_frame, image=pharma_img, bg="#f4f6f9")
    pharma_label.image = pharma_img  # prevent garbage collection
    pharma_label.pack(pady=10)
except:
    tk.Label(image_frame, text="[ D:\Collage Project\m1.jpg]", bg="#f4f6f9", fg="gray").pack(pady=40)

show_medicines()

root.mainloop()
