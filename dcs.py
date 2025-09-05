import zipfile
import tempfile
import luadata
import logging

from typing import Dict, Tuple
from enum import StrEnum
from pathlib import Path


log = logging.getLogger(__name__)
from scenery import Scenery

class DCSMizFileName(StrEnum):
    """The goddamned filenames in .miz files"""
    MISSION = "mission"
    THEATER = "theatre"
    OPTIONS = "options"
    WAREHOUSES = "warehouses"

    
def load_miz(path: str|Path) -> Tuple[Dict, Scenery]:
    with zipfile.ZipFile(path, "r") as miz:
        mission_contents = miz.read(DCSMizFileName.MISSION).decode("utf-8")
        mission_data = luadata.unserialize(mission_contents)
        theatre = Scenery[miz.read(DCSMizFileName.THEATER).decode("utf-8")]

        return (mission_data, theatre, )


def update_miz(path: str|Path, mission_data: Dict = None) -> None:
    pass


class Mission:
    def __init__(self, path: str|Path):
        self.path = path
        self.mission_data, self.theatre = load_miz(self.path)

    def save(self, path = None) -> None:
        path = self.path if path is None else path
        update_miz(path, self.mission_data)
        self.path = path
