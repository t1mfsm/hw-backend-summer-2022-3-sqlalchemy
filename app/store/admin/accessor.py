import typing

from sqlalchemy import select

from app.admin.models import Admin, AdminModel
from app.base.base_accessor import BaseAccessor

if typing.TYPE_CHECKING:
    from app.web.app import Application


class AdminAccessor(BaseAccessor):
    async def get_by_email(self, email: str) -> Admin | None:
        async with self.app.database.session() as session:  # noqa
            result = (
                (
                    await session.execute(
                        select(AdminModel).where(AdminModel.email == email)
                    )
                )
                .scalars()
                .first()
            )

        if not result:
            return

        return Admin(id=result.id, email=result.email, password=result.password)

    async def create_admin(self, email: str, password: str) -> Admin:
        new_admin = AdminModel(email=email, password=password)
        async with self.app.database.session() as session:  # noqa
            session.add(new_admin)
            await session.commit()

        return Admin(id=new_admin.id, email=new_admin.email)
