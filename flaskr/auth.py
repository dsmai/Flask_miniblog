import functools

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

# The url_prefix will be prepended to all the URLs associated with the blueprint.
bp = Blueprint("auth", __name__, url_prefix="/auth")


# When Flask receives a request to auth/register, it will call the
# register() view function, which returns render_template("auth/register.html")
# as response.
@bp.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None

        if not username:
            error = "Invalid entry. Username is required."
        elif not password:
            error = "Invalid entry. Password is required."

        if error is None:
            try:
                # here we execute() take a SQL query
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template("auth/register.html")


# This view function allow user to log in
@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None

        # first, query/get the user from the database, select from table "user"
        user = db.execute("SELECT * FROM user WHERE username = ?", (username,)).fetchone()

        # now check if username and password entered is correct
        if user is None:
            error = "Incorrect username."
        elif not check_password_hash(user["password"], password):
            error = "Incorrect password."

        if error is None:
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("index"))

        flash(error)

    return render_template("auth/login.html")
