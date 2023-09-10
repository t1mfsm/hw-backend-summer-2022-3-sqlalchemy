from aiohttp.web_exceptions import HTTPBadRequest, HTTPConflict, HTTPNotFound
from aiohttp_apispec import querystring_schema, request_schema, response_schema
from sqlalchemy.exc import IntegrityError

from app.quiz.models import Answer
from app.quiz.schemes import (ListQuestionSchema, QuestionSchema, ThemeIdSchema, ThemeListSchema, ThemeSchema)
from app.web.app import View
from app.web.mixins import AuthRequiredMixin
from app.web.utils import json_response


class ThemeAddView(AuthRequiredMixin, View):
    @request_schema(ThemeSchema)
    @response_schema(ThemeSchema)
    async def post(self):
        try:
            theme = await self.store.quizzes.create_theme(title=self.data["title"])
        except IntegrityError as e:
            match e.orig.pgcode:
                case '23505':
                    raise HTTPConflict

        return json_response(data=ThemeSchema().dump(theme))


class ThemeListView(AuthRequiredMixin, View):
    @response_schema(ThemeListSchema)
    async def get(self):
        themes = await self.store.quizzes.list_themes()
        return json_response(data=ThemeListSchema().dump({"themes": themes}))


class QuestionAddView(AuthRequiredMixin, View):
    @request_schema(QuestionSchema)
    @response_schema(QuestionSchema)
    async def post(self):
        answers = [
            Answer(title=answer["title"], is_correct=answer["is_correct"])
            for answer in self.data["answers"]
        ]

        if len(set(answer.is_correct for answer in answers)) == 1:
            raise HTTPBadRequest

        try:
            question = await self.store.quizzes.create_question(
                title=self.data["title"],
                theme_id=self.data["theme_id"],
                answers=answers,
            )
        except IntegrityError as e:
            match e.orig.pgcode:
                case '23503':
                    raise HTTPNotFound

        return json_response(data=QuestionSchema().dump(question))


class QuestionListView(AuthRequiredMixin, View):
    @querystring_schema(ThemeIdSchema)
    @response_schema(ListQuestionSchema)
    async def get(self):
        questions = await self.store.quizzes.list_questions(
            theme_id=self.data.get("theme_id")
        )

        return json_response(
            data=ListQuestionSchema().dump({"questions": questions})
        )
