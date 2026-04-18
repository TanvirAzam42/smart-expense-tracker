from flask import Flask, request, jsonify
from flask_cors import CORS
from db import init_db, mysql

app = Flask(__name__)
CORS(app)

init_db(app)


@app.route('/')
def home():
    return "Expense Tracker API Running"


# ================= REGISTER =================
@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.json

        username = data['username'].strip()
        password = data['password'].strip()

        if username == "" or password == "":
            return jsonify({"message": "Username and Password required"}), 400

        cur = mysql.connection.cursor()

        cur.execute(
            "INSERT INTO users(username,password) VALUES(%s,%s)",
            (username, password)
        )

        mysql.connection.commit()
        cur.close()

        return jsonify({"message": "Registered Successfully"})

    except Exception as e:
        return jsonify({"message": str(e)}), 400


# ================= LOGIN =================
@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.json

        username = data['username'].strip()
        password = data['password'].strip()

        if username == "" or password == "":
            return jsonify({"message": "Enter Username and Password"}), 400

        cur = mysql.connection.cursor()

        cur.execute(
            "SELECT id, username FROM users WHERE username=%s AND password=%s",
            (username, password)
        )

        user = cur.fetchone()
        cur.close()

        if user:
            return jsonify({
                "message": "Login Success",
                "user_id": user[0],
                "username": user[1]
            })

        return jsonify({"message": "Invalid Credentials"}), 401

    except Exception as e:
        return jsonify({"message": str(e)}), 400


# ================= ADD EXPENSE =================
@app.route('/add-expense', methods=['POST'])
def add_expense():
    try:
        data = request.json

        cur = mysql.connection.cursor()

        cur.execute("""
            INSERT INTO expenses(title, amount, category, date, user_id)
            VALUES(%s,%s,%s,%s,%s)
        """, (
            data['title'],
            data['amount'],
            data['category'],
            data['date'],
            data['user_id']
        ))

        mysql.connection.commit()
        cur.close()

        return jsonify({"message": "Expense Added"})

    except Exception as e:
        return jsonify({"message": str(e)}), 400


# ================= GET USER EXPENSES =================
@app.route('/expenses/<int:user_id>', methods=['GET'])
def get_expenses(user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM expenses WHERE user_id=%s", (user_id,))
    data = cur.fetchall()
    cur.close()

    return jsonify(data)


# ================= DELETE =================
@app.route('/delete-expense/<int:id>', methods=['DELETE'])
def delete_expense(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM expenses WHERE id=%s", (id,))
    mysql.connection.commit()
    cur.close()

    return jsonify({"message": "Deleted"})


# ================= UPDATE =================
@app.route('/update-expense/<int:id>', methods=['PUT'])
def update_expense(id):
    try:
        data = request.json

        cur = mysql.connection.cursor()

        cur.execute("""
            UPDATE expenses
            SET title=%s, amount=%s, category=%s, date=%s
            WHERE id=%s
        """, (
            data['title'],
            data['amount'],
            data['category'],
            data['date'],
            id
        ))

        mysql.connection.commit()
        cur.close()

        return jsonify({"message": "Updated"})

    except Exception as e:
        return jsonify({"message": str(e)}), 400


# ================= SEARCH =================
@app.route('/search-expense/<int:user_id>', methods=['GET'])
def search_expense(user_id):
    q = request.args.get('q')

    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT * FROM expenses
        WHERE user_id=%s
        AND (
            title LIKE %s OR
            category LIKE %s OR
            date LIKE %s
        )
    """, (
        user_id,
        f"%{q}%",
        f"%{q}%",
        f"%{q}%"
    ))

    data = cur.fetchall()
    cur.close()

    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)