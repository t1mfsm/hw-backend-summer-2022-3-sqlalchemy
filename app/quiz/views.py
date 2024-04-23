from aiohttp.web_exceptions import HTTPConflict, HTTPNotFound
from aiohttp_apispec import querystring_schema, request_schema, response_schema

from app.quiz.models import AnswerModel
from app.quiz.schemes import (
    ListQuestionSchema,
    QuestionSchema,
    ThemeIdSchema,
    ThemeListSchema,
    ThemeSchema,
)
from app.web.app import View
from app.web.mixins import AuthRequiredMixin
from app.web.utils import json_response


class ThemeAddView(View):
    @request_schema(ThemeSchema)
    @response_schema(ThemeSchema)
    async def post(self):
        await AuthRequiredMixin.check_auth_admin(self.request)
        data = self.data
        theme = await self.store.quizzes.get_theme_by_title(data.get("title"))
        if theme:
            raise HTTPConflict

        theme = await self.store.quizzes.create_theme(data.get("title"))

        return json_response(data=ThemeSchema().dump(theme))


class ThemeListView(View):
    @response_schema(ThemeListSchema)
    async def get(self):
        await AuthRequiredMixin.check_auth_admin(self.request)
        themes = await self.store.quizzes.list_themes()

        return json_response(data={"themes": [ThemeSchema().dump(theme) for theme in themes]})


class QuestionAddView(View):
    @request_schema(QuestionSchema)
    @response_schema(QuestionSchema)
    async def post(self):
        await AuthRequiredMixin.check_auth_admin(self.request)
        data = self.data
        theme = await self.store.quizzes.check_theme_by_id(data.get("theme_id"))
        if not theme:
            raise HTTPNotFound

        question = await self.store.quizzes.create_question(data.get("title"), data.get("theme_id"),
                                                            [AnswerModel(**answer_data) for answer_data in
                                                             data.get("answers")])

        return json_response(data=QuestionSchema().dump(question))


class QuestionListView(View):
    @querystring_schema(ThemeIdSchema)
    @response_schema(ListQuestionSchema)
    async def get(self):
        await AuthRequiredMixin.check_auth_admin(self.request)

        questions = await self.store.quizzes.list_questions()

        return json_response(data={"questions": [QuestionSchema().dump(question) for question in questions]})
