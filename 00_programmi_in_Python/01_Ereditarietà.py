class Persona:
    def __init__(self, nome, cognome, eta):
        self.nome = nome
        self.cognome = cognome
        self.eta = eta

    def __str__(self):
        return f"Nome e Cognome: {self.nome} {self.cognome}\nEtà: {self.eta}"

class Paziente(Persona):
    def __init__(self, nome, cognome, eta, codice_id, gruppo_sanguigno):
        super().__init__(nome, cognome, eta)
        self.codice_id = codice_id
        self.gruppo_sanguigno = gruppo_sanguigno
        self.patologie = []
        self.allergie = []

    def __str__(self):
        base_info = super().__str__()
        return f"{base_info}\nID: {self.codice_id}\nGruppo Sanguigno: {self.gruppo_sanguigno}"

    def aggiungi_patologia(self, patologia):
        self.patologie.append(patologia)

    def aggiungi_allergia(self, allergia):
        self.allergie.append(allergia)

    def mostra_cartella_clinica(self):
        print(f"\n--- Cartella Clinica: {self.nome} {self.cognome} ---")
        print(f"Patologie: {', '.join(self.patologie) if self.patologie else 'Nessuna'}")
        print(f"Allergie: {', '.join(self.allergie) if self.allergie else 'Nessuna'}")

class Dottore(Persona):
    def __init__(self, nome, cognome, eta, matricola, specializzazione, reparto):
        super().__init__(nome, cognome, eta)
        self.matricola = matricola
        self.specializzazione = specializzazione
        self.reparto = reparto
        self.pazienti_in_cura = []

    def __str__(self):
        base_info = super().__str__()
        return f"{base_info}\nMatricola: {self.matricola}\nSpecializzazione: {self.specializzazione}\nReparto: {self.reparto}"

    def assegna_paziente(self, paziente):
        if isinstance(paziente, Paziente):
            self.pazienti_in_cura.append(paziente)
        else:
            print("Errore: puoi assegnare solo oggetti di tipo Paziente.")

    def mostra_pazienti(self):
        print(f"\n--- Pazienti in cura dal Dott. {self.cognome} ---")
        if not self.pazienti_in_cura:
            print("Nessun paziente assegnato.")
        else:
            for p in self.pazienti_in_cura:
                print(f"[{p.codice_id}] {p.nome} {p.cognome}")


def crea_paziente_da_input():
    print("\n--- Inserimento Nuovo Paziente ---")
    nome = input("Nome: ")
    cognome = input("Cognome: ")
    eta = int(input("Età: "))
    codice = input("Codice Identificativo: ")
    gruppo = input("Gruppo Sanguigno: ")
    
    p = Paziente(nome, cognome, eta, codice, gruppo)
    
    pato_str = input("Inserisci patologie separate da virgola (es. asma, diabete): ")
    if pato_str:
        p.patologie = [item.strip() for item in pato_str.split(',')]
    
    alle_str = input("Inserisci allergie separate da virgola (o premi Invio per saltare): ")
    if alle_str:
        p.allergie = [item.strip() for item in alle_str.split(',')]
        
    return p

def crea_dottore_da_input():
    print("\n--- Inserimento Nuovo Dottore ---")
    nome = input("Nome: ")
    cognome = input("Cognome: ")
    eta = int(input("Età: "))
    matricola = input("Matricola: ")
    specializzazione = input("Specializzazione: ")
    reparto = input("Reparto: ")
    
    return Dottore(nome, cognome, eta, matricola, specializzazione, reparto)

def main():

    dottori = []
    pazienti = []

    while True:
        print("\n=== SISTEMA OSPEDALIERO ===")
        print("1. Aggiungi Dottore")
        print("2. Aggiungi Paziente")
        print("3. Mostra tutti")
        print("4. Esci")
        
        scelta = input("Scegli un'opzione: ")

        if scelta == "1":
            dottore = crea_dottore_da_input()
            dottori.append(dottore)
            print(f"Dott. {dottore.cognome} aggiunto con successo!")

        elif scelta == "2":
            paziente = crea_paziente_da_input()
            pazienti.append(paziente)
            print(f"Paziente {paziente.cognome} aggiunto con successo!")
            
            if not dottori:
                print("Non ci sono dottori nel sistema, il paziente non è stato assegnato.")
            else:
                print("\nA quale dottore vuoi assegnarlo?")

                for i, d in enumerate(dottori):
                    print(f"{i}) Dott. {d.cognome} ({d.specializzazione})")
                
                while True:
                    try:
                        scelta_doc = int(input("Inserisci il numero del dottore: "))

                        if 0 <= scelta_doc < len(dottori):
                            dottori[scelta_doc].assegna_paziente(paziente)
                            print(f"Paziente assegnato al Dott. {dottori[scelta_doc].cognome}")
                            break
                        else:
                            print(f"Errore: inserisci un numero tra 0 e {len(dottori)-1}")
                    except ValueError:
                        print("Errore: devi inserire un numero intero!")

        elif scelta == "3":
            for d in dottori:
                print(f"\n--- DOTTORE ---")
                print(d)
                d.mostra_pazienti()
            
            for p in pazienti:
                print("\n--- PAZIENTE ---")
                print(p)
                p.mostra_cartella_clinica()

        elif scelta == "4":
            print("Chiusura sistema...")
            break
        else:
            print("Opzione non valida!")

if __name__ == "__main__":
    main()