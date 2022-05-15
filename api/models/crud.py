from sqlalchemy import func
from sqlalchemy.orm import Session

from . import models
from services import service
from schemas.schema import (CategoriesCountSchema, CategorySchema, AddCategorySchema, PostSchema, AddPostSchema,
                            AddImageSchema, ImageSchema)


def get_all_category(db: Session) -> list[models.Category]:
    return db.query(models.Category).all()


def get_all_count_category(db: Session) -> list[CategoriesCountSchema]:
    categories = db.query(models.Category.id, models.Category.title).order_by(models.Category.id).all()
    counts = db.query(func.count(models.Post.id), models.Post.category_id).group_by(models.Post.category_id).order_by(
        models.Post.category_id).all()
    return service.create_response_category_count(categories, counts)


def get_category_by_id(db: Session, category_id: int) -> CategorySchema:
    return db.query(models.Category).filter(models.Category.id == category_id).one()


def delete_category(db: Session, category_id: int) -> CategorySchema:
    category = db.query(models.Category).filter(models.Category.id == category_id).one()
    db.delete(category)
    db.flush()
    db.commit()
    return category


def create_category(db: Session, data: AddCategorySchema) -> CategorySchema:
    category = models.Category(title=data.title)
    db.add(category)
    db.flush()
    db.commit()
    return category


def get_posts_by_category_id(db: Session, category_id: int) -> list[PostSchema]:
    return db.query(models.Post).filter(models.Post.category_id == category_id).all()


def create_post(db: Session, data: AddPostSchema) -> PostSchema:
    post = models.Post(
        title=data.title,
        category_id=data.category_id,
        text=data.text
    )
    db.add(post)
    db.flush()
    db.commit()
    return post


def get_all_posts(db: Session) -> list[PostSchema]:
    return db.query(models.Post).all()


def update_post_add_image(db: Session, data: AddImageSchema) -> ImageSchema:
    post = db.query(models.Post).filter(models.Post.id == data.post_id).one()
    img = models.Image(
        post_id=data.post_id,
        img=data.img
    )
    post.img.append(img)
    db.add(post)
    db.flush()
    db.commit()
    return img
