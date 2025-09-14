from typing import Any, Callable, Dict, Type, TypeVar, cast

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    AsyncSessionTransaction,
    async_sessionmaker,
)

RepoType = TypeVar("RepoType")

class SQLAlchemySessionUoW:
    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession],
        repo_factories: Dict[type[Any], Callable[[AsyncSession], Any]]
    ):
        self._session_factory = session_factory
        self._repo_factories = repo_factories
        self._repo_instances: Dict[type[Any], Any] = {}
        self.session: AsyncSession | None = None
        self._transaction: AsyncSessionTransaction | None

    async def __aenter__(self):
        self.session = self._session_factory()
        self._transaction  = await self.session.begin()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        try:
            if exc and self._transaction and self._transaction.is_active:
                await self._transaction.rollback()
            elif self._transaction and self._transaction.is_active:
                await self._transaction.commit()
        finally:
            if self.session:
                await self.session.close()
            self._repo_instances.clear()
            self.session = None
            self._transaction = None

    def get(self, repo_interface: Type[RepoType]) -> RepoType:
        if repo_interface in self._repo_instances:
            return cast(RepoType, self._repo_instances[repo_interface])

        factory = self._repo_factories.get(repo_interface)
        if factory is None:
            raise KeyError(f"No factory registered for {repo_interface!r}")

        assert self.session is not None, "The Unit of Work must be used within an 'async with' context"
        instance = factory(self.session)
        self._repo_instances[repo_interface] = instance
        return cast(RepoType, instance)
