from app import app, USERS


@app.route("/")
def index():
    response = (
        "<h1>Hello! This is my first project on flask!</h1> "
        "<br>"
        "<h2> The current data about users: </h2>"
        f"{'<br>'.join([user.repr() for user in USERS.values()])}<br>"
    )
    return response
