from typing import TYPE_CHECKING

from app.admin.models import AdminModel
from app.base.base_accessor import BaseAccessor

if TYPE_CHECKING:
    from app.web.app import Application


class AdminAccessor(BaseAccessor):
    async def connect(self, app: "Application") -> None:
        self.app = app

    async def get_by_email(self, email: str) -> AdminModel | None:
        for admin in self.app.store.admins:
            if email == admin:
                pass

    async def create_admin(self, email: str, password: str) -> AdminModel:
        raise NotImplementedError
