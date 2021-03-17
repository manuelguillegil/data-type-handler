class Struct:
    def __init__(self, name, elements, representation= None, alignment = None, elements_packed = None, elements_unpacked = None, elements_optimized = None, waste = None):
        self.name = name
        self.elements = elements
        self.representation = representation
        self.alignment = alignment
        self.waste = waste
        self.elements_packed = elements_packed
        self.elements_unpacked = elements_unpacked
        self.elements_optimized = elements_optimized