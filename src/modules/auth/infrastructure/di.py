from ..domain.ports import IRolePermissionReader, IRoleReader
from .repositories import RolePermissionRepository, RoleRepository


def register_auth(reg: dict):
    # Role
    reg[IRoleReader] = RoleRepository
    
    # Role permission
    reg[IRolePermissionReader] = RolePermissionRepository
    