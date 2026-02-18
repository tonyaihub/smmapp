from fastapi import FastAPI, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from .database import engine, Base
from .auth.router import router as auth_router, current_active_user
from .api.v1.generate import router as generate_router
from .api.v1.payments import router as payments_router

app = FastAPI(title="SEO Content SaaS")

templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Создание таблиц (в проде → alembic)
import asyncio
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
asyncio.run(init_db())

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(generate_router, prefix="/api/v1", tags=["generate"])
app.include_router(payments_router, prefix="/api/v1", tags=["payments"])

@app.get("/")
async def root(request: Request, user = Depends(current_active_user)):
    return templates.TemplateResponse("dashboard.html", {"request": request, "user": user})
