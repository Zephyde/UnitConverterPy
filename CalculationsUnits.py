# CalculationsUnits.py
import re
from collections import defaultdict
from pint import UnitRegistry, UndefinedUnitError, DimensionalityError

from UnitLoader import (
    ALIAS_TO_PINT,
    METRIC_TARGETS,
    IMPERIAL_TARGETS,
    IMPERIAL_ALIASES,
    METRIC_ALIASES,
    IMPERIAL_PATTERN_FRAGMENT,
    METRIC_PATTERN_FRAGMENT,
)

ureg = UnitRegistry()

print("=== Episode V: The Metric Strikes Back ===")
print("Darth Convertor says: 'I find your lack of metric... disturbing.'")


def normalize_number(value_str: str) -> str:
    return value_str.replace(',', '').replace(' ', '')


def normalize_unit_string(unit_str: str) -> str:
    """Resolves an alias string to its pint unit name."""
    unit_str = unit_str.lower().strip()
    unit_str = re.sub(r'\s*[∕/]\s*', '/', unit_str)
    return ALIAS_TO_PINT.get(unit_str, unit_str)


def get_metric_target(pint_unit: str) -> str:
    return METRIC_TARGETS.get(pint_unit, pint_unit)


def get_imperial_target(pint_unit: str) -> str:
    return IMPERIAL_TARGETS.get(pint_unit, pint_unit)


def _convert(value: float, pint_unit: str, target_unit: str) -> str | None:
    """Core conversion — returns formatted string or None on failure."""
    try:
        quantity = ureg.Quantity(value, pint_unit)
        converted = quantity.to(target_unit)
        mag = converted.magnitude

        formatted = str(int(mag)) if mag == int(mag) else f"{mag:.2f}".rstrip('0').rstrip('.')
        return f"{formatted} {converted.units:~}"
    except (UndefinedUnitError, DimensionalityError, ValueError, AttributeError):
        return None


def _build_pattern(fragment: str) -> str:
    return (
        r'(?P<value>\d{1,3}(?:,\d{3})*(?:\.\d+)?|\d+\.?\d*)'
        r'[-\s]*'
        r'(?P<unit>' + fragment + r')'
        r'(?=\s|[^\w]|$)'
    )


def _replace_units(text: str, aliases: set, get_target, clean_fn=None) -> str:
    pattern = _build_pattern(
        IMPERIAL_PATTERN_FRAGMENT if get_target == get_metric_target
        else METRIC_PATTERN_FRAGMENT
    )

    def replace_func(match):
        value_str = match.group('value')
        unit_raw = match.group('unit').strip().lower()
        unit_raw = re.sub(r'[-\s,;.]+$', '', unit_raw)
        unit_clean = re.sub(r'\s*[∕/·\-]\s*', '/', unit_raw).replace('.', '').replace('-', '')

        if unit_clean not in aliases:
            return match.group(0)

        try:
            value = float(normalize_number(value_str))
            pint_unit = normalize_unit_string(unit_clean)
            target = get_target(pint_unit)
            result = _convert(value, pint_unit, target)
            return result + ' ' if result else match.group(0)
        except Exception:
            return match.group(0)

    return re.sub(pattern, replace_func, text)


def extractAndReplaceUnits(text: str) -> str:
    return _replace_units(text, IMPERIAL_ALIASES, get_metric_target)


def extractAndReplaceMetricUnits(text: str) -> str:
    return _replace_units(text, METRIC_ALIASES, get_imperial_target)


def _extract_units(text: str, pattern_fragment: str, aliases: set) -> dict:
    pattern = _build_pattern(pattern_fragment)
    units_dict = defaultdict(list)

    for match in re.finditer(pattern, text):
        value_str = match.group('value')
        unit = match.group('unit').strip().lower()
        unit = re.sub(r'\s*[∕/]\s*', '/', unit)
        unit_clean = re.sub(r'[-\s,;.]+$', '', unit).replace('.', '')

        if unit_clean not in aliases:
            continue
        try:
            units_dict[unit_clean].append(float(normalize_number(value_str)))
        except ValueError:
            continue

    return dict(units_dict)


def extractUnitsFromText(text: str) -> dict:
    return _extract_units(text, IMPERIAL_PATTERN_FRAGMENT, IMPERIAL_ALIASES)


def extractUnitsFromAnswer(text: str) -> dict:
    return _extract_units(text, METRIC_PATTERN_FRAGMENT, METRIC_ALIASES)


def _convert_dict(units_dict: dict, get_target) -> list[str]:
    lines = []
    for unit, values in units_dict.items():
        pint_unit = normalize_unit_string(unit)
        target = get_target(pint_unit)
        for value in values:
            result = _convert(value, pint_unit, target)
            lines.append(f"{value} {unit} → {result}" if result else f"⚠️ Unrecognized unit: {unit}")
    return lines


def ConvertImpToMetSeparate(units_dict: dict) -> list[str]:
    return _convert_dict(units_dict, get_metric_target)


def ConvertMetToImpSeparate(units_dict: dict) -> list[str]:
    return _convert_dict(units_dict, get_imperial_target)