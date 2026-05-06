from random import randint

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: int | None = None


my_posts = [
    {"title": "title_1", "content": "content_1", "id": 1},
    {"title": "title_2", "content": "content_2", "id": 2},
    {"title": "title_3", "content": "content_3", "id": 3},
]


def find_post(id: int) -> dict | None:
    posts = [post for post in my_posts if post.get("id", None) == id]
    return posts[0] if posts else None


def find_index(id: int) -> int | None:
    for i, post in enumerate(my_posts):
        if post.get("id") == id:
            return i
    return None


@app.get("/")
def root():
    return {"data": "hello world"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.model_dump()
    post_dict["id"] = randint(1, 500)
    my_posts.append(post_dict)
    return {"data": post}


@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} was not found",
        )
    return {"data": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index(id)
    if index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} was not found",
        )
    my_posts.pop(index)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index(id)

    if index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} was not found",
        )
    post_dict = post.model_dump()
    post_dict["id"] = id
    my_posts[index] = post_dict
    return {"data": post_dict}
