from typing import Any, List, Type
import inspect

def get_all_class_parameters(class_object: Type[Any]) -> List[str]:
    """
    """
    return [
        param for param in inspect.signature(class_object).parameters if param != 'self'
    ]