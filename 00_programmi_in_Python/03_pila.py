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

# inizializziamo le pile
history = Stack()
forward = Stack()

# visitiamo le pagine
history.push("google.com")
history.push("wikipedia.org")
history.push("python.org")

current = history.pop()   # "python.org" — pagina corrente

print(f"Pagina corrente: {current}")   # python.org
print(f"Cronologia: {history}")        # Stack(['google.com', 'wikipedia.org'])

# --- torniamo indietro ---
forward.push(current)
current = history.pop()

print(f"Pagina corrente: {current}")   # wikipedia.org
print(f"Avanti: {forward}")            # Stack(['python.org'])

# --- andiamo avanti ---
history.push(current)
current = forward.pop()

print(f"Pagina corrente: {current}")   # python.org


# --- proviamo a violare l'incapsulamento ---
history.__data.append("yahoo.com")
# AttributeError: 'Stack' object has no attribute '__data'

history._Stack__data.append("yahoo.com")
# funziona — ma è un atto deliberato, non un errore accidentale
