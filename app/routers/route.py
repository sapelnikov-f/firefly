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

@router.get("/route")
def get_route(from_id: int, to_id: int):
    try:
        result = graph_service.find_route(from_id, to_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
