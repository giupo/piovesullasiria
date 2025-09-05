from fastapi import APIRouter

from scenery import Scenery
from weather import mean_metar

from typing import Dict, Optional

router = APIRouter(prefix="/api")

@router.get("/")
def hello_world():
    return {
        "msg": "Hello World!"
    }

@router.get("/metar/{scenery}")
def get_mean_metar(scenery: Scenery) -> Optional[Dict]
    return mean_metar(scenery = scenery)
