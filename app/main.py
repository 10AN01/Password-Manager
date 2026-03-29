from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pathlib import Path
from app.routers import auth
from app.routers import passwordmanager
app = FastAPI()
@app.get("/", response_class=HTMLResponse)
def serve_index():
    return Path("app/index.html").read_text(encoding="utf-8")
app.include_router(auth.router)
app.include_router(passwordmanager.router,prefix="/password-manager")


