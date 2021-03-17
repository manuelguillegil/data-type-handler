class Atomic:
    def __init__(self, name, representation, alignment):
        self.name = name
        self.representation = representation
        self.alignment = alignment

    def __str__(self):
        return "Atómico de nombre: " + self.name + ". Rep: " + str(self.representation) + " Alin: " + str(self.alignment)