from fastapi import FastAPI
from src.controllers import auth_controller

app = FastAPI()

app.include_router(auth_controller.user_router)

@app.get("/health")
def health():
    return {"status": "OK"}

