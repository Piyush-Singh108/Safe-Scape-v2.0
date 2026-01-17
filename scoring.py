# scoring.py
from datetime import datetime
from math import exp

# 🔑 Tunable constants (safe for demo + viva)
BASE_RADIUS_METERS = 150
MAX_SEGMENT_RISK = 15.0


def calculate_segment_risk(crimes, time_of_travel: datetime) -> float:
    """
    Returns a non-zero, normalized risk score per route segment
    based on:
    - number of crimes
    - severity
    - night-time amplification
    """

    if not crimes:
        return 0.5  # 🔑 VERY IMPORTANT: empty areas still have baseline risk

    total_severity = 0.0

    for crime in crimes:
        severity = getattr(crime, "severity_score", None) or 2

        # 🌙 Night-time amplification
        if time_of_travel.hour >= 20 or time_of_travel.hour <= 5:
            severity *= 1.6

        total_severity += severity

    # 🔥 Density amplification (more crimes = exponentially riskier)
    density_factor = 1 - exp(-len(crimes) / 3)

    raw_risk = total_severity * density_factor

    # 🔒 Clamp to avoid runaway values
    return min(raw_risk, MAX_SEGMENT_RISK)
