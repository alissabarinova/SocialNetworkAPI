from app import app, USERS


@app.route("/")
def index():
    response = (
        "<h1>Hello! This is my first project on flask!</h1> "
        "<h2> The current data: </h2>"
        f"USERS: <br>"
        f"{'<br>'.join([user.repr() for user in USERS.values() if user.status == 'exists'])}<br>"
        f"{[k for k in USERS.keys()]}"
    )
    return response
