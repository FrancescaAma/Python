class Stack:
    def __init__(self):
        self.__data = []

    def push(self, item):
        self.__data.append(item)

    def pop(self):
        if self.isEmpty():
            raise IndexError("pop from empty stack")
        return self.__data.pop()

    def peek(self):
        if self.isEmpty():
            raise IndexError("empty stack")
        return self.__data[-1]

    def isEmpty(self):
        return len(self.__data) == 0

    def size(self):
        return len(self.__data)

    def __repr__(self):
        return f"Stack({self.__data})"


class Notifiche:
    def __init__(self):
        self.__pila = Stack()

    def arriva(self, messaggio):
        self.__pila.push(messaggio)

    def leggi(self):
        if self.__pila.isEmpty():
            print("Nessuna notifica.")
        else:
            print(f"Letta: {self.__pila.pop()}")

    def prossima(self):
        if self.__pila.isEmpty():
            print("Nessuna notifica in cima.")
        else:
            print(f"In cima: {self.__pila.peek()}")


n = Notifiche()

n.arriva("WhatsApp: Ciao!")
n.arriva("Gmail: Hai un nuovo messaggio")
n.arriva("Instagram: Ti hanno taggato")

n.prossima()   

n.leggi()
n.leggi()
n.leggi()
n.leggi()