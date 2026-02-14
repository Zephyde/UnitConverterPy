import re
from collections import defaultdict
from pint import UnitRegistry, UndefinedUnitError, DimensionalityError

ureg = UnitRegistry()

print("=== Episode V: The Metric Strikes Back ===")
print("Darth Convertor says: 'I find your lack of metric... disturbing.'")


def normalize_number(value_str):
    return value_str.replace(',', '').replace(' ', '')


def normalize_unit_string(unit_str):
    unit_str = unit_str.lower().strip()
    unit_str = re.sub(r'\s*[∕/]\s*', '/', unit_str)

    unit_map = {
        'ft': 'foot', 'ft.': 'foot', 'feet': 'foot',
        'in': 'inch', 'in.': 'inch', 'inches': 'inch',
        'lb': 'pound', 'lbs': 'pound', 'pounds': 'pound',
        'slug': 'slug', 'slugs': 'slug',
        'ft/s': 'foot/second', 'ft/sec': 'foot/second',
        'ft/s²': 'foot/second**2', 'ft/s2': 'foot/second**2',
        'ft/sec²': 'foot/second**2', 'ft/sec2': 'foot/second**2',
        'mi/hr': 'mile/hour', 'mph': 'mile/hour',
        'lb/ft': 'pound_force/foot',
        'hp': 'horsepower',
        'rad/s': 'radian/second',
        'gal': 'gal',

        'm': 'meter', 'm.': 'meter', 'meters': 'meter', 'metres': 'meter', 'metre': 'meter',
        'cm': 'centimeter', 'cm.': 'centimeter',
        'mm': 'millimeter', 'mm.': 'millimeter',
        'kg': 'kilogram', 'kg.': 'kilogram', 'kgs': 'kilogram',
        'kilograms': 'kilogram', 'kilogram': 'kilogram',
        'm/s': 'meter/second', 'm/sec': 'meter/second',
        'm/s²': 'meter/second**2', 'm/s2': 'meter/second**2',
        'm/sec²': 'meter/second**2', 'm/sec2': 'meter/second**2',
        'km/h': 'kilometer/hour', 'km/hr': 'kilometer/hour',
        'n': 'newton', 'newtons': 'newton',
        'n/m': 'newton/meter', 'n·m': 'newton*meter', 'n-m': 'newton*meter',
        'w': 'watt', 'watts': 'watt', 'watt': 'watt',
        'kw': 'kilowatt', 'kilowatts': 'kilowatt', 'kilowatt': 'kilowatt',
    }

    return unit_map.get(unit_str, unit_str)


def get_metric_target(pint_unit):
    targets = {
        'foot': 'meter', 'inch': 'meter', 'mile': 'meter',
        'pound': 'kilogram', 'slug': 'kilogram',
        'foot/second': 'meter/second', 'mile/hour': 'meter/second',
        'foot/second**2': 'meter/second**2',
        'pound_force/foot': 'newton/meter',
        'horsepower': 'watt',
        'radian/second': 'radian/second',
        'gal': 'meter/second**2',
    }
    return targets.get(pint_unit, pint_unit)


def get_imperial_target(pint_unit):
    targets = {
        'meter': 'foot', 'centimeter': 'inch', 'millimeter': 'inch',
        'kilogram': 'pound',
        'meter/second': 'foot/second', 'kilometer/hour': 'mile/hour',
        'meter/second**2': 'foot/second**2',
        'newton': 'pound_force', 'newton/meter': 'pound_force/foot',
        'watt': 'horsepower', 'kilowatt': 'horsepower',
        'radian/second': 'radian/second',
    }
    return targets.get(pint_unit, pint_unit)


def replace_match(match, conversions):
    """ Exchanged the manual conversion logic for pint conversion logic
        As constantly adding new manual conversion factors became annoying."""
    value_str = match.group('value')
    unit_raw = match.group('unit').strip().lower()

    try:
        value = float(normalize_number(value_str))
    except ValueError:
        return match.group(0)

    unit_clean = re.sub(r'\s*[∕/]\s*', '/', unit_raw)

    if unit_clean in conversions:
        try:
            pint_unit = normalize_unit_string(unit_clean)

            if conversions == 'to_metric':
                target_unit = get_metric_target(pint_unit)
            else:
                target_unit = get_imperial_target(pint_unit)

            quantity = ureg.Quantity(value, pint_unit)
            converted = quantity.to(target_unit)
            converted_value = converted.magnitude

            if converted_value == int(converted_value):
                formatted_value = str(int(converted_value))
            else:
                formatted_value = f"{converted_value:.2f}".rstrip('0').rstrip('.')

            return f"{formatted_value} {converted.units:~}"

        except (UndefinedUnitError, DimensionalityError, ValueError, AttributeError):
            return match.group(0)
    else:
        return match.group(0)


