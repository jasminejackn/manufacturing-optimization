from simulation import (
    create_production_line,
    calculate_capacity,
    simulate_production
)

from analysis import (
    identify_bottleneck,
    calculate_utilization,
    calculate_yield,
    scenario_analysis,
    calculate_cost
)

from visualization import (
    create_dashboard
)


def main():

    print("\n")
    print("=" * 65)
    print("       MANUFACTURING PROCESS OPTIMIZATION")
    print("=" * 65)

    # -----------------------------------------
    # Create production line
    # -----------------------------------------

    stations = create_production_line()

    # -----------------------------------------
    # Calculate capacity
    # -----------------------------------------

    capacity_data = calculate_capacity(
        stations
    )

    capacity_data = calculate_utilization(
        capacity_data
    )

    # -----------------------------------------
    # Identify bottleneck
    # -----------------------------------------

    bottleneck = identify_bottleneck(
        capacity_data
    )

    # -----------------------------------------
    # Calculate quality
    # -----------------------------------------

    overall_yield = calculate_yield(
        stations
    )

    # -----------------------------------------
    # Monte Carlo simulation
    # -----------------------------------------

    simulation_results = simulate_production(
        stations,
        simulations=1000
    )

    # -----------------------------------------
    # Improvement scenarios
    # -----------------------------------------

    scenarios = scenario_analysis(
        stations,
        calculate_capacity
    )

    # -----------------------------------------
    # Display analysis
    # -----------------------------------------

    print("\nPRODUCTION LINE")

    print(
        capacity_data[
            [
                "Station",
                "Cycle_Time_sec",
                "Operators",
                "Availability",
                "Capacity",
                "Utilization"
            ]
        ].to_string(
            index=False
        )
    )

    print("\n")
    print(f"Bottleneck: {bottleneck}")

    print(
        f"Overall Yield: "
        f"{overall_yield * 100:.2f}%"
    )

    print(
        f"Average Simulated Output: "
        f"{simulation_results.mean():.1f} units/shift"
    )

    print(
        f"10th Percentile Output: "
        f"{__import__('numpy').percentile(simulation_results, 10):.1f}"
    )

    print(
        f"90th Percentile Output: "
        f"{__import__('numpy').percentile(simulation_results, 90):.1f}"
    )

    # -----------------------------------------
    # Improvement scenarios
    # -----------------------------------------

    print("\nIMPROVEMENT SCENARIOS")

    baseline = scenarios[0]["Throughput"]

    for scenario in scenarios:

        improvement = (
            scenario["Throughput"] /
            baseline - 1
        ) * 100

        print(
            f"{scenario['Scenario']:35}"
            f"{scenario['Throughput']:8.1f} units"
            f" ({improvement:+.1f}%)"
        )

    # -----------------------------------------
    # Cost analysis
    # -----------------------------------------

    average_output = (
        simulation_results.mean()
    )

    costs = calculate_cost(
        average_output
    )

    print("\nCOST ANALYSIS")

    print(
        f"Labor Cost: "
        f"${costs['Labor Cost']:.2f}"
    )

    print(
        f"Material Cost: "
        f"${costs['Material Cost']:.2f}"
    )

    print(
        f"Total Cost: "
        f"${costs['Total Cost']:.2f}"
    )

    print(
        f"Cost per Good Unit: "
        f"${costs['Cost Per Good Unit']:.2f}"
    )

    # -----------------------------------------
    # Save data
    # -----------------------------------------

    capacity_data.to_csv(
        "results/station_analysis.csv",
        index=False
    )

    # -----------------------------------------
    # Dashboard
    # -----------------------------------------

    create_dashboard(
        capacity_data,
        scenarios,
        simulation_results
    )

    print("\n")
    print("Analysis complete!")
    print(
        "Results saved in the 'results' folder."
    )


if __name__ == "__main__":
    main()
