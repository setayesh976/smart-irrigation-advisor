"""
Irrigation Control Simulator
-------------------------------
A simulation of a smart sprinkler control system for a farm, inspired by
watching a family member irrigate and spray crops manually at night. This
program simulates multiple sprinkler zones and decides, for each one,
whether to irrigate, for how long, at what flow rate, and whether it
also needs fertilizer, based on simple rule-based logic.

This is a rule-based simulation, not a trained model: every decision
here is a direct comparison or calculation from fixed rules and
thresholds, not something learned from data. A more advanced version of
this idea, using real soil/weather sensors and a model trained to
predict moisture and nutrient needs ahead of time, is something I'd
like to build as I learn more about AI — this version is a first,
simplified step toward that, built with the tools and skills I
currently have.
"""

import random

# Each zone represents one sprinkler/area of the field.
# "days_since_fertilized" simulates how long it's been since this zone
# last received fertilizer.
zones = {
    "Zone A": {"moisture": 0, "crop": "Wheat", "days_since_fertilized": 0},
    "Zone B": {"moisture": 0, "crop": "Tomatoes", "days_since_fertilized": 0},
    "Zone C": {"moisture": 0, "crop": "Corn", "days_since_fertilized": 0},
    "Zone D": {"moisture": 0, "crop": "Beans", "days_since_fertilized": 0},
}

# Moisture is simulated on a 0-100 scale (percentage).
# Below this threshold, a zone is considered too dry and needs irrigation.
MOISTURE_THRESHOLD = 40

# How many minutes to irrigate per 10%-point the zone is below threshold.
MINUTES_PER_10_POINTS = 5

# Flow rate depends on how dry the zone is: very dry zones get a faster
# flow rate so they catch up more quickly.
FAST_FLOW_THRESHOLD = 20

# Each crop type needs fertilizer at a different interval (in days),
# and a different amount per application (in kilograms, for this zone
# size). These numbers are simplified reference values for this
# simulation, not measured agricultural data.
FERTILIZER_NEEDS = {
    "Wheat":    {"interval_days": 20, "amount_kg": 2.0},
    "Tomatoes": {"interval_days": 14, "amount_kg": 1.5},
    "Corn":     {"interval_days": 18, "amount_kg": 2.5},
    "Beans":    {"interval_days": 25, "amount_kg": 1.0},
}


def simulate_sensor_readings():
    """
    Simulates reading current soil moisture and days since last
    fertilizing for each zone. In a real system, this would come from
    sensors and a logging system; here it's simulated for demonstration.
    """
    for zone in zones:
        zones[zone]["moisture"] = random.randint(10, 90)
        zones[zone]["days_since_fertilized"] = random.randint(0, 30)


def needs_irrigation(zone_name):
    """
    Simple rule-based decision: irrigate if moisture is below the
    threshold, otherwise skip.
    """
    return zones[zone_name]["moisture"] < MOISTURE_THRESHOLD


def calculate_duration_minutes(zone_name):
    """
    Longer irrigation time for drier zones: the deficit (how far below
    the threshold the zone is) is converted into minutes using a fixed
    rate.
    """
    moisture = zones[zone_name]["moisture"]
    deficit = max(0, MOISTURE_THRESHOLD - moisture)
    return round((deficit / 10) * MINUTES_PER_10_POINTS)


def calculate_flow_rate(zone_name):
    """
    Picks "Fast" or "Normal" flow based on how dry the zone is.
    """
    moisture = zones[zone_name]["moisture"]
    deficit = MOISTURE_THRESHOLD - moisture
    return "Fast" if deficit >= FAST_FLOW_THRESHOLD else "Normal"


def needs_fertilizer(zone_name):
    """
    Simple rule: a zone needs fertilizer if more days have passed since
    its last feeding than that crop's recommended interval. No learning
    involved — just a comparison against a fixed, crop-specific number.
    """
    crop = zones[zone_name]["crop"]
    interval = FERTILIZER_NEEDS[crop]["interval_days"]
    return zones[zone_name]["days_since_fertilized"] >= interval


def get_fertilizer_amount(zone_name):
    crop = zones[zone_name]["crop"]
    return FERTILIZER_NEEDS[crop]["amount_kg"]


def build_irrigation_plan():
    plan = {}
    for zone_name in zones:
        if needs_irrigation(zone_name):
            plan[zone_name] = {
                "duration": calculate_duration_minutes(zone_name),
                "flow_rate": calculate_flow_rate(zone_name),
            }
    return plan


def build_fertilizer_plan():
    plan = {}
    for zone_name in zones:
        if needs_fertilizer(zone_name):
            crop = zones[zone_name]["crop"]
            interval = FERTILIZER_NEEDS[crop]["interval_days"]
            plan[zone_name] = {
                "amount_kg": get_fertilizer_amount(zone_name),
                "days_overdue": zones[zone_name]["days_since_fertilized"] - interval,
            }
    return plan


def print_zone_status():
    print("\n=== Zone Readings ===")
    print(f"{'Zone':<10}{'Crop':<12}{'Moisture':<12}{'Days Since Fert.':<18}")
    print("-" * 52)
    for zone_name, info in zones.items():
        print(f"{zone_name:<10}{info['crop']:<12}{info['moisture']:<12}{info['days_since_fertilized']:<18}")


def print_irrigation_plan(plan):
    print("\n=== Irrigation Plan ===")
    if not plan:
        print("  All zones have sufficient moisture. No irrigation needed.")
        return
    print(f"{'Zone':<10}{'Duration':<14}{'Flow Rate':<10}")
    print("-" * 34)
    for zone_name, details in plan.items():
        print(f"{zone_name:<10}{str(details['duration']) + ' min':<14}{details['flow_rate']:<10}")


def print_fertilizer_plan(plan):
    print("\n=== Fertilizer Plan ===")
    if not plan:
        print("  No zones need fertilizer right now.")
        return
    print(f"{'Zone':<10}{'Amount':<12}{'Days Overdue':<14}")
    print("-" * 36)
    for zone_name, details in plan.items():
        print(f"{zone_name:<10}{str(details['amount_kg']) + ' kg':<12}{details['days_overdue']:<14}")


def print_cycle_summary(irrigation_plan, fertilizer_plan):
    total_minutes = sum(details["duration"] for details in irrigation_plan.values())
    total_fertilizer = sum(details["amount_kg"] for details in fertilizer_plan.values())
    print("\n=== Cycle Summary ===")
    print(f"  Zones irrigated: {len(irrigation_plan)} / {len(zones)}")
    print(f"  Total irrigation time: {total_minutes} minutes")
    print(f"  Zones fertilized: {len(fertilizer_plan)} / {len(zones)}")
    print(f"  Total fertilizer used: {total_fertilizer} kg")


def main():
    print("=== Irrigation Control Simulator ===")
    print(f"Moisture threshold: {MOISTURE_THRESHOLD}% (below this = irrigation needed)\n")

    simulate_sensor_readings()
    print_zone_status()

    irrigation_plan = build_irrigation_plan()
    fertilizer_plan = build_fertilizer_plan()

    print_irrigation_plan(irrigation_plan)
    print_fertilizer_plan(fertilizer_plan)
    print_cycle_summary(irrigation_plan, fertilizer_plan)


if __name__ == "__main__":
    main()
