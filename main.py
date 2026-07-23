from fastapi import FastAPI, Request, status

from controllers.item_controller import item_controller
from database import initialize_database
from models.item import Item, ItemCreate


app = FastAPI(title="FastAPI Project", version="0.1.0")


@app.on_event("startup")
def startup() -> None:
    initialize_database()


@app.middleware("http")
async def log_api_request(request: Request, call_next):
    response = await call_next(request)
    print(f"[API] {request.method} {request.url.path} -> {response.status_code}")
    return response


@app.get("/")
def read_root() -> dict[str, object]:
    return {
        "message": "Welcome to your first API",
        "endpoints": {
            "get_items": "GET /items",
            "post_item": "POST /items",
            "documentation": "GET /docs",
        },
    }


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/items", response_model=list[Item], tags=["items"])
def get_items() -> list[Item]:
    return item_controller.list_items()


@app.post("/items", response_model=Item, status_code=status.HTTP_201_CREATED, tags=["items"])
def post_item(item_data: ItemCreate) -> Item:
    return item_controller.create_item(item_data)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
