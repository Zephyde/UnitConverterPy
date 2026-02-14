import re
from collections import defaultdict

print("=== Episode V: The Metric Strikes Back ===")
print("Darth Convertor says: 'I find your lack of metric... disturbing.'")


def replace_match(match, conversions):
    value = float(match.group('value'))
    unit_raw = match.group('unit').strip().lower()

    unit_clean = re.sub(r'\s*[∕/]\s*', '/', unit_raw)

    if unit_clean in conversions:
        converted_value = value * conversions[unit_clean]['factor']
        target_unit = conversions[unit_clean]['unit']

        if converted_value == int(converted_value):
            formatted_value = str(int(converted_value))
        else:
            formatted_value = f"{converted_value:.2f}".rstrip('0').rstrip('.')

        return f"{formatted_value} {target_unit}"
    else:
        return match.group(0)


def extractAndReplaceUnits(text):
    conversions = {
        'ft': {'factor': 0.3048, 'unit': 'm'},
        'feet': {'factor': 0.3048, 'unit': 'm'},
        'in': {'factor': 0.0254, 'unit': 'm'},
        'inches': {'factor': 0.0254, 'unit': 'm'},
        'lb': {'factor': 0.453592, 'unit': 'kg'},
        'pounds': {'factor': 0.453592, 'unit': 'kg'},
        'slug': {'factor': 14.5939, 'unit': 'kg'},
        'slugs': {'factor': 14.5939, 'unit': 'kg'},
        'ft/s': {'factor': 0.3048, 'unit': 'm/s'},
        'ft/sec': {'factor': 0.3048, 'unit': 'm/s'},
        'ft/s²': {'factor': 0.3048, 'unit': 'm/s²'},
        'ft/s2': {'factor': 0.3048, 'unit': 'm/s²'},
        'ft/sec²': {'factor': 0.3048, 'unit': 'm/s²'},
        'mi/hr': {'factor': 0.44704, 'unit': 'm/s'},
        'lb/ft': {'factor': 14.5939, 'unit': 'N/m'},
        'hp': {'factor': 745.7, 'unit': 'W'},
        'rad/s': {'factor': 1.0, 'unit': 'rad/s'},  # Already metric
    }

    pattern = r'(?P<value>\d{1,3}(?:,\d{3})*(?:\.\d+)?|\d+\.?\d*)[-\s]*?(?P<unit>(?:rad\s*[/∕]\s*s|mi\s*[/∕]\s*hr|ft[/∕]sec²|ft[/∕]s²|ft[/∕]s2|ft[/∕]sec|ft[/∕]s|lb[/∕]ft|in(?:ches)?\.?|ft\.?|feet|pounds?|lb(?:\s*[/∕]\s*ft)?|slug(?:s)?|hp|gal)\b)'


    converted_text = re.sub(pattern, lambda match: replace_match(match, conversions), text)
    return converted_text


def extractAndReplaceMetricUnits(text):
    conversions = {
        'm': {'factor': 3.28084, 'unit': 'ft'},
        'meters': {'factor': 3.28084, 'unit': 'ft'},
        'metre': {'factor': 3.28084, 'unit': 'ft'},
        'metres': {'factor': 3.28084, 'unit': 'ft'},
        'cm': {'factor': 0.393701, 'unit': 'in'},
        'mm': {'factor': 0.0393701, 'unit': 'in'},
        'kg': {'factor': 2.20462, 'unit': 'lb'},
        'kilograms': {'factor': 2.20462, 'unit': 'lb'},
        'kilogram': {'factor': 2.20462, 'unit': 'lb'},
        'm/s': {'factor': 3.28084, 'unit': 'ft/s'},
        'm/sec': {'factor': 3.28084, 'unit': 'ft/s'},
        'm/s²': {'factor': 3.28084, 'unit': 'ft/s²'},
        'm/s2': {'factor': 3.28084, 'unit': 'ft/s²'},
        'm/sec²': {'factor': 3.28084, 'unit': 'ft/s²'},
        'km/h': {'factor': 0.621371, 'unit': 'mi/hr'},
        'km/hr': {'factor': 0.621371, 'unit': 'mi/hr'},
        'n': {'factor': 0.224809, 'unit': 'lb'},  # Newtons to pounds-force
        'n/m': {'factor': 0.737562, 'unit': 'lb/ft'},  # Torque
        'w': {'factor': 0.00134102, 'unit': 'hp'},
        'watts': {'factor': 0.00134102, 'unit': 'hp'},
        'watt': {'factor': 0.00134102, 'unit': 'hp'},
        'kw': {'factor': 1.34102, 'unit': 'hp'},
        'kilowatts': {'factor': 1.34102, 'unit': 'hp'},
        'kilowatt': {'factor': 1.34102, 'unit': 'hp'},
        'rad/s': {'factor': 1.0, 'unit': 'rad/s'},  # Already same
    }

    pattern = r'(?P<value>\d{1,3}(?:,\d{3})*(?P<unit>(?:rad[/∕]s|km[/∕]h|km[/∕]hr|m[/∕]s²|m[/∕]s2|m[/∕]sec²|m[/∕]sec|m[/∕]s|n[/∕]m|n·m|n-m|cm\.?|mm\.?|m\.?|meters?|metres?|metre|kg\.?|kilograms?|kilogram|n|w|kw|watts?|watt|kilowatts?|kilowatt)\b)'

    converted_text = re.sub(pattern, lambda match: replace_match(match, conversions), text)
    return converted_text

