from pydantic import BaseModel
from typing import Optional

class TenantProductMapBase(BaseModel):
    product_id: int

class TenantProductMapCreate(TenantProductMapBase):
    pass


class TenantProductMapInDBBase(TenantProductMapBase):
    id: int
    tenant_id: int

    class Config:
        from_attributes = True
