#!/usr/bin/env python

import logging
from typing import List

import click

from dcs import Mission
from log import LogLevel, configure_logging
from scenery import Scenery
from weather import mean_metar

# third party libraries (expect to install)





log = logging.getLogger(__name__)


def unfold_icaos(icaos: str | None):
    if not icaos:
        return None

    return [icao.strip() for icao in icaos.split(",")]


@click.group()
@click.option(
    "--level", default="INFO", type=click.Choice(LogLevel, case_sensitive=False)
)
def main(level):
    configure_logging(level)


@main.command(help="Update METAR on mission file")
@click.option("--miz", prompt="Path to MIZ ?", help="path to MIZ")
@click.option("--icao", nargs=1, default=None, help="comma separeted list of ICAOs")
def update(miz, icao) -> None:
    mission = Mission(miz)
    data = mean_metar(mission.theatre, icaos=unfold_icaos(icao))
    log.info(data)


@main.command(help="Shows METAR")
@click.option("--scenery", default=None, help="Name of the Scenery", type=Scenery)
@click.option("--icao", nargs=1, default=None, help="Comma separated list of ICAOs")
def show(scenery: Scenery | None, icao: List[str] | None) -> None:
    import pprint

    pprint.pprint(mean_metar(scenery=scenery, icaos=unfold_icaos(icao)))


if __name__ == "__main__":
    main()
