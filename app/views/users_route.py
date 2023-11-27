from app import app, USERS, models, EMAILS
from flask import request, Response, url_for
import json
import uuid
from http import HTTPStatus
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt



@app.post("/users/create")
def user_create():
    data = request.get_json()
    user_id = str(uuid.uuid1())
    first_name = data["first_name"]
    last_name = data["last_name"]
    email = data["email"]

    if not models.users_class.User.is_valid_email(email):
        return Response(status=HTTPStatus.BAD_REQUEST)
    if email in EMAILS:
        return Response(
            "This email is already registered", status=HTTPStatus.BAD_REQUEST
        )

    if user_id in USERS.keys():
        return Response(
            "This user is already registered", status=HTTPStatus.BAD_REQUEST
        )

    EMAILS.append(email)
    new_user = models.users_class.User(user_id, first_name, last_name, email, 0, [])

    USERS[user_id] = new_user
    new_user_posts = json.dumps(
        [
            {
                "id": p.post_id,
                "author_id": p.author_id,
                "text": p.text,
                "reactions": p.reactions,
            }
            for p in new_user.posts
        ]
    )

    response = Response(
        json.dumps(
            {
                "id": new_user.id,
                "first_name": new_user.first_name,
                "last_name": new_user.last_name,
                "email": new_user.email,
                "total_reactions": new_user.total_reactions,
                "posts": new_user_posts,
            }
        ),
        HTTPStatus.OK,
        mimetype="application/json",
    )
    return response


@app.get("/users/<user_id>")
def get_user(user_id):
    if user_id not in USERS.keys():
        return Response(status=HTTPStatus.NOT_FOUND)
    temp_user = USERS[user_id]
    temp_user_posts = json.dumps(
        [
            {
                "id": p.post_id,
                "author_id": p.author_id,
                "text": p.text,
                "reactions": p.reactions,
            }
            for p in temp_user.posts
        ]
    )

    response = Response(
        json.dumps(
            {
                "id": temp_user.id,
                "first_name": temp_user.first_name,
                "last_name": temp_user.last_name,
                "email": temp_user.email,
                "total_reactions": temp_user.total_reactions,
                "posts": temp_user_posts,
            }
        ),
        HTTPStatus.OK,
        mimetype="application/json",
    )
    return response


@app.delete("/users/<user_id>")
def delete_user(user_id):
    if user_id not in USERS.keys():
        return Response(status=HTTPStatus.NOT_FOUND)
    temp_user = USERS[user_id]
    temp_user.status = "deleted"
    EMAILS.pop(EMAILS.index(temp_user.email))
    temp_user_posts = json.dumps(
        [
            {
                "id": p.post_id,
                "author_id": p.author_id,
                "text": p.text,
                "reactions": p.reactions,
            }
            for p in temp_user.posts
        ]
    )
    response = Response(
        json.dumps(
            {
                "id": temp_user.id,
                "first_name": temp_user.first_name,
                "last_name": temp_user.last_name,
                "email": temp_user.email,
                "total_reactions": temp_user.total_reactions,
                "posts": temp_user_posts,
                "status": temp_user.status,
            }
        ),
        HTTPStatus.OK,
        mimetype="application/json",
    )

    return response



@app.get("/users/<user_id>/posts")
def get_users_posts(user_id):
    data = request.get_json()
    type_sort = data["sort"]
    user = USERS[user_id]

    if type_sort == "asc":
        sorted_posts = [post.to_dict() for post in sorted(user.posts) if post.status == "exists"]
        return Response(
            json.dumps({"posts": sorted_posts}),
            status=HTTPStatus.OK,
            mimetype="application/json",
        )
    elif type_sort == "desc":
        sorted_posts = [post.to_dict() for post in sorted(user.posts, reverse=True) if post.status == "exists"]
        return Response(
            json.dumps({"posts": sorted_posts}),
            status=HTTPStatus.OK,
            mimetype="application/json",
        )
    else:
        return Response(status=HTTPStatus.BAD_REQUEST)




@app.get("/users/leaderboard")
def get_statistics():
    data = request.get_json()
    stat_type = data["type"]
    if stat_type == "graph":
        tempUSERS = dict(sorted(USERS.items(), reverse=True))
        sorted_users = [tempUSERS[k].to_dict() for k in tempUSERS.keys() if tempUSERS[k].status == "exists"]

        fig, ax = plt.subplots()

        user_names = [
            f'{user["first_name"]} {user["last_name"]} id: {user["id"]}'
            for user in sorted_users
        ]
        users_reactions = [user["total_reactions"] for user in sorted_users]

        ax.bar(user_names, users_reactions)
        ax.set_ylabel("User's total reactions")
        ax.set_title("Graph of users by number of reactions")

        plt.savefig("app/static/graph_of_users_reactions.png")

        return Response(
            f"""<img src= "{url_for('static', filename='graph_of_users_reactions.png')}">""",
            status=HTTPStatus.OK,
            mimetype="text/html",
        )

    elif stat_type == "list":
        stat_sort = data["sort"]

        if stat_sort == "asc":
            temp_USERS = dict(sorted(USERS.items()))
            sorted_users = [temp_USERS[k].to_dict() for k in temp_USERS.keys() if temp_USERS[k].status == "exists"]
            return Response(
                json.dumps({"users": sorted_users}),
                status=HTTPStatus.OK,
                mimetype="application/json",
            )

        elif stat_sort == "desc":
            temp_USERS = dict(sorted(USERS.items(), reverse=True))
            sorted_users = [temp_USERS[k].to_dict() for k in temp_USERS.keys() if temp_USERS[k].status == "exists"]
            return Response(
                json.dumps({"users": sorted_users}),
                status=HTTPStatus.OK,
                mimetype="application/json",
            )

        else:
            return Response(status=HTTPStatus.BAD_REQUEST)

    else:
        return Response(status=HTTPStatus.BAD_REQUEST)