def extractAndReplaceUnits(text):
    imperial_units = {
        'ft', 'feet', 'in', 'inches', 'lb', 'pounds', 'slug', 'slugs',
        'ft/s', 'ft/sec', 'ft/s²', 'ft/s2', 'ft/sec²',
        'mi/hr', 'mph', 'lb/ft', 'hp', 'rad/s', 'gal'
    }

    pattern = r'(?P<value>\d{1,3}(?:,\d{3})*(?:\.\d+)?|\d+\.?\d*)[-\s]*(?P<unit>(?:mi\s*[/∕]\s*hr|mph|rad\s*[/∕]\s*s|ft\s*[/∕]\s*sec²|ft\s*[/∕]\s*s²|ft\s*[/∕]\s*s2|ft\s*[/∕]\s*sec|ft\s*[/∕]\s*s|lb\s*[/∕]\s*ft|in(?:ches)?\.?|ft-?|feet|pounds?|lb|slug(?:s)?|hp|gal)(?:\s|$|[,;.\-]))'

    def replace_func(match):
        value_str = match.group('value')
        unit_raw = match.group('unit').strip().lower()

        unit_raw = re.sub(r'[-\s,;.]+$', '', unit_raw)

        unit_clean = re.sub(r'\s*[∕/]\s*', '/', unit_raw)
        unit_clean = unit_clean.replace('-', '')  # Remove hyphens

        if unit_clean in imperial_units:
            try:
                value = float(normalize_number(value_str))
                pint_unit = normalize_unit_string(unit_clean)
                target_unit = get_metric_target(pint_unit)

                quantity = ureg.Quantity(value, pint_unit)
                converted = quantity.to(target_unit)
                converted_value = converted.magnitude

                if converted_value == int(converted_value):
                    formatted_value = str(int(converted_value))
                else:
                    formatted_value = f"{converted_value:.2f}".rstrip('0').rstrip('.')

                trailing = match.group(0)[-1] if match.group(0)[-1] in ' ,;.-\n' else ' '
                return f"{formatted_value} {converted.units:~}{trailing}"
            except:
                return match.group(0)

        return match.group(0)

    converted_text = re.sub(pattern, replace_func, text)
    return converted_text


def extractAndReplaceMetricUnits(text):
    metric_units = {
        'm', 'meters', 'metres', 'metre', 'cm', 'mm',
        'kg', 'kilograms', 'kilogram',
        'm/s', 'm/sec', 'm/s²', 'm/s2', 'm/sec²',
        'km/h', 'km/hr',
        'n', 'n/m', 'n·m', 'n-m',
        'w', 'watts', 'watt', 'kw', 'kilowatts', 'kilowatt',
        'rad/s'
    }

    pattern = r'(?P<value>\d{1,3}(?:,\d{3})*(?:\.\d+)?|\d+\.?\d*)[-\s]*(?P<unit>(?:rad\s*[/∕]\s*s|km\s*[/∕]\s*h|km\s*[/∕]\s*hr|m\s*[/∕]\s*s²|m\s*[/∕]\s*s2|m\s*[/∕]\s*sec²|m\s*[/∕]\s*sec|m\s*[/∕]\s*s|n\s*[/∕]\s*m|n\s*·\s*m|n\s*-\s*m|cm\.?|mm\.?|m\.?|meters?|metres?|metre|kg\.?|kilograms?|kilogram|n|w|kw|watts?|watt|kilowatts?|kilowatt)(?:\s|$|[,;.\-]))'

    def replace_func(match):
        value_str = match.group('value')
        unit_raw = match.group('unit').strip().lower()

        unit_raw = re.sub(r'[-\s,;.]+$', '', unit_raw)

        unit_clean = re.sub(r'\s*[∕/·\-]\s*', '/', unit_raw)
        unit_clean = unit_clean.replace('.', '')

        if unit_clean in metric_units:
            try:
                value = float(normalize_number(value_str))
                pint_unit = normalize_unit_string(unit_clean)
                target_unit = get_imperial_target(pint_unit)

                quantity = ureg.Quantity(value, pint_unit)
                converted = quantity.to(target_unit)
                converted_value = converted.magnitude

                if converted_value == int(converted_value):
                    formatted_value = str(int(converted_value))
                else:
                    formatted_value = f"{converted_value:.2f}".rstrip('0').rstrip('.')

                trailing = match.group(0)[-1] if match.group(0)[-1] in ' ,;.-\n' else ' '
                return f"{formatted_value} {converted.units:~}{trailing}"
            except:
                return match.group(0)

        return match.group(0)

    converted_text = re.sub(pattern, replace_func, text)
    return converted_text


