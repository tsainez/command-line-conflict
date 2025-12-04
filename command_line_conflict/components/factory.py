
class Factory:
    """Component that defines a factory's production capability.

    Attributes:
        input_unit (str): The name of the unit type required as input (e.g., 'chassis').
        output_unit (str): The name of the unit type produced (e.g., 'rover').
    """

    def __init__(self, input_unit: str, output_unit: str):
        self.input_unit = input_unit
        self.output_unit = output_unit
