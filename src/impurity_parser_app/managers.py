from ipywidgets import widgets
from IPython.display import display
from typing import Protocol, Callable


class InputField(Protocol):
    value: str


class InputManager:
    def __init__(self):
        self.input_field = None
        self.processing_function = None

    def connect_to_input(self, input_field: InputField):
        self.input_field = input_field

    def add_processing_function(self, processing_function: Callable):
        self.processing_function = processing_function

    def add_diagonal_conversion_function(self, convert_to_diagonal: Callable):
        self.convert_to_diagonal_function = convert_to_diagonal

    def process_input(self):
        try:
            processed_input = self.processing_function(self.get_input())
        except ZeroDivisionError:
            processed_input = None
        return processed_input

    def create_diagonal_matrix(self):
        try:
            processed_input = self.processing_function(self.get_input())
            diagonal_matrix = self.convert_to_diagonal_function(
                processed_input.fillna(0).to_numpy()
            )
        except ZeroDivisionError:
            diagonal_matrix = None
        return diagonal_matrix

    def get_input(self):
        return self.input_field.value

    def set_input(self, text):
        self.input_field.value = text


class OutputManager:
    def __init__(self):
        self.output_widget = widgets.Output()

    def display(self, content):
        with self.output_widget:
            self.output_widget.clear_output(wait=True)
            display(content)

    def display_multiple_items(self, contents):
        with self.output_widget:
            self.output_widget.clear_output(wait=True)
            for content in contents:
                display(content)
