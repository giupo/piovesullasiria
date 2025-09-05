from enum import StrEnum
from typing import List

Icao = str
IcaoList = List[Icao]


class Scenery(StrEnum):
    Caucasus = "Caucasus"
    Syria = "Syria"
    Sinai = "Sinai"


icao_by_scenery = {}
icao_by_scenery[Scenery.Syria] = [
    "OSDI",  # Damasco
    "OLBA",  # Beirut
    "OSAP",  # Aleppo
    "OJAI",  # Aamman
    "LLHA",  # Haifa
]

icao_by_scenery[Scenery.Caucasus] = [
    "UGKO",  # Kutaisi
    "URSS",  # Sochi
    "URKK",  # Krasondar
    "UGSB",  # Batumi
    "URMT",  # Stavropol
]
