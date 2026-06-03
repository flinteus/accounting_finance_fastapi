from fastapi import FastAPI
import uvicorn

from app.api.v1.wallets import router as wallets_router
from app.api.v1.operations import router as operations_router
from app.api.v1.users import router as users_router
from app.database import Base, engine


app = FastAPI()

app.include_router(wallets_router, prefix="/api/v1", tags=["wallets"])
app.include_router(operations_router, prefix="/api/v1", tags=["operations"])
app.include_router(users_router, prefix="/api/v1", tags=["users"])

Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
