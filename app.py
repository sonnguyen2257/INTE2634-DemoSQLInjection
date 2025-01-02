from flask import Flask, request, jsonify,render_template
import hashlib
import sqlite3,os

if "test.db" in os.listdir():
    os.remove("test.db")

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()
    # Create a basic users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        hashed_passwd TEXT NOT NULL
    )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS shoppinglist (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   things TEXT NOT NULL,
                   type TEXT NOT NULL
                   )
    """)
    # Add some sample data
    cursor.execute("INSERT OR IGNORE INTO users (username, password, hashed_passwd) VALUES ('intruder1', 'admin123', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9')")
    cursor.execute("INSERT OR IGNORE INTO users (username, password, hashed_passwd) VALUES ('intruder2', 's3cure4Passwd@59383a', '008ee9c46305f856b4b98a3c3b9304785ee995bfbf2b38beddd572b54cc658b1')")

    conn.commit()
    conn.close()

@app.route("/")
def home():
    # return "Welcome to the Vulnerable Flask App! Test SQL injection at /vuln."
    return render_template("login.html")

# Vulnerable endpoint
@app.route("/api", methods=["GET"])
def vuln():
    username = request.args.get("username")
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()
    
    # Deliberately vulnerable query (string concatenation instead of parameterized query)
    query = f"SELECT * FROM users WHERE username = '{username}'"

    try:
        print(f"Executing query: {query}")  # Log the query for debugging/testing
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()

        if rows:
            # Obfuscate sensitive information (e.g., hide password or mask it)
            sanitized_rows = [
                {"id": row[0], "username": row[1]} for row in rows
            ]
            return jsonify(sanitized_rows)  # Return data without leaking sensitive info
        else:
            return jsonify({"message": "No users found."}), 404
    except sqlite3.OperationalError as e:
        print(f"Something went wrong with the query. Exception: {e}")
        conn.close()
        return jsonify({"message": "Bad query syntax."}), 400


# @app.route("/login",methods=["GET"])
# def loginPage():
#     return render_template("login.html")

@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    # convert password to sha256 hash  
    if not isinstance(password, str):
        password = str(password)
    password = hashlib.sha256(password.encode()).hexdigest()
    print(f"Hashed password: {password}")

    # Connect to the database
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()

    # Deliberately vulnerable query (string concatenation instead of parameterized query)
    query = f"SELECT * FROM users WHERE username = '{username}'"

    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        if rows and len(rows[0]) == 4:
            retrieved_password = rows[0][3]
            print(f"Retrieved password: {retrieved_password}")
            if password == retrieved_password:
                welcome_user_html = f'<html><body><h1>Welcome back <b style="color:green">{username}</b></h1></body></html>'
                return welcome_user_html
        else:
            return '<html>Invalid login <a href="/">click here</a> to return</html>'
    except sqlite3.OperationalError as e:
        print(f"Something went wrong with the query. Exception: {e}")
        bad_response = {"message":"bad query"}
        conn.close()
        return bad_response 


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=8080)