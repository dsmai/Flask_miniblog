import sqlite3

import click
from flask import current_app, g


# connect to the database
# g is a speicial object unique for each request
# It is used to store data that might be accessed by multiple functions during the request.
# The connection is stored and reused
# instead of creating a new connection if get_db is called a second time in the same request.


def get_db():
    if "db" not in g:
        # establishes a connection to the file pointed at by the "DATABASE" config key
        g.db = sqlite3.connect(current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES)

        # sqlite3.Row tells the connection to return rows that behave like dicts.
        # This allows accessing the columns by name.
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db():
    # get_db() returns a database connection, which is used
    # to execute the commands read from the file
    db = get_db()

    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))


# this decorator here is to link to a command line command
# CL command "init-db" will calll init_db() function
# and show success message to the user.
@click.command("init-db")
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")


# register with the Application
# close_db() and init_db_command() need to be registered
# with the application instance.
# write a function that takes an application and does the registration
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
