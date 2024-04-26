import stat
from abc import ABC, abstractmethod

class BasePermissions(ABC):
    """
    """
    @property
    def no_permissions(self) -> int:
        return 0o000

    @property
    @abstractmethod
    def read_write_execute(self) -> int:
        pass
    
    @property
    @abstractmethod
    def read_write(self) -> int:
        pass
    
    @property
    @abstractmethod
    def read(self) -> int:
        pass
    
    @property
    @abstractmethod
    def read_execute(self) -> int:
        pass
    
    @property
    @abstractmethod
    def write_execute(self) -> int:
        pass

    @property
    @abstractmethod
    def write(self) -> int:
        pass

    @property
    @abstractmethod
    def execute(self) -> int:
        pass


class OwnerPermissions(BasePermissions):
    """
    """
    @property
    def read_write_execute(self) -> int:
        return stat.S_IRWXU
    
    @property
    def read_write(self) -> int:
        return stat.S_IRUSR | stat.S_IWUSR
    
    @property
    def read(self) -> int:
        return stat.S_IRUSR
    
    @property
    def read_execute(self) -> int:
        return stat.S_IRUSR | stat.S_IXUSR
    
    @property
    def write_execute(self) -> int:
        return stat.S_IWUSR | stat.S_IXUSR

    @property
    def write(self) -> int:
        return stat.S_IWUSR
    
    @property
    def execute(self) -> int:
        return stat.S_IXUSR


class GroupPermissions(BasePermissions):
    """
    """
    @property
    def read_write_execute(self) -> int:
        return stat.S_IRWXG
    
    @property
    def read_write(self) -> int:
        return stat.S_IRGRP | stat.S_IWGRP
    
    @property
    def read(self) -> int:
        return stat.S_IRGRP
    
    @property
    def read_execute(self) -> int:
        return stat.S_IRGRP | stat.S_IXGRP
    
    @property
    def write_execute(self) -> int:
        return stat.S_IWGRP | stat.S_IXGRP

    @property
    def write(self) -> int:
        return stat.S_IWGRP

    @property
    def execute(self) -> int:
        return stat.S_IXGRP


class OthersPermissions(BasePermissions):
    """
    """
    @property
    def read_write_execute(self) -> int:
        return stat.S_IRWXO
    
    @property
    def read_write(self) -> int:
        return stat.S_IROTH | stat.S_IWOTH
    
    @property
    def read(self) -> int:
        return stat.S_IROTH
    
    @property
    def read_execute(self) -> int:
        return stat.S_IROTH | stat.S_IXOTH
    
    @property
    def write_execute(self) -> int:
        return stat.S_IWOTH | stat.S_IXOTH

    @property
    def write(self) -> int:
        return stat.S_IWOTH

    @property
    def execute(self) -> int:
        return stat.S_IXOTH