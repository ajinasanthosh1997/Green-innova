# solar_engine.py
import math

# Constants (mirroring your SOLAR_PARAMS)
SOLAR_PARAMS = {
    'utility_rate': 0.032,          # BHD per kWh (flat rate for non‑subsidized/commercial)
    'peak_sun_hours': 5.5,
    'performance_ratio': 0.75,
    'panel_wattage': 450,
    'co2_per_kwh': 0.5,
    'trees_per_kg_co2': 0.05,
    'annual_degradation': 0.005,
    'utility_inflation': 0.03
}

# Residential subsidized tiers (rates in BHD per unit)
# Unit ranges are inclusive of lower bound, exclusive of upper bound (except last)
SUBSIDIZED_TIERS = [
    (0, 2900, 0.003),      # 0–2900 units → 3 fils/unit
    (2900, 4900, 0.009),   # 2901–4900 → 9 fils/unit
    (4900, float('inf'), 0.016)  # 4901+ → 16 fils/unit
]

def calculate_monthly_bill(units, customer_type, is_subsidized):
    """
    Calculate monthly bill based on units, customer type, and subsidy status.
    - customer_type: 'Residential' or 'Commercial'
    - is_subsidized: bool (only matters for Residential)
    Returns bill in BHD.
    """
    if customer_type == 'Commercial':
        # Commercial always uses flat 32 fils/unit regardless of subsidy flag
        return units * 0.032

    # Residential
    if not is_subsidized:
        # Non‑subsidized residential also uses flat 32 fils/unit
        return units * 0.032

    # Subsidized residential – tiered pricing
    bill = 0.0
    remaining = units
    for lower, upper, rate in SUBSIDIZED_TIERS:
        if remaining <= 0:
            break
        tier_units = min(remaining, upper - lower)
        bill += tier_units * rate
        remaining -= tier_units
    return bill

def convert_bill_to_units(bill, customer_type, is_subsidized):
    """
    Reverse‑calculate units from a given bill amount.
    Used when user inputs a bill instead of units.
    Returns approximate units (float).
    """
    if customer_type == 'Commercial':
        return bill / 0.032

    if not is_subsidized:
        return bill / 0.032

    # Subsidized residential – need to invert tiered rates
    # We know the rate progression: 0.003, then 0.009, then 0.016
    # Determine which tier the bill falls into
    # Compute cumulative bill at tier boundaries
    tier1_max_bill = 2900 * 0.003                    # = 8.7
    tier2_max_bill = tier1_max_bill + (4900-2900) * 0.009  # 8.7 + 18 = 26.7

    if bill <= tier1_max_bill:
        return bill / 0.003
    elif bill <= tier2_max_bill:
        # bill = 8.7 + (units - 2900) * 0.009
        return 2900 + (bill - tier1_max_bill) / 0.009
    else:
        # bill = 26.7 + (units - 4900) * 0.016
        return 4900 + (bill - tier2_max_bill) / 0.016

def calculate_solar(monthly_bill, customer_type, is_subsidized):
    """
    Compute solar system size, yearly production, savings, etc.
    Mirrors the JavaScript `calculateSolar` function.
    """
    # Calibration: 70 BHD monthly bill → 11 kW system (from your JS)
    scale_factor = monthly_bill / 70.0
    system_size = 11.0 * scale_factor

    # Number of panels (using 450W panels)
    num_panels = math.ceil((system_size * 1000) / SOLAR_PARAMS['panel_wattage'])

    # Area required (approx 63 m² for 11 kW system)
    area_required = 63.0 * scale_factor

    # Yearly production (kWh)
    yearly_production = system_size * SOLAR_PARAMS['peak_sun_hours'] * 365 * SOLAR_PARAMS['performance_ratio']

    # Yearly savings (ballpark 90% offset of current bill)
    yearly_savings = monthly_bill * 12 * 0.9

    # Environmental metrics
    co2_saved = yearly_production * SOLAR_PARAMS['co2_per_kwh']
    trees_planted = round(co2_saved * SOLAR_PARAMS['trees_per_kg_co2'])

    # Plan data (matching your frontend)
    def generate_plan_data(savings_at_70, upfront):
        net_25_year_savings = round(savings_at_70 * scale_factor * (25 / 20))
        # Simple projection array (optional)
        projections = [round(net_25_year_savings * i / 25) for i in range(1, 26)]
        return {
            'net_25_year_savings': net_25_year_savings,
            'out_of_pocket': upfront,
            'payback': '5.2 Years' if upfront > 0 else 'Immediate',
            'projections': projections
        }

    return {
        'monthly_bill': monthly_bill,
        'system_size': round(system_size, 1),
        'num_panels': num_panels,
        'yearly_production': round(yearly_production),
        'yearly_savings': round(yearly_savings),
        'co2_saved': round(co2_saved),
        'trees_planted': trees_planted,
        'area_required': round(area_required),
        'plans': {
            'performance': generate_plan_data(120, 0),
            'fixed': generate_plan_data(95, 0),
            'lease_to_own': {
                **generate_plan_data(1500, 0),
                'monthly_payment': round(100 * scale_factor),
                'lease_period': '60 Months',
                'out_of_pocket': '0 BHD'
            }
        },
        'technical_specs': {
            'panel_type': 'Monocrystalline Perc',
            'inverter_efficiency': '98.2%',
            'mounting_system': 'Aluminum Rail (Roof)',
            'monitoring': 'Cloud‑based WiFi App'
        }
    }