import logging
import zipfile
from enum import StrEnum, auto
from pathlib import Path
from typing import Dict, Optional, Tuple

import luadata

log = logging.getLogger(__name__)
from scenery import Scenery

DcsPath = str | Path
MissionData = Dict

UTF_8 = "utf-8"


class DCSMizFileName(StrEnum):
    """The goddamned filenames in .miz files"""

    MISSION = auto()
    THEATRE = auto()
    OPTIONS = auto()
    WAREHOUSES = auto()


class DCSMissionKeys(StrEnum):
    WEATHER = auto()


def load_miz(path: DcsPath) -> Tuple[Dict, Scenery]:
    with zipfile.ZipFile(path, "r") as miz:
        mission_contents = miz.read(DCSMizFileName.MISSION).decode(UTF_8)
        mission_data = luadata.unserialize(mission_contents)
        theatre = Scenery[miz.read(DCSMizFileName.THEATRE).decode(UTF_8)]

        return (
            mission_data,
            theatre,
        )


def update_miz(path: DcsPath, mission_data: MissionData) -> None:
    # Serializza di nuovo in stringa Lua
    new_mission_text = luadata.serialize(mission_data, indent="\t")
    new_mission_bytes = new_mission_text.encode(UTF_8)

    # Crea nuovo zip copiando tutto, tranne che sostituiamo "mission"
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as zout:
        # Scriviamo la mission modificata
        zout.writestr(DCSMizFileName.MISSION, new_mission_bytes)


class Mission:
    def __init__(self, path: DcsPath):
        self.path = path
        self.mission_data, self.theatre = load_miz(self.path)

    def save(self, path: Optional[DcsPath] = None) -> None:
        path = self.path if path is None else path
        update_miz(path, self.mission_data)
        self.path = path

    def update(self, key: DCSMissionKeys, value):
        self.mission_data[key] = value
