from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Integer, Boolean, Text, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from typing import List, Optional

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(200), nullable=False)
    profile_image_url: Mapped[str] = mapped_column(String(200), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False, default=True)

    fav_character: Mapped[List["FavoriteCharacter"]] = relationship(
        back_populates='user', 
        cascade='all, delete-orphan')

    blog_posts: Mapped[List["BlogPost"]] = relationship(
        back_populates='author', 
        cascade='all, delete-orphan')

    fav_planet: Mapped[List["FavoritePlanet"]] = relationship(
        back_populates='user', 
        cascade='all, delete-orphan')

    # Relationship back to posts
    posts: Mapped[List["Post"]] = relationship(back_populates="author")

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "profile_image_url": self.profile_image_url,
            "is_active": self.is_active,
        }
    

class Post(db.Model):
    __tablename__ = "post"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    image_url: Mapped[str] = mapped_column(String(200), nullable=False)
    caption: Mapped[str] = mapped_column(String(255))
    location: Mapped[str] = mapped_column(String(100))
    is_active: Mapped[bool] = mapped_column(Boolean(), default=True)

    # Relationship to user
    author: Mapped["User"] = relationship(back_populates="posts")
    
    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "image_url": self.image_url,
            "caption": self.caption,
            "location": self.location,
            "is_active": self.is_active
        }
    
class Follower(db.Model):
    __tablename__ = 'followers'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)

    
class Character(db.Model):
    __tablename__ = 'character'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    height: Mapped[Optional[str]] = mapped_column(String(20))
    mass: Mapped[Optional[str]] = mapped_column(String(20))
    hair_color: Mapped[Optional[str]] = mapped_column(String(50))
    skin_color: Mapped[Optional[str]] = mapped_column(String(50))
    eye_color: Mapped[Optional[str]] = mapped_column(String(50))
    birth_year: Mapped[Optional[str]] = mapped_column(String(20))
    gender: Mapped[Optional[str]] = mapped_column(String(20))

    # Relationships
    favorited_by: Mapped[List["FavoriteCharacter"]] = relationship(
        back_populates='character', cascade='all, delete-orphan')

    def __repr__(self) -> str:
        return f'<Character {self.name}>'

    def serialize(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year,
            "gender": self.gender
        }


class FavoriteCharacter(db.Model):
    __tablename__ = 'favorite_character'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    character_id: Mapped[int] = mapped_column(ForeignKey('character.id'), nullable=False)

    # Relationships
    user: Mapped["User"] = relationship(back_populates='fav_character')
    character: Mapped["Character"] = relationship(back_populates='favorited_by')

    __table_args__ = (
        UniqueConstraint('user_id', 'character_id', name='unique_user_character'),
    )

    def __repr__(self) -> str:
        return f'<FavoriteCharacter user_id={self.user_id} character_id={self.character_id}>'

    def serialize(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character_id": self.character_id,
            "character": self.character.serialize() if self.character else None
        }


class Planet(db.Model):
    __tablename__ = 'planet'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    orbital_period: Mapped[Optional[str]] = mapped_column(String(20))
    diameter: Mapped[Optional[str]] = mapped_column(String(20))
    climate: Mapped[Optional[str]] = mapped_column(String(100))
    gravity: Mapped[Optional[str]] = mapped_column(String(50))

    # Relationships
    favorited_by: Mapped[List["FavoritePlanet"]] = relationship(
        back_populates='planet', cascade='all, delete-orphan')

    def __repr__(self) -> str:
        return f'<Planet {self.name}>'

    def serialize(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "orbital_period": self.orbital_period,
            "diameter": self.diameter,
            "climate": self.climate,
            "gravity": self.gravity
        }

class FavoritePlanet(db.Model):
    __tablename__ = 'favorite_planet'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    planet_id: Mapped[int] = mapped_column(ForeignKey('planet.id'), nullable=False)

    # Relationships
    user: Mapped["User"] = relationship(back_populates='fav_planet')
    planet: Mapped["Planet"] = relationship(back_populates='favorited_by')

    __table_args__ = (
        UniqueConstraint('user_id', 'planet_id', name='unique_user_planet'),
    )

    def __repr__(self) -> str:
        return f'<FavoritePlanet user_id={self.user_id} planet_id={self.planet_id}>'

    def serialize(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
            "planet": self.planet.serialize() if self.planet else None
        }


class BlogPost(db.Model):
    __tablename__ = 'blog_post'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    is_published: Mapped[bool] = mapped_column(Boolean, default=False)
    featured_image_url: Mapped[Optional[str]] = mapped_column(String(500))

    # Relationships
    author: Mapped["User"] = relationship(back_populates='blog_posts')

    def __repr__(self) -> str:
        return f'<BlogPost {self.title}>'

    def serialize(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "author_id": self.author_id,
            "is_published": self.is_published,
            "featured_image_url": self.featured_image_url,
        }





# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import String, Boolean
# from sqlalchemy.orm import Mapped, mapped_column

# db = SQLAlchemy()

# class User(db.Model):
#     id: Mapped[int] = mapped_column(primary_key=True)
#     email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
#     password: Mapped[str] = mapped_column(nullable=False)
#     is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)


#     def serialize(self):
#         return {
#             "id": self.id,
#             "email": self.email,
#             # do not serialize the password, its a security breach
#         }
