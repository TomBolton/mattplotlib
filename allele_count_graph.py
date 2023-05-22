"""
Guidance from Matt:
    Sample: Individuals

    Genotype: What DNA sequence they have. Everyone one has 2 copies of their genes, if they
    are the same we call this Homozygous (Hom), if different they are heterozygous (het).

    I am looking at a single sequence change, and so a homozygous can either have:
     - `het` the common sequence on one copy, and the alternate sequence on the other
     - `hom_ref` reference sequence on both copies
     - `hom_alt` the alternate sequence on both copies

    Allele 1/2 count: How much activity is coming off of each copy of the gene.

    I want it plotted as follows:
    - First divided by the Genotype
    - Then I want 2 parallel sets of data with the allele counts, and most importantly a line connecting the 2 counts originating
    from the same donor.

    Extra reading: I want to show that the sequence change is causing a change in expression,
    and so if an individual has 2 low expressing copies, both should be low, if they have 2 high
    expressing copies, both should be high, but if they have 1 copy of each I want to show that
    these individuals have 1 high and 1 low. I have 50 data points, with varying genotypes.
"""

import argparse
import json

import matplotlib.pyplot as plt


GENOTYPES = ['hom_ref', 'het', 'hom_alt']

GENOTYPE_SPACING = 2

GENOTYPE_COLOURS = {
    "hom_ref": "blue",
    "het": "orange",
    "hom_alt": "red"
}

GENOTYPE_LABELS = {
    "hom_ref": "Homozygous\nreference",
    "het": "Heterozygous",
    "hom_alt": "Homozygous\nalternate",
}

ALLELE_MARKERS = {
    "allele_1": "o",
    "allele_2": "x"
}

EXAMPLE_DATA = {
    "1": {"genotype": "hom_ref", "allele_1_count": 2, "allele_2_count": 4},
    "2": {"genotype": "hom_ref", "allele_1_count": 3, "allele_2_count": 6},
    "3": {"genotype": "het", "allele_1_count": 4, "allele_2_count": 40},
    "4": {"genotype": "het", "allele_1_count": 5, "allele_2_count": 39},
    "5": {"genotype": "hom_alt", "allele_1_count": 60, "allele_2_count": 54},
    "6": {"genotype": "hom_alt", "allele_1_count": 58, "allele_2_count": 62},
}


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--input-json", type=str)
    parser.add_argument("--save-plot", action="store_true")

    return parser.parse_args()


def read_data(path_to_json):
    if path_to_json is None:
        return EXAMPLE_DATA
    else:
        with open(path_to_json, "r") as f:
            return json.load(f)


def create_plot(counts):
    plt.figure(figsize=(10, 10))

    # First divide by genotype
    data_by_genotype = {
        genotype: [counts[sample] for sample in counts if counts[sample]["genotype"] == genotype]
        for genotype in GENOTYPES
    }

    # On the x-axis we want the genotype, and then on the y-axis we want the allele counts. Within each genotype
    # we want to plot the allele counts for each sample, and then connect the 2 points for each sample.
    for i, genotype in enumerate(GENOTYPES):
        # Get the data for this genotype
        data = data_by_genotype[genotype]

        x_1 = [i * GENOTYPE_SPACING - 0.5] * len(data)
        x_2 = [i * GENOTYPE_SPACING + 0.5] * len(data)

        y_1 = [sample["allele_1_count"] for sample in data]
        y_2 = [sample["allele_2_count"] for sample in data]

        # Plot the data
        plt.scatter(x_1, y_1, color=GENOTYPE_COLOURS[genotype], marker=ALLELE_MARKERS["allele_1"], s=100)
        plt.scatter(x_2, y_2, color=GENOTYPE_COLOURS[genotype], marker=ALLELE_MARKERS["allele_2"], s=100)

        # Connect the points
        for x1, x2, y1, y2 in zip(x_1, x_2, y_1, y_2):
            plt.plot([x1, x2], [y1, y2], color=GENOTYPE_COLOURS[genotype])

    # Add a legend to show that the different marker symbols
    # correspond to different alleles
    plt.legend(
        [plt.scatter([], [], color="black", marker=marker, s=100) for marker in ALLELE_MARKERS.values()],
        ["Allele 1", "Allele 2"],
        loc="upper left",
        fontsize=14,
    )

    # Find the max value and use it to set the y-axis limits
    max_value = max(*[max([sample["allele_1_count"], sample["allele_2_count"]] for sample in counts.values())])
    plt.ylim(0, max_value + 10)

    # Add the genotype labels, with the font colour matching the genotype colour
    for i, genotype in enumerate(GENOTYPES):
        plt.text(
            i * GENOTYPE_SPACING, -1,
            GENOTYPE_LABELS[genotype],
            color=GENOTYPE_COLOURS[genotype],
            ha="center",
            va="top",
            fontsize=10,
            fontweight="bold",
        )

    # Make the plot pretty
    plt.xlabel("Genotype", fontsize=14, labelpad=30)
    plt.ylabel("Allele Count", fontsize=14)
    plt.title("Allele Counts by Genotype", fontsize=20)

    # Remove x-axis ticks and labels
    plt.gca().set_xticks([])
    plt.gca().set_xticklabels([])

    # Remove the top and right spines
    plt.gca().spines["top"].set_visible(False)
    plt.gca().spines["right"].set_visible(False)

    # Make plot background grey
    plt.gca().set_facecolor("#EAEAF2")

    # Set both x and y grid lines to be white
    plt.grid(color="white")


if __name__ == "__main__":
    args = parse_args()

    allele_counts = read_data(args.input_json)

    create_plot(allele_counts)

    if args.save_plot:
        plt.savefig("allele_count_graph.png", dpi=300)
