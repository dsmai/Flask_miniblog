import os
from flask import Flask


# this is the application factory function
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello, there is a decorator here
    # this means the view function hello() will be called
    # once a request is made to the "/hello" URL.
    # The route decorator @app.route("/hello")
    # associates the "/hello" URL with the hello() function.
    # In short, route decorator in Flask associates URl routes
    # with view functions, defining the behavior of web app
    # based on the requested URL.
    @app.route("/miumiu")
    def hello():
        return "Hello, Miu Miu!"

    from . import db

    db.init_app(app)

    from . import auth

    # this is to register the blueprint with the main Flask application
    app.register_blueprint(auth.bp)

    from . import blog

    # this is to register the blueprint with the main Flask application
    app.register_blueprint(blog.bp)
    app.add_url_rule("/", endpoint="index")  # this means that the root "/" is also at "index", equivalent
    # it maps the root URL "/" to any endpoint named "index"
    # the actual reason why I need to do the above is, with url_for(),
    # I have to pass in a param which is the view function. From that
    # it will create a URL whose endpoint is the view function name. If
    # let's say my view function name is index(), then the URL endpoint will be like "/index".
    # so to link that with "/" (basically saying they refer to same thing),
    # I need to use add_rule_url()

    return app
