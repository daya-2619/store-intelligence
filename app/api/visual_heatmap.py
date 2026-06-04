from fastapi import APIRouter
from fastapi.responses import JSONResponse
import os

router = APIRouter()

@router.get("/stores/{store_id}/visual-heatmap")
def get_visual_heatmap(store_id: str):
    image_url = f"/heatmaps/{store_id}.png"
        
    return JSONResponse(content={
        "image_url": image_url
    })
