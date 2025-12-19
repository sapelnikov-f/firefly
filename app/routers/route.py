from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.data_loader import DataLoader
from app.services.graph_service import GraphService

router = APIRouter()

loader = DataLoader()
graph_service = GraphService()


class BuildRouteRequest(BaseModel):
    start_id: int
    must_visit: list[int]
    difficulty: int


difficulty_dict = {
    1: 15,
    2: 20,
    3: 25
}


@router.post("/api/find-route")
def find_route(data: BuildRouteRequest):
    try:
        pois = loader.load_pois()
        segments = loader.load_segments()

        graph_service.build_graph(pois, segments)

        return graph_service.build_route(
            start=143,
            must_visit=data.must_visit,
            daily_limit=difficulty_dict[data.difficulty]
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/api/pois")
def get_pois():
    special_pois = [
        {
        "id": 91,
        "name": "Большое Софийское озеро",
        "description": "Группа озёр, часть маршрута перед перевалом Кара-Джаш.",
        "pass_category": None,
        "category": "озеро",
        "coords": [
        43.4495727,
        41.2303908
        ]
        },
        {
        "id": 30,
        "name": "Чилик",
        "description": "Озеро Чилик, место ночевки после перевала Богатырский.",
        "pass_category": None,
        "category": "озеро",
        "coords": [
        43.6351116,
        41.0831699
        ]
        },
        {
        "id": 50,
        "name": "Семицветное",
        "description": "Озеро Семицветное, место ночёвки перед перевалом Айюлю.",
        "pass_category": None,
        "category": "озеро",
        "coords": [
        43.4874634,
        41.0753416
        ]
    },  {
        "id": 106,
        "name": "Иркиз",
        "description": "Расположен С-Ю, Софийский хребет, соединяет реки Кашха-Эчкичат и Гаммеш-Чат. Подъем по набитой тропе, склон мелко осыпной. Спуск по травянисто-осыпному склону, тропа крутая в верхней части.",
        "pass_category": "1А",
        "category": "перевал",
        "coords": [
        43.4484367,
        41.2327201
        ]
    },
        {
        "id": 29,
        "name": "Ацгара",
        "description": "Река Ацгара, вдоль которой проходит часть маршрута.",
        "pass_category": None,
        "category": "река",
        "coords": [
        43.6723819,
        41.0180578
        ]
    },
        {
        "id": 92,
        "name": "Кара-Джаш",
        "description": "Перевал Кара-Джаш (1А, 2900 м). Перевал весь покрыт снегом, подъём крутой, требует навыков работы с ледорубом.",
        "pass_category": "1А",
        "category": "перевал",
        "coords": [
        43.4574259,
        41.2167936
        ]
    },
        {
        "id": 97,
        "name": "Агур",
        "description": "Перевал Агур (1А, 2850 м). Узкая щель в гребне, подъём по снежнику.",
        "pass_category": "1А",
        "category": "перевал",
        "coords": [
        43.5899369,
        41.1856175
        ]
    }
    ]
    return [
        {
            "id": p["id"],
            "name": p["name"]
        }
        for p in special_pois
    ]
