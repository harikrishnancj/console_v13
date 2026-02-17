from pydantic import BaseModel
from typing import Optional

class SuperAdminBase(BaseModel):
    name: str
    email: str
    hashed_password: str
    is_active: bool = True

class SuperAdminCreate(SuperAdminBase):
    pass

class SuperAdminInDBBase(SuperAdminBase):
    id: int

    class Config:
        from_attributes = True
