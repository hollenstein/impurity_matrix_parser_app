from ipywidgets import widgets
import base64

import pandas as pd


def create_input_area(
    input_manager,
    description="Isotope Impurity:",
    placeholder="Paste copied reporter isotope impurity text here.",
):
    input_text_area = widgets.Textarea(
        value="",
        placeholder=placeholder,
        description=description,
        disabled=False,
        style={"description_width": "100px", "text-align": "left"},
    )
    input_manager.connect_to_input(input_text_area)
    return input_text_area


def create_example_input_button(
    input_manager, description="Example input", example_input=""
):
    def on_button_clicked(_):
        input_manager.set_input(example_input)

    example_input_button = widgets.Button(
        description=description,
        tooltip="Click to fill the input area with an example input",
    )
    example_input_button.on_click(on_button_clicked)
    return example_input_button


def create_process_input_button(
    input_manager, output_manager, description="Process matrix"
):
    def on_button_clicked(_):
        impurity_matrix = input_manager.process_input()
        diagonal_matrix = pd.DataFrame(input_manager.create_diagonal_matrix())
        if impurity_matrix is not None:
            full_matrix_as_tsv = impurity_matrix.fillna(0).to_csv(
                index=True, header=True, sep="\t"
            )
            diagonal_matrix_as_tsv = diagonal_matrix.to_csv(
                index=False, header=False, sep="\t"
            )

            download_label = widgets.Label(value="Download data as TSV file:")
            download_button_1 = create_download_tsv_button_widget(
                full_matrix_as_tsv,
                text="Impurity Table",
                tooltip="Press to download the displayed table as TSV file.",
                filename="impurity_matrix.tsv",
            )
            download_button_2 = create_download_tsv_button_widget(
                diagonal_matrix_as_tsv,
                text="Diagonal Matrix",
                tooltip="Press to download a diagonal matrix as TSV file.",
                filename="diagonal_impurity_matrix.tsv",
            )

            hbox = widgets.HBox([download_label, download_button_1, download_button_2])
            output_manager.display_multiple_items([hbox, impurity_matrix])
        else:
            output_manager.display("Empty matrix")

    preview_button = widgets.Button(description=description)
    preview_button.on_click(on_button_clicked)
    return preview_button


def create_download_tsv_button_widget(
    tsv_as_string,
    text="Download TSV",
    filename="data.tsv",
    tooltip="Press to download a TSV file",
):
    """Creates a download button widget for a TSV file.

    Args:
        tsv_as_string: The TSV table as a string
        text: The text to display on the button
        filename: The filename to use when downloading the TSV file
        tooltip: The tooltip to display when hovering over the button
    """
    # Convert the DataFrame to a TSV file in memory
    b64 = base64.b64encode(tsv_as_string.encode())
    payload = b64.decode()

    # Define CSS styles for the button
    button_styles = """
    <style>
        .download-button {
            background-color: #007BFF; /* Button background color */
            color: #fff; /* Text color */
            padding: 10px 20px; /* Padding inside the button */
            border: none;
            border-radius: 5px; /* Rounded edges */
            cursor: pointer;
            font-size: 12px; /* Font size */
        }
        .download-button:hover {
            background-color: #0056b3; /* Hover background color */
        }
    </style>
    """

    # Generate HTML for the download button with CSS styles
    button_html = f"""
    <html>
    <head>
        {button_styles}
    </head>
    <body>
        <a href="data:text/csv;base64,{payload}" download="{filename}">
            <button class="download-button", title="{tooltip}">{text}</button>
        </a>
    </body>
    </html>
    """
    return widgets.HTML(button_html)
