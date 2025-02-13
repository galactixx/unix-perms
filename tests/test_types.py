import pytest

from unix_perms import (
    InvalidOctalError,
    PermissionsByte,
    PermissionsConfig,
    PermissionsMode,
)


def test_permissions_config() -> None:
    """
    Testing the 'from_octal_digit' class method from PermissionsConfig
    which creates a new PermissionsConfig instance from an octal digit.
    """
    ALL_PERMISSIONS_CONFIG = PermissionsConfig(read=True, write=True, execute=True)
    READ_PERMISSIONS_CONFIG = PermissionsConfig(read=True, write=False, execute=False)
    WRITE_PERMISSIONS_CONFIG = PermissionsConfig(read=False, write=True, execute=False)
    EXECUTE_PERMISSIONS_CONFIG = PermissionsConfig(
        read=False, write=False, execute=True
    )

    assert (
        PermissionsConfig.from_octal_digit(octal_digit="4") == READ_PERMISSIONS_CONFIG
    )
    assert (
        PermissionsConfig.from_octal_digit(octal_digit=1) == EXECUTE_PERMISSIONS_CONFIG
    )
    assert PermissionsConfig.from_octal_digit(octal_digit=2) == WRITE_PERMISSIONS_CONFIG
    assert (
        PermissionsConfig.from_octal_digit(octal_digit="007") == ALL_PERMISSIONS_CONFIG
    )

    with pytest.raises(InvalidOctalError) as exc_info:
        _ = PermissionsConfig.from_octal_digit(octal_digit=700)
    assert str(exc_info.value) == (
        "Integer representation of an octal digit must be a single digit ranging from 0 to 7"
    )


def test_permissions_byte() -> None:
    """
    Testing the PermissionsByte class which allows creation of structured objects
    centered around permission modes for singular Unix authorities.
    """
    WRITE_PERMISSIONS_CONFIG = PermissionsConfig(read=False, write=True, execute=False)
    ALL_PERMISSIONS_CONFIG = PermissionsConfig(read=True, write=True, execute=True)

    owner_permissions = PermissionsByte(
        authority="owner", config=WRITE_PERMISSIONS_CONFIG
    )
    assert owner_permissions.authority == "owner"
    assert not owner_permissions.execute_permission
    assert not owner_permissions.read_permission
    assert owner_permissions.write_permission
    assert owner_permissions.permissions_mode == "200"
    assert owner_permissions.permissions_mode_as_decimal_repr == 128
    assert owner_permissions.permissions_mode_as_octal_literal == "0o200"
    assert owner_permissions.permissions_mode_as_int == 200
    assert owner_permissions.permissions_description == "Write permission only"
    assert owner_permissions.permissions_description_detailed == {
        "authority": "owner",
        "mode": "200",
        "read": False,
        "write": True,
        "execute": False,
    }

    group_permissions = PermissionsByte(
        authority="group", config=ALL_PERMISSIONS_CONFIG
    )
    permission_mode = owner_permissions + group_permissions

    assert isinstance(permission_mode, PermissionsMode)
    assert permission_mode.permissions_mode == "274"


def test_permissions_mode() -> None:
    """
    Testing the PermissionsMode class which allows creation of structured objecs
    centered around full Unix permission modes.
    """
    WRITE_PERMISSIONS_CONFIG = PermissionsConfig(read=False, write=True, execute=False)
    ALL_PERMISSIONS_CONFIG = PermissionsConfig(read=True, write=True, execute=True)
    READ_PERMISSIONS_CONFIG = PermissionsConfig(read=True, write=False, execute=False)

    owner_permissions = PermissionsByte(
        authority="owner", config=WRITE_PERMISSIONS_CONFIG
    )
    group_permissions = PermissionsByte(
        authority="group", config=ALL_PERMISSIONS_CONFIG
    )
    others_permissions = PermissionsByte(
        authority="others", config=READ_PERMISSIONS_CONFIG
    )

    permissions_mode = PermissionsMode(
        owner=owner_permissions, group=group_permissions, others=others_permissions
    )

    assert permissions_mode.permissions_mode == "274"
    assert permissions_mode.permissions_mode_as_octal_literal == "0o274"
    assert permissions_mode.permissions_mode_as_int == 274
    assert permissions_mode.permissions_mode_as_decimal_repr == 188

    group_permissions_new = PermissionsByte(
        authority="group", config=ALL_PERMISSIONS_CONFIG
    )
    permission_mode_sub = permissions_mode - group_permissions_new

    assert permission_mode_sub.permissions_mode == "204"
    assert permission_mode_sub.permissions_mode_as_octal_literal == "0o204"
    assert permission_mode_sub.permissions_mode_as_int == 204
    assert permission_mode_sub.permissions_mode_as_decimal_repr == 132

    others_permissions_new = PermissionsByte(
        authority="others", config=WRITE_PERMISSIONS_CONFIG
    )
    permission_mode_add = permissions_mode + others_permissions_new

    assert permission_mode_add.permissions_mode == "276"
    assert permission_mode_add.permissions_mode_as_octal_literal == "0o276"
    assert permission_mode_add.permissions_mode_as_int == 276
    assert permission_mode_add.permissions_mode_as_decimal_repr == 190
