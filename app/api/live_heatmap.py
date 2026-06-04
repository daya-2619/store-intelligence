from fastapi import APIRouter

from ml_pipeline.state_manager import StoreStateManager

router = APIRouter()


@router.get(
    "/stores/{store_id}/heatmap/live"
)
def get_heatmap(store_id: str):
    state = StoreStateManager(store_id)
    return {

        "points":
        state.heatmap_points[-5000:]
    }

@router.get("/stores/{store_id}/visual-heatmap")
def get_visual_heatmap(store_id: str):
    # In a real system, this would return a dynamically generated image or URL
    # For now, we mock the path where heatmap_generator.py would save the image
    return {
        "image_url": f"/heatmaps/{store_id}.png"
    }