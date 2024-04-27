from typing import Dict, Literal, Union

from pydantic import BaseModel

from py_perms.utils import get_all_class_parameters
from py_perms.permissions import OctalPermissions
from py_perms.octals import (
    from_decimal_repr_to_octal_integer,
    from_octal_bit_to_config,
    from_octal_integer,
    OctalConfig
)

class PermissionsConfig(BaseModel):
    """
    """
    read: bool = False
    write: bool = False
    execute: bool = False

    @classmethod
    def from_octal_bit(cls, octal_bit: Union[str, int]) -> 'PermissionsConfig':
        octal_config: OctalConfig = from_octal_bit_to_config(octal_bit=octal_bit)
        return cls(
            read=octal_config.read, write=octal_config.write, execute=octal_config.execute
        )


class PermissionsByte:
    """
    """
    def __init__(
        self,
        authority: Literal['owner', 'group', 'others'],
        config: PermissionsConfig = PermissionsConfig()
    ):
        self.authority = authority
        self._config = config

        # set permissions for specific authority
        self.permissions = OctalPermissions(authority=self.authority)

    def __add__(self, permission_byte: 'PermissionsByte') -> 'PermissionsCode':
        if not isinstance(permission_byte, PermissionsByte):
            raise TypeError(
                f'can only add PermissionsByte (not "{type(permission_byte)}") to PermissionsByte'
            )
        
        return PermissionsCode._from_permissions_bytes(
            permissions_byte_one=self, permissions_byte_two=permission_byte
        )

    def __str__(self) -> str:
        return repr(self)

    def __repr__(self) -> str:
        return (
            f'<{self.__class__.__name__} authority={self.authority} '
            f'permissions_code={self.permissions_code}>'
        )
        
    @property
    def read_permission(self) -> bool:
        return self._config.read

    @property
    def write_permission(self) -> bool:
        return self._config.write

    @property
    def execute_permission(self) -> bool:
        return self._config.execute
        
    @property
    def permissions_code(self) -> str:
        base_permissions = self.permissions.no_permissions
        if self._config.read:
            base_permissions |= self.permissions.read
        
        if self._config.write:
            base_permissions |= self.permissions.write
        
        if self._config.execute:
            base_permissions |= self.permissions.execute

        return format(base_permissions, 'o').zfill(3)
    
    @property
    def permissions_description(self) -> str:
        permissions_code = self.permissions_code.strip('0')
        permissions_code = permissions_code or 0
        permissions_code = int(permissions_code)
        octal_config: OctalConfig = from_octal_bit_to_config(octal_bit=permissions_code)
        return octal_config.description

    @property
    def permissions_description_detailed(self) -> Dict[str, Union[str, bool]]:
        return {
            'authority': self.authority,
            'code': self.permissions_code,
            'read': self.read_permission,
            'write': self.write_permission,
            'execute': self.execute_permission
        }
    
    @property
    def permissions_code_as_decimal_repr(self) -> int:
        return int(self.permissions_code, 8)

    @property
    def permissions_code_as_int(self) -> int:
        return int(self.permissions_code)

    @property
    def permissions_code_as_octal_literal(self) -> str:
        return f'0o{self.permissions_code}'


class PermissionsCode:
    """
    """
    def __init__(
        self,
        owner: PermissionsByte,
        group: PermissionsByte,
        others: PermissionsByte
    ):
        self.owner = owner
        self.group = group
        self.others = others
    
    def __sub__(self, permission_byte: PermissionsByte) -> 'PermissionsCode':
        if not isinstance(permission_byte, PermissionsByte):
            raise TypeError(
                f'can only subtract PermissionsByte (not "{type(permission_byte)}") from PermissionsCode'
            )

    def __add__(self, permission_byte: PermissionsByte) -> 'PermissionsCode':
        if not isinstance(permission_byte, PermissionsByte):
            raise TypeError(
                f'can only add PermissionsByte (not "{type(permission_byte)}") to PermissionsCode'
            )

        setattr(self, permission_byte.authority, permission_byte)
        return self

    def __str__(self) -> str:
        return repr(self)

    def __repr__(self) -> str:
        return (
            f'<{self.__class__.__name__} permissions_code={self.permissions_code}>'
        )

    @staticmethod
    def __generate_class_arguments_from_code(permission_code: str) -> Dict[str, PermissionsByte]:
        owner_config = PermissionsConfig.from_octal_bit(octal_bit=permission_code[0])
        group_config = PermissionsConfig.from_octal_bit(octal_bit=permission_code[1])
        others_config = PermissionsConfig.from_octal_bit(octal_bit=permission_code[2])

        class_arguments = {
            'owner_byte': PermissionsByte(authority='owner', config=owner_config),
            'group_byte': PermissionsByte(authority='group', config=group_config),
            'others_byte': PermissionsByte(authority='others',config=others_config)
        }

        return class_arguments
    
    @classmethod
    def _from_permissions_bytes(
        cls,
        permissions_byte_one: PermissionsByte,
        permissions_byte_two: PermissionsByte
    ) -> 'PermissionsCode':
        class_arguments = dict()
        class_parameters = get_all_class_parameters(class_object=cls)
        if permissions_byte_one.authority == permissions_byte_two.authority:
            raise ValueError("'authority' cannot be the same for both PermissionsByte objects")

        for byte in [permissions_byte_one, permissions_byte_two]:
            class_parameters.remove(byte.authority)
            class_arguments.update({byte.authority: byte})

        for parameter in class_parameters:
            class_arguments.update(
                {parameter: PermissionsByte(authority=parameter, config=PermissionsConfig())}
            )

        return cls(**class_arguments)

    @classmethod
    def from_octal_integer(cls, octal_object: Union[str, int]) -> 'PermissionsCode':
        permission_code: str = from_octal_integer(octal_object=octal_object)
        class_arguments: Dict[str, PermissionsByte] = PermissionsCode.__generate_class_arguments_from_code(
            permission_code=permission_code
        )

        return cls(**class_arguments)

    @classmethod
    def from_octal_decimal_repr(cls, octal_object: Union[str, int]) -> 'PermissionsCode':
        permission_code: str = from_decimal_repr_to_octal_integer(octal_object=octal_object)
        class_arguments: Dict[str, PermissionsByte] = PermissionsCode.__generate_class_arguments_from_code(
            permission_code=permission_code
        )

        return cls(**class_arguments)

    @property
    def permissions_code(self) -> str:
        permissions_code = (
            self.owner.permissions_code_as_decimal_repr |
            self.group.permissions_code_as_decimal_repr |
            self.others.permissions_code_as_decimal_repr
        )
        return format(permissions_code, 'o').zfill(3)

    @property
    def permissions_code_as_decimal_repr(self) -> int:
        return int(self.permissions_code, 8)

    @property
    def permissions_code_as_int(self) -> int:
        return int(self.permissions_code)
    
    @property
    def permissions_code_as_octal_literal(self) -> str:
        return f'0o{self.permissions_code}'