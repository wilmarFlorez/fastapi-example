import psycopg2
from fastapi import FastAPI, HTTPException, status
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


my_posts = [
    {"title": "title_1", "content": "content_1", "id": 1},
    {"title": "title_2", "content": "content_2", "id": 2},
    {"title": "title_3", "content": "content_3", "id": 3},
]


try:
    conn = psycopg2.connect(
        host="localhost",
        dbname="fastapi",
        user="postgres",
        password="123456",
        cursor_factory=RealDictCursor,
    )
    cursor = conn.cursor()
    print("🛢️ DATABASE CONECTED ")
except Exception as e:
    print("DATABASE CONNECTION FAILED")
    print(e)


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
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    print("POSTS", posts)
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute(
        """INSERT INTO posts (title, content, published)
        VALUES(%s,%s,%s) RETURNING *""",
        (post.title, post.content, post.published),
    )
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}


@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    post = cursor.fetchone()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} was not found",
        )
    return {"data": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id=%s returning *""", (str(id)))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} was not found",
        )


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute(
        """UPDATE posts SET title = %s, content = %s, published = %s
        WHERE ID = %s RETURNING *""",
        (post.title, post.content, post.published, str(id)),
    )

    update_post = cursor.fetchone()
    conn.commit()

    if update_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} was not found",
        )

    return {"data": update_post}
