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


# this view creates a new blog post
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


# this helper function gets the post of the author with id "id"
def get_post(id, check_author=True):
    db = get_db()
    post = db.execute(
        "SELECT p.id, title, body, created, author_id, username"
        " FROM post p JOIN user u ON p.author_id = u.id"
        " WHERE p.id = ?",
        (id,),
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} does not exist.")

    if check_author and post["author_id"] != g.user["id"]:
        abort(403)

    return post


# this view updates the post by user id
@bp.route("/<int:id>/update", methods=("GET", "POST"))
@login_required
def update(id):
    post = get_post(id)

    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error = None

        if not title:
            error = "Title is required."

        # if there is error
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute("UPDATE post SET title = ?, body = ?" " WHERE id = ?", (title, body, id))
            db.commit()
            return redirect(url_for("blog.index"))

    return render_template("blog/update.html", post=post)


# this view/endpoint deletes a blog post
@bp.route("/<int:id>/delete", methods=("POST",))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute("DELETE FROM post WHERE id = ?", (id,))
    db.commit()
    return redirect(url_for("blog.index"))
