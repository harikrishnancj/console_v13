from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from typing import Optional
from app.core.database import get_db
from app.crud import crud4super as superadmin_crud
from app.crud import product as product_crud
from app.schemas.superadmin import SuperAdminCreate
from app.schemas.tenant import TenantInDBBase
from app.schemas.tenant_product_map import TenantProductMapInDBBase
from app.schemas.product import ProductInDBBase, ProductCreate, ProductUpdate
from app.utils.response import wrap_response
from app.schemas.base import BaseResponse

router = APIRouter()

@router.post("/products", response_model=BaseResponse[ProductInDBBase])
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    result = product_crud.create_product(schema=product, db=db)
    return wrap_response(data=result, message="Product created successfully")

@router.put("/products/{product_id}", response_model=BaseResponse[ProductInDBBase])
def update_product(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    result = product_crud.update_product(schema=product, db=db, product_id=product_id)
    if not result:
        raise HTTPException(status_code=404, detail="Product not found")
    return wrap_response(data=result, message="Product updated successfully")

@router.delete("/products/{product_id}", response_model=BaseResponse[ProductInDBBase])
def delete_product(product_id: int, db: Session = Depends(get_db)):
    result = product_crud.delete_product(db=db, product_id=product_id)
    if not result:
        raise HTTPException(status_code=404, detail="Product not found")
    return wrap_response(data=result, message="Product deleted successfully")

@router.post("/superadmin", response_model=BaseResponse[SuperAdminCreate])
def create_super_admin(super_admin: SuperAdminCreate, db: Session = Depends(get_db)):
    result = superadmin_crud.create_super_admin(schema=super_admin, db=db)
    return wrap_response(data=result, message="Super admin created successfully")

@router.put("/superadmin/{super_admin_id}", response_model=BaseResponse[SuperAdminCreate])
def update_super_admin(super_admin_id: int, super_admin: SuperAdminCreate, db: Session = Depends(get_db)):
    result = superadmin_crud.update_super_admin(db=db, super_admin_id=super_admin_id, super_admin=super_admin)
    if not result:
        raise HTTPException(status_code=404, detail="Super admin not found")
    return wrap_response(data=result, message="Super admin updated successfully")

@router.delete("/superadmin/{super_admin_id}", response_model=BaseResponse[SuperAdminCreate])
def delete_super_admin(super_admin_id: int, db: Session = Depends(get_db)):
    result = superadmin_crud.delete_super_admin(db=db, super_admin_id=super_admin_id)
    if not result:
        raise HTTPException(status_code=404, detail="Super admin not found")
    return wrap_response(data=result, message="Super admin deleted successfully")

@router.get("/tenants", response_model=BaseResponse[List[TenantInDBBase]])
def get_all_tenant(db: Session = Depends(get_db)):
    result = superadmin_crud.get_all_tenant(db=db)
    return wrap_response(data=result, message="Tenants fetched successfully")

@router.get("/tenantproductmappings", response_model=BaseResponse[List[TenantProductMapInDBBase]])
def get_all_tenant_product_mapping(tenant_id: Optional[int] = None, db: Session = Depends(get_db)):
    result = superadmin_crud.get_product_mappings_for_a_tenant(db=db, tenant_id=tenant_id)
    return wrap_response(data=result, message="Tenant product mappings fetched successfully")

