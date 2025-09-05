"""
This module contains stuff related to weather, like metars and methods
to maniplate it.
"""

import logging
from typing import Dict, List, Optional

# third party libraries
import requests
from metar.Metar import Metar

# my own
from scenery import Scenery, icao_by_scenery, IcaoList

log = logging.getLogger(__name__)

MetarList = List[Metar]

def download_metar(icao: str) -> Optional[Metar]:
    """This needs realy to be documented? REALLY!?"""
    try:
        url = f"https://tgftp.nws.noaa.gov/data/observations/metar/stations/{icao}.TXT"
        log.debug("Downloading metar for %s from $s", icao, url)
        response = requests.get(url)
        raw_metar = response.text.split("\n")[1]
        metar = Metar(raw_metar)
        log.info("Metar of %s is %s", icao, metar.code)
        log.debug("%s", metar.string())
        return metar
    except Exception as e:
        log.error(e)
        return None


def average_metars(metars: MetarList) -> Dict:
    """
    Compute the "mean" metar from a list of METARs, for whatever
    meaning this could have...
    """
    import math
    from statistics import mean

    winds_u, winds_v, gusts, vis, qnh, temps, dewps = [], [], [], [], [], [], []
    clouds_all = []

    for m in metars:
        # it can happen if cannot download a metar...
        if m is None:
            continue

        # vento
        if m.wind_speed and m.wind_dir:
            speed = m.wind_speed.value("KT")
            if not speed:
                speed = 0
            dir_rad = math.radians(m.wind_dir.value())
            u = -speed * math.sin(dir_rad)
            v = -speed * math.cos(dir_rad)
            winds_u.append(u)
            winds_v.append(v)
        if m.wind_gust:
            gusts.append(m.wind_gust.value("KT"))

        # visibilità
        if m.vis:
            vis.append(m.vis.value("M"))

        # pressione
        if m.press:
            qnh.append(m.press.value("HPA"))

        # temperatura e dew point
        if m.temp:
            temps.append(m.temp.value("C"))
        if m.dewpt:
            dewps.append(m.dewpt.value("C"))

        # nuvole
        if m.sky:
            clouds_all.append(m.sky)

    # media vento
    mean_u = mean(winds_u) if winds_u else 0
    mean_v = mean(winds_v) if winds_v else 0
    wind_dir = (math.degrees(math.atan2(-mean_u, -mean_v)) + 360) % 360
    wind_speed = math.hypot(mean_u, mean_v)

    result = {
        "wind_dir_deg": round(wind_dir),
        "wind_speed_kt": round(wind_speed),
        "wind_gusts_kt": round(mean(gusts)) if gusts else None,
        "visibility_m": round(mean(vis)) if vis else None,
        "qnh_hpa": round(mean(qnh)) if qnh else None,
        "temperature_c": round(mean(temps)) if temps else None,
        "dewpoint_c": round(mean(dewps)) if dewps else None,
        "clouds": None,
    }

    # media nuvole (grezza: prende la quota media per ogni strato simile)
    if clouds_all:
        flat = [layer for sky in clouds_all for layer in sky]
        if flat:
            # raggruppo per tipo (FEW, SCT, BKN, OVC)
            grouped = {}

            for cover, height, _ in flat:
                if cover not in grouped:
                    grouped[cover] = []
                if height:
                    grouped[cover].append(height.value("FT"))

            avg_clouds = []

            for cover, heights in grouped.items():
                avg_h = round(mean(heights)) if heights else None
                avg_clouds.append((cover, avg_h))

            result["clouds"] = avg_clouds

    return result


def mean_metar(scenery: Optional[Scenery], icaos: Optional[IcaoList]) -> Optional[Dict]:
    """
    Download and evaluate an average of METARs starting from a Scenery
    (for which are predefined a list of ICAOs or an explicit list of
    ICAOs.
    """

    if icaos is None and scenery is None:
        return None
    
    list_icaos = icao_by_scenery[scenery] if not icaos else icaos
    
    metars : MetarList = []
    for icao in list_icaos:
        metar: Optional[Metar] = download_metar(icao)
        if metar:
            metars.append(metar)
        
    return average_metars(metars)
