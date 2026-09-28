import numpy as np
import pandas as pd


SHIFT_HOURS = 8
SHIFT_MINUTES = SHIFT_HOURS * 60


def create_production_line():

    return pd.DataFrame({
        "Station": [
            "Cutting",
            "Drilling",
            "Assembly",
            "Inspection",
            "Packaging"
        ],

        "Cycle_Time_sec": [
            55,
            72,
            95,
            65,
            50
        ],

        "Operators": [
            1,
            1,
            2,
            1,
            1
        ],

        "Availability": [
            0.96,
            0.91,
            0.94,
            0.98,
            0.97
        ],

        "Defect_Rate": [
            0.015,
            0.025,
            0.030,
            0.010,
            0.005
        ]
    })


def calculate_capacity(stations):

    results = stations.copy()

    results["Available_Minutes"] = (
        SHIFT_MINUTES *
        results["Availability"]
    )

    cycle_minutes = (
        results["Cycle_Time_sec"] / 60
    )

    results["Capacity"] = (
        results["Available_Minutes"]
        / cycle_minutes
        * results["Operators"]
    )

    return results


def simulate_production(
    stations,
    simulations=1000
):

    output_results = []

    for _ in range(simulations):

        station_capacities = []

        for _, station in stations.iterrows():

            availability = np.random.normal(
                station["Availability"],
                0.015
            )

            availability = np.clip(
                availability,
                0.70,
                1.0
            )

            cycle_time = np.random.normal(
                station["Cycle_Time_sec"],
                station["Cycle_Time_sec"] * 0.05
            )

            available_minutes = (
                SHIFT_MINUTES *
                availability
            )

            capacity = (
                available_minutes
                / (cycle_time / 60)
                * station["Operators"]
            )

            station_capacities.append(
                capacity
            )

        line_capacity = min(
            station_capacities
        )

        overall_yield = np.prod(
            1 - stations["Defect_Rate"]
        )

        finished_units = (
            line_capacity *
            overall_yield
        )

        output_results.append(
            finished_units
        )

    return np.array(output_results)