def ConvertImpToMetSeparate(units_dict):
    conversions = {
        'ft': {'factor': 0.3048, 'unit': 'm'},
        'feet': {'factor': 0.3048, 'unit': 'm'},
        'in': {'factor': 0.0254, 'unit': 'm'},
        'inches': {'factor': 0.0254, 'unit': 'm'},
        'lb': {'factor': 0.453592, 'unit': 'kg'},
        'pounds': {'factor': 0.453592, 'unit': 'kg'},
        'slug': {'factor': 14.5939, 'unit': 'kg'},
        'slugs': {'factor': 14.5939, 'unit': 'kg'},
        'ft/s': {'factor': 0.3048, 'unit': 'm/s'},
        'ft/sec': {'factor': 0.3048, 'unit': 'm/s'},
        'ft/s²': {'factor': 0.3048, 'unit': 'm/s²'},
        'ft/s2': {'factor': 0.3048, 'unit': 'm/s²'},
        'ft/sec²': {'factor': 0.3048, 'unit': 'm/s²'},
        'mi/hr': {'factor': 0.44704, 'unit': 'm/s'},
        'lb/ft': {'factor': 14.5939, 'unit': 'N/m'},
        'hp': {'factor': 745.7, 'unit': 'W'},
        'rad/s': {'factor': 1.0, 'unit': 'rad/s'},
    }

    outputDict = {}

    print("\n🧪 Conversions: ")
    for unit, values in units_dict.items():
        for value in values:
            if unit in conversions:
                metric_value = round(value * conversions[unit]['factor'], 4)
                metric_unit = conversions[unit]['unit']
                outputDict[metric_unit] = metric_value
                print(f"{value} {unit} → {metric_value} {metric_unit}")
            else:
                print(f"⚠️ Unrecognized unit: {unit}")

    return outputDict






def extractUnitsFromText(text):
    imperial_pattern = r'(?P<value>\d+\.?\d*)[-\s]*?(?P<unit>(?:rad\s*[/∕]\s*s|mi\s*[/∕]\s*hr|ft[/∕]sec²|ft[/∕]s²|ft[/∕]s2|ft[/∕]sec|ft[/∕]s|lb[/∕]ft|in(?:ches)?\.?|ft\.?|feet|pounds?|lb(?:\s*[/∕]\s*ft)?|slug(?:s)?|hp)\b)'
    matches = re.finditer(imperial_pattern, text)

    units_dict = defaultdict(list)

    for match in matches:
        value = float(match.group('value'))
        unit = match.group('unit').strip().lower()

        unit = re.sub(r'\s*[∕/]\s*', '/', unit)
        unit = unit.replace('lbs', 'lb').replace('in.', 'in')
        units_dict[unit].append(value)

    ConvertImpToMetSeparate(units_dict)
    return dict(units_dict)


def extractUnitsFromAnswer(text):
    metric_pattern = r'(?P<value>\d+\.?\d*)[-\s]*?(?P<unit>(?:rad[/∕]s|km[/∕]h|km[/∕]hr|m[/∕]s²|m[/∕]s2|m[/∕]sec²|m[/∕]sec|m[/∕]s|N[/∕]m|N·m|N-m|cm\.?|mm\.?|m\.?|meters?|metre(?:s)?|kg\.?|kilograms?|kilogram(?:s)?|N|W|kW|watts?|kilowatts?)\b)'

    matches = re.finditer(metric_pattern, text)
    metric_units_dict = defaultdict(list)

    for match in matches:
        value = float(match.group("value"))
        unit = match.group("unit").strip().lower()
        unit = re.sub(r'\s*[∕/]\s*', '/', unit)

        # Add metric unit normalizations
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


