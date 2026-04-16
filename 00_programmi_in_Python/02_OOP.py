from abc import ABC, abstractmethod

# 1. ESEMPIO DI CLASSE
class Persona(ABC):
    def __init__(self, nome, eta):
        self._nome = nome # 2. ESEMPIO DI INCAPSULAMENTO (SETTER)
        self.eta = eta

    # 2. ESEMPIO DI INCAPSULAMENTO (GETTER)
    @property
    def nome(self):
        return self._nome
    @nome.setter
    def nome(self, nuovo_nome):
        if len(nuovo_nome) > 0:
            self._nome = nuovo_nome
        else:
            print("Errore: Il nome non può essere vuoto!")

    # 5. ESEMPIO ASTRAZIONE
    @abstractmethod
    def attivita_principale(self):
        pass

    def saluta(self):
        return f"Ciao, mi chiamo {self._nome} e ho {self.eta} anni."

# 3. ESEMPIO DI EREDITARIETA'
class Studente(Persona):
    universita = "UniCT"

    def __init__(self, nome, eta, matricola):
        super().__init__(nome, eta)
        self.matricola = matricola

    def saluta(self):
        saluto_base = super().saluta()
        return f"{saluto_base} Studio alla {self.universita} (Matricola: {self.matricola})."

    # 4. ESEMPIO DI POLIMORFISMO
    def attivita_principale(self):
        return f" Sto studiando per l'esame."

class Professore(Persona):
    universita = "UniMI"

    def __init__(self, nome, eta, materia):
        super().__init__(nome, eta)
        self.materia = materia

    def saluta(self):
        saluto_base = super().saluta()
        return f"{saluto_base} Insegno alla {self.universita} la materia {self.materia}."

    def attivita_principale(self):
        return "Sto correggendo i compiti degli studenti."



print("--- OGGETTI ED EREDITARIETÀ ---")
s1 = Studente("Gianpiero", 20, "CT-123")
p1 = Professore("Casadei", 55, "Informatica")
print(s1.saluta())
print(p1.saluta())

print("\n--- INCAPSULAMENTO (Getter/Setter) ---")
print(f"Nome attuale: {s1.nome}") # GETTER
s1.nome = "Franco"              # SETTER
print(f"Nuovo nome: {s1.nome}")
s1.nome = ""

print("\n--- ASTRAZIONE ---")
try:
    # Tentativo di creare una Persona generica
    test_astrazione = Persona("Chiara", 24)
except TypeError as e:
    print(f"Non posso istanziare una Persona generica: {e}")

print("\n--- POLIMORFISMO ---")
lista_persone = [
    Studente("Jasmine", 22, "CT-456"),
    Professore("Paolillo", 45, "Italiano"),
    s1
]
for persona in lista_persone:
    print(f"{persona.nome}: {persona.attivita_principale()}")

