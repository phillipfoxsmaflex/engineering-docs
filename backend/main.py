

from fastapi import FastAPI
from .database import database
from .routes import users, auth, me

app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Engineering Document Management System"}

# Include routers
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(me.router)

