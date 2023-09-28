from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint("blog", __name__)


# this view function display all the blog posts, starting from the latest
@bp.route("/")
def index():
    db = get_db()
    # here is the JOIN SQL query
    posts = db.execute(
        "SELECT p.id, title, body, created, author_id, username"
        " FROM post p JOIN user u ON p.author_id = u.id"
        " ORDER BY created DESC"
    ).fetchall()
    return render_template("blog/index.html", plugs=posts)  # 2nd param is the keywords argument


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error = None
        # created = something # why/how do we store the time the post created in db?
        # no need because it's auto-create the time-stamp here
        # created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, (check schema)

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute("INSERT INTO post (title, body, author_id)" " VALUES (?, ?, ?)", (title, body, g.user["id"]))
            db.commit()
            return redirect(url_for("blog.index"))
    return render_template("blog/create.html")
