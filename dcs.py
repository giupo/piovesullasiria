import logging
# import tempfile
import zipfile
from enum import StrEnum, auto
from pathlib import Path
from typing import Dict, Tuple, Optional

import luadata

log = logging.getLogger(__name__)
from scenery import Scenery

DcsPath = str | Path
MissionData = Dict

class DCSMizFileName(StrEnum):
    """The goddamned filenames in .miz files"""

    MISSION = auto()
    THEATER = auto()
    OPTIONS = auto()
    WAREHOUSES = auto()


def load_miz(path: DcsPath) -> Tuple[Dict, Scenery]:
    with zipfile.ZipFile(path, "r") as miz:
        mission_contents = miz.read(DCSMizFileName.MISSION).decode("utf-8")
        mission_data = luadata.unserialize(mission_contents)
        theatre = Scenery[miz.read(DCSMizFileName.THEATER).decode("utf-8")]

        return (
            mission_data,
            theatre,
        )


def update_miz(path: DcsPath, mission_data: MissionData) -> None:
    log.debug("path: %s", path)
    if "x" in mission_data:
        log.info("Delete me")
        
    pass


class Mission:
    def __init__(self, path: DcsPath):
        self.path = path
        self.mission_data, self.theatre = load_miz(self.path)

    def save(self, path: Optional[DcsPath] = None) -> None:
        path = self.path if path is None else path
        update_miz(path, self.mission_data)
        self.path = path
