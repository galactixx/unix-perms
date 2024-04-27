from pydantic import BaseModel

class Authority(BaseModel):
    read_write_execute: int
    read_write: int
    read: int
    read_execute: int
    write_execute: int
    write: int
    execute: int