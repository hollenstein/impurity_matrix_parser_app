from IPython.display import display
from ipywidgets import widgets

from .layout import (
    create_input_area,
    create_example_input_button,
    create_process_input_button,
)
from .managers import InputManager, OutputManager
from .process_vendor_matrix import parse_thermo_matrix, transform_into_diagonal_matrix

EXAMPLE_INPUT = """
TMTpro-126 126.127726 N/A N/A N/A N/A 100% 0.31% 9.09%
(127C)
0.02% 0.32%
""".strip()


def start_app():
    # Prepare buttons
    input_manager = InputManager()
    input_manager.add_processing_function(parse_thermo_matrix)
    input_manager.add_diagonal_conversion_function(transform_into_diagonal_matrix)
    output_manager = OutputManager()

    input_text_area = create_input_area(input_manager)
    example_input_button = create_example_input_button(
        input_manager, example_input=EXAMPLE_INPUT
    )
    process_input_button = create_process_input_button(input_manager, output_manager)

    # Generate layout
    preview_area = widgets.VBox([example_input_button, process_input_button])
    input_and_process_area = widgets.HBox([input_text_area, preview_area])

    # Display all buttons, fields, and output
    display(input_and_process_area, output_manager.output_widget)
