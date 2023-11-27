import random
from http import HTTPStatus
import requests


ENDPOINT = "http://127.0.0.1:5000"


def create_payload():
    return {
        "first_name": "Name",
        "last_name": "Surname",
        "email": "test@mail.com",
    }


def test_user_create():
    payload = create_payload()
    create_response = requests.post(f"{ENDPOINT}/users/create", json=payload)
    assert create_response.status_code == HTTPStatus.OK

    user_data = create_response.json()
    
    user_id = user_data["id"]

    assert user_data["first_name"] == payload["first_name"]
    assert user_data["last_name"] == payload["last_name"]
    assert user_data["email"] == payload["email"]
    assert user_data["posts"] == "[]"
    assert user_data["total_reactions"] == 0


    get_response = requests.get(f"{ENDPOINT}/users/{user_id}")
    assert get_response.json()["first_name"] == payload["first_name"]
    assert get_response.json()["last_name"] == payload["last_name"]
    assert get_response.json()["email"] == payload["email"]
    assert get_response.json()["posts"] == "[]"
    assert get_response.json()["total_reactions"] == 0
    assert get_response.json()["id"] == user_id


    delete_response = requests.delete(f"{ENDPOINT}/users/{user_id}")
    assert delete_response.status_code == HTTPStatus.OK
    assert delete_response.json()["first_name"] == payload["first_name"]
    assert delete_response.json()["last_name"] == payload["last_name"]
    assert delete_response.json()["email"] == payload["email"]
    assert delete_response.json()["total_reactions"] == 0
    assert delete_response.json()["status"] == "deleted"


def test_post_create():
    payload = create_payload()
    create_response = requests.post(f"{ENDPOINT}/users/create", json=payload)
    assert create_response.status_code == HTTPStatus.OK

    user_data = create_response.json()

    user_id = user_data["id"]

    assert user_data["first_name"] == payload["first_name"]
    assert user_data["last_name"] == payload["last_name"]
    assert user_data["email"] == payload["email"]
    assert user_data["posts"] == "[]"
    assert user_data["total_reactions"] == 0

    get_response = requests.get(f"{ENDPOINT}/users/{user_id}")
    assert get_response.json()["first_name"] == payload["first_name"]
    assert get_response.json()["last_name"] == payload["last_name"]
    assert get_response.json()["email"] == payload["email"]
    assert get_response.json()["posts"] == "[]"
    assert get_response.json()["total_reactions"] == 0
    assert get_response.json()["id"] == user_id

    post_payload = {
        "author_id": user_id,
        "text": "text"
    }

    create_post_response = requests.post(f"{ENDPOINT}/posts/create", json=post_payload)
    assert create_post_response.status_code == HTTPStatus.OK

    post_data = create_post_response.json()
    post_id = post_data["id"]
    assert post_data["author_id"] == post_payload["author_id"]
    assert post_data["text"] == post_payload["text"]
    assert post_data["reactions"] == []
    assert post_data["id"] == post_id

    get_post_response = requests.get(f"{ENDPOINT}/posts/{post_id}")
    assert get_post_response.json()["author_id"] == post_payload["author_id"]
    assert get_post_response.json()["text"] == post_payload["text"]
    assert get_post_response.json()["id"] == post_id
    assert get_post_response.json()["reactions"] == []

    delete_post_response = requests.delete(f"{ENDPOINT}/posts/{post_id}")
    assert delete_post_response.status_code == HTTPStatus.OK
    assert delete_post_response.json()["author_id"] == post_payload["author_id"]
    assert delete_post_response.json()["text"] == post_payload["text"]
    assert delete_post_response.json()["id"] == post_id
    assert delete_post_response.json()["reactions"] == []
    assert delete_post_response.json()["status"] == "deleted"

    delete_response = requests.delete(f"{ENDPOINT}/users/{user_id}")
    assert delete_response.status_code == HTTPStatus.OK
    assert delete_response.json()["first_name"] == payload["first_name"]
    assert delete_response.json()["last_name"] == payload["last_name"]
    assert delete_response.json()["email"] == payload["email"]
    assert delete_response.json()["total_reactions"] == 0
    assert delete_response.json()["status"] == "deleted"


def test_user_create_wrong_data():
    payload = create_payload()
    payload["email"] = "test"
    create_response = requests.post(f"{ENDPOINT}/users/create", json=payload)
    assert create_response.status_code == HTTPStatus.BAD_REQUEST

