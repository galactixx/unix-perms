import pytest

from unix_perms import (InvalidOctalError, PermissionsByte, PermissionsCode,
                        PermissionsConfig)


def test_permissions_config() -> None:
    """
    Testing the 'from_octal_bit' class method from 'PermissionsConfig'
    which creates a 'PermissionsConfig' object from an octal bit.
    """
    ALL_PERMISSIONS_CONFIG = PermissionsConfig(read=True, write=True, execute=True)
    READ_PERMISSIONS_CONFIG = PermissionsConfig(read=True, write=False, execute=False)
    WRITE_PERMISSIONS_CONFIG = PermissionsConfig(read=False, write=True, execute=False)
    EXECUTE_PERMISSIONS_CONFIG = PermissionsConfig(read=False, write=False, execute=True)

    assert PermissionsConfig.from_octal_bit(octal_bit='4') == READ_PERMISSIONS_CONFIG
    assert PermissionsConfig.from_octal_bit(octal_bit=0o001) == EXECUTE_PERMISSIONS_CONFIG
    assert PermissionsConfig.from_octal_bit(octal_bit=2) == WRITE_PERMISSIONS_CONFIG
    assert PermissionsConfig.from_octal_bit(octal_bit='007') == ALL_PERMISSIONS_CONFIG

    with pytest.raises(InvalidOctalError) as exc_info:
        _ = PermissionsConfig.from_octal_bit(octal_bit=0o700)
        assert exc_info == "an integer representation of an octal bit must be a single digit ranging from 0 to 7"


def test_permissions_byte() -> None:
    """
    Testing the 'PermissionsByte' class which allows creation of structured objects centered around permission codes for
    singular Unix authorities.
    """
    WRITE_PERMISSIONS_CONFIG = PermissionsConfig(read=False, write=True, execute=False)
    ALL_PERMISSIONS_CONFIG = PermissionsConfig(read=True, write=True, execute=True)

    owner_permissions = PermissionsByte(authority='owner', config=WRITE_PERMISSIONS_CONFIG)
    assert owner_permissions.authority == 'owner'
    assert not owner_permissions.execute_permission
    assert not owner_permissions.read_permission
    assert owner_permissions.write_permission
    assert owner_permissions.permissions_code == '200'
    assert owner_permissions.permissions_code_as_decimal_repr == 128
    assert owner_permissions.permissions_code_as_octal_literal == '0o200'
    assert owner_permissions.permissions_code_as_int == 200
    assert owner_permissions.permissions_description == 'Write permission only'
    assert owner_permissions.permissions_description_detailed == {
        'authority': 'owner', 'code': '200', 'read': False, 'write': True, 'execute': False
    }

    group_permissions = PermissionsByte(authority='group', config=ALL_PERMISSIONS_CONFIG)
    permission_code = owner_permissions + group_permissions

    assert isinstance(permission_code, PermissionsCode)
    assert permission_code.permissions_code == '270'


def test_permissions_code() -> None:
    """
    Testing the 'PermissionsCode' class which allows creation of structured objecs centered around full Unix permission codes.
    """
    WRITE_PERMISSIONS_CONFIG = PermissionsConfig(read=False, write=True, execute=False)
    ALL_PERMISSIONS_CONFIG = PermissionsConfig(read=True, write=True, execute=True)
    READ_PERMISSIONS_CONFIG = PermissionsConfig(read=True, write=False, execute=False)

    owner_permissions = PermissionsByte(authority='owner', config=WRITE_PERMISSIONS_CONFIG)
    group_permissions = PermissionsByte(authority='group', config=ALL_PERMISSIONS_CONFIG)
    others_permissions = PermissionsByte(authority='others', config=READ_PERMISSIONS_CONFIG)

    permissions_code = PermissionsCode(
        owner=owner_permissions, group=group_permissions, others=others_permissions
    )

    assert permissions_code.permissions_code == '274'
    assert permissions_code.permissions_code_as_octal_literal == '0o274'
    assert permissions_code.permissions_code_as_int == 274
    assert permissions_code.permissions_code_as_decimal_repr == 188

    group_permissions_new = PermissionsByte(authority='group', config=ALL_PERMISSIONS_CONFIG)
    permission_code_sub = permissions_code - group_permissions_new

    assert permission_code_sub.permissions_code == '204'
    assert permission_code_sub.permissions_code_as_octal_literal == '0o204'
    assert permission_code_sub.permissions_code_as_int == 204
    assert permission_code_sub.permissions_code_as_decimal_repr == 132

    others_permissions_new = PermissionsByte(authority='others', config=WRITE_PERMISSIONS_CONFIG)
    permission_code_add = permissions_code + others_permissions_new

    assert permission_code_add.permissions_code == '276'
    assert permission_code_add.permissions_code_as_octal_literal == '0o276'
    assert permission_code_add.permissions_code_as_int == 276
    assert permission_code_add.permissions_code_as_decimal_repr == 190
