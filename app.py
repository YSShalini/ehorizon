from flask import Flask, redirect, url_for, render_template, request, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'ehorizon project'

# Function to connect to the MySQL database
def connect_db():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='YSshalini@09',
            database='ehorizon'
        )
        print("Database connected successfully")
        return conn
    except Exception as e:
        print("Error connecting to database:", str(e))
        raise

# Function to check if a user exists in the database
def user_exists(rollno, password):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM user WHERE rollno=%s AND password=%s", (rollno, password))
    user = cur.fetchone()
    conn.close()
    return user

# Function to add a new user to the database
# Function to add a new user to the database
def add_user(rollno, password, firstname, lastname, email, busnumber, busstop):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO user (rollno, password, firstname, lastname, email, busnumber, busstop) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (rollno, password, firstname, lastname, email, busnumber, busstop))
    conn.commit()
    conn.close()

def fetch_bus_details(bus_number):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM busdetails WHERE busno = %s", (bus_number,))
    bus_details = cur.fetchall()
    conn.close()
    return bus_details

@app.route("/show_transport", methods=["GET", "POST"])
def show_transport():
    if request.method == "POST":
        bus_number = request.form.get("bus_number")
        if bus_number:
            bus_details = fetch_bus_details(bus_number)
            return render_template("transport.html", bus_details=bus_details)
    return render_template("transport_form.html")

@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        rollno = request.form["rollno"]
        password = request.form["password"]
        user = user_exists(rollno, password)
        if user:
            # Store user information in session
            session['rollno'] = rollno
            session['firstname'] = user[2]  # Assuming the firstname is stored at index 2
            # Redirect to home page
            return redirect(url_for("home"))
        else:
            error = "Invalid credentials. Please try again."
    return render_template("login.html", error=error)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        rollno = request.form.get("rollno")
        password = request.form.get("password")
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        email = request.form.get("email")
        busno = request.form.get("busnumber")  # Change 'busno' to 'busnumber'
        busstop = request.form.get("busstop")

        # Check if any required field is missing
        if None in [rollno, password, firstname, lastname, email, busno, busstop]:
            error_message = "One or more required fields are missing."
            return render_template("login.html", error=error_message)

        try:
            add_user(rollno, password, firstname, lastname, email, busno, busstop)
            return redirect(url_for("home"))
        except Exception as e:
            error_message = "Error occurred while registering user: {}".format(str(e))
            return render_template("login.html", error=error_message)
    return render_template("login.html")


@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route('/transport')
def transport():
    return render_template('transport_form.html')

if __name__ == "__main__":
    app.run(debug=True)