def test_create_reaction():
    payload = create_payload()
    create_response = requests.post(f"{ENDPOINT}/users/create", json=payload)
    assert create_response.status_code == HTTPStatus.OK

    user_data = create_response.json()

    user_id = user_data["id"]

    assert user_data["first_name"] == payload["first_name"]
    assert user_data["last_name"] == payload["last_name"]
    assert user_data["email"] == payload["email"]
    assert user_data["posts"] == "[]"
    assert user_data["total_reactions"] == 0

    get_response = requests.get(f"{ENDPOINT}/users/{user_id}")
    assert get_response.json()["first_name"] == payload["first_name"]
    assert get_response.json()["last_name"] == payload["last_name"]
    assert get_response.json()["email"] == payload["email"]
    assert get_response.json()["posts"] == "[]"
    assert get_response.json()["total_reactions"] == 0
    assert get_response.json()["id"] == user_id

    post_payload = {
        "author_id": user_id,
        "text": "text"
    }

    create_post_response = requests.post(f"{ENDPOINT}/posts/create", json=post_payload)
    assert create_post_response.status_code == HTTPStatus.OK

    post_data = create_post_response.json()
    post_id = post_data["id"]
    assert post_data["author_id"] == post_payload["author_id"]
    assert post_data["text"] == post_payload["text"]
    assert post_data["reactions"] == []
    assert post_data["id"] == post_id

    get_post_response = requests.get(f"{ENDPOINT}/posts/{post_id}")
    assert get_post_response.json()["author_id"] == post_payload["author_id"]
    assert get_post_response.json()["text"] == post_payload["text"]
    assert get_post_response.json()["id"] == post_id
    assert get_post_response.json()["reactions"] == []

    react_payload = {
        "user_id": user_id,
        "reaction": "string"
    }
    create_react_response = requests.post(f"{ENDPOINT}/posts/{post_id}/reaction", json=react_payload)
    assert create_react_response.status_code == HTTPStatus.OK

    delete_post_response = requests.delete(f"{ENDPOINT}/posts/{post_id}")
    assert delete_post_response.status_code == HTTPStatus.OK
    assert delete_post_response.json()["author_id"] == post_payload["author_id"]
    assert delete_post_response.json()["text"] == post_payload["text"]
    assert delete_post_response.json()["id"] == post_id
    assert delete_post_response.json()["reactions"] == []
    assert delete_post_response.json()["status"] == "deleted"

    delete_response = requests.delete(f"{ENDPOINT}/users/{user_id}")
    assert delete_response.status_code == HTTPStatus.OK
    assert delete_response.json()["first_name"] == payload["first_name"]
    assert delete_response.json()["last_name"] == payload["last_name"]
    assert delete_response.json()["email"] == payload["email"]
    assert delete_response.json()["total_reactions"] == 0
    assert delete_response.json()["status"] == "deleted"


