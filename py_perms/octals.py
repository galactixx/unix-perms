from typing import Dict, Set, Union
from collections import namedtuple

from py_perms.exceptions import InvalidOctalError

OctalConfig = namedtuple('OctalConfig', ['description', 'read', 'write', 'execute'])

OCTAL_MODE_BIT_0 = OctalConfig(description='No permissions', read=False, write=False, execute=False)
OCTAL_MODE_BIT_1 = OctalConfig(description='Execute permission only', read=False, write=False, execute=True)
OCTAL_MODE_BIT_2 = OctalConfig(description='Write permission only', read=False, write=True, execute=False)
OCTAL_MODE_BIT_3 = OctalConfig(description='Write and execute permissions', read=False, write=True, execute=True)
OCTAL_MODE_BIT_4 = OctalConfig(description='Read permission only', read=True, write=False, execute=False)
OCTAL_MODE_BIT_5 = OctalConfig(description='Read and execute permissions', read=True, write=False, execute=True)
OCTAL_MODE_BIT_6 = OctalConfig(description='Read and write permissions', read=True, write=True, execute=False)
OCTAL_MODE_BIT_7 = OctalConfig(description='Read, write, and execute permissions', read=True, write=True, execute=True)

OCTAL_BIT_CONFIGURATIONS: Dict[int, OctalConfig] = {
    0: OCTAL_MODE_BIT_0,
    1: OCTAL_MODE_BIT_1,
    2: OCTAL_MODE_BIT_2,
    3: OCTAL_MODE_BIT_3,
    4: OCTAL_MODE_BIT_4,
    5: OCTAL_MODE_BIT_5,
    6: OCTAL_MODE_BIT_6,
    7: OCTAL_MODE_BIT_7
}

def _get_octal_bit_config(octal_bit: int) -> OctalConfig:
    if 0 <= octal_bit <= 7:
        return OCTAL_BIT_CONFIGURATIONS.get(octal_bit)
    else:
        raise InvalidOctalError(
            "an integer representation of an octal bit must be a single digit ranging from 0 to 7"
        )


def from_octal_bit_to_config(octal_bit: Union[str, int]) -> OctalConfig:
    """
    """
    if isinstance(octal_bit, str):
        try:
            octal_bit_as_int = int(octal_bit)
        except ValueError:
            raise InvalidOctalError(
                "expecting a string representation of the octal number being a single digit integer"
            )
        else:
            return _get_octal_bit_config(octal_bit=octal_bit_as_int)
    elif isinstance(octal_bit, int):
        return _get_octal_bit_config(octal_bit=octal_bit)
    else:
        raise TypeError(
            f"{type(octal_bit)} is not a valid 'octal_bit' type"
        )


def _octal_integer_validation(octal_int_as_str: str) -> str:
    """
    """
    valid_bits: Set[str] = {str(num) for num in range(8)}

    octal_string_length: int = len(octal_int_as_str)

    if not 1 <= octal_string_length <= 3:
        raise InvalidOctalError(
            'invalid octal representation length, must have a length ranging from 0 to 3'
        )
    
    any_invalid_bits: bool = any(bit not in valid_bits for bit in octal_int_as_str)
    if any_invalid_bits:
        raise InvalidOctalError(
            'invalid bits in octal representation, bits must range from 0 to 7'
        )

    octal_int_string_repr: str = octal_int_as_str.zfill(3)
    return octal_int_string_repr


def _to_octal_str_repr_conversion(octal_object: int) -> str:
    """
    """
    octal_string: str = format(octal_object, 'o')
    octal_int_string_repr: str = _octal_integer_validation(octal_int_as_str=octal_string)
    return octal_int_string_repr


def from_decimal_repr_to_octal_integer(octal_object: Union[str, int]) -> str:
    """
    """
    if isinstance(octal_object, str):
        if octal_object.startswith('0o'):
            try:
                octal_decimal = int(octal_object, 8)
            except ValueError:
                raise InvalidOctalError("must be a valid octal literal")
            else:
                return _to_octal_str_repr_conversion(octal_object=octal_decimal)
        else:
            try:
                octal_decimal = int(octal_object)
            except ValueError:
                raise InvalidOctalError("must be a valid decimal representation of an octal")
            else:
                return _to_octal_str_repr_conversion(octal_object=octal_decimal)
    elif isinstance(octal_object, int):
        return _to_octal_str_repr_conversion(octal_object=octal_object)
    else:
        raise TypeError(
            f"{type(octal_decimal)} is not a valid 'octal_decimal' type, must be of type ('str', 'int')"
        )
    

def from_octal_integer(octal_object: Union[str, int]) -> str:
    """
    """
    if isinstance(octal_object, str):
        return _octal_integer_validation(octal_int_as_str=octal_object)
    elif isinstance(octal_object, int):
        octal_object = str(octal_object)
        return _octal_integer_validation(octal_int_as_str=octal_object)
    else:
        raise TypeError(
            f"{type(octal_object)} is not a valid 'octal_object' type, must be of type ('str', 'int')"
        )
    

def is_octal_integer(octal_integer: Union[str, int]) -> bool:
    """
    """
    try:
        _ = from_octal_integer(octal_object=octal_integer)
    except InvalidOctalError:
        is_octal_int = False
    else:
        is_octal_int = True
    return is_octal_int