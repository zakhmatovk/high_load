
from fastapi import FastAPI

from social_network.api.user import router as user_router


app = FastAPI()
app.include_router(user_router)
