from sqlalchemy import select, ScalarResult
from sqlalchemy.orm import joinedload, selectinload

from app.base.base_accessor import BaseAccessor
from app.quiz.models import (
    Answer,
    AnswerModel,
    Question,
    QuestionModel,
    Theme,
    ThemeModel,
)


class QuizAccessor(BaseAccessor):
    async def create_theme(self, title: str) -> Theme:
        new_theme = ThemeModel(title=title)

        async with self.app.database.session.begin() as session:
            session.add(new_theme)

        return Theme(id=new_theme.id, title=new_theme.title)

    async def get_theme_by_title(self, title: str) -> Theme | None:
        query = select(ThemeModel).where(ThemeModel.title == title)

        async with self.app.database.session() as session:
            theme: ThemeModel | None = await session.scalar(query)

        if not theme:
            return None

        return Theme(id=theme.id, title=theme.title)

    async def get_theme_by_id(self, id_: int) -> Theme | None:
        query = select(ThemeModel).where(ThemeModel.id == id_)

        async with self.app.database.session() as session:
            theme: ThemeModel | None = await session.scalar(query)

        if not theme:
            return None

        return Theme(id=theme.id, title=theme.title)

    async def list_themes(self) -> list[Theme]:
        query = select(ThemeModel)

        async with self.app.database.session() as session:
            themes: ScalarResult[ThemeModel] = await session.scalars(query)

        if not themes:
            return []

        return [Theme(id=theme.id, title=theme.title) for theme in themes.all()]

    async def create_answers(
        self, question_id: int, answers: list[Answer]
    ) -> list[Answer]:
        new_answers = [
            AnswerModel(
                title=answer.title,
                is_correct=answer.is_correct,
                question_id=question_id,
            )
            for answer in answers
        ]

        async with self.app.database.session() as session:  # noqa
            session.add_all(new_answers)

        return [
            Answer(title=answer.title, is_correct=answer.is_correct)
            for answer in new_answers
        ]

    async def create_question(
        self, title: str, theme_id: int, answers: list[Answer]
    ) -> Question:
        new_question = QuestionModel(
            title=title,
            theme_id=theme_id,
            answers=[
                AnswerModel(
                    title=answer.title,
                    is_correct=answer.is_correct,
                )
                for answer in answers
            ],
        )

        async with self.app.database.session.begin() as session:
            session.add(new_question)

        return Question(
            id=new_question.id,
            title=new_question.title,
            theme_id=new_question.theme_id,
            answers=[
                Answer(title=answer.title, is_correct=answer.is_correct)
                for answer in new_question.answers
            ],
        )

    async def get_question_by_title(self, title: str) -> Question | None:
        query = (
            select(QuestionModel)
            .where(QuestionModel.title == title)
            .options(selectinload(QuestionModel.answers))
        )

        async with self.app.database.session() as session:
            question: QuestionModel | None = await session.scalar(query)

        if not question:
            return None

        return Question(
            id=question.id,
            title=question.title,
            theme_id=question.theme_id,
            answers=[
                Answer(
                    title=answer.title,
                    is_correct=answer.is_correct
                )
                for answer in question.answers
            ],
        )

    async def list_questions(self, theme_id: int | None = None) -> list[Question]:
        query = select(QuestionModel)
        if theme_id:
            query = query.where(QuestionModel.theme_id == theme_id)
        query = query.options(joinedload(QuestionModel.answers))

        async with self.app.database.session() as session:  # noqa
            questions: ScalarResult[QuestionModel] = await session.scalars(query)

        return [
            Question(
                id=question.id,
                title=question.title,
                theme_id=question.theme_id,
                answers=[
                    Answer(title=answer.title, is_correct=answer.is_correct)
                    for answer in question.answers
                ],
            )
            for question in questions.unique()
        ]
