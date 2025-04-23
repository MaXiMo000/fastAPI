import time
from fastapi import FastAPI, Response, status, HTTPException
# from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
# from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

# idx = 1
# myPosts = [{"title": "title of post", "content": "content of post", "published": False, "id": 1}, 
#         {"title": "title of post 2", "content": "content of post 2", "published": True, "id": 2}]

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    # rating: Optional[int] = None
while True:
    try:
        conn = psycopg2.connect(
        host='localhost',
        port='5433',
        database='fastAPI',
        user='postgres',
        password='Ritish@1995',
        cursor_factory=RealDictCursor
        )
        cursor = conn.cursor()
        print("Database connection successful")
        break
    except Exception as error:
        print("Database connection failed:")
        print(error)
        time.sleep(2)


@app.get("/")
def root():
    return {"Hello": "World"}

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    print(posts)

    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    # print(f"Title: {post.title} Content: {post.content} Published: {post.published} Rating: {post.rating}")
    # post_data = post.model_dump()
    # global idx
    # idx += 1
    # post_data['id'] = idx
    # myPosts.append(post_data)
    # return {f"data": post_data}

    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    new_post = cursor.fetchone()

    conn.commit()
    return{"data": f"created post and {new_post}"}

# def find_post(id):
#     for i in myPosts:
#         if i["id"] == id:
#             return i

# @app.get("/posts/latest")
# def get_latest_post():
#     latest = myPosts[-1]
#     return {"latest posts": latest}

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    # post = find_post(id)
    # if(post == None):
    #     return {"post details: No post with that id found"}
    # if not post:
        # response.status_code = 404
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"Post details: No post with id {id} found"}
        # raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"Post details: No post with id {id} found")

    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    post = cursor.fetchone()

    print(post)

    return {"Post details": f"Here for id {id} and data: {post}"}

# def find_index_post(id):
#     for i, p in enumerate(myPosts):
#         if p['id'] == id:
#             return i # returns index

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # index = find_index_post(id)

    cursor.execute("""DELETE FROM posts where id = %s RETURNING *""", (str((id))))
    deleted_post = cursor.fetchone()
    conn.commit()

    if(deleted_post == None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist")
    # myPosts.pop(index)
    # return {"message" :"Posts was successfully deleted"}
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    # post_data = post.model_dump()

    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
            (post.title, post.content, post.published, id))
    updated_post = cursor.fetchone()
    conn.commit()

    if(updated_post == None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist")
    
    # global idx
    # idx += 1
    # post_data['id'] = idx
    # myPosts[index] = post_data

    return{"message": f"Post with id {id} Updated"}