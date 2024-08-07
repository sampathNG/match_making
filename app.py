from fastapi import FastAPI
from controllers.api import router as router
app = FastAPI()
app.include_router(router)