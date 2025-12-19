from fastapi import APIRouter, HTTPException
from app.services.data_loader import DataLoader
from app.services.graph_service import GraphService
from pydantic import BaseModel


router = APIRouter()

loader = DataLoader()
graph_service = GraphService()

pois = loader.load_pois()
segments = loader.load_segments()
graph_service.build_graph(pois, segments)



@router.get("/route")
def get_route(from_id: int, to_id: int):
    try:
        result = graph_service.find_route(from_id, to_id)
        points = [next((p for p in pois if p["id"] == pid), {"id": pid}) for pid in result.get("path", [])]
        return {
            "path": result.get("path", []),
            "points": points,
            "distance_km": result.get("distance_km"),
            "elevation_gain_m": result.get("elevation_gain_m"),
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/api/pois")
def get_pois():
    """
    Отдаёт список точек для выбора на фронте
    """
    return [
        {
            "id": p["id"],
            "name": p["name"],
            "category": p["category"]
        }
        for p in pois
    ]

class BuildRouteRequest(BaseModel):
    start_id: int
    must_visit: list[int]
    difficulty: int

difficulty_dict = {
    1: 15,
    2: 20,
    3: 25
}

@router.post("/api/build-route")
def build_route_api(data: BuildRouteRequest):

    # 1. Берём difficulty
    difficulty = data.difficulty

    if difficulty not in difficulty_dict:
        raise HTTPException(status_code=400, detail="Invalid difficulty")

    # 2. Переводим difficulty → daily_limit
    daily_limit = difficulty_dict[difficulty]

    # 3. Стартовая точка
    start_point = data.start_id

    # 4. Точки интереса
    points = data.must_visit

    # 5. ВЫЗОВ ТОЧНО КАК ТЫ ХОЧЕШЬ
    result = graph_service.build_route(
        start=start_point,
        must_visit=points,
        daily_limit=daily_limit
        # days НЕ передаём → возьмётся days=20
    )

    return result
