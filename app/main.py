from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from app.routers import route

app = FastAPI(title="Arkhyz Routing API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # или указать фронтенд URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(route.router)


@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <html>
      <head><title>Arkhyz</title></head>
      <body>
    
        <h1>Это домашняя страница</h1>
      </body>
    </html>
    """
