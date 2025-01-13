from cs50 import SQL
from datetime import date
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///tasks.db")


# Create a function that is a decorator required to access certain routes
def login_required(f):
    """
    Decorate routes to require login.
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


@app.route("/")
@login_required
def index():
    """Set the route / and renders the index.html page"""
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Validate the presence of a username, password and confirmation match
        if not username:
            flash("Must provide username.", "danger")
            return redirect("/register")
        if not password:
            flash("Must provide password.", "danger")
            return redirect("/register")
        if password != confirmation:
            flash("Passwords do not match.", "danger")
            return redirect("/register")

        # Check to see if username already exists
        existing_user = db.execute("SELECT * FROM users WHERE username = ?", username)
        if existing_user:
            flash("Username already exists.", "danger")
            return redirect("/register")

        # Hash the user's password for secure storage
        hashed_password = generate_password_hash(password)

        # Insert the new user into the database
        db.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                   username, hashed_password)

        # Redirect the user to the login page after successful registration
        flash("Registration successful! Please log in.", "success")
        return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # User reached route via POST
    if request.method == "POST":
        # Ensure there is a username
        if not request.form.get("username"):
            flash("Must provide username.", "danger")
            return redirect("/login")

        # Ensure there is a password
        elif not request.form.get("password"):
            flash("Must provide password", "danger")
            return redirect("/login")

        # Retrieve user from the database
        user = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(user) != 1 or not check_password_hash(
            user[0]["password"], request.form.get("password")
        ):
            flash("Invalid username or password", "danger")
            return redirect("/login")

        # Remember which user has logged in
        session["user_id"] = user[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/tasks", methods=["GET"])
@login_required
def tasks():
    """Display all tasks to the logged-in user, ordered by due date"""
    tasks = db.execute("SELECT * FROM tasks WHERE user_id = ? ORDER BY due_date",
                       session["user_id"])

    # Get today's date
    today = date.today()

    # Group tasks by due date
    tasks_by_date = {}
    for task in tasks:
        # Convert due_date to date object
        due_date = date.fromisoformat(task["due_date"])
        if due_date >= today:
            # Format the date to "Month Day, Year"
            formatted_due_date = due_date.strftime("%B %d, %Y")
            if formatted_due_date not in tasks_by_date:
                tasks_by_date[formatted_due_date] = []

            tasks_by_date[formatted_due_date].append(task)

    # Pass the grouped tasks to tasks.html for display
    return render_template("tasks.html", tasks_by_date=tasks_by_date)


@app.route("/add_task", methods=["POST"])
@login_required
def add_task():
    """Add a new task to the database"""
    # Get task description and due date from the form
    description = request.form.get("description")
    due_date = request.form.get("due_date")

    # Check if there is a description and a due date
    if not description or not due_date:
        flash("You must provide a task and a due date.", "danger")
        return redirect("/tasks")

    # Insert the task into the database
    db.execute("INSERT INTO tasks (user_id, description, due_date, completed) VALUES (?, ?, ?, ?)",
               session["user_id"], description, due_date, 0)

    return redirect("/tasks")


@app.route("/complete_task/<int:task_id>", methods=["POST"])
@login_required
def complete_task(task_id):
    """Mark a task as completed"""
    # Update the tasks completed status in the database
    db.execute("UPDATE tasks SET completed = 1 WHERE id = ? AND user_id = ?",
               task_id, session["user_id"])

    return redirect("/tasks")


@app.route("/unmark_task/<int:task_id>", methods=["POST"])
@login_required
def unmark_task(task_id):
    """Unselect completed tasks"""
    db.execute("UPDATE tasks SET completed = 0 WHERE id = ? AND user_id = ?",
               task_id, session["user_id"])

    return redirect("/tasks")


@app.route("/delete_task/<int:task_id>", methods=["POST"])
@login_required
def delete_task(task_id):
    """Delete task from the database"""
    # Remove task from the database
    db.execute("DELETE FROM tasks WHERE id = ? AND user_id = ?", task_id, session["user_id"])

    return redirect("/tasks")


@app.route("/past_tasks", methods=["GET"])
@login_required
def past_tasks():
    """Display past tasks to the logged-in user, ordered by due date"""
    tasks = db.execute("SELECT * FROM tasks WHERE user_id = ? ORDER BY due_date DESC",
                       session["user_id"])

    # Get today's date
    today = date.today()

    # Filter past tasks only
    past_tasks = []
    for task in tasks:
        due_date = date.fromisoformat(task["due_date"])
        if due_date < today:
            # Format the date to "Month Day, Year"
            formatted_due_date = due_date.strftime("%B %d, %Y")
            task["formatted_due_date"] = formatted_due_date
            past_tasks.append(task)

    # Pass past tasks to past_tasks.html for display
    return render_template("past_tasks.html", past_tasks=past_tasks)


@app.route("/statistics", methods=["GET"])
@login_required
def statistics():
    """Display statistics for the logged-in user"""
    # Get total number of tasks and completed tasks
    total_tasks = db.execute("SELECT COUNT(*) FROM tasks WHERE user_id = ?",
                             session["user_id"])[0]['COUNT(*)']
    completed_tasks = db.execute(
        "SELECT COUNT(*) FROM tasks WHERE user_id = ? AND completed = 1", session["user_id"])[0]['COUNT(*)']

    # Get current date and current month
    today = date.today()
    current_month = today.strftime("%Y-%m")

    # Query to get task completion data grouped by date (replaced DATE(timestamp) with DATE(due_date))
    daily_completion = db.execute(
        "SELECT DATE(due_date) as task_date, COUNT(CASE WHEN completed = 1 THEN 1 END) as completed_tasks, COUNT(*) as total_tasks FROM tasks WHERE user_id = ? AND strftime('%Y-%m', due_date) = ? GROUP BY task_date ORDER BY task_date", session["user_id"], current_month)

    # Extract the labels (dates) and the completion rates
    dates = [
        date.fromisoformat(row['task_date']).strftime("%B %d, %Y")
        for row in daily_completion
    ]
    completion_rates = [
        round((row['completed_tasks'] / row['total_tasks'])
              * 100, 2) if row['total_tasks'] > 0 else 0
        for row in daily_completion
    ]

    # Query to get task completion data grouped by month (for line chart)
    monthly_completion = db.execute(
        "SELECT STRFTIME('%Y-%m', due_date) as task_month, COUNT(CASE WHEN completed = 1 THEN 1 END) as completed_tasks, COUNT(*) as total_tasks FROM tasks WHERE user_id = ? GROUP BY task_month ORDER BY task_month", session["user_id"])

    # Extract the labels (months) and the completion rates for the line chart
    months = [
        date.fromisoformat(row['task_month'] + '-01').strftime("%B, %Y")
        for row in monthly_completion
    ]
    monthly_completion_rates = [
        round((row['completed_tasks'] / row['total_tasks'])
              * 100, 2) if row['total_tasks'] > 0 else 0
        for row in monthly_completion
    ]

    return render_template("statistics.html",
                           total_tasks=total_tasks,
                           completed_tasks=completed_tasks,
                           dates=dates,
                           completion_rates=completion_rates,
                           months=months,
                           monthly_completion_rates=monthly_completion_rates
                           )


@app.route("/useful_links", methods=["GET"])
@login_required
def useful_links():
    """Set the route /useful_links and renders the useful_links.html page"""
    return render_template("useful_links.html")
