from fastapi import APIRouter, Depends, HTTPException, Request

router = APIRouter(prefix="/api")

@router.get("/")
async def hello_world():
    yield "Hello World!"
