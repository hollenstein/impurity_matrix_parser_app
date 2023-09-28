from itertools import chain, repeat
from typing import Optional

import numpy as np
import pandas as pd


COLUMNS_TMT_KITS = {
    "tmt_16plex": [
        "Mass Tag",
        "Reporter Ion Mass",
        "-2x 13C",
        "-13C -15N",
        "-13C",
        "-15N",
        "0",
        "+15N",
        "+13C",
        "+15N +13C",
        "+2x 13C",
    ],
    "tmt_10plex": [
        "Mass Tag",
        "Reporter Ion Mass",
        "-2",
        "-1",
        "0",
        "+1",
        "+2",
    ],
    "tmt_6plex": [
        "Mass Tag",
        "Mass Reporter",
        "Reporter Ion Mass",
        "-2",
        "-1",
        "0",
        "+1",
        "+2",
    ],
}

INDEX_COLUMN_NUM_TMT_KITS = {
    "tmt_16plex": 2,
    "tmt_10plex": 2,
    "tmt_6plex": 3,
}


def parse_thermo_matrix(text):
    values = split_thermo_text_into_values(text)
    nrows, ncols = calculate_tmt_matrix_shape(values)

    # So far the isotope impurity matrix from each Thermo TMT kit has different column
    # number that can be used to guess which one is parsed.
    column_num_mapping = {len(cols): name for name, cols in COLUMNS_TMT_KITS.items()}
    tmt_kit_name = column_num_mapping[ncols]
    matrix_columns = COLUMNS_TMT_KITS[tmt_kit_name]
    index_column_num = INDEX_COLUMN_NUM_TMT_KITS[tmt_kit_name]
    index_columns = matrix_columns[0:index_column_num]

    # columns = ["Mass Tag", "Reporter Ion Mass"] + [str(i) for i in range(ncols - 2)]
    matrix = convert_thermo_values_to_dataframe(values, matrix_columns, index_columns)
    return matrix


def split_thermo_text_into_values(text):
    nested_values = [entry.split(" ") for entry in text.split("\n")]
    values = [
        i for i in chain.from_iterable(nested_values) if i and not i.startswith("(")
    ]
    return values


def calculate_tmt_matrix_shape(values):
    # So far the isotope impurity matrix from each Thermo TMT kit has one column with
    # entries that start with "TMT", this can be used to calculate the number of rows.
    num_rows = sum(["tmt" in value.lower() for value in values])
    num_values = len(values)
    num_columns = num_values // num_rows
    return num_rows, num_columns


def convert_thermo_values_to_dataframe(values, columns, index_columns):
    chunk_size = len(columns)
    impurity_matrix = pd.DataFrame(
        divide_into_chunks(values, chunk_size), columns=columns
    )
    impurity_matrix = impurity_matrix.set_index(index_columns)
    impurity_matrix = impurity_matrix.astype(str)
    impurity_matrix = impurity_matrix.map(lambda s: s.replace("%", ""))
    impurity_matrix = impurity_matrix.replace("N/A", None)
    impurity_matrix = impurity_matrix.astype(float)
    return impurity_matrix


def divide_into_chunks(iterable, chunk_size):
    """Devide an interable into a list of sub lists with length chunk_size."""
    chunks = []
    for i in range(0, len(iterable), chunk_size):
        chunks.append(iterable[i : i + chunk_size])
    return chunks


def transform_into_diagonal_matrix(
    matrix: np.array, center: Optional[int] = None
) -> np.array:
    """Transforms a reporter isotope impurity matrix into a diagonal format.

    Args:
        matrix: A two-dimensional reporter isotope impurity matrix where rows correspond
            to the individual reporter channels and columns indicate the percentage of
            isotope contamination of each reporter channel into its neighboring
            channels.
        center_column: Optional, specify the column position that contains the
            percentage of signal that a reporter contributes to its own channel. Note
            that column positions are zero-indexed. By default, the central column of
            the input matrix is used.

    Returns:
        Returns a reporter isotope impurity matrix in a diagonal format. Each row
        corresponds to a reporter's theoretical isotope distribution, describing its
        contamination into neighboring channels. Columns correspond to the observed
        signal of a specific reporter channel, with values indicating contamination
        from neighboring channels. The returned numpy array is square with rows and
        columns corresponding to the number of rows from the input matrix. The diagonal
        elements represent the reporter's contribution to its own channel.
    """
    center = center if center is not None else matrix.shape[1] // 2
    pre_channels = center
    post_channels = matrix.shape[1] - (center + 1)

    transformed_matrix = list()
    last_row_position = len(matrix) - 1
    for row_position, row_values in enumerate(matrix):
        pre_padding = repeat(0.0, row_position)
        post_padding = repeat(0.0, last_row_position - row_position)
        new_row = list(chain(pre_padding, row_values, post_padding))
        transformed_matrix.append(new_row[pre_channels:-post_channels])

    return np.array(transformed_matrix)
