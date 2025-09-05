from fastapi import APIRouter, Depends, HTTPException, Request

router = APIRouter(prefix="/api")

@router.get("/")
def hello_world():
    return {
        "msg": "Hello World!"
    }
