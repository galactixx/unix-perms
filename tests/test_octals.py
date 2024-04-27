import stat
import pytest

from py_perms import (
    from_decimal_repr_to_octal_integer,
    from_octal_bit_to_config,
    from_octal_integer,
    InvalidOctalError,
    is_decimal_repr,
    is_octal_integer,
    OctalPermissions
)

from py_perms.octals import (
    OCTAL_MODE_BIT_0,
    OCTAL_MODE_BIT_1,
    OCTAL_MODE_BIT_2,
    OCTAL_MODE_BIT_3,
    OCTAL_MODE_BIT_4,
    OCTAL_MODE_BIT_5,
    OCTAL_MODE_BIT_6,
    OCTAL_MODE_BIT_7
)


def test_is_octal_integer() -> None:
    """
    Testing the 'is_octal_integer' boolean function which determines if an input is a valid octal integer.
    """
    assert not is_octal_integer(octal_integer='999')
    assert not is_octal_integer(octal_integer='009')
    assert not is_octal_integer(octal_integer=934)
    assert not is_octal_integer(octal_integer=-1)
    assert not is_octal_integer(octal_integer='-318')
    assert not is_octal_integer(octal_integer='4173')
    assert not is_octal_integer(octal_integer=6665)
    assert is_octal_integer(octal_integer=0)
    assert is_octal_integer(octal_integer='010')
    assert is_octal_integer(octal_integer='111')
    assert is_octal_integer(octal_integer='777')
    assert is_octal_integer(octal_integer=163)
    assert is_octal_integer(octal_integer='416')
    assert is_octal_integer(octal_integer='725')


def test_is_decimal_repr() -> None:
    """
    Testing the 'is_decimal_repr' boolean function which determines if an input is a
    valid octal decimal representation.
    """
    assert not is_decimal_repr(octal_object='not a decimal')
    assert not is_decimal_repr(octal_object=0o1052)
    assert not is_decimal_repr(octal_object=0o7433)
    assert not is_decimal_repr(octal_object=999)
    assert not is_decimal_repr(octal_object=-0o322)
    assert not is_decimal_repr(octal_object='0o813')
    assert is_decimal_repr(octal_object='0o443')
    assert is_decimal_repr(octal_object='0o777')
    assert is_decimal_repr(octal_object=0o322)
    assert is_decimal_repr(octal_object=0o070 | 0o001)
    assert is_decimal_repr(octal_object=0o001)
    assert is_decimal_repr(octal_object=438)
    assert is_decimal_repr(octal_object=0o111 | 0o200)


def test_from_octal_integer() -> None:
    """
    Testing the 'from_octal_integer' function which standardizes an octal integer into a string
    representation of a 3 digit octal integer.
    """
    assert from_octal_integer(octal_object='111') == '111'
    assert from_octal_integer(octal_object=111) == '111'
    assert from_octal_integer(octal_object=732) == '732'
    assert from_octal_integer(octal_object=1) == '001'
    assert from_octal_integer(octal_object=51) == '051'
    assert from_octal_integer(octal_object=0) == '000'
    assert from_octal_integer(octal_object='03') == '003'

    with pytest.raises(InvalidOctalError) as exc_info:
        _ = from_octal_integer(octal_object='118')
        assert exc_info == 'invalid bits in octal representation, bits must range from 0 to 7'

    with pytest.raises(InvalidOctalError) as exc_info:
        _ = from_octal_integer(octal_object=7777)
        assert exc_info == 'invalid octal representation length, must have a length ranging from 0 to 3'


def test_from_decimal_repr_to_octal_integer() -> None:
    """
    Testing the 'from_decimal_repr_to_octal_integer' function which standardizes a decimal representation into a string
    representation of a 3 digit octal integer.
    """
    assert from_decimal_repr_to_octal_integer(octal_object='0o777') == '777'
    assert from_decimal_repr_to_octal_integer(octal_object='438') == '666'
    assert from_decimal_repr_to_octal_integer(octal_object=438) == '666'
    assert from_decimal_repr_to_octal_integer(octal_object='001') == '001'
    assert from_decimal_repr_to_octal_integer(octal_object=0o100 | 0o200 | 0o070) == '370'
    assert from_decimal_repr_to_octal_integer(octal_object=0o000) == '000'
    assert from_decimal_repr_to_octal_integer(octal_object=0) == '000'

    with pytest.raises(InvalidOctalError) as exc_info:
        _ = from_decimal_repr_to_octal_integer(octal_object=3333)
        assert exc_info == 'invalid octal representation length, must have a length ranging from 0 to 3'

    with pytest.raises(InvalidOctalError) as exc_info:
        _ = from_decimal_repr_to_octal_integer(octal_object='999')
        assert exc_info == 'invalid bits in octal representation, bits must range from 0 to 7'


def test_from_octal_bit_to_config() -> None:
    """
    Testing the 'from_octal_bit_to_config' function which returns on OctalConfig object from an octal bit.
    """
    assert from_octal_bit_to_config(octal_bit=6) == OCTAL_MODE_BIT_6
    assert from_octal_bit_to_config(octal_bit=2) == OCTAL_MODE_BIT_2
    assert from_octal_bit_to_config(octal_bit='000') == OCTAL_MODE_BIT_0
    assert from_octal_bit_to_config(octal_bit='0005') == OCTAL_MODE_BIT_5
    assert from_octal_bit_to_config(octal_bit='4') == OCTAL_MODE_BIT_4
    assert from_octal_bit_to_config(octal_bit=3) == OCTAL_MODE_BIT_3
    assert from_octal_bit_to_config(octal_bit=1) == OCTAL_MODE_BIT_1
    assert from_octal_bit_to_config(octal_bit=7) == OCTAL_MODE_BIT_7
    assert from_octal_bit_to_config(octal_bit='7') == OCTAL_MODE_BIT_7
    assert from_octal_bit_to_config(octal_bit='007') == OCTAL_MODE_BIT_7
    assert from_octal_bit_to_config(octal_bit=5) == OCTAL_MODE_BIT_5
    assert from_octal_bit_to_config(octal_bit=0o001) == OCTAL_MODE_BIT_1

    with pytest.raises(InvalidOctalError) as exc_info:
        _ = from_octal_bit_to_config(octal_bit='47')
        assert exc_info == "an integer representation of an octal bit must be a single digit ranging from 0 to 7"


def test_octal_permissions() -> None:
    """
    Testing the 'OctalPermissions' object which provides an abstract interface for accessing permission settings.
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