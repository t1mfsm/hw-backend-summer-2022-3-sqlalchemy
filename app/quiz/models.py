from sqlalchemy import Column, BigInteger, String, ForeignKey

from app.store.database.sqlalchemy_base import BaseModel


class ThemeModel(BaseModel):
    __tablename__ = "themes"
    id = Column(BigInteger, primary_key=True)
    title = Column(String, unique=True, nullable=False)



class QuestionModel(BaseModel):
    __tablename__ = "questions"
    id = Column(BigInteger, primary_key=True)
    theme_id = Column(BigInteger, ForeignKey("themes.id"), nullable=False)
    title = Column(String, unique=True, nullable=False)


class AnswerModel(BaseModel):
    __tablename__ = "answers"
    id = Column(BigInteger, primary_key=True)
