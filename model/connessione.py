from dataclasses import dataclass

@dataclass
class Connessione:
    v1:int
    v2:int
    peso:int


    def __str__(self):
        return f"{self.v1} - {self.v2}"