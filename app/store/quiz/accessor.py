from typing import TYPE_CHECKING

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.base.base_accessor import BaseAccessor
from app.quiz.models import (
    Answer,
    AnswerModel,
    Question,
    QuestionModel,
    Theme,
    ThemeModel,
)

if TYPE_CHECKING:
    pass


class QuizAccessor(BaseAccessor):
    async def create_theme(self, title: str) -> Theme:
        new_theme = ThemeModel(title=title)
        async with self.app.database.session.begin() as session:  # noqa
            session.add(new_theme)

        return Theme(id=new_theme.id, title=new_theme.title)

    async def get_theme_by_title(self, title: str) -> Theme | None:
        async with self.app.database.session() as session:  # noqa
            result = (
                (
                    await session.execute(
                        select(ThemeModel).where(ThemeModel.title == title)
                    )
                )
                .scalars()
                .first()
            )

        if not result:
            return

        return Theme(id=result.id, title=result.title)

    async def get_theme_by_id(self, id_: int) -> Theme | None:
        async with self.app.database.session() as session:  # noqa
            result = (
                (await session.execute(select(ThemeModel).where(ThemeModel.id == id_)))
                .scalars()
                .first()
            )

        if not result:
            return

        return Theme(id=result.id, title=result.title)

    async def list_themes(self) -> list[Theme]:
        async with self.app.database.session() as session:  # noqa
            result = (await session.execute(select(ThemeModel))).scalars().all()

        if not result:
            return result

        return [Theme(id=theme.id, title=theme.title) for theme in result]

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
            await session.commit()

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
        async with self.app.database.session.begin() as session:  # noqa
            session.add(new_question)

        return new_question.to_dc()

    async def get_question_by_title(self, title: str) -> Question | None:
        async with self.app.database.session() as session:  # noqa
            result = await session.execute(
                select(QuestionModel)
                .where(QuestionModel.title == title)
                .options(joinedload(QuestionModel.answers))
            )

        obj: QuestionModel | None = result.scalar()
        if obj is None:
            return

        return obj.to_dc()

    async def list_questions(self, theme_id: int | None = None) -> list[Question]:
        query = select(QuestionModel)
        if theme_id:
            query = query.where(QuestionModel.theme_id == theme_id)
        async with self.app.database.session() as session:  # noqa
            result = await session.execute(
                query.options(joinedload(QuestionModel.answers))
            )

        return [o.to_dc() for o in result.scalars().unique()]
