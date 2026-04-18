# Smart Expense Tracker

Multi-user Expense Tracker Dashboard built with Python, Flask, Tkinter and MySQL.

## Features

- User Register/Login
- Add / Update / Delete Expenses
- Search Expenses
- User-wise Data
- Pie Chart Analytics
- Bar Chart Analytics
- Dashboard UI

## Tech Stack

- Python
- Tkinter
- Flask
- SqLite
- Matplotlib


Prerequisites

Install on your system:

✅ Python 3.8+
✅ pip
✅ (Optional) Git

📁 Project Setup
1️⃣ Clone Repository
git clone https://github.com/TanvirAzam42/smart-expense-tracker.git
cd smart-expense-tracker

2️⃣ Create Virtual Environment
python -m venv .venv

3️⃣ Activate Virtual Environment
Windows
.venv\Scripts\activate
Mac/Linux
source .venv/bin/activate

4️⃣ Install Dependencies
pip install flask flask-cors requests matplotlib pyinstaller
run this - pyinstaller --onefile --windowed main_app.py  
🚀 Run Application (Recommended)
Single Command Launch
python main_app.py

This will:

✅ Start Flask backend automatically
✅ Open GUI login window
✅ Connect SQLite database

💾 Database

SQLite database file auto-creates:

expense_tracker.db

No MySQL setup required.

🔐 Usage Flow
Register New User

Create username + password.

Login

Use credentials.

Dashboard
Add Expense
Update Expense
Delete Expense
Search Expense
View Charts
🖥 Build EXE (Optional)
pyinstaller --onefile --windowed main_app.py


EXE created in:

dist/
📂 Project Structure
smart-expense-tracker/
│── backend/
│   └── app.py
│── frontend/
│   └── gui.py
│── main_app.py
│── expense_tracker.db
│── README.md
⚠️ If Port 5000 Busy

Close previous Python/Flask process and run again.

💡Developed by Tanvir Azam