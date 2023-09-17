from typing import Optional
from app.library.db import db
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

class BookModel(db.Model):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(unique=True, primary_key=True)
    title: Mapped[str] = mapped_column(String)
    subtitle: Optional[Mapped[str]] = mapped_column(String)
    reference: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    description = db.Column(db.String, nullable=True)
