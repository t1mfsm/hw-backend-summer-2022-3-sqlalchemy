from aiohttp_apispec import request_schema, response_schema, docs

from app.admin.schemes import AdminSchema
from app.web.app import View


class AdminLoginView(View):
    @docs(tags=["admin"], summary="Login admin", description="Login admin")
    @request_schema(AdminSchema)
    @response_schema(AdminSchema, 200)
    async def post(self):
        raise NotImplementedError


class AdminCurrentView(View):
    @docs(tags=["admin"], summary="Admin current", description="Get admin current data")
    @response_schema(AdminSchema, 200)
    async def get(self):
        raise NotImplementedError
