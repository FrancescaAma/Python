class NodoBST:
    def __init__(self, valore):
        self.valore = valore
        self.left   = None   # figlio sinistro — valori minori
        self.right  = None   # figlio destro — valori maggiori


class BST:
    def __init__(self):
        self.__radice = None

    def insert(self, valore):
        if self.__radice is None:
            self.__radice = NodoBST(valore)
        else:
            # partiamo dalla radice e scendiamo nell'albero
            # la funzione chiamerà se stessa finché non trova un posto libero
            self.__insertRicorsivo(self.__radice, valore)


    def __insertRicorsivo(self, nodo, valore):
        if valore < nodo.valore:
            # il valore è minore — dobbiamo andare a sinistra
            if nodo.left is None:
                # CASO BASE: posto libero a sinistra — inseriamo qui
                nodo.left = NodoBST(valore)
            else:
                # CASO RICORSIVO: c'è già un nodo a sinistra
                # richiamiamo la stessa funzione sul figlio sinistro
                # il problema si riduce: scendiamo di un livello
                self.__insertRicorsivo(nodo.left, valore)
        else:
            # il valore è maggiore — dobbiamo andare a destra
            if nodo.right is None:
                # CASO BASE: posto libero a destra — inseriamo qui
                nodo.right = NodoBST(valore)
            else:
                # CASO RICORSIVO: c'è già un nodo a destra
                # richiamiamo la stessa funzione sul figlio destro
                self.__insertRicorsivo(nodo.right, valore)

    def search(self, valore):
        # partiamo dalla radice
        return self.__searchRicorsivo(self.__radice, valore)

    def __searchRicorsivo(self, nodo, valore):
        # CASO BASE 1: nodo inesistente — il valore non è nell'albero
        if nodo is None:
            return False

        # CASO BASE 2: trovato — il valore corrisponde
        if nodo.valore == valore:
            return True

        if valore < nodo.valore:
            # il valore è minore — non può essere a destra
            # CASO RICORSIVO: cerchiamo solo nel sottoalbero sinistro
            return self.__searchRicorsivo(nodo.left, valore)
        else:
            # il valore è maggiore — non può essere a sinistra
            # CASO RICORSIVO: cerchiamo solo nel sottoalbero destro
            return self.__searchRicorsivo(nodo.right, valore)

    def inOrder(self):
        # inOrder restituisce i valori in ordine crescente
        # perché visita prima sinistra, poi radice, poi destra
        elementi = []
        self.__inOrderRicorsivo(self.__radice, elementi)
        return elementi

    def __inOrderRicorsivo(self, nodo, elementi):
        # CASO BASE: nodo inesistente — non c'è nulla da visitare
        if nodo is None:
            return

        # CASO RICORSIVO:
        # 1. visita prima tutto il sottoalbero sinistro (valori minori)
        self.__inOrderRicorsivo(nodo.left, elementi)

        # 2. poi aggiungi il valore del nodo corrente
        elementi.append(nodo.valore)

        # 3. poi visita tutto il sottoalbero destro (valori maggiori)
        self.__inOrderRicorsivo(nodo.right, elementi)

    def isEmpty(self):
        return self.__radice is None

    def __repr__(self):
        return f"BST(inOrder={self.inOrder()})"

albero = BST()

albero.insert(10)   # diventa la radice
albero.insert(6)    # 6 < 10  → va a sinistra
albero.insert(15)   # 15 > 10 → va a destra
albero.insert(3)    # 3 < 10  → sinistra, 3 < 6 → sinistra
albero.insert(8)    # 8 < 10  → sinistra, 8 > 6 → destra
albero.insert(20)   # 20 > 10 → destra, 20 > 15 → destra

print(albero)   # BST(inOrder=[3, 6, 8, 10, 15, 20])

# search — ad ogni passo elimina metà dell'albero
print(albero.search(8))    # True  — 8 < 10 → sinistra, 8 > 6 → destra, trovato
print(albero.search(99))   # False — 99 > 10 → destra, 99 > 15 → destra, 99 > 20 → None
