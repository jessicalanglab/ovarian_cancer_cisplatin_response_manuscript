from enum import Enum
import biomart
import pandas as pd
import gzip
import sklearn.metrics as metrics
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Change path as necessary
full_path_to_reference_folder = "/Volumes/kueck/PublicDataAnalysis/CASCAM_style_subtype_classification/data/reference"

class Subtype(Enum):
    HGSC = "high_grade_serous_carcinoma"
    LGSC = "low_grade_serous_carcinoma"
    EC = "endometrioid_carcinoma"
    CCC = "clear_cell_carcinoma"
    MC = "mucinous_carcinoma"


subtype_dict = {
    Subtype.HGSC: 1,
    Subtype.LGSC: 2,
    Subtype.EC: 3,
    Subtype.CCC: 4,
    Subtype.MC: 5,
}


def convert_subtype_to_int(subtype):
    if type(subtype) == str:
        subtype = getattr(Subtype, subtype)
    return subtype_dict[subtype]


def convert_int_to_subtype(subtype_int):
    for subtype, value in subtype_dict.items():
        if value == subtype_int:
            return subtype
    raise ValueError(f"Invalid subtype_int: {subtype_int}")


# Example of how to use Subtype
# print(f"Subtype.HGSC: {Subtype.HGSC}")
# print(f"Subtype.HGSC.value: {Subtype.HGSC.value}")
# print(f"Subtype.HGSC.name: {Subtype.HGSC.name}")


# This code adapted from https://gist.github.com/ben-heil/cffbebf8865795fe2efbbfec041da969
def get_ensembl_mappings_grch38():
    grch38_mappings_path = f"{full_path_to_reference_folder}/ensembl_gene_symbol_mappings_grch38.pkl"
    
    # Check if we have the mappings saved
    try:
        ensembl_to_genesymbol = pd.read_pickle(grch38_mappings_path)
        return ensembl_to_genesymbol
    except FileNotFoundError:
        print("No saved mappings found. Fetching from biomart...")
    
    # Set up connection to server
    server = biomart.BiomartServer("http://www.ensembl.org/biomart")
    mart = server.datasets["hsapiens_gene_ensembl"]

    # List the types of data we want
    attributes = ["ensembl_gene_id", "external_gene_name"]

    # Get the mapping between the attributes
    response = mart.search({"attributes": attributes})
    data = response.raw.data.decode("ascii")

    ensembl_to_genesymbol = pd.DataFrame(
        columns=["ensembl_gene_id", "external_gene_name"]
    )
    num_skipped = 0
    # Store the data in a dict
    for line in data.splitlines():
        line = line.split("\t")
        # The entries are in the same order as in the `attributes` variable
        ensembl_gene = line[0]
        gene_symbol = line[1]

        if len(gene_symbol) == 0:
            num_skipped += 1
            continue
        # Add to data frame
        ensembl_to_genesymbol.loc[len(ensembl_to_genesymbol)] = [
            ensembl_gene,
            gene_symbol,
        ]
    print(f"Skipped {num_skipped} entries because they were missing gene_symbol")
    
    # Save the mappings
    ensembl_to_genesymbol.to_pickle(grch38_mappings_path)
    
    return ensembl_to_genesymbol


# This code adapted from https://gist.github.com/ben-heil/cffbebf8865795fe2efbbfec041da969
def get_ensembl_mappings_grch37():
    grch37_mappings_path = f"{full_path_to_reference_folder}/ensembl_gene_symbol_mappings_grch37.pkl"
    
    # Check if we have the mappings saved
    try:
        ensembl_to_genesymbol = pd.read_pickle(grch37_mappings_path)
        return ensembl_to_genesymbol
    except FileNotFoundError:
        print("No saved mappings found. Fetching from biomart...")

    # Set up connection to server
    server = biomart.BiomartServer("http://grch37.ensembl.org/biomart")
    mart = server.datasets["hsapiens_gene_ensembl"]

    # List the types of data we want
    attributes = ["ensembl_gene_id", "external_gene_name"]

    # Get the mapping between the attributes
    response = mart.search({"attributes": attributes})
    with gzip.GzipFile(fileobj=response.raw, mode="rb") as f:
        data = f.read().decode("utf-8")

    ensembl_to_genesymbol = pd.DataFrame(
        columns=["ensembl_gene_id", "external_gene_name"]
    )
    num_skipped = 0
    # Store the data in a dict
    for line in data.splitlines():
        line = line.split("\t")
        # The entries are in the same order as in the `attributes` variable
        ensembl_gene = line[0]
        gene_symbol = line[1]

        if len(gene_symbol) == 0:
            num_skipped += 1
            continue
        # Add to data frame
        ensembl_to_genesymbol.loc[len(ensembl_to_genesymbol)] = [
            ensembl_gene,
            gene_symbol,
        ]
    print(f"Skipped {num_skipped} entries because they were missing gene_symbol")

    # Save the mappings
    ensembl_to_genesymbol.to_pickle(grch37_mappings_path)

    return ensembl_to_genesymbol


# ensembl_to_gene_symbol_df_grch37 = get_ensembl_mappings_grch37()
# print(ensembl_to_gene_symbol_df_grch37)


