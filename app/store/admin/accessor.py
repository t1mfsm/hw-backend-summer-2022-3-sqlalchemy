from sqlalchemy import select

from app.admin.models import Admin, AdminModel
from app.base.base_accessor import BaseAccessor


class AdminAccessor(BaseAccessor):
    async def get_by_email(self, email: str) -> Admin | None:
        query = select(AdminModel).where(AdminModel.email == email)

        async with self.app.database.session() as session:
            admin: AdminModel | None = await session.scalar(query)

        if not admin:
            return None

        return Admin(id=admin.id, email=admin.email, password=admin.password)

    async def create_admin(self, email: str, password: str) -> Admin:
        new_admin = AdminModel(email=email, password=password)

        async with self.app.database.session() as session:
            session.add(new_admin)

        return Admin(id=new_admin.id, email=new_admin.email)
