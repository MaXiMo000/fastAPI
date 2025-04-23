from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import List, Optional
from sqlalchemy.orm import Session
from .. import models, schemas, Oauth2
from ..database import get_db
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags= ["Posts"]
)

@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: str = Depends(Oauth2.get_current_user), limit: int = 10, skip:int = 0, search: Optional[str] = ""):
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes"))\
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)\
        .filter(models.Post.title.contains(search))\
        .group_by(models.Post.id)\
        .offset(skip)\
        .limit(limit)\
        .all()

    return [{"post": post, "votes": votes} for post, votes in results]


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(Oauth2.get_current_user)
):
    print(f"Current user email: {current_user.email}, ID: {current_user.id}")

    new_post = models.Post(
        **post.model_dump(),
        owner_id=current_user.id
    )

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    print(post)

    if(post == None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist")

    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: str = Depends(Oauth2.get_current_user)):
    print(current_user.email)
    post_query = db.query(models.Post).filter(models.Post.id == id)

    if(post_query.first() == None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist")
    
    if(post_query.first().owner_id != current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not author of this post")
    
    post_query.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: str = Depends(Oauth2.get_current_user)): 
    print(current_user.email) 
    post_query = db.query(models.Post).filter(models.Post.id == id)

    updated_post = post_query.first()

    if(updated_post == None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist")
    
    if(post_query.first().owner_id != current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not author of this post")
    
    post_query.update(post.model_dump(), synchronize_session=False)

    db.commit()

    return post_query.first()
