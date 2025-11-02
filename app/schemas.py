from pydantic import BaseModel

class createPost(BaseModel):
    title : str
    content : str

