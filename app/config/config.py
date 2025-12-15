from typing import Union

from pydantic import BaseModel

class ConfigResponse(BaseModel):
    max_file_size: int
    allowed_file_types: list[str]
    storage_cleanup_days: int

class ConfigSetRequest(BaseModel):
    key: str
    value: Union[str, int, bool, list]

class ConfigSetResponse(BaseModel):
    message: str
