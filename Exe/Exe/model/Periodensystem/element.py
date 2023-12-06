#Diese Klasse dient dazu um aus der JSON nur die für uns benötigten Daten abzuspeichern.
class Element():

    def __str__(self) -> str:
        return "Name: " + self.name + " Nummer: " + str(self.number)
    
    def __repr__(self) -> str:
        return "Name: " + self.name + " Nummer: " + str(self.number)

    def __init__(self, name , atomic_mass, density, number, symbol, electronegativity) -> None:
        
        self.name = name
        self.atomic_mass = atomic_mass
        self.density = density
        self.number = number
        self.symbol = symbol
        self.electronegativity = electronegativity

