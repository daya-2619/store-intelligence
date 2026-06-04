from fastapi import APIRouter

from app.services.pos_loader import (
    load_pos_csv
)

router = APIRouter()


@router.post("/pos/load")
def pos_load_trigger():
    import glob
    import os
    try:
        csv_files = glob.glob(os.path.join("data", "pos", "*.csv"))
        if not csv_files:
            return {"error": "No CSV files found in data/pos/"}, 404
            
        res = load_pos_csv(csv_files[0])
        return {"status": "success", "result": res}
    except Exception as e:
        return {"error": str(e)}, 500