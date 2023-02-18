import uuid
from pydantic import BaseModel, Field
from typing import Optional

class Blog(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    title: str = Field(...)
    content: str = Field(...)
    author: str = Field(...)
    upVote: int = Field(...)
    downVote: int = Field(...)
    
    # since FastAPI allow to test endpoints by providing a REST API swagger interface , we need to pass a static object to be displayed as payload in the POST request in interface
    # that's what exactly schema_extra do
    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "title": "Aloui blog",
                "content": "Aloui content",
                "author": "Aloui Kahouli",
                "upVore": 0,
                "downVore": 0
            }
        }



class BlogUpdate(BaseModel):
    title: str = Optional[str]
    content: str = Optional[str]
    author: str = Optional[str]
    upVote: int = Optional[int]
    downVote: int = Optional[int]
    # the same here having a static payload to test the PUT request
    class Config:
        schema_extra = {
            "example": {
                "title": "Aloui blog",
                "content": "Aloui content",
                "author": "Aloui Kahouli",
                "upVore": 0,
                "downVore": 0
            }
        }

