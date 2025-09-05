import logging
import tempfile
import zipfile
from enum import StrEnum, auto
from pathlib import Path
from typing import Dict, Tuple

import luadata

log = logging.getLogger(__name__)
from scenery import Scenery


class DCSMizFileName(StrEnum):
    """The goddamned filenames in .miz files"""

    MISSION = auto()
    THEATER = auto()
    OPTIONS = auto()
    WAREHOUSES = auto()


def load_miz(path: str | Path) -> Tuple[Dict, Scenery]:
    with zipfile.ZipFile(path, "r") as miz:
        mission_contents = miz.read(DCSMizFileName.MISSION).decode("utf-8")
        mission_data = luadata.unserialize(mission_contents)
        theatre = Scenery[miz.read(DCSMizFileName.THEATER).decode("utf-8")]

        return (
            mission_data,
            theatre,
        )


def update_miz(path: str | Path, mission_data: Dict = None) -> None:
    pass


class Mission:
    def __init__(self, path: str | Path):
        self.path = path
        self.mission_data, self.theatre = load_miz(self.path)

    def save(self, path=None) -> None:
        path = self.path if path is None else path
        update_miz(path, self.mission_data)
        self.path = path
