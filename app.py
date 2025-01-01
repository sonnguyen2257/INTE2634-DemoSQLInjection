from flask import Flask, request, jsonify
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
        password TEXT NOT NULL
    )
    """)
    # Add some sample data
    cursor.execute("INSERT OR IGNORE INTO users (username, password) VALUES ('admin', '083a301369cd711e9803f7d90d342a3778f9cb864ab22992b49fccddc3b9256c')")
    cursor.execute("INSERT OR IGNORE INTO users (username, password) VALUES ('user123', 'userpassword')")
    conn.commit()
    conn.close()

@app.route("/")
def home():
    return "Welcome to the Vulnerable Flask App! Test SQL injection at /vuln."

# Vulnerable endpoint
@app.route("/vuln", methods=["GET"])
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


@app.route("/login",methods=["GET"])
def loginPage():
    return "<html><body><form action='/login' method='post'>Username: <input type='text' name='username'><br>Password: <input type='password' name='password'><br><input type='submit' value='Login'></form></body></html>"

@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()
    # Deliberately vulnerable query (string concatenation instead of parameterized query)
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    print(f"Executing query: {query}") 
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()
    except sqlite3.OperationalError as e:
        print(f"Something went wrong with the query. Exception: {e}")
        bad_response = {"message":"bad query"}
        conn.close()
        return bad_response 


    if rows:
        return jsonify(rows)
    else:
        return jsonify("No users found."),404

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=8080)