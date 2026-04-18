import tkinter as tk
from tkinter import ttk, messagebox
import requests
from collections import defaultdict

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

API_URL = "http://127.0.0.1:5000"

# ================= GLOBAL =================
user_id = None
username = None

bg = "#1e1e2f"
card = "#2b2b3d"


# =====================================================
# ---------------- AUTH FUNCTIONS ---------------------
# =====================================================

def register_user():
    username_val = login_user_entry.get().strip()
    password_val = login_pass_entry.get().strip()

    if username_val == "" or password_val == "":
        messagebox.showerror("Error", "Username and Password required")
        return

    try:
        response = requests.post(f"{API_URL}/register", json={
            "username": username_val,
            "password": password_val
        })

        if response.status_code == 200:
            messagebox.showinfo("Success", "Registered Successfully")
        else:
            try:
                msg = response.json()["message"]
            except:
                msg = "Registration Failed"
            messagebox.showerror("Error", msg)

    except Exception as e:
        messagebox.showerror("Error", str(e))


def login_user():
    global user_id, username

    username_val = login_user_entry.get().strip()
    password_val = login_pass_entry.get().strip()

    if username_val == "" or password_val == "":
        messagebox.showerror("Error", "Enter Username and Password")
        return

    try:
        response = requests.post(f"{API_URL}/login", json={
            "username": username_val,
            "password": password_val
        })

        if response.status_code == 200:
            data = response.json()

            user_id = data["user_id"]
            username = data["username"]

            login_window.destroy()
            open_dashboard()

        else:
            messagebox.showerror("Error", response.json()["message"])

    except Exception as e:
        messagebox.showerror("Error", str(e))


# =====================================================
# ---------------- DASHBOARD --------------------------
# =====================================================

def open_dashboard():
    global root, tree, title_entry, amount_entry
    global category_combo, date_entry, search_entry
    global total_label, chart_frame

    root = tk.Tk()
    root.title("Smart Expense Tracker")
    root.geometry("1350x760")
    root.config(bg=bg)

    tk.Label(
        root,
        text=f"💰 Welcome {username}",
        font=("Segoe UI", 24, "bold"),
        fg="white",
        bg=bg
    ).pack(pady=10)

    main = tk.Frame(root, bg=bg)
    main.pack(fill="both", expand=True)

    # LEFT PANEL
    left = tk.Frame(main, bg=card, width=320)
    left.pack(side="left", fill="y", padx=15, pady=10)

    # RIGHT PANEL
    right = tk.Frame(main, bg=card)
    right.pack(side="right", fill="both", expand=True, padx=15, pady=10)

    # ---------- LEFT ----------
    tk.Label(left, text="Add Expense",
             font=("Segoe UI", 18, "bold"),
             fg="white", bg=card).pack(pady=15)

    tk.Label(left, text="Title", fg="white", bg=card).pack()
    title_entry = tk.Entry(left, width=28)
    title_entry.pack(pady=5)

    tk.Label(left, text="Amount", fg="white", bg=card).pack()
    amount_entry = tk.Entry(left, width=28)
    amount_entry.pack(pady=5)

    tk.Label(left, text="Category", fg="white", bg=card).pack()
    category_combo = ttk.Combobox(
        left,
        values=["Food", "Travel", "Bills", "Shopping", "Other"],
        width=25
    )
    category_combo.pack(pady=5)

    tk.Label(left, text="Date (YYYY-MM-DD)", fg="white", bg=card).pack()
    date_entry = tk.Entry(left, width=28)
    date_entry.pack(pady=5)

    tk.Button(left, text="Add", width=22, bg="green",
              fg="white", command=add_expense).pack(pady=5)

    tk.Button(left, text="Update", width=22, bg="orange",
              fg="white", command=update_expense).pack(pady=5)

    tk.Button(left, text="Delete", width=22, bg="red",
              fg="white", command=delete_expense).pack(pady=5)

    tk.Label(left, text="Search", fg="white", bg=card).pack(pady=10)

    search_entry = tk.Entry(left, width=28)
    search_entry.pack()

    tk.Button(left, text="Search", width=22,
              bg="#2196F3", fg="white",
              command=search_expense).pack(pady=5)

    tk.Button(left, text="Refresh", width=22,
              bg="gray", fg="white",
              command=lambda: [load_expenses(), show_analytics()]).pack(pady=5)

    tk.Button(left, text="Logout", width=22,
              bg="black", fg="white",
              command=logout).pack(pady=20)

    # ---------- RIGHT ----------
    total_label = tk.Label(
        right,
        text="Total Expense: ₹0",
        font=("Segoe UI", 16, "bold"),
        fg="white",
        bg=card
    )
    total_label.pack(pady=8)

    columns = ("ID", "Title", "Amount", "Category", "Date", "Created", "UserID")

    tree = ttk.Treeview(right, columns=columns, show="headings", height=10)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=115)

    tree.pack(fill="x", padx=10, pady=10)

    tree.bind("<ButtonRelease-1>", select_row)

    chart_frame = tk.Frame(right, bg=card)
    chart_frame.pack(fill="both", expand=True)

    load_expenses()
    show_analytics()

    root.mainloop()


# =====================================================
# ---------------- CRUD FUNCTIONS ---------------------
# =====================================================

