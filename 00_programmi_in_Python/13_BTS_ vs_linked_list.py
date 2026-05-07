import random
import time

# LINKED LIST

class Nodo:
    def __init__(self, valore):
        self.valore = valore
        self.next   = None


class LinkedList:
    def __init__(self):
        self.__testa = None
        self.__size  = 0

    def insertFirst(self, valore):
        nuovo        = Nodo(valore)
        nuovo.next   = self.__testa
        self.__testa = nuovo
        self.__size += 1

    def insertLast(self, valore):
        nuovo = Nodo(valore)
        if self.__testa is None:
            self.__testa = nuovo
        else:
            corrente = self.__testa
            while corrente.next is not None:
                corrente = corrente.next
            corrente.next = nuovo
        self.__size += 1

    def insertAfter(self, valore_riferimento, nuovo_valore):
        corrente = self.__testa
        while corrente is not None:
            if corrente.valore == valore_riferimento:
                nuovo         = Nodo(nuovo_valore)
                nuovo.next    = corrente.next
                corrente.next = nuovo
                self.__size += 1
                return
            corrente = corrente.next
        raise ValueError(f"{valore_riferimento} non trovato nella lista")

    def insertBefore(self, valore_riferimento, nuovo_valore):
        if self.isEmpty():
            raise IndexError("lista vuota")
        if self.__testa.valore == valore_riferimento:
            self.insertFirst(nuovo_valore)
            return
        corrente = self.__testa
        while corrente.next is not None:
            if corrente.next.valore == valore_riferimento:
                nuovo         = Nodo(nuovo_valore)
                nuovo.next    = corrente.next
                corrente.next = nuovo
                self.__size += 1
                return
            corrente = corrente.next
        raise ValueError(f"{valore_riferimento} non trovato nella lista")

    def removeFirst(self):
        if self.isEmpty():
            raise IndexError("removeFirst da una lista vuota")
        valore       = self.__testa.valore
        self.__testa = self.__testa.next
        self.__size -= 1
        return valore

    def removeLast(self):
        if self.isEmpty():
            raise IndexError("removeLast da una lista vuota")
        if self.__testa.next is None:
            valore       = self.__testa.valore
            self.__testa = None
            self.__size -= 1
            return valore
        corrente = self.__testa
        while corrente.next.next is not None:
            corrente = corrente.next
        valore        = corrente.next.valore
        corrente.next = None
        self.__size -= 1
        return valore

    def peekFirst(self):
        if self.isEmpty():
            raise IndexError("lista vuota")
        return self.__testa.valore

    def isEmpty(self):
        return self.__testa is None

    def size(self):
        return self.__size

    def search(self, valore):
        corrente = self.__testa
        while corrente is not None:
            if corrente.valore == valore:
                return True
            corrente = corrente.next
        return False

    def __repr__(self):
        elementi = []
        corrente = self.__testa
        while corrente is not None:
            elementi.append(str(corrente.valore))
            corrente = corrente.next
        return "LinkedList([" + " → ".join(elementi) + "])"


# BST

class NodoBST:
    def __init__(self, valore):
        self.valore = valore
        self.left   = None
        self.right  = None


class BST:
    def __init__(self):
        self.__radice = None

    def insert(self, valore):
        if self.__radice is None:
            self.__radice = NodoBST(valore)
        else:
            self.__insertRicorsivo(self.__radice, valore)

    def __insertRicorsivo(self, nodo, valore):
        if valore < nodo.valore:
            if nodo.left is None:
                nodo.left = NodoBST(valore)
            else:
                self.__insertRicorsivo(nodo.left, valore)
        else:
            if nodo.right is None:
                nodo.right = NodoBST(valore)
            else:
                self.__insertRicorsivo(nodo.right, valore)

    def search(self, valore):
        return self.__searchRicorsivo(self.__radice, valore)

    def __searchRicorsivo(self, nodo, valore):
        if nodo is None:
            return False
        if nodo.valore == valore:
            return True
        if valore < nodo.valore:
            return self.__searchRicorsivo(nodo.left, valore)
        else:
            return self.__searchRicorsivo(nodo.right, valore)

    def isEmpty(self):
        return self.__radice is None


# 1.Genera una lista di 1000 numeri casuali tra 1 e 10k usando una list comprehnsion

numeri = [random.randint(1, 10000) for _ in range(1000)]


#  2. Inserisci gli stessi 1000 numeri sia nella lista linkata che nel BST

lista  = LinkedList()
albero = BST()

for n in numeri:
    lista.insertLast(n)
    albero.insert(n)


#  3. Scegli un numero da cercare - prendi il 500esimo elemento della lista generata

target = numeri[499]
print(f"Numero da cercare: {target}")
print(f"Elementi inseriti: {lista.size()}")



#  4. Misura il tempo di ricerca nella lista collegata usando time.perf_counter()


inizio_l  = time.perf_counter()
trovato_l = lista.search(target)
fine_l    = time.perf_counter()
tempo_l   = fine_l - inizio_l



#  5. Misura il tempo di ricerca nel BST usando time.perf_counter()


inizio_bst  = time.perf_counter()
trovato_bst = albero.search(target)
fine_bst    = time.perf_counter()
tempo_bst   = fine_bst - inizio_bst



#  6. Stampa i due tempi e calcola quante volte una struttura è più veloce dell'altra



print(f"\nLinkedList trovato: {trovato_l}  |  {tempo_l:.10f} s")
print(f"BST trovato: {trovato_bst}  |  {tempo_bst:.10f} s\n")

if tempo_l > 0 and tempo_bst > 0:
    if tempo_l > tempo_bst:
        rapporto = tempo_l / tempo_bst
        print(f"Il BST è {rapporto:.1f}x più veloce della LinkedList")
    else:
        rapporto = tempo_bst / tempo_l
        print(f"La LinkedList è {rapporto:.1f}x più veloce del BST")