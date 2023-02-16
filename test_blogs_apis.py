from fastapi import FastAPI
from fastapi.testclient import TestClient
from dotenv import dotenv_values
from pymongo import MongoClient
from routes import router as blog_router

app = FastAPI()
config = dotenv_values(".env")
app.include_router(blog_router, tags=["blog"], prefix="/blog")


@app.on_event("startup")
async def startup_event():
    app.mongodb_client = MongoClient(config["ATLAS_URI"])
    app.database = app.mongodb_client[config["DB_NAME"] + "test"]

# @app.on_event("shutdown")
# async def shutdown_event():
#     app.mongodb_client.close()
#     app.database.drop_collection("blogs")

def test_create_blog():
    with TestClient(app) as client:
        response = client.post("/blog/", json={"title": "Title test", "content": "Content test", "author": "Kahouli test", "voteFlag": "False"})
        assert response.status_code == 201

        body = response.json()
        assert body.get("title") == "Title test"
        assert body.get("content") == "Content test"
        assert body.get("author") == "Kahouli test"
        assert body.get("voteFlag") == "False"
        assert "_id" in body


def test_create_blog_missing_title():
    with TestClient(app) as client:
        response = client.post("/blog/", json={"content": "Content test", "author": "Kahouli test", "voteFlag": "False"})
        assert response.status_code == 422


def test_create_blog_missing_author():
    with TestClient(app) as client:
        response = client.post("/blog/", json={"title": "Title test", "content": "Content test", "voteFlag": "False"})
        assert response.status_code == 422


def test_create_blog_missing_voteFlag():
    with TestClient(app) as client:
        response = client.post("/blog/", json={"title": "Title test", "content": "Content test", "author": "Kahouli test"})
        assert response.status_code == 422


def test_get_blog():
    with TestClient(app) as client:
        new_blog = client.post("/blog/", json={"title": "Title test", "content": "Content test", "author": "Kahouli test", "voteFlag": "False"}).json()

        get_blog_response = client.get("/blog/" + new_blog.get("_id"))
        assert get_blog_response.status_code == 200
        assert get_blog_response.json() == new_blog


def test_get_blog_unexisting():
    with TestClient(app) as client:
        get_blog_response = client.get("/blog/unexisting_id")
        assert get_blog_response.status_code == 404


# def test_update_book():
#     with TestClient(app) as client:
#         new_book = client.post("/book/", json={"title": "Don Quixote", "author": "Miguel de Cervantes", "synopsis": "..."}).json()

#         response = client.put("/book/" + new_book.get("_id"), json={"title": "Don Quixote 1"})
#         assert response.status_code == 200
#         assert response.json().get("title") == "Don Quixote 1"


# def test_update_book_unexisting():
#     with TestClient(app) as client:
#         update_book_response = client.put("/book/unexisting_id", json={"title": "Don Quixote 1"})
#         assert update_book_response.status_code == 404


# def test_delete_book():
#     with TestClient(app) as client:
#         new_book = client.post("/book/", json={"title": "Don Quixote", "author": "Miguel de Cervantes", "synopsis": "..."}).json()

#         delete_book_response = client.delete("/book/" + new_book.get("_id"))
#         assert delete_book_response.status_code == 204


# def test_delete_book_unexisting():
    # with TestClient(app) as client:
    #     delete_book_response = client.delete("/book/unexisting_id")
    #     assert delete_book_response.status_code == 404

