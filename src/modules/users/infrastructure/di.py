from ..domain.ports import IUserReader, IUserWriter
from .repositories.user_repository import UserRepository


def register_users(reg: dict):
    reg[IUserReader] = UserRepository
    reg[IUserWriter] = UserRepository
