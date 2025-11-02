from fastapi import FastAPI, HTTPException
from app.schemas import createPost


app = FastAPI()

text_posts = {
    3: {"author": "Alex", "content": "FastAPI is really fast!"},
    4: {"author": "Sarah", "content": "Just learned about Pydantic models."},
    5: {"author": "Mike", "content": "How do I use path parameters?"},
    6: {"author": "Jenna", "content": "My first endpoint is working! 🎉"},
    7: {"author": "Chris", "content": "Working on data validation."},
    8: {"author": "Emily", "content": "What's the best way to handle errors?"},
    9: {"author": "David", "content": "Exploring dependency injection."},
    10: {"author": "Laura", "content": "Trying to connect to a database."},
    11: {"author": "Ronith", "content": "Here is my second post about testing."},
    12: {"author": "Abhinav", "content": "Async and await are powerful."}
}

@app.get("/posts")
def get_posts(limit: int=None):
    if limit:
        return list(text_posts.values())[:limit]
    return text_posts

@app.get("/posts/{id}")
def get_post(id : int):
    if id not in text_posts:
        raise HTTPException(status_code=404, detail="Post not found")
    else:
        return text_posts.get(id)

@app.post("/posts")
def create_post(post : createPost):
    new_post = {"title" : post.title, "content" : post.content}
    text_posts[max(text_posts.keys()) + 1] = new_post
    return new_post
