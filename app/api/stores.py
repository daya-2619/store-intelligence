from fastapi import APIRouter, HTTPException
from app.db import SessionLocal
from app.models import Store, Camera
from pydantic import BaseModel
from typing import List

router = APIRouter()

class StoreResponse(BaseModel):
    store_id: str
    store_name: str
    city: str | None
    region: str | None
    active: bool
    layout_path: str | None = None
    
    class Config:
        from_attributes = True

class CameraResponse(BaseModel):
    camera_id: str
    store_id: str
    camera_name: str | None = None
    camera_type: str | None = None
    zone_name: str | None = None
    is_heatmap_enabled: bool = True
    stream_url: str | None
    source_path: str | None
    status: str
    
    class Config:
        from_attributes = True

@router.get("/stores", response_model=List[StoreResponse])
def get_stores():
    db = SessionLocal()
    try:
        stores = db.query(Store).filter(Store.active == True).all()
        return stores
    finally:
        db.close()

@router.get("/stores/{store_id}/cameras", response_model=List[CameraResponse])
def get_store_cameras(store_id: str):
    db = SessionLocal()
    try:
        cameras = db.query(Camera).filter(Camera.store_id == store_id).all()
        return cameras
    finally:
        db.close()

@router.get("/stores/{store_id}/layout")
def get_store_layout(store_id: str):
    db = SessionLocal()
    try:
        store = db.query(Store).filter(Store.store_id == store_id).first()
        if not store:
            raise HTTPException(status_code=404, detail="Store not found")
            
        return {
            "layout_path": store.layout_path
        }
    finally:
        db.close()
