from random import randint

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: int | None = None


my_posts = [
    {"title": "title 1", "content": "content 1", "id": 1},
    {"title": "title 2", "content": "content 2", "id": 2},
]


def find_post(id: int):
    post = [post for post in my_posts if post.get("id") == id]
    return post[0] if post else None


@app.get("/")
def root():
    return {"message": "Hello world"}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


@app.post("/posts")
def create_posts(post: Post):
    post_dict = post.model_dump()
    post_dict["id"] = randint(1, 5000)
    my_posts.append(post_dict)
    return {"data": post}


@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)            
    return {"post_detail": post}
