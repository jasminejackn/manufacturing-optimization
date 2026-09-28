import matplotlib.pyplot as plt


def create_dashboard(
    capacity_data,
    scenario_data,
    simulation_results
):
    """
    Create a manufacturing engineering dashboard.
    """

    fig, axes = plt.subplots(
        2,
        2,
        figsize=(14, 9)
    )

    # -----------------------------------------
    # Production capacity
    # -----------------------------------------

    axes[0, 0].bar(
        capacity_data["Station"],
        capacity_data["Capacity"],
        color="steelblue"
    )

    axes[0, 0].set_title(
        "Production Capacity by Station"
    )

    axes[0, 0].set_ylabel(
        "Units per Shift"
    )

    axes[0, 0].tick_params(
        axis="x",
        rotation=30
    )

    axes[0, 0].grid(
        axis="y",
        alpha=0.3
    )

    # -----------------------------------------
    # Utilization
    # -----------------------------------------

    axes[0, 1].bar(
        capacity_data["Station"],
        capacity_data["Utilization"] * 100,
        color="darkorange"
    )

    axes[0, 1].set_title(
        "Workstation Utilization"
    )

    axes[0, 1].set_ylabel(
        "Utilization (%)"
    )

    axes[0, 1].tick_params(
        axis="x",
        rotation=30
    )

    axes[0, 1].grid(
        axis="y",
        alpha=0.3
    )

    # -----------------------------------------
    # Improvement scenarios
    # -----------------------------------------

    scenario_names = [
        item["Scenario"]
        for item in scenario_data
    ]

    throughput = [
        item["Throughput"]
        for item in scenario_data
    ]

    axes[1, 0].bar(
        scenario_names,
        throughput,
        color="seagreen"
    )

    axes[1, 0].set_title(
        "Process Improvement Scenarios"
    )

    axes[1, 0].set_ylabel(
        "Units per Shift"
    )

    axes[1, 0].tick_params(
        axis="x",
        rotation=35
    )

    axes[1, 0].grid(
        axis="y",
        alpha=0.3
    )

    # -----------------------------------------
    # Monte Carlo simulation
    # -----------------------------------------

    axes[1, 1].hist(
        simulation_results,
        bins=30,
        color="purple",
        alpha=0.75
    )

    axes[1, 1].axvline(
        simulation_results.mean(),
        color="red",
        linestyle="--",
        label="Average"
    )

    axes[1, 1].set_title(
        "Production Throughput Distribution"
    )

    axes[1, 1].set_xlabel(
        "Units per Shift"
    )

    axes[1, 1].set_ylabel(
        "Frequency"
    )

    axes[1, 1].legend()

    plt.tight_layout()

    plt.savefig(
        "results/manufacturing_analysis.png",
        dpi=300
    )

    plt.show()
