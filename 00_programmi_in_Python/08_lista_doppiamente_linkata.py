class NodoD:
    def __init__(self, valore):
        self.valore = valore
        self.next   = None   # puntatore al nodo successivo
        self.prev   = None   # puntatore al nodo precedente


class DoublyLinkedList:
    def __init__(self):
        self.__testa = None
        self.__coda  = None   # novità rispetto a LinkedList
        self.__size  = 0

    def insertFirst(self, valore):
        nuovo = NodoD(valore)
        if self.isEmpty():
            self.__testa = nuovo
            self.__coda  = nuovo
        else:
            nuovo.next        = self.__testa
            self.__testa.prev = nuovo   # novità: aggiorniamo prev
            self.__testa      = nuovo
        self.__size += 1

    def insertLast(self, valore):
        nuovo = NodoD(valore)
        if self.isEmpty():
            self.__testa = nuovo
            self.__coda  = nuovo
        else:
            nuovo.prev       = self.__coda
            self.__coda.next = nuovo    # novità: usiamo __coda direttamente — O(1)
            self.__coda      = nuovo
        self.__size += 1

    def insertAfter(self, valore_riferimento, nuovo_valore):
        corrente = self.__testa
        while corrente is not None:
            if corrente.valore == valore_riferimento:
                if corrente == self.__coda:
                    self.insertLast(nuovo_valore)
                    return
                nuovo              = NodoD(nuovo_valore)
                nuovo.next         = corrente.next
                nuovo.prev         = corrente          # novità: aggiorniamo prev
                corrente.next.prev = nuovo             # novità: aggiorniamo prev del successivo
                corrente.next      = nuovo
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
        while corrente is not None:
            if corrente.valore == valore_riferimento:
                nuovo              = NodoD(nuovo_valore)
                nuovo.next         = corrente
                nuovo.prev         = corrente.prev     # novità: aggiorniamo prev
                corrente.prev.next = nuovo             # novità: aggiorniamo next del precedente
                corrente.prev      = nuovo
                self.__size += 1
                return
            corrente = corrente.next
        raise ValueError(f"{valore_riferimento} non trovato nella lista")

    def removeFirst(self):
        if self.isEmpty():
            raise IndexError("removeFirst da una lista vuota")
        valore = self.__testa.valore
        if self.__testa == self.__coda:
            self.__testa = None
            self.__coda  = None
        else:
            self.__testa      = self.__testa.next
            self.__testa.prev = None               # novità: aggiorniamo prev
        self.__size -= 1
        return valore

    def removeLast(self):
        if self.isEmpty():
            raise IndexError("removeLast da una lista vuota")
        valore = self.__coda.valore
        if self.__testa == self.__coda:
            self.__testa = None
            self.__coda  = None
        else:
            self.__coda      = self.__coda.prev    # novità: usiamo __coda direttamente — O(1)
            self.__coda.next = None
        self.__size -= 1
        return valore

    def peekFirst(self):
        if self.isEmpty():
            raise IndexError("lista vuota")
        return self.__testa.valore

    def peekLast(self):                            # novità rispetto a LinkedList
        if self.isEmpty():
            raise IndexError("lista vuota")
        return self.__coda.valore

    def isEmpty(self):
        return self.__testa is None

    def size(self):
        return self.__size

    def __repr__(self):
        elementi = []
        corrente = self.__testa
        while corrente is not None:
            elementi.append(str(corrente.valore))
            corrente = corrente.next
        return "DoublyLinkedList([" + " ⟷ ".join(elementi) + "])"

dll = DoublyLinkedList()

dll.insertLast(10)
dll.insertLast(20)
dll.insertLast(30)
dll.insertLast(40)
print("Lista iniziale:    ", dll)

dll.insertFirst(5)
dll.insertAfter(20, 25)
dll.insertBefore(40, 35)
print("Dopo inserimenti:  ", dll)      

print("Primo elemento:    ", dll.peekFirst())
print("Ultimo elemento:   ", dll.peekLast())

dll.removeFirst()
dll.removeLast()
print("Dopo rimozioni:    ", dll)         
print("Dimensione:        ", dll.size())   