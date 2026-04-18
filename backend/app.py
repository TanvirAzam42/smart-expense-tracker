from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

DB_NAME = "expense_tracker.db"


# =====================================================
# DATABASE FUNCTIONS
# =====================================================

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    # Users table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # Expenses table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            user_id INTEGER,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()


# =====================================================
# HOME
# =====================================================

@app.route('/')
def home():
    return "Expense Tracker SQLite API Running"


# =====================================================
# REGISTER
# =====================================================

@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.json

        username = data['username'].strip()
        password = data['password'].strip()

        if username == "" or password == "":
            return jsonify({"message": "Username and Password required"}), 400

        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO users(username,password) VALUES (?,?)",
            (username, password)
        )

        conn.commit()
        conn.close()

        return jsonify({"message": "Registered Successfully"})

    except Exception as e:
        return jsonify({"message": str(e)}), 400


# =====================================================
# LOGIN
# =====================================================

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.json

        username = data['username'].strip()
        password = data['password'].strip()

        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "SELECT id, username FROM users WHERE username=? AND password=?",
            (username, password)
        )

        user = cur.fetchone()
        conn.close()

        if user:
            return jsonify({
                "message": "Login Success",
                "user_id": user["id"],
                "username": user["username"]
            })

        return jsonify({"message": "Invalid Credentials"}), 401

    except Exception as e:
        return jsonify({"message": str(e)}), 400


# =====================================================
# ADD EXPENSE
# =====================================================

@app.route('/add-expense', methods=['POST'])
def add_expense():
    try:
        data = request.json

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO expenses(title, amount, category, date, user_id)
            VALUES (?, ?, ?, ?, ?)
        """, (
            data['title'],
            data['amount'],
            data['category'],
            data['date'],
            data['user_id']
        ))

        conn.commit()
        conn.close()

        return jsonify({"message": "Expense Added"})

    except Exception as e:
        return jsonify({"message": str(e)}), 400


# =====================================================
# GET USER EXPENSES
# =====================================================

@app.route('/expenses/<int:user_id>', methods=['GET'])
def get_expenses(user_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM expenses WHERE user_id=? ORDER BY id DESC",
        (user_id,)
    )

    rows = cur.fetchall()
    conn.close()

    data = [dict(row) for row in rows]

    return jsonify(data)


# =====================================================
# UPDATE
# =====================================================

@app.route('/update-expense/<int:id>', methods=['PUT'])
def update_expense(id):
    try:
        data = request.json

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            UPDATE expenses
            SET title=?, amount=?, category=?, date=?
            WHERE id=?
        """, (
            data['title'],
            data['amount'],
            data['category'],
            data['date'],
            id
        ))

        conn.commit()
        conn.close()

        return jsonify({"message": "Updated Successfully"})

    except Exception as e:
        return jsonify({"message": str(e)}), 400


# =====================================================
# DELETE
# =====================================================

@app.route('/delete-expense/<int:id>', methods=['DELETE'])
def delete_expense(id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM expenses WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Deleted Successfully"})


# =====================================================
# SEARCH
# =====================================================

@app.route('/search-expense/<int:user_id>', methods=['GET'])
def search_expense(user_id):
    q = request.args.get('q', '').strip()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT * FROM expenses
        WHERE user_id=?
        AND (
            title LIKE ?
            OR category LIKE ?
            OR date LIKE ?
        )
        ORDER BY id DESC
    """, (
        user_id,
        f"%{q}%",
        f"%{q}%",
        f"%{q}%"
    ))

    rows = cur.fetchall()
    conn.close()

    data = [dict(row) for row in rows]

    return jsonify(data)


# =====================================================
# MAIN
# =====================================================

if __name__ == '__main__':
    init_db()
    app.run(debug=True)