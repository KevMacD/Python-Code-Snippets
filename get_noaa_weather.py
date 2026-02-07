from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Optional
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError


NOAA_F107_URL = "https://services.swpc.noaa.gov/json/f107_cm_flux.json"
NOAA_KP_URL = "https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json"
NOAA_SSN_URL = "https://services.swpc.noaa.gov/json/solar-cycle/observed-solar-cycle-indices.json"


def _fetch_json(url: str, timeout_s: float = 10.0) -> Optional[Any]:
    """Fetch JSON from a URL. Returns parsed JSON or None on failure."""
    try:
        req = Request(url, headers={"User-Agent": "space-weather-client/1.0"})
        with urlopen(req, timeout=timeout_s) as resp:
            body = resp.read().decode("utf-8")
            return json.loads(body)
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError):
        return None


def _compute_conditions(sfi: Optional[int], k_index: Optional[float]) -> str:
    if sfi is None or k_index is None:
        return "UNKNOWN"
    # Match your JS logic/thresholds
    if sfi >= 150 and k_index <= 2:
        return "EXCELLENT"
    if sfi >= 100 and k_index <= 3:
        return "GOOD"
    if sfi >= 70 and k_index <= 5:
        return "FAIR"
    return "POOR"


def get_noaa_space_weather(timeout_s: float = 10.0) -> Dict[str, Any]:
    """
    Retrieves space weather data from NOAA SWPC and returns:
      - solarFlux (int or None)
      - kIndex (float or None)
      - sunspotNumber (int or None)
      - conditions (str)
      - lastUpdate (datetime, UTC)
    """

    flux_data = _fetch_json(NOAA_F107_URL, timeout_s=timeout_s)
    kp_data = _fetch_json(NOAA_KP_URL, timeout_s=timeout_s)
    ssn_data = _fetch_json(NOAA_SSN_URL, timeout_s=timeout_s)

    solar_flux: Optional[int] = None
    k_index: Optional[float] = None
    sunspot_number: Optional[int] = None

    # F10.7 flux: list of dicts; last item has flux or value
    if isinstance(flux_data, list) and flux_data:
        last = flux_data[-1]
        if isinstance(last, dict):
            raw = last.get("flux", last.get("value"))
            try:
                if raw is not None:
                    solar_flux = int(round(float(raw)))
            except (ValueError, TypeError):
                solar_flux = None

    # Planetary K-index: JSON array, first row header; last row has [time, kp, ...]
    if isinstance(kp_data, list) and len(kp_data) > 1:
        last_row = kp_data[-1]
        if isinstance(last_row, list) and len(last_row) > 1:
            raw = last_row[1]
            try:
                if raw is not None and raw != "":
                    k_index = float(raw)
            except (ValueError, TypeError):
                k_index = None

    # Sunspot number: list of dicts; last item has ssn
    if isinstance(ssn_data, list) and ssn_data:
        last = ssn_data[-1]
        if isinstance(last, dict):
            raw = last.get("ssn")
            try:
                if raw is not None:
                    sunspot_number = int(round(float(raw)))
            except (ValueError, TypeError):
                sunspot_number = None

    conditions = _compute_conditions(solar_flux, k_index)

    return {
        "solar_flux": solar_flux,              # e.g., 178
        "k_index": k_index,                    # e.g., 4.0
        "SSN": sunspot_number,      # e.g., 210
        "conditions": conditions,             # EXCELLENT/GOOD/FAIR/POOR/UNKNOWN
        "lastUpdate": datetime.now(timezone.utc),
    }
#if __name__ == "__main__":
    #data = get_noaa_space_weather(timeout_s=8)
    #print(data)
