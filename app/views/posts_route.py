from app import app, USERS, models, POSTS
from flask import request, Response
import json
import uuid
from http import HTTPStatus


@app.post("/posts/create")
def post_create():
    data = request.get_json()
    post_id = str(uuid.uuid1())
    author_id = data["author_id"]
    text = data["text"]
    if author_id not in USERS.keys():
        return Response(status=HTTPStatus.NOT_FOUND)

    new_post = models.posts_class.Post(post_id, author_id, text, [])
    POSTS[post_id] = new_post

    temp_user = USERS[author_id]
    temp_user.posts.append(new_post)

    response_data = {
        "id": new_post.post_id,
        "author_id": new_post.author_id,
        "text": new_post.text,
        "reactions": new_post.reactions,
    }

    response = Response(
        json.dumps(response_data), HTTPStatus.OK, mimetype="application/json"
    )
    return response


@app.get("/posts/<post_id>")
def get_post(post_id):
    if post_id not in POSTS.keys():
        return Response(status=HTTPStatus.NOT_FOUND)
    temp_post = POSTS[post_id]
    response_data = {
        "id": temp_post.post_id,
        "author_id": temp_post.author_id,
        "text": temp_post.text,
        "reactions": temp_post.reactions,
    }

    response = Response(
        json.dumps(response_data), HTTPStatus.OK, mimetype="application/json"
    )
    return response

@app.delete("/posts/<post_id>")
def delete_post(post_id):
    if post_id not in POSTS.keys():
        return Response(status=HTTPStatus.NOT_FOUND)
    temp_post = POSTS[post_id]

    t = len(temp_post.reactions)
    user = USERS[temp_post.author_id]
    user.total_reactions -= t

    temp_post.reactions = []
    temp_post.status = "deleted"
    response_data = {
        "id": temp_post.post_id,
        "author_id": temp_post.author_id,
        "text": temp_post.text,
        "reactions": temp_post.reactions,
        "status": temp_post.status,
    }

    response = Response(
        json.dumps(response_data), HTTPStatus.OK, mimetype="application/json"
    )
    return response

@app.post("/posts/<post_id>/reaction")
def create_reaction(post_id):
    data = request.get_json()
    user_id = data["user_id"]
    new_reaction = data["reaction"]
    if post_id not in POSTS.keys() or user_id not in USERS.keys():
        return Response(status=HTTPStatus.NOT_FOUND)
    current_post = POSTS[post_id]
    current_post.reactions.append(new_reaction)
    temp_user = USERS[user_id]
    temp_user.total_reactions += 1
    return Response(status=HTTPStatus.OK)
