from collections.abc import Iterable, Sequence

from aiohttp.web_exceptions import HTTPConflict, HTTPBadRequest
from sqlalchemy import select, insert

from app.base.base_accessor import BaseAccessor
from app.quiz.models import (
    AnswerModel,
    QuestionModel,
    ThemeModel,
)


class QuizAccessor(BaseAccessor):
    async def create_theme(self, title: str) -> ThemeModel:
        if not title:
            raise HTTPConflict

        insert_request = insert(ThemeModel).values(title=title)
        async with self.app.database.session() as session:
            await session.execute(insert_request)
            await session.commit()

            return await self.get_theme_by_title(title)

    async def get_theme_by_title(self, title: str) -> ThemeModel | None:
        select_request = select(ThemeModel).where(ThemeModel.title == title)
        async with self.app.database.session() as session:
            res = await session.execute(select_request)

            try:
                new_res = res.scalars().one()
                return ThemeModel(id=new_res.id, title=new_res.title)
            except Exception:
                return None

    async def check_theme_by_id(self, id_: int) -> ThemeModel | None:
        select_request = select(ThemeModel).where(ThemeModel.id == id_)
        async with self.app.database.session() as session:
            try:
                res = await session.execute(select_request)
                new_res = res.scalars().one()
            except Exception:
                return None

            return ThemeModel(id=new_res.id, title=new_res.title)

    async def get_theme_by_id(self, id_: int) -> ThemeModel | None:
        select_request = select(ThemeModel).where(ThemeModel.id == id_)
        async with self.app.database.session() as session:
            res = await session.execute(select_request)
            new_res = res.scalars().one()

            return ThemeModel(id=new_res.id, title=new_res.title)

    async def list_themes(self) -> Sequence[ThemeModel]:
        select_request = select(ThemeModel)
        async with self.app.database.session() as session:
            res = await session.execute(select_request)
            new_res = res.scalars()

            data = list()
            for row in new_res:
                data.append(ThemeModel(id=row.id, title=row.title))

            return data

    async def check_answers(self, answers: list[AnswerModel]) -> None:
        true_answers_count = 0
        for answer in answers:
            if answer.is_correct:
                true_answers_count += 1

        if true_answers_count != 1 or len(answers) <= 1:
            raise HTTPBadRequest

    async def create_question(
        self, title: str, theme_id: int, answers: Iterable[AnswerModel]
    ) -> QuestionModel:
        await self.check_answers(answers)

        insert_request = insert(QuestionModel).values(title=title, theme_id=theme_id)
        async with self.app.database.session() as session:
            await session.execute(insert_request)
            await session.commit()

            res = await session.execute(select(QuestionModel).where(QuestionModel.title == title))
            result_question = res.scalars().one()
            id_ = result_question.id

            for answer in answers:
                insert_request_answer = insert(AnswerModel).values(question_id=id_, title=answer.title,
                                                                   is_correct=answer.is_correct)
                await session.execute(insert_request_answer)
                await session.commit()

            return QuestionModel(id=result_question.id, title=result_question.title, theme_id=result_question.theme_id,
                                 answers=await self.get_answers_by_question_id(id_))

    async def get_answers_by_question_id(self, id_: int) -> Sequence[AnswerModel]:
        answers_data = []
        select_request = select(AnswerModel).where(AnswerModel.question_id == id_)
        async with self.app.database.session() as session:
            res = await session.execute(select_request)
            data = res.scalars().all()

            for row in data:
                answers_data.append(AnswerModel(id=row.id, title=row.title, is_correct=row.is_correct,
                                                question_id=row.question_id))

            return answers_data

    async def get_question_by_title(self, title: str) -> QuestionModel | None:
        select_request = select(QuestionModel).where(QuestionModel.title == title)
        async with self.app.database.session() as session:
            res = await session.execute(select_request)
            data = res.scalars().one()

            return QuestionModel(id=data.id, title=data.title, theme_id=data.theme_id)

    async def list_questions(
        self, theme_id: int | None = None
    ) -> Sequence[QuestionModel]:
        questions = []
        select_request = select(QuestionModel)
        async with self.app.database.session() as session:
            res = await session.execute(select_request)

            for row in res.scalars().all():
                ind = row.id
                questions.append(QuestionModel(id=row.id, theme_id=row.theme_id, title=row.title,
                                               answers=await self.get_answers_by_question_id(row.id)))

        return questions
