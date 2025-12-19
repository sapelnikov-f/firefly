from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from app.routers import route

app = FastAPI(title="Arkhyz Routing API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(route.router)


@app.get("/", response_class=HTMLResponse)
def index():
    return FileResponse("app/static/index.html")


# 👉 builder
@app.get("/route", response_class=HTMLResponse)
def route_builder():
    return FileResponse("app/static/builder.html")


# 👉 результат
@app.get("/route/result", response_class=HTMLResponse)
def route_result():
    return FileResponse("app/static/more_page.html")
