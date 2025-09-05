#!/usr/bin/env python

import logging
import pprint
from typing import Optional

# third party libs
import click

# my own
from dcs import Mission
from log import LogLevel, configure_logging
from scenery import Scenery, Icao, IcaoList
from weather import mean_metar


log = logging.getLogger(__name__)


def unfold_icaos(icaos: Optional[Icao]) -> Optional[IcaoList]:
    if not icaos:
        return None

    return [icao.strip() for icao in icaos.split(",")]


@click.group()
@click.option(
    "--level", default="INFO", type=click.Choice(list(LogLevel), case_sensitive=False)
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
def show(scenery: Optional[Scenery], icao: Optional[Icao]) -> None:
    pprint.pprint(mean_metar(scenery=scenery, icaos=unfold_icaos(icao)))


if __name__ == "__main__":
    main()
