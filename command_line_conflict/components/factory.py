class Factory:
    """Component that defines a factory's production capability.

    Attributes:
        input_unit (str): The name of the unit type required as input (e.g., 'chassis').
        output_unit (str): The name of the unit type produced (e.g., 'rover').
    """

    def __init__(self, input_unit: str, output_unit: str):
        VALID_UNITS = {"chassis", "rover", "arachnotron", "observer", "immortal", "extractor"}
        if input_unit not in VALID_UNITS:
            raise ValueError(f"Invalid input_unit: {input_unit}")
        if output_unit not in VALID_UNITS:
            raise ValueError(f"Invalid output_unit: {output_unit}")
        self.input_unit = input_unit
        self.output_unit = output_unit
