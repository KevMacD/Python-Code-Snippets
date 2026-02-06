from typing import Dict


def calculate_band_conditions(
    solar_flux: int,
    k_index: int,
    utc_hour: int,
    latitude_deg: float
) -> Dict[str, str]:
    """
    Calculate HF/VHF band conditions based on solar flux, K-index,
    UTC hour, and latitude.

    Model assumptions:
      - Daytime: 06–18 UTC (simplified)
      - Grayline width increases with |latitude|
    """

    bands = [
        '160m', '80m', '60m', '40m', '30m',
        '20m', '17m', '15m', '12m',
        '11m', '10m', '6m', '2m', '70cm'
    ]

    sfi = int(solar_flux)
    k = int(k_index)
    hour = int(utc_hour) % 24

    # Base day window
    day_start = 6
    day_end = 18
    is_daytime = day_start <= hour <= day_end

    # Grayline width grows with latitude (1–3 hours)
    lat = abs(float(latitude_deg))
    lat_clamped = min(lat, 66.0)
    grayline_width = 1.0 + (lat_clamped / 66.0) * 2.0

    def hour_distance(a: float, b: float) -> float:
        d = abs(a - b) % 24
        return min(d, 24 - d)

    is_grayline = (
        hour_distance(hour, day_start) <= grayline_width
        or hour_distance(hour, day_end) <= grayline_width
    )

    sfi_impact = {
        '160m': (sfi - 100) * 0.05,
        '80m': (sfi - 100) * 0.10,
        '60m': (sfi - 100) * 0.15,
        '40m': (sfi - 100) * 0.20,
        '30m': (sfi - 100) * 0.25,
        '20m': (sfi - 100) * 0.35,
        '17m': (sfi - 100) * 0.40,
        '15m': (sfi - 100) * 0.45,
        '12m': (sfi - 100) * 0.50,
        '11m': (sfi - 100) * 0.52,
        '10m': (sfi - 100) * 0.55,
        '6m':  (sfi - 100) * 0.60,
        '2m':  0,
        '70cm': 0
    }

    time_impact = {
        '160m': -30 if is_daytime else 25,
        '80m':  -20 if is_daytime else 20,
        '60m':  -10 if is_daytime else 15,
        '40m':  20 if is_grayline else (5 if is_daytime else 15),
        '30m':  15 if is_daytime else 10,
        '20m':  25 if is_daytime else -15,
        '17m':  25 if is_daytime else -20,
        '15m':  20 if is_daytime else -25,
        '12m':  15 if is_daytime else -30,
        '11m':  15 if is_daytime else -32,
        '10m':  15 if is_daytime else -35,
        '6m':   10 if is_daytime else -40,
        '2m':   10,
        '70cm': 10
    }

    conditions: Dict[str, str] = {}

    for band in bands:
        score = 50

        score += sfi_impact.get(band, 0)

        if k <= 1:
            score += 15
        elif k <= 2:
            score += 5
        elif k >= 5:
            score -= 40
        elif k >= 4:
            score -= 25
        elif k >= 3:
            score -= 10

        score += time_impact.get(band, 0)

        if band in {'10m', '11m', '12m', '6m'} and sfi < 100:
            score -= 30
        if band in {'15m', '17m'} and sfi < 80:
            score -= 15

        if score >= 65:
            conditions[band] = 'GOOD'
        elif score >= 40:
            conditions[band] = 'FAIR'
        else:
            conditions[band] = 'POOR'

    return conditions


#VANCOUVER_LAT = 49.2827

#conditions = calculate_band_conditions(
#    solar_flux=178,
#    k_index=4,
#    utc_hour=23,
#    latitude_deg=VANCOUVER_LAT
#)
