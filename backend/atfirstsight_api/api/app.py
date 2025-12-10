from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from atfirstsight_api.api.exception_handlers import add_exception_handlers
from atfirstsight_api.api.lifespan import lifespan
from atfirstsight_api.api.routes import chats, profiles

app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost",
    "http://localhost:8081",
    "exp://*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

app.include_router(chats.router)
app.include_router(profiles.router)

add_exception_handlers(app)