def test_get_users_posts():
    for i in range(1, 4):
        payload = {
            "first_name": f"Name{i}",
            "last_name": f"Surname{i}",
            "email": f"test{i}@mail.com",
        }
        create_response = requests.post(f"{ENDPOINT}/users/create", json=payload)
        assert create_response.status_code == HTTPStatus.OK

        user_data = create_response.json()

        user_id = user_data["id"]

        assert user_data["first_name"] == payload["first_name"]
        assert user_data["last_name"] == payload["last_name"]
        assert user_data["email"] == payload["email"]
        assert user_data["posts"] == "[]"
        assert user_data["total_reactions"] == 0

        get_response = requests.get(f"{ENDPOINT}/users/{user_id}")
        assert get_response.json()["first_name"] == payload["first_name"]
        assert get_response.json()["last_name"] == payload["last_name"]
        assert get_response.json()["email"] == payload["email"]
        assert get_response.json()["posts"] == "[]"
        assert get_response.json()["total_reactions"] == 0
        assert get_response.json()["id"] == user_id

        for j in range(3):
            post_payload = {
                "author_id": user_id,
                "text": f"text{j}"
            }
            create_post_response = requests.post(f"{ENDPOINT}/posts/create", json=post_payload)
            assert create_post_response.status_code == HTTPStatus.OK

            post_data = create_post_response.json()
            post_id = post_data["id"]
            assert post_data["author_id"] == post_payload["author_id"]
            assert post_data["text"] == post_payload["text"]
            assert post_data["reactions"] == []
            assert post_data["id"] == post_id

            get_post_response = requests.get(f"{ENDPOINT}/posts/{post_id}")
            assert get_post_response.json()["author_id"] == post_payload["author_id"]
            assert get_post_response.json()["text"] == post_payload["text"]
            assert get_post_response.json()["id"] == post_id
            assert get_post_response.json()["reactions"] == []

            if i == 1:
                for k in range(j+4):
                    react_payload = {
                        "user_id": user_id,
                        "reaction": f"{random.randint(1,6)}"
                    }
                    create_react_response = requests.post(f"{ENDPOINT}/posts/{post_id}/reaction", json=react_payload)
                    assert create_react_response.status_code == HTTPStatus.OK
            elif i == 2:
                for k in range(j+2):
                    react_payload = {
                        "user_id": user_id,
                        "reaction": f"{random.randint(1,6)}"
                    }
                    create_react_response = requests.post(f"{ENDPOINT}/posts/{post_id}/reaction", json=react_payload)
                    assert create_react_response.status_code == HTTPStatus.OK
            else:
                for k in range(j+1):
                    react_payload = {
                        "user_id": user_id,
                        "reaction": f"{random.randint(1, 6)}"
                    }
                    create_react_response = requests.post(f"{ENDPOINT}/posts/{post_id}/reaction", json=react_payload)
                    assert create_react_response.status_code == HTTPStatus.OK



        for sort_type in ["asc", "desc"]:
            sort_payload = {"sort": f"{sort_type}"}
            create_sort_response = requests.get(f"{ENDPOINT}/users/{user_id}/posts", json=sort_payload)
            assert create_sort_response.status_code == HTTPStatus.OK
            posts_data = create_sort_response.json()
            if i == 1:
                if sort_type == "asc":
                    assert len(posts_data["posts"][0]["reactions"]) == 4
                    assert len(posts_data["posts"][1]["reactions"]) == 5
                    assert len(posts_data["posts"][2]["reactions"]) == 6
                else:
                    assert len(posts_data["posts"][0]["reactions"]) == 6
                    assert len(posts_data["posts"][1]["reactions"]) == 5
                    assert len(posts_data["posts"][2]["reactions"]) == 4
            elif i == 2:
                if sort_type == "asc":
                    assert len(posts_data["posts"][0]["reactions"]) == 2
                    assert len(posts_data["posts"][1]["reactions"]) == 3
                    assert len(posts_data["posts"][2]["reactions"]) == 4
                else:
                    assert len(posts_data["posts"][0]["reactions"]) == 4
                    assert len(posts_data["posts"][1]["reactions"]) == 3
                    assert len(posts_data["posts"][2]["reactions"]) == 2
            else:
                if sort_type == "asc":
                    assert len(posts_data["posts"][0]["reactions"]) == 1
                    assert len(posts_data["posts"][1]["reactions"]) == 2
                    assert len(posts_data["posts"][2]["reactions"]) == 3
                else:
                    assert len(posts_data["posts"][0]["reactions"]) == 3
                    assert len(posts_data["posts"][1]["reactions"]) == 2
                    assert len(posts_data["posts"][2]["reactions"]) == 1


    for sort_type in ["asc", "desc"]:
        list_payload = {"type": "list",
                        "sort": f"{sort_type}",
                        }
        create_list_response = requests.get(f"{ENDPOINT}/users/leaderboard", json=list_payload)
        assert create_list_response.status_code == HTTPStatus.OK

        list_data = create_list_response.json()
        if sort_type == "asc":
            assert list_data["users"][0]["first_name"] == "Name1"
            assert list_data["users"][1]["first_name"] == "Name2"
            assert list_data["users"][2]["first_name"] == "Name3"
        else:
            assert list_data["users"][0]["first_name"] == "Name3"
            assert list_data["users"][1]["first_name"] == "Name2"
            assert list_data["users"][2]["first_name"] == "Name1"


    graph_payload = {
        "type": "graph",
        }
    graph_response = requests.get(f"{ENDPOINT}/users/leaderboard", json=graph_payload)
    assert graph_response.status_code == HTTPStatus.OK