def add_expense():
    title = title_entry.get().strip()
    amount = amount_entry.get().strip()
    category = category_combo.get().strip()
    date = date_entry.get().strip()

    if title == "" or amount == "" or category == "" or date == "":
        messagebox.showerror("Error", "All fields required")
        return

    try:
        requests.post(f"{API_URL}/add-expense", json={
            "title": title,
            "amount": amount,
            "category": category,
            "date": date,
            "user_id": user_id
        })

        clear_fields()
        load_expenses()
        show_analytics()

    except Exception as e:
        messagebox.showerror("Error", str(e))


def load_expenses():
    for row in tree.get_children():
        tree.delete(row)

    data = requests.get(f"{API_URL}/expenses/{user_id}").json()

    for row in data:
        tree.insert("", tk.END, values=row)


def clear_fields():
    title_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)
    category_combo.set("")
    date_entry.delete(0, tk.END)


def select_row(event):
    selected = tree.focus()

    if not selected:
        return

    values = tree.item(selected, "values")

    if values:
        title_entry.delete(0, tk.END)
        title_entry.insert(0, values[1])

        amount_entry.delete(0, tk.END)
        amount_entry.insert(0, values[2])

        category_combo.set(values[3])

        date_entry.delete(0, tk.END)
        date_entry.insert(0, values[4])


def update_expense():
    selected = tree.focus()

    if not selected:
        messagebox.showerror("Error", "Select row first")
        return

    values = tree.item(selected, "values")
    expense_id = values[0]

    try:
        requests.put(f"{API_URL}/update-expense/{expense_id}", json={
            "title": title_entry.get(),
            "amount": amount_entry.get(),
            "category": category_combo.get(),
            "date": date_entry.get()
        })

        clear_fields()
        load_expenses()
        show_analytics()

    except Exception as e:
        messagebox.showerror("Error", str(e))


def delete_expense():
    selected = tree.focus()

    if not selected:
        messagebox.showerror("Error", "Select row first")
        return

    values = tree.item(selected, "values")
    expense_id = values[0]

    try:
        requests.delete(f"{API_URL}/delete-expense/{expense_id}")

        load_expenses()
        show_analytics()

    except Exception as e:
        messagebox.showerror("Error", str(e))


def search_expense():
    q = search_entry.get().strip()

    for row in tree.get_children():
        tree.delete(row)

    data = requests.get(
        f"{API_URL}/search-expense/{user_id}?q={q}"
    ).json()

    for row in data:
        tree.insert("", tk.END, values=row)


# =====================================================
# ---------------- ANALYTICS --------------------------
# =====================================================

def show_analytics():
    for widget in chart_frame.winfo_children():
        widget.destroy()

    data = requests.get(f"{API_URL}/expenses/{user_id}").json()

    if not data:
        total_label.config(text="Total Expense: ₹0")
        return

    category_data = defaultdict(float)
    monthly_data = defaultdict(float)
    total = 0

    for row in data:
        amount = float(row[2])
        category = row[3]
        month = str(row[4])[:7]

        total += amount
        category_data[category] += amount
        monthly_data[month] += amount

    total_label.config(text=f"Total Expense: ₹ {total:.2f}")

    # Pie Chart
    fig1 = plt.Figure(figsize=(4, 3), dpi=90)
    ax1 = fig1.add_subplot(111)
    ax1.pie(
        category_data.values(),
        labels=category_data.keys(),
        autopct="%1.1f%%"
    )
    ax1.set_title("Category Wise")

    canvas1 = FigureCanvasTkAgg(fig1, chart_frame)
    canvas1.get_tk_widget().grid(row=0, column=0, padx=10, pady=10)

    # Bar Chart
    fig2 = plt.Figure(figsize=(4, 3), dpi=90)
    ax2 = fig2.add_subplot(111)
    ax2.bar(monthly_data.keys(), monthly_data.values())
    ax2.set_title("Monthly Expense")

    canvas2 = FigureCanvasTkAgg(fig2, chart_frame)
    canvas2.get_tk_widget().grid(row=0, column=1, padx=10, pady=10)


# =====================================================
# ---------------- LOGOUT -----------------------------
# =====================================================

def logout():
    root.destroy()
    open_login()


# =====================================================
# ---------------- LOGIN WINDOW -----------------------
# =====================================================

def open_login():
    global login_window, login_user_entry, login_pass_entry

    login_window = tk.Tk()
    login_window.title("Expense Tracker Login")
    login_window.geometry("420x360")
    login_window.config(bg=bg)

    tk.Label(
        login_window,
        text="🔐 Expense Tracker Login",
        font=("Segoe UI", 20, "bold"),
        fg="white",
        bg=bg
    ).pack(pady=25)

    tk.Label(login_window, text="Username",
             fg="white", bg=bg).pack()

    login_user_entry = tk.Entry(login_window, width=28)
    login_user_entry.pack(pady=8)

    tk.Label(login_window, text="Password",
             fg="white", bg=bg).pack()

    login_pass_entry = tk.Entry(login_window, show="*", width=28)
    login_pass_entry.pack(pady=8)

    tk.Button(
        login_window,
        text="Login",
        width=20,
        bg="green",
        fg="white",
        command=login_user
    ).pack(pady=10)

    tk.Button(
        login_window,
        text="Register",
        width=20,
        bg="#2196F3",
        fg="white",
        command=register_user
    ).pack(pady=5)

    login_window.mainloop()


# ================= START APP =================
open_login()