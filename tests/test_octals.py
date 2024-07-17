import stat

import pytest

from unix_perms import (InvalidOctalError, OctalPermissions,
                        from_octal_digit_to_config,
                        from_octal_to_permissions_mode, is_permissions_mode)
from unix_perms.octals import (OCTAL_MODE_DIGIT_0, OCTAL_MODE_DIGIT_1,
                               OCTAL_MODE_DIGIT_2, OCTAL_MODE_DIGIT_3,
                               OCTAL_MODE_DIGIT_4, OCTAL_MODE_DIGIT_5,
                               OCTAL_MODE_DIGIT_6, OCTAL_MODE_DIGIT_7)


def test_is_permissions_mode() -> None:
    """
    Testing the 'is_permissions_mode' boolean function which determines if
    an octal representation is a valid Unix permissions mode.
    """
    assert not is_permissions_mode(octal=0o1052)
    assert not is_permissions_mode(octal=0o7433)
    assert not is_permissions_mode(octal=999)
    assert not is_permissions_mode(octal='999')
    assert not is_permissions_mode(octal='009')
    assert not is_permissions_mode(octal='-318')
    assert not is_permissions_mode(octal='4173')
    assert is_permissions_mode(octal='010')
    assert is_permissions_mode(octal='111')
    assert is_permissions_mode(octal='777')
    assert is_permissions_mode(octal='416')
    assert is_permissions_mode(octal='725')
    assert is_permissions_mode(octal=0o070 | 0o001)
    assert is_permissions_mode(octal=0o001)
    assert is_permissions_mode(octal=438)
    assert is_permissions_mode(octal=0o111 | 0o200)


def test_from_octal_to_permissions_mode() -> None:
    """
    Testing the 'from_octal_to_permissions_mode' function which converst an
    octal representation to a Unix permissions mode.
    """
    assert from_octal_to_permissions_mode(octal='111') == '111'
    assert from_octal_to_permissions_mode(octal='732') == '732'
    assert from_octal_to_permissions_mode(octal='0') == '000'
    assert from_octal_to_permissions_mode(octal='03') == '003'
    assert from_octal_to_permissions_mode(octal=0o100 | 0o200 | 0o070) == '370'
    assert from_octal_to_permissions_mode(octal=0o000) == '000'
    assert from_octal_to_permissions_mode(octal=0) == '000'
    assert from_octal_to_permissions_mode(octal=438) == '666'

    with pytest.raises(InvalidOctalError) as exc_info:
        _ = from_octal_to_permissions_mode(octal='118')
    assert str(exc_info.value) == (
        'Invalid digits in octal representation, digits must range from 0 to 7'
    )

    with pytest.raises(InvalidOctalError) as exc_info:
        _ = from_octal_to_permissions_mode(octal='7777')
    assert str(exc_info.value) == (
        'Invalid octal representation length, must have a length ranging from 0 to 3'
    )

    with pytest.raises(InvalidOctalError) as exc_info:
        _ = from_octal_to_permissions_mode(octal=3333)
    assert str(exc_info.value) == (
        'Invalid octal representation length, must have a length ranging from 0 to 3'
    )


def test_from_octal_digit_to_config() -> None:
    """
    Testing the 'from_octal_digit_to_config' function which returns an
    OctalConfig object from an octal digit.
    """
    assert from_octal_digit_to_config(octal_digit=6) == OCTAL_MODE_DIGIT_6
    assert from_octal_digit_to_config(octal_digit=2) == OCTAL_MODE_DIGIT_2
    assert from_octal_digit_to_config(octal_digit='000') == OCTAL_MODE_DIGIT_0
    assert from_octal_digit_to_config(octal_digit='0005') == OCTAL_MODE_DIGIT_5
    assert from_octal_digit_to_config(octal_digit='4') == OCTAL_MODE_DIGIT_4
    assert from_octal_digit_to_config(octal_digit=3) == OCTAL_MODE_DIGIT_3
    assert from_octal_digit_to_config(octal_digit=1) == OCTAL_MODE_DIGIT_1
    assert from_octal_digit_to_config(octal_digit=7) == OCTAL_MODE_DIGIT_7
    assert from_octal_digit_to_config(octal_digit='7') == OCTAL_MODE_DIGIT_7
    assert from_octal_digit_to_config(octal_digit='007') == OCTAL_MODE_DIGIT_7
    assert from_octal_digit_to_config(octal_digit=5) == OCTAL_MODE_DIGIT_5

    with pytest.raises(InvalidOctalError) as exc_info:
        _ = from_octal_digit_to_config(octal_digit='47')
    assert str(exc_info.value) == (
        "Integer representation of an octal digit must be a single digit ranging from 0 to 7"
    )


def test_octal_permissions() -> None:
    """
    Testing the 'OctalPermissions' object which provides an abstract
    interface for accessing permission settings.
    """
    octal_permission = OctalPermissions(authority='owner')
    assert octal_permission.read_write_execute == stat.S_IRWXU
    assert octal_permission.read_execute == stat.S_IRUSR | stat.S_IXUSR
    assert octal_permission.read_write == stat.S_IRUSR | stat.S_IWUSR
    assert octal_permission.read == stat.S_IRUSR
    assert octal_permission.write == stat.S_IWUSR
    assert octal_permission.execute == stat.S_IXUSR
    assert octal_permission.write_execute == stat.S_IWUSR | stat.S_IXUSR

    octal_permission = OctalPermissions(authority='group')
    assert octal_permission.read_write_execute == stat.S_IRWXG
    assert octal_permission.read_execute == stat.S_IRGRP | stat.S_IXGRP
    assert octal_permission.read_write == stat.S_IRGRP | stat.S_IWGRP
    assert octal_permission.read == stat.S_IRGRP
    assert octal_permission.write == stat.S_IWGRP
    assert octal_permission.execute == stat.S_IXGRP
    assert octal_permission.write_execute == stat.S_IWGRP | stat.S_IXGRP

    octal_permission = OctalPermissions(authority='others')
    assert octal_permission.read_write_execute == stat.S_IRWXO
    assert octal_permission.read_execute == stat.S_IROTH | stat.S_IXOTH
    assert octal_permission.read_write == stat.S_IROTH | stat.S_IWOTH
    assert octal_permission.read == stat.S_IROTH
    assert octal_permission.write == stat.S_IWOTH
    assert octal_permission.execute == stat.S_IXOTH
    assert octal_permission.write_execute == stat.S_IWOTH | stat.S_IXOTH