# Computes evaluation metrics and displays metrics and confusion matrix
def evaluate_predictions(y_test, y_pred, possible_labels):
    if type(y_test) != np.ndarray:
        y_test = np.array(y_test)
    if type(y_pred) != np.ndarray:
        y_pred = np.array(y_pred)
    # test_df = pd.DataFrame({"Predicted": y_pred, "Actual": y_test})
    # display(test_df)

    # Compute metrics
    metrics_df = pd.DataFrame(
        columns=["Precision", "Recall", "F1", "Accuracy", "Num_in_test_set"]
    )

    precision = metrics.precision_score(
        y_test, y_pred, average="weighted"
    )  # TODO: should we use weighted/macro/micro for averaging?
    recall = metrics.recall_score(y_test, y_pred, average="weighted")
    f1 = metrics.f1_score(y_test, y_pred, average="weighted")
    accuracy = metrics.accuracy_score(y_test, y_pred)
    metrics_df.loc["Overall (weighted)"] = [
        precision,
        recall,
        f1,
        accuracy,
        len(y_test),
    ]

    # Compute metrics per label
    for label in possible_labels:
        subset_indices = y_test == label
        subset_test = np.array(y_test[subset_indices])
        subset_pred = np.array(y_pred[subset_indices])
        if len(subset_test) == 0:
            continue
        if len(subset_pred) == 0:
            continue

        precision = metrics.precision_score(
            subset_test, subset_pred, average="weighted"
        )
        recall = metrics.recall_score(subset_test, subset_pred, average="weighted")
        f1 = metrics.f1_score(subset_test, subset_pred, average="weighted")
        accuracy = metrics.accuracy_score(
            subset_test,
            subset_pred,
        )
        metrics_df.loc[label] = [precision, recall, f1, accuracy, len(subset_test)]

    # Display metrics
    display(metrics_df)

    # Confusion matrix
    confusion_matrix = metrics.confusion_matrix(y_test, y_pred, labels=possible_labels)
    # display(pd.DataFrame(confusion_matrix,
    #                      columns=[f"Predicted {i}" for i in CancerType.__members__.keys()],
    #                      index=[f"Actual {i}" for i in CancerType.__members__.keys()]))
    plt.figure(figsize=(20, 15))
    sns.heatmap(
        confusion_matrix, annot=True, cmap="Blues", fmt="g", annot_kws={"size": 7}
    )
    plt.xticks(np.arange(len(possible_labels)) + 0.5, possible_labels)
    plt.yticks(np.arange(len(possible_labels)) + 0.5, possible_labels, rotation=0)
    plt.xlabel("Predicted Label")
    plt.ylabel("Actual Label")
    plt.title("Confusion Matrix")
    plt.show()


# # Test evaluation function
# possible_labels = ["HGSC", "LGSC", "EC", "CCC", "MC"]
# y_test = np.array(
#     [
#         "HGSC",
#         "HGSC",
#         "LGSC",
#         "HGSC",
#         "LGSC",
#         "HGSC",
#         "HGSC",
#         "EC",
#         "CCC",
#         "HGSC",
#         "HGSC",
#         "HGSC",
#         "CCC",
#         "HGSC",
#         "HGSC",
#         "HGSC",
#         "HGSC",
#         "HGSC",
#         "HGSC",
#         "HGSC",
#         "HGSC",
#         "HGSC",
#         "HGSC",
#         "CCC",
#         "HGSC",
#         "HGSC",
#         "EC",
#         "HGSC",
#         "HGSC",
#         "EC",
#         "CCC",
#         "HGSC",
#         "HGSC",
#         "HGSC",
#         "HGSC",
#         "HGSC",
#         "CCC",
#         "HGSC",
#         "HGSC",
#         "HGSC",
#         "HGSC",
#         "HGSC",
#         "HGSC",
#         "HGSC",
#         "HGSC",
#         "HGSC",
#         "HGSC",
#         "HGSC",
#         "HGSC",
#         "CCC",
#         "HGSC",
#         "HGSC",
#         "HGSC",
#         "HGSC",
#         "HGSC",
#         "HGSC",
#         "MC",
#         "HGSC",
#         "HGSC",
#         "HGSC",
#         "CCC",
#         "HGSC",
#         "HGSC",
#         "HGSC",
#         "MC",
#         "HGSC",
#         "HGSC",
#         "CCC",
#         "CCC",
#         "HGSC",
#         "HGSC",
#         "HGSC",
#     ]
# )
# y_pred = np.array(
#     [
#         "HGSC",
#         "HGSC",
#         "HGSC",
#         "HGSC",
#         "HGSC",
#         "HGSC",
#         "HGSC",
#         "HGSC",
#         "HGSC",
#         "HGSC",
#         "HGSC",
#         "HGSC",
#         "CCC",
#         "HGSC",
#         "HGSC",
#         "CCC",
#         "HGSC",
#         "HGSC",
#         "HGSC",
#         "CCC",
#         "HGSC",
#         "HGSC",
#         "HGSC",
#         "HGSC",
#         "HGSC",
#         "HGSC",
#         "HGSC",
#         "HGSC",
#         "HGSC",
#         "HGSC",
#         "HGSC",
#         "HGSC",
#         "HGSC",
#         "HGSC",
#         "HGSC",
#         "HGSC",
#         "CCC",
#         "HGSC",
#         "HGSC",
#         "HGSC",
#         "HGSC",
#         "HGSC",
#         "HGSC",
#         "HGSC",
#         "HGSC",
#         "HGSC",
#         "HGSC",
#         "HGSC",
#         "HGSC",
#         "HGSC",
#         "HGSC",
#         "HGSC",
#         "HGSC",
#         "HGSC",
#         "HGSC",
#         "HGSC",
#         "CCC",
#         "HGSC",
#         "HGSC",
#         "HGSC",
#         "HGSC",
#         "HGSC",
#         "HGSC",
#         "HGSC",
#         "HGSC",
#         "HGSC",
#         "HGSC",
#         "CCC",
#         "CCC",
#         "HGSC",
#         "HGSC",
#         "HGSC",
#     ]
# )
# evaluate_predictions(y_test, y_pred, possible_labels)
