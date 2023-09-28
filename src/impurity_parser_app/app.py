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
TMT6-126
126
126.127726
0.0%
0.0%
100%
8.3%
0.3%
TMT6-127
127N
127.124761
0.0%
0.1%
100%
7.8%
0.1%
TMT6-128
128C
128.134436
0.0%
1.5%
100%
6.2%
0.2%
TMT6-129
129N
129.131471
0.0%
1.5%
100%
5.7%
0.1%
TMT6-130
130C
130.141145
0.0%
3.1%
100%
3.6%
0.0%
TMT6-131
131
131.138180
0.1%
2.9%
100%
3.8%
0.0%
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
