from dataclasses import dataclass, field

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, mapped_column, Mapped

from app.store.database.sqlalchemy_base import db


@dataclass
class Theme:
    id: int | None
    title: str


@dataclass
class Question:
    id: int | None
    title: str
    theme_id: int
    answers: list["Answer"] = field(default_factory=list)


@dataclass
class Answer:
    title: str
    is_correct: bool


class ThemeModel(db):
    __tablename__ = "themes"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(unique=True)
    question = relationship("QuestionModel")

    def to_dc(self) -> Theme:
        return Theme(
            id=self.id,
            title=self.title,
        )


class QuestionModel(db):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(unique=True)
    theme_id: Mapped[int] = mapped_column(
        ForeignKey("themes.id", ondelete="CASCADE"), nullable=False
    )
    answers = relationship("AnswerModel")

    def to_dc(self) -> Question:
        return Question(
            id=self.id,
            title=self.title,
            theme_id=self.theme_id,
            answers=[a.to_dc() for a in self.answers],
        )


class AnswerModel(db):
    __tablename__ = "answers"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    is_correct: Mapped[bool]
    question_id: Mapped[int] = mapped_column(
        ForeignKey("questions.id", ondelete="CASCADE")
    )

    def to_dc(self) -> Answer:
        return Answer(title=self.title, is_correct=self.is_correct)
