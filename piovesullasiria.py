#!/usr/bin/env python

# stdlib
import logging

# third party libraries (expect to install)

import click


# std lib
from typing import List

# my own stuff
from log import LogLevel
from weather import mean_metar
from scenery import Scenery
from log import configure_logging
from dcs import Mission

log = logging.getLogger(__name__)

def unfold_icaos(icaos: str | None):
    if not icaos:
        return None

    return [icao.strip() for icao in icaos.split(",")]


@click.group()
@click.option("--level", default="INFO", type=click.Choice(LogLevel, case_sensitive=False))
def main(level):
    configure_logging(level)

@main.command()
@click.option("--miz", prompt="Path to MIZ ?")
@click.option("--icao", nargs=1, default=None)
def update(miz, icao) -> None:
    mission = Mission(miz)
    data = mean_metar(mission.theatre, icaos=unfold_icaos(icao))
    log.info(data)

    
@main.command()
@click.option("--scenery", default=None)
@click.option("--icao", nargs=1, default=None)
def show(scenery: Scenery|None, icao : List[str]|None) -> None:
    import pprint
    pprint.pprint(mean_metar(scenery = scenery, icaos = unfold_icaos(icao)))
    
    
if __name__ == "__main__":
   main()
