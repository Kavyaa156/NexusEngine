from typing import TypeVar, Generic, Type, Optional, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from models_db import Base

ModelType = TypeVar("ModelType", bound=Base)

class BaseRepository(Generic[ModelType]):
    def __init__(self, session: AsyncSession, model: Type[ModelType]):
        self.session = session
        self.model = model

    async def get_by_id(self, id: Any) -> Optional[ModelType]:
        return await self.session.get(self.model, id)

    async def create(self, obj_in: ModelType) -> ModelType:
        self.session.add(obj_in)
        await self.session.commit()
        await self.session.refresh(obj_in)
        return obj_in

    async def update(self, obj_in: ModelType) -> ModelType:
        await self.session.commit()
        await self.session.refresh(obj_in)
        return obj_in
    async def delete(self, id: Any) -> bool:
        """Delete a record by its primary key. Returns True if deleted, False if not found."""
        obj = await self.get_by_id(id)
        if obj:
            await self.session.delete(obj)
            await self.session.commit()
            return True
        return False

    async def exists(self, id: Any) -> bool:
        """Check if a record exists by primary key."""
        obj = await self.get_by_id(id)
        return obj is not None

    async def count(self) -> int:
        """Return the total count of records in the table."""
        stmt = select(func.count()).select_from(self.model)
        result = await self.session.execute(stmt)
        return result.scalar_one()