def ConvertImpToMetSeparate(units_dict):
    lines = []

    for unit, values in units_dict.items():
        for value in values:
            try:
                pint_unit = normalize_unit_string(unit)
                target = get_metric_target(pint_unit)

                quantity = ureg.Quantity(value, pint_unit)
                converted = quantity.to(target)

                metric_value = round(converted.magnitude, 4)
                metric_unit = f"{converted.units:~}"  # nice abbreviations
                lines.append(f"{value} {unit} → {metric_value} {metric_unit}")

            except (UndefinedUnitError, DimensionalityError, ValueError, AttributeError):
                lines.append(f"⚠️ Unrecognized unit: {unit}")

    return lines

def ConvertMetToImpSeparate(units_dict):
    lines = []

    for unit, values in units_dict.items():
        for value in values:
            try:
                pint_unit = normalize_unit_string(unit)
                target = get_imperial_target(pint_unit)

                quantity = ureg.Quantity(value, pint_unit)
                converted = quantity.to(target)

                imp_value = round(converted.magnitude, 4)
                imp_unit = f"{converted.units:~}"
                lines.append(f"{value} {unit} → {imp_value} {imp_unit}")

            except (UndefinedUnitError, DimensionalityError, ValueError, AttributeError):
                lines.append(f"⚠️ Unrecognized unit: {unit}")

    return lines




def extractUnitsFromText(text):
    imperial_pattern = r'(?P<value>\d{1,3}(?:,\d{3})*(?:\.\d+)?|\d+\.?\d*)[-\s]*?(?P<unit>(?:rad\s*[/∕]\s*s|mi\s*[/∕]\s*hr|mph|ft[/∕]sec²|ft[/∕]s²|ft[/∕]s2|ft[/∕]sec|ft[/∕]s|lb[/∕]ft|in(?:ches)?\.?|ft\.?|feet|pounds?|lb|slug(?:s)?|hp|gal)\b)'

    matches = re.finditer(imperial_pattern, text)
    units_dict = defaultdict(list)

    for match in matches:
        value_str = match.group('value')
        unit = match.group('unit').strip().lower()

        try:
            value = float(normalize_number(value_str))
        except ValueError:
            continue

        unit = re.sub(r'\s*[∕/]\s*', '/', unit)
        unit = unit.replace('lbs', 'lb').replace('in.', 'in')
        units_dict[unit].append(value)

    if units_dict:
        ConvertImpToMetSeparate(units_dict)

    return dict(units_dict)


def extractUnitsFromAnswer(text):
    metric_pattern = r'(?P<value>\d{1,3}(?:,\d{3})*(?:\.\d+)?|\d+\.?\d*)[-\s]*?(?P<unit>(?:rad[/∕]s|km[/∕]h|km[/∕]hr|m[/∕]s²|m[/∕]s2|m[/∕]sec²|m[/∕]sec|m[/∕]s|N[/∕]m|N·m|N-m|cm\.?|mm\.?|m\.?|meters?|metres?|kg\.?|kilograms?|N|W|kW|watts?|kilowatts?)\b)'

    matches = re.finditer(metric_pattern, text)
    metric_units_dict = defaultdict(list)

    for match in matches:
        value_str = match.group("value")
        unit = match.group("unit").strip().lower()

        try:
            value = float(normalize_number(value_str))
        except ValueError:
            continue

        unit = re.sub(r'\s*[∕/]\s*', '/', unit)

        unit = unit.replace('kgs', 'kg')
        unit = unit.replace('kg.', 'kg')
        unit = unit.replace('m.', 'm')
        unit = unit.replace('cm.', 'cm')
        unit = unit.replace('mm.', 'mm')
        unit = unit.replace('metres', 'm')
        unit = unit.replace('metre', 'm')
        unit = unit.replace('meters', 'm')
        unit = unit.replace('meter', 'm')
        unit = unit.replace('kilograms', 'kg')
        unit = unit.replace('kilogram', 'kg')
        unit = unit.replace('watts', 'w')
        unit = unit.replace('watt', 'w')
        unit = unit.replace('kilowatts', 'kw')
        unit = unit.replace('kilowatt', 'kw')
        unit = unit.replace('km/hr', 'km/h')
        unit = unit.replace('n·m', 'n/m')
        unit = unit.replace('n-m', 'n/m')
        unit = unit.replace('m/s2', 'm/s²')
        unit = unit.replace('m/sec2', 'm/s²')
        unit = unit.replace('m/sec²', 'm/s²')

        metric_units_dict[unit].append(value)

    return dict(metric_units_dict)