from fastapi import APIRouter, Body, Request, HTTPException, Response, status
from fastapi.encoders import jsonable_encoder
from typing import List
from models import Blog, BlogUpdate

router = APIRouter()


#creating new blog
@router.post("/", response_description="Add Blog", status_code=status.HTTP_201_CREATED, response_model=Blog)
def create_book(request: Request, blog: Blog = Body(...)):
    blog = jsonable_encoder(blog)
    new_blog = request.app.database["blogs"].insert_one(blog)
    created_book = request.app.database["blogs"].find_one({"_id": new_blog.inserted_id})


    return created_book


# fetshing all blogs
@router.get("/", response_description="fetch blogs", response_model=List[Blog])
def list_blogs(request: Request):
    blogs = list(request.app.database["blogs"].find())
    return blogs


# fetch blog by Id
@router.get("/{id}", response_description="Fetsh blog by id", response_model=Blog)
def find_blog(id: str, request: Request):
    if (blog := request.app.database["blogs"].find_one({"_id":id})) is not None:
        return blog

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with ID {id} not found")


# Bonus: full text search filter
@router.get("/search/{query}", response_description="full text search", response_model={})
async def search(query: str, request: Request):
    # Perform the search
    result = list(request.app.database["blogs"].find({
        "$or": [{
            "title": {
                "$regex": query,
                "$options": "i"
            }
        }, {
            "content": {
                "$regex": query,
                "$options": "i"
            }
        }, {
            "author": {
                "$regex": query,
                "$options": "i"
            }
        }]
    }))
    return result



@router.put("/{id}", response_description="Update a blog", response_model=Blog)
def update_blog(id: str, request: Request, blog: BlogUpdate = Body(...)):
    blog = {k: v for k, v in blog.dict().items() if v is not None}

    if len(blog) >= 1:
        update_result = request.app.database["blogs"].update_one(
            {"_id": id}, {"$set": blog}
        )

        if update_result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with ID {id} not found")

    if (
        existing_blog := request.app.database["blogs"].find_one({"_id": id})
    ) is not None:
        return existing_blog

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with ID {id} not found")


@router.delete("/{id}", response_description="Delete a blog")
def delete_blog(id: str, request: Request, response: Response):
    delete_result = request.app.database["blogs"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with ID {id} not found")
