from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from config import ROOM_ID, FILTERS
from cpp_module.filter import apply_filter_cpp

app = FastAPI()

# Додаємо CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8001"],  # Можна ["*"] для дозволу з усіх джерел
    allow_methods=["*"],
    allow_headers=["*"],
)

_store = []  # Проста пам’ять для малювання

# ✅ Pydantic модель для обробки фільтрації зображень
class FilterPayload(BaseModel):
    image_data: List[int]       # Пікселі або дані зображення
    width: int
    height: int
    filter_name: str


@app.post("/draw/{room_id}")
def draw(room_id: str, command: dict):
    if room_id != ROOM_ID:
        raise HTTPException(status_code=404, detail="Room not found")
    _store.append(command)
    return {"status": "ok"}


@app.get("/draw/{room_id}")
def get_draw(room_id: str):
    if room_id != ROOM_ID:
        raise HTTPException(status_code=404, detail="Room not found")
    return _store


@app.post("/filter/{room_id}")
def filter_image(room_id: str, payload: FilterPayload):
    if room_id != ROOM_ID:
        raise HTTPException(status_code=404, detail="Room not found")

    if payload.filter_name not in FILTERS:
        raise HTTPException(status_code=400, detail=f"Unsupported filter: {payload.filter_name}")

    try:
        filtered = apply_filter_cpp(
            payload.image_data,
            payload.width,
            payload.height,
            payload.filter_name
        )
        return {"image_data": filtered}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Filter application failed: {str(e)}")
