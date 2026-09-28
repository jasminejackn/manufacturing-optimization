import numpy as np


def identify_bottleneck(capacity_data):
    """
    Identify the station with the lowest production capacity.
    """

    index = capacity_data["Capacity"].idxmin()

    return capacity_data.loc[
        index,
        "Station"
    ]


def calculate_utilization(capacity_data):
    """
    Calculate workstation utilization.
    """

    results = capacity_data.copy()

    line_capacity = results["Capacity"].min()

    results["Utilization"] = (
        line_capacity /
        results["Capacity"]
    )

    return results


def calculate_yield(stations):
    """
    Calculate overall manufacturing yield.
    """

    yields = (
        1 - stations["Defect_Rate"]
    )

    return np.prod(yields)


def scenario_analysis(stations, calculate_capacity):
    """
    Compare different manufacturing improvement strategies.
    """

    scenarios = []

    # --------------------------------------------------------
    # Current system
    # --------------------------------------------------------

    current = stations.copy()

    result = calculate_capacity(current)

    scenarios.append({
        "Scenario": "Current System",
        "Throughput": result["Capacity"].min()
    })

    # --------------------------------------------------------
    # Add assembly operator
    # --------------------------------------------------------

    assembly = stations.copy()

    assembly.loc[
        assembly["Station"] == "Assembly",
        "Operators"
    ] = (
        assembly.loc[
            assembly["Station"] == "Assembly",
            "Operators"
        ] + 1
    )

    result = calculate_capacity(assembly)

    scenarios.append({
        "Scenario": "Add Assembly Operator",
        "Throughput": result["Capacity"].min()
    })

    # --------------------------------------------------------
    # Improve drilling cycle time by 20%
    # --------------------------------------------------------

    drilling = stations.copy()

    drilling["Cycle_Time_sec"] = (
        drilling["Cycle_Time_sec"]
        .astype(float)
    )

    drilling.loc[
        drilling["Station"] == "Drilling",
        "Cycle_Time_sec"
    ] = (
        drilling.loc[
            drilling["Station"] == "Drilling",
            "Cycle_Time_sec"
        ] * 0.80
    )

    result = calculate_capacity(drilling)

    scenarios.append({
        "Scenario": "Improve Drilling Cycle Time",
        "Throughput": result["Capacity"].min()
    })

    # --------------------------------------------------------
    # Improve assembly cycle time by 20%
    # --------------------------------------------------------

    assembly_fast = stations.copy()

    assembly_fast["Cycle_Time_sec"] = (
        assembly_fast["Cycle_Time_sec"]
        .astype(float)
    )

    assembly_fast.loc[
        assembly_fast["Station"] == "Assembly",
        "Cycle_Time_sec"
    ] = (
        assembly_fast.loc[
            assembly_fast["Station"] == "Assembly",
            "Cycle_Time_sec"
        ] * 0.80
    )

    result = calculate_capacity(assembly_fast)

    scenarios.append({
        "Scenario": "Improve Assembly Cycle Time",
        "Throughput": result["Capacity"].min()
    })

    # --------------------------------------------------------
    # Improve equipment availability
    # --------------------------------------------------------

    maintenance = stations.copy()

    maintenance["Availability"] = (
        maintenance["Availability"].astype(float)
    )

    maintenance["Availability"] = np.minimum(
        maintenance["Availability"] + 0.04,
        1.0
    )

    result = calculate_capacity(maintenance)

    scenarios.append({
        "Scenario": "Improve Equipment Availability",
        "Throughput": result["Capacity"].min()
    })

    return scenarios



def calculate_cost(
    throughput,
    operators=6,
    labor_cost_per_hour=25,
    material_cost_per_unit=12,
    defect_rate=0.03
):
    """
    Estimate manufacturing cost.
    """

    labor_cost = (
        operators *
        labor_cost_per_hour *
        8
    )

    material_cost = (
        throughput *
        material_cost_per_unit
    )

    scrap = (
        throughput *
        defect_rate
    )

    good_units = (
        throughput - scrap
    )

    total_cost = (
        labor_cost +
        material_cost
    )

    cost_per_good_unit = (
        total_cost /
        max(good_units, 1)
    )

    return {
        "Labor Cost": labor_cost,
        "Material Cost": material_cost,
        "Total Cost": total_cost,
        "Good Units": good_units,
        "Cost Per Good Unit": cost_per_good_unit
    }
