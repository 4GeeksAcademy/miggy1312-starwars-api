from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from typing import List, Optional

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(80), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    
    favorites: Mapped[List["Favorite"]] = relationship(back_populates="user")

    def serialize(self):
        return { "id": self.id, "email": self.email }

class People(db.Model):
    __tablename__ = 'people'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    
    favorites: Mapped[List["Favorite"]] = relationship(back_populates="people")

    def serialize(self):
        return { "id": self.id, "name": self.name }

class Planet(db.Model):
    __tablename__ = 'planet'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    
    favorites: Mapped[List["Favorite"]] = relationship(back_populates="planet")

    def serialize(self):
        return { "id": self.id, "name": self.name }

class Favorite(db.Model):
    __tablename__ = 'favorite'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    planet_id: Mapped[Optional[int]] = mapped_column(ForeignKey('planet.id'), nullable=True)
    people_id: Mapped[Optional[int]] = mapped_column(ForeignKey('people.id'), nullable=True)

    user: Mapped["User"] = relationship(back_populates="favorites")
    planet: Mapped["Planet"] = relationship(back_populates="favorites")
    people: Mapped["People"] = relationship(back_populates="favorites")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
            "people_id": self.people_id,
            "planet_name": self.planet.name if self.planet else None,
            "people_name": self.people.name if self.people else None
        }