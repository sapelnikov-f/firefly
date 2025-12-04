from fastapi import APIRouter, HTTPException
from app.services.data_loader import DataLoader
from app.services.graph_service import GraphService

router = APIRouter()

loader = DataLoader()
graph_service = GraphService()

print("Loading POIs and segments...")
pois = loader.load_pois()
segments = loader.load_segments()
graph_service.build_graph(pois, segments)

poi_map = {p["id"]: {
    "id": p["id"],
    "name": p.get("name"),
    "elevation": p.get("elevation"),
    "category": p.get("category"),
    "lon": float(p.get("lon")) if p.get("lon") is not None else None,
    "lat": float(p.get("lat")) if p.get("lat") is not None else None,
} for p in pois}

@router.get("/route")
def get_route(from_id: int, to_id: int):
    try:
        result = graph_service.find_route(from_id, to_id)
        points = [poi_map.get(pid, {"id": pid}) for pid in result.get("path", [])]
        return {
            "path": result.get("path", []),
            "points": points,
            "distance_m": result.get("distance_m"),
            "elevation_gain_m": result.get("elevation_gain_m"),
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
