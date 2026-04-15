# unit_loader.py
import tomllib
from pathlib import Path

def load_units() -> dict:
    core_path = Path(__file__).parent / "units.toml"
    with open(core_path, "rb") as f:
        units = tomllib.load(f)

    return units


def build_lookups(units: dict):

    alias_to_pint    = {}
    metric_targets   = {}
    imperial_targets = {}
    imperial_aliases = set()
    metric_aliases   = set()
    imperial_patterns = []
    metric_patterns   = []

    for key, unit in units.items():
        pint_name = unit["pint"]
        direction = unit.get("direction", "")

        for alias in unit.get("aliases", []):
            alias_to_pint[alias] = pint_name

        if "metric_target" in unit:
            metric_targets[pint_name] = unit["metric_target"]
        if "imperial_target" in unit:
            imperial_targets[pint_name] = unit["imperial_target"]

        pat = unit.get("pattern", "")
        if direction in ("imperial", "both"):
            imperial_aliases.update(unit.get("aliases", []))
            if pat:
                imperial_patterns.append(pat)
        if direction in ("metric", "both"):
            metric_aliases.update(unit.get("aliases", []))
            if pat:
                metric_patterns.append(pat)

    combined_imperial_pattern = "|".join(imperial_patterns)
    combined_metric_pattern   = "|".join(metric_patterns)

    return (
        alias_to_pint,
        metric_targets,
        imperial_targets,
        imperial_aliases,
        metric_aliases,
        combined_imperial_pattern,
        combined_metric_pattern,
    )


# Load once at import time so every module that imports this shares the same data
UNITS = load_units()
(
    ALIAS_TO_PINT,
    METRIC_TARGETS,
    IMPERIAL_TARGETS,
    IMPERIAL_ALIASES,
    METRIC_ALIASES,
    IMPERIAL_PATTERN_FRAGMENT,
    METRIC_PATTERN_FRAGMENT,
) = build_lookups(UNITS